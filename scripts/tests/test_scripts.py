from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock


SCRIPTS = Path(__file__).resolve().parents[1]


def load_module(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


inventory_repo = load_module("inventory_repo")
validate_book = load_module("validate_book")


class InventoryRepoTests(unittest.TestCase):
    def test_filesystem_fallback_handles_monorepo_spaces_and_exclusions(self):
        with tempfile.TemporaryDirectory(prefix="project learning ") as directory:
            repo = Path(directory)
            (repo / "backend").mkdir()
            (repo / "backend" / "pyproject.toml").write_text(
                "[project]\nname = 'demo'\n[project.scripts]\napp = 'app:main'\n",
                encoding="utf-8",
            )
            (repo / "backend" / "app.py").write_text("print('ok')\n", encoding="utf-8")
            (repo / "backend" / "docker-compose.dev.yml").write_text("services: {}\n", encoding="utf-8")
            (repo / "front end").mkdir()
            (repo / "front end" / "package.json").write_text("{}\n", encoding="utf-8")
            (repo / "front end" / "index.ts").write_text("export {}\n", encoding="utf-8")
            (repo / "node_modules" / "pkg").mkdir(parents=True)
            (repo / "node_modules" / "pkg" / "package.json").write_text("{}", encoding="utf-8")
            (repo / ".env").write_text("API_KEY=sk-this-must-not-appear-anywhere\n", encoding="utf-8")

            result = inventory_repo.build_inventory(repo, prefer_rg=False)
            serialized = json.dumps(result)

            self.assertEqual(result["repository_shape"], "monorepo")
            self.assertEqual(result["discovery_source"], "filesystem")
            self.assertIn("backend/app.py", result["entrypoints"])
            backend_types = next(item["types"] for item in result["project_types"] if item["path"] == "backend")
            self.assertIn("cli", backend_types)
            self.assertIn("backend/docker-compose.dev.yml", result["manifests"])
            self.assertNotIn("front end/index.ts", result["entrypoints"])
            self.assertIn("front end/index.ts", result["entrypoint_candidates"])
            self.assertFalse(any("node_modules" in path for path in result["manifests"]))
            self.assertNotIn("sk-this-must-not-appear-anywhere", serialized)

    def test_non_git_repository_and_file_limit(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            for index in range(3):
                (repo / f"file-{index}.txt").write_text("x", encoding="utf-8")
            result = inventory_repo.build_inventory(repo, prefer_rg=False, max_files=2)
            self.assertIsNone(result["head_sha"])
            self.assertTrue(result["truncated"])
            self.assertEqual(result["file_count"], 2)

    def test_inventory_is_read_only(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            sentinel = repo / "README.md"
            sentinel.write_text("unchanged", encoding="utf-8")
            before = (sentinel.read_bytes(), sentinel.stat().st_mtime_ns)
            inventory_repo.build_inventory(repo, prefer_rg=False)
            after = (sentinel.read_bytes(), sentinel.stat().st_mtime_ns)
            self.assertEqual(before, after)


class ValidateBookTests(unittest.TestCase):
    def set_preservation(self, book: Path) -> None:
        manifest_path = book / ".learning-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["preservation"] = {
            "captured_at": "2026-09-06T00:00:00Z",
            "chapters": validate_book.snapshot_chapters(book),
        }
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    def make_book(self, repo: Path, mode: str = "full", targets: list[str] | None = None) -> Path:
        source = repo / "src" / "app.py"
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text("print('ok')\n", encoding="utf-8")
        book = repo / "project-book"
        book.mkdir()
        for chapter in validate_book.CHAPTERS:
            (book / chapter).write_text(
                f"# {chapter}\n\nEvidence: `src/app.py:1`\n",
                encoding="utf-8",
            )
        (book / "03-architecture.md").write_text(
            "# Architecture\n\nEvidence: `src/app.py:1`\n\n"
            "<!-- diagram:system-structure -->\n"
            "```mermaid\nflowchart LR\n    User --> App\n```\n",
            encoding="utf-8",
        )
        (book / "04-core-flow.md").write_text(
            "# Core flow\n\nEvidence: `src/app.py:1`\n\n"
            "<!-- diagram:core-flow-sequence -->\n"
            "```mermaid\nsequenceDiagram\n    User->>App: run\n    App-->>User: result\n```\n",
            encoding="utf-8",
        )
        diagrams = [
            {
                "id": "system-structure",
                "chapter": "03-architecture.md",
                "role": "system_structure",
                "type": "component",
                "status": "static",
                "purpose": "Orient the learner to the application boundary.",
                "sources": ["src/app.py"],
                "node_count": 2,
                "edge_count": 1,
                "reason": "Renderer unavailable.",
            },
            {
                "id": "runtime-deployment",
                "chapter": "03-architecture.md",
                "role": "runtime_deployment",
                "type": "deployment",
                "status": "not_applicable",
                "purpose": "Account for deployment topology.",
                "sources": [],
                "node_count": 0,
                "edge_count": 0,
                "reason": "The fixture has no deployment configuration.",
            },
            {
                "id": "core-flow-sequence",
                "chapter": "04-core-flow.md",
                "role": "core_flow",
                "type": "sequence",
                "status": "static",
                "purpose": "Explain the representative request and response.",
                "sources": ["src/app.py"],
                "node_count": 2,
                "edge_count": 2,
                "reason": "Renderer unavailable.",
            },
        ]
        if mode == "targeted":
            target_set = set(targets or [])
            diagrams = [entry for entry in diagrams if entry["chapter"] in target_set]
        manifest = {
            "schema_version": 2,
            "repo_root": ".",
            "head_sha": None,
            "generated_at": "2026-09-06T00:00:00Z",
            "mode": mode,
            "targets": targets or [],
            "subprojects": [{"path": ".", "manifests": []}],
            "project_types": [{"path": ".", "types": ["service"]}],
            "entrypoints": ["src/app.py"],
            "chapter_sources": {chapter: ["src/app.py"] for chapter in validate_book.CHAPTERS},
            "diagrams": diagrams,
            "validation": {
                "paths": {"status": "passed", "reason": None},
                "markdown": {"status": "passed", "reason": None},
                "placeholders": {"status": "passed", "reason": None},
                "secrets": {"status": "passed", "reason": None},
                "diagrams": {"status": "static", "reason": "Renderer unavailable."},
                "examples": {
                    "status": "passed",
                    "reason": "syntax check",
                    "command": "python -m py_compile src/app.py",
                    "exit_code": 0,
                    "level": "syntax",
                },
            },
        }
        (book / ".learning-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        if mode == "targeted":
            self.set_preservation(book)
        return book

    def test_full_and_fast_books_pass(self):
        for mode in ("full", "fast"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as directory:
                repo = Path(directory)
                book = self.make_book(repo, mode)
                self.assertTrue(validate_book.validate(repo, book, mode=mode).ok)

    def test_targeted_mode_requires_only_target_chapter(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            book = self.make_book(repo, "targeted", ["03-architecture.md"])
            for chapter in validate_book.CHAPTERS:
                if chapter != "03-architecture.md":
                    (book / chapter).unlink()
            self.set_preservation(book)
            result = validate_book.validate(repo, book, mode="targeted")
            self.assertTrue(result.ok, result.errors)

    def test_targeted_mode_ignores_unrelated_broken_chapter(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            book = self.make_book(repo, "targeted", ["03-architecture.md"])
            unrelated = book / "04-core-flow.md"
            unrelated.write_text("```python\n[项目路径]\nAPI_TOKEN=real-secret-value\n", encoding="utf-8")
            self.set_preservation(book)
            before = (unrelated.read_bytes(), unrelated.stat().st_mtime_ns)
            result = validate_book.validate(repo, book, mode="targeted")
            after = (unrelated.read_bytes(), unrelated.stat().st_mtime_ns)
            self.assertTrue(result.ok, result.errors)
            self.assertEqual(before, after)

    def test_targeted_mode_detects_unrelated_chapter_change(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            book = self.make_book(repo, "targeted", ["03-architecture.md"])
            unrelated = book / "04-core-flow.md"
            unrelated.write_text("# Unexpected rewrite\n", encoding="utf-8")
            result = validate_book.validate(repo, book, mode="targeted")
            self.assertIn(
                "unrelated chapter changed during targeted update: 04-core-flow.md",
                result.errors,
            )

    def test_targeted_mode_requires_preservation_baseline(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            book = self.make_book(repo, "targeted", ["03-architecture.md"])
            manifest_path = book / ".learning-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest.pop("preservation")
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            result = validate_book.validate(repo, book, mode="targeted")
            self.assertIn("targeted mode requires preservation.chapters baseline", result.errors)

    def test_detects_broken_fence_path_placeholder_and_secret(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            book = self.make_book(repo)
            (book / "03-architecture.md").write_text(
                "# Architecture\n\n```python\n[项目路径]\nEvidence: `missing/file.py:9`\nAPI_TOKEN=real-secret-value\n",
                encoding="utf-8",
            )
            result = validate_book.validate(repo, book)
            joined = "\n".join(result.errors)
            self.assertIn("unbalanced Markdown fence", joined)
            self.assertIn("unresolved placeholder", joined)
            self.assertIn("missing evidence path", joined)
            self.assertIn("possible unredacted secret assignment", joined)

    def test_detects_credential_bearing_url(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            book = self.make_book(repo)
            (book / "02-installation.md").write_text(
                "# Installation\n\nDATABASE_URL=postgresql://user:realpassword@db/app\nEvidence: `src/app.py:1`\n",
                encoding="utf-8",
            )
            result = validate_book.validate(repo, book)
            self.assertIn("possible credential-bearing URL", result.errors)

    def test_lowercase_program_variable_is_not_treated_as_env_secret(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            book = self.make_book(repo)
            (book / "08-examples.md").write_text(
                "# Example\n\n```python\napi_key = context.get('api_key', '')\n```\n"
                "\nEvidence: `src/app.py:1`\n",
                encoding="utf-8",
            )
            result = validate_book.validate(repo, book)
            self.assertFalse(
                any("unredacted secret assignment" in error for error in result.errors),
                result.errors,
            )

    def test_evidence_path_with_spaces_is_validated(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            book = self.make_book(repo)
            source = repo / "src" / "my app.py"
            source.write_text("first\n", encoding="utf-8")
            (book / "03-architecture.md").write_text(
                "# Architecture\n\nEvidence: `src/my app.py:2`\n",
                encoding="utf-8",
            )
            result = validate_book.validate(repo, book)
            self.assertIn("evidence line out of range in 03-architecture.md: src/my app.py:2", result.errors)

    def test_chapter_requires_inline_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            book = self.make_book(repo)
            (book / "03-architecture.md").write_text(
                "# Architecture\n\nThis chapter only declares evidence in the manifest.\n",
                encoding="utf-8",
            )
            result = validate_book.validate(repo, book)
            self.assertIn("missing inline file:line evidence in 03-architecture.md", result.errors)

    def test_inline_evidence_must_be_declared_in_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            book = self.make_book(repo)
            other = repo / "src" / "other.py"
            other.write_text("print('other')\n", encoding="utf-8")
            (book / "03-architecture.md").write_text(
                "# Architecture\n\nEvidence: `src/other.py:1`\n",
                encoding="utf-8",
            )
            result = validate_book.validate(repo, book)
            self.assertIn(
                "inline evidence not declared in chapter_sources for 03-architecture.md: src/other.py",
                result.errors,
            )

    def test_passed_example_requires_command_exit_code_and_level(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            book = self.make_book(repo, "fast")
            manifest_path = book / ".learning-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["validation"]["examples"] = {"status": "passed", "reason": None}
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            result = validate_book.validate(repo, book, mode="fast")
            joined = "\n".join(result.errors)
            self.assertIn("requires a command", joined)
            self.assertIn("requires exit_code 0", joined)
            self.assertIn("requires level", joined)

    def test_full_mode_requires_all_core_diagram_roles(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            book = self.make_book(repo)
            manifest_path = book / ".learning-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["diagrams"] = [
                entry for entry in manifest["diagrams"] if entry["role"] != "runtime_deployment"
            ]
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            result = validate_book.validate(repo, book)
            self.assertIn("full mode missing required diagram role: runtime_deployment", result.errors)

    def test_unregistered_mermaid_block_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            book = self.make_book(repo)
            chapter = book / "05-core-concepts.md"
            chapter.write_text(
                chapter.read_text(encoding="utf-8")
                + "\n```mermaid\nclassDiagram\n    class App\n```\n",
                encoding="utf-8",
            )
            result = validate_book.validate(repo, book)
            self.assertIn("unregistered Mermaid block in 05-core-concepts.md", result.errors)

    def test_diagram_complexity_and_sources_are_enforced(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            book = self.make_book(repo)
            manifest_path = book / ".learning-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["diagrams"][0]["node_count"] = 13
            manifest["diagrams"][0]["edge_count"] = 19
            manifest["diagrams"][0]["sources"] = ["missing.py"]
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            result = validate_book.validate(repo, book)
            joined = "\n".join(result.errors)
            self.assertIn("missing diagram source", joined)
            self.assertIn("node_count must be between 1 and 12", joined)
            self.assertIn("edge_count must be between 0 and 18", joined)

    def test_not_applicable_diagram_requires_reason_and_zero_counts(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            book = self.make_book(repo)
            manifest_path = book / ".learning-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            deployment = next(
                entry for entry in manifest["diagrams"] if entry["role"] == "runtime_deployment"
            )
            deployment["reason"] = ""
            deployment["node_count"] = 1
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            result = validate_book.validate(repo, book)
            joined = "\n".join(result.errors)
            self.assertIn("not_applicable diagram requires a reason", joined)
            self.assertIn("not_applicable diagram must have empty sources and zero counts", joined)

    def test_passed_diagram_validation_requires_render_proof(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            book = self.make_book(repo)
            manifest_path = book / ".learning-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["validation"]["diagrams"] = {"status": "passed", "reason": None}
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            result = validate_book.validate(repo, book)
            joined = "\n".join(result.errors)
            self.assertIn("requires a renderer command", joined)
            self.assertIn("requires exit_code 0", joined)
            self.assertIn("requires level render", joined)

    def test_fast_mode_requires_validated_example(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            book = self.make_book(repo, "fast")
            manifest_path = book / ".learning-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["validation"]["examples"] = {"status": "not_run", "reason": "tool unavailable"}
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            result = validate_book.validate(repo, book, mode="fast")
            self.assertIn("fast mode requires at least one syntax-validated example", result.errors)

    def test_stale_git_baseline_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            book = self.make_book(repo)
            with mock.patch.object(validate_book, "_git_head", return_value="current-head"):
                result = validate_book.validate(repo, book)
            self.assertTrue(any("head_sha is stale" in error for error in result.errors))

    def test_book_only_commit_does_not_stale_source_baseline(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            book = self.make_book(repo)
            manifest_path = book / ".learning-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["head_sha"] = "source-head"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            with mock.patch.object(validate_book, "_git_head", return_value="book-commit"), mock.patch.object(
                validate_book,
                "_git_changed_paths",
                return_value=["project-book/.learning-manifest.json", "project-book/01-project-overview.md"],
            ):
                result = validate_book.validate(repo, book)
            self.assertFalse(any("head_sha is stale" in error for error in result.errors), result.errors)

    def test_source_commit_stales_baseline_even_with_book_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            book = self.make_book(repo)
            manifest_path = book / ".learning-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["head_sha"] = "source-head"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            with mock.patch.object(validate_book, "_git_head", return_value="new-head"), mock.patch.object(
                validate_book,
                "_git_changed_paths",
                return_value=["project-book/01-project-overview.md", "src/app.py"],
            ):
                result = validate_book.validate(repo, book)
            self.assertTrue(any("head_sha is stale" in error for error in result.errors), result.errors)

    def test_cli_mode_and_targets_must_match_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            book = self.make_book(repo, "targeted", ["03-architecture.md"])
            result = validate_book.validate(
                repo,
                book,
                mode="full",
                targets=["04-core-flow.md"],
            )
            self.assertIn("CLI mode 'full' does not match manifest mode 'targeted'", result.errors)
            self.assertIn("CLI targets do not match manifest targets", result.errors)

    def test_manifest_root_must_be_object(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            book = self.make_book(repo)
            (book / ".learning-manifest.json").write_text("[]", encoding="utf-8")
            result = validate_book.validate(repo, book)
            self.assertIn("manifest root must be a JSON object", result.errors)

    def test_empty_manifest_object_fails_schema_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            book = self.make_book(repo)
            (book / ".learning-manifest.json").write_text("{}", encoding="utf-8")
            result = validate_book.validate(repo, book)
            self.assertTrue(any(error.startswith("manifest missing keys:") for error in result.errors))
            self.assertIn("manifest schema_version must be 2", result.errors)

    def test_validation_is_read_only(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            book = self.make_book(repo)
            sentinel = book / "01-project-overview.md"
            before = (sentinel.read_bytes(), sentinel.stat().st_mtime_ns)
            time.sleep(0.001)
            validate_book.validate(repo, book)
            after = (sentinel.read_bytes(), sentinel.stat().st_mtime_ns)
            self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
