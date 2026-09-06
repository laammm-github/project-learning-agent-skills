#!/usr/bin/env python3
"""Validate a project-learning-agent book and manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path


CHAPTERS = [
    "01-project-overview.md",
    "02-installation.md",
    "03-architecture.md",
    "04-core-flow.md",
    "05-core-concepts.md",
    "06-source-code-guide.md",
    "07-extension-guide.md",
    "08-examples.md",
    "09-faq.md",
    "10-learning-checklist.md",
]
REQUIRED_MANIFEST_KEYS = {
    "schema_version",
    "repo_root",
    "head_sha",
    "generated_at",
    "mode",
    "targets",
    "subprojects",
    "project_types",
    "entrypoints",
    "chapter_sources",
    "diagrams",
    "validation",
}
ALLOWED_STATES = {"passed", "failed", "static", "not_run"}
DIAGRAM_ROLES = {
    "system_structure": {"context", "component"},
    "runtime_deployment": {"deployment"},
    "core_flow": {"sequence"},
    "domain_model": {"class"},
    "lifecycle": {"state"},
}
REQUIRED_DIAGRAM_ROLES = {
    "full": {"system_structure", "runtime_deployment", "core_flow"},
    "fast": {"system_structure", "core_flow"},
    "targeted": set(),
}
DIAGRAM_STATUSES = {"passed", "static", "not_applicable"}
DIAGRAM_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MERMAID_BLOCK_RE = re.compile(
    r"(?ms)(?:<!--\s*diagram:([^>]+?)\s*-->\s*\r?\n)?"
    r"^[ \t]*```mermaid[ \t]*\r?\n(.*?)^[ \t]*```[ \t]*$"
)
PLACEHOLDER_RE = re.compile(r"\[(?:项目|路径|文件|模块|参数|组件|类型|请替换|入口|基类|注册)[^\]]*\]")
INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")
EVIDENCE_SUFFIX_RE = re.compile(r"^(.+):([1-9][0-9]*)$")
SECRET_PATTERNS = [
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\bgh[oprsu]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]
SECRET_URI_RE = re.compile(
    r"(?i)\b(?:postgres(?:ql)?|mysql|mariadb|mongodb(?:\+srv)?|redis|rediss|amqp|amqps|https?)://"
    r"[^\s/:@]+:[^\s/@]+@"
)
SECRET_ASSIGNMENT_RE = re.compile(
    r"(?m)^\s*(?:export\s+)?[A-Z0-9_]*(?:API_KEY|TOKEN|SECRET|PASSWORD|COOKIE)[A-Z0-9_]*\s*=\s*([^\s#]+)"
)
SAFE_SECRET_VALUES = re.compile(r"(?i)^(?:<redacted>|redacted|your[-_].*|example|placeholder|changeme|\$\{.*\})$")


@dataclass
class Result:
    errors: list[str]
    warnings: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


def _git_head(repo: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=repo, text=True, encoding="utf-8", errors="replace", capture_output=True, check=False
        )
    except OSError:
        return None
    value = result.stdout.strip()
    return value if result.returncode == 0 and value else None


def _git_changed_paths(repo: Path, old_head: str, new_head: str) -> list[str] | None:
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", f"{old_head}..{new_head}"],
            cwd=repo,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            check=False,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    return [line.replace("\\", "/") for line in result.stdout.splitlines() if line.strip()]


def _fences_are_balanced(text: str) -> bool:
    opening: tuple[str, int] | None = None
    for line in text.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if not match:
            continue
        marker = match.group(1)
        if opening is None:
            opening = (marker[0], len(marker))
        elif marker[0] == opening[0] and len(marker) >= opening[1] and not match.group(2).strip():
            opening = None
    return opening is None


def snapshot_chapters(book: Path) -> dict[str, dict[str, int | str] | None]:
    snapshot: dict[str, dict[str, int | str] | None] = {}
    for chapter in CHAPTERS:
        path = book / chapter
        if not path.is_file():
            snapshot[chapter] = None
            continue
        snapshot[chapter] = {
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "mtime_ns": path.stat().st_mtime_ns,
        }
    return snapshot


def _normalize_targets(targets: list[str]) -> list[str]:
    normalized: list[str] = []
    for target in targets:
        if target in CHAPTERS:
            normalized.append(target)
            continue
        match = re.match(r"^(\d{1,2})", target)
        if match:
            prefix = f"{int(match.group(1)):02d}-"
            normalized.extend(chapter for chapter in CHAPTERS if chapter.startswith(prefix))
    return list(dict.fromkeys(normalized))


def _evidence_references(text: str) -> list[tuple[str, int]]:
    references: list[tuple[str, int]] = []
    for inline in INLINE_CODE_RE.findall(text):
        match = EVIDENCE_SUFFIX_RE.match(inline.strip())
        if not match:
            continue
        raw_path, line_number = match.groups()
        if "/" not in raw_path and "\\" not in raw_path:
            continue
        if "://" in raw_path:
            continue
        references.append((raw_path.replace("\\", "/"), int(line_number)))
    return references


def _mermaid_blocks(text: str) -> list[tuple[str | None, str]]:
    return [
        (match.group(1).strip() if match.group(1) else None, match.group(2))
        for match in MERMAID_BLOCK_RE.finditer(text)
    ]


def _mermaid_type(body: str) -> str | None:
    first_line = next((line.strip() for line in body.splitlines() if line.strip()), "")
    if first_line.startswith(("flowchart", "graph")):
        return "flowchart"
    if first_line == "sequenceDiagram":
        return "sequence"
    if first_line == "classDiagram":
        return "class"
    if first_line.startswith("stateDiagram"):
        return "state"
    return None


def _validate_diagrams(
    repo: Path,
    book: Path,
    manifest: dict,
    effective_mode: str,
    required_chapters: list[str],
    chapter_sources: dict,
    errors: list[str],
    warnings: list[str],
) -> None:
    diagrams = manifest.get("diagrams")
    if not isinstance(diagrams, list):
        errors.append("diagrams must be a list")
        return

    active_entries: list[dict] = []
    seen_ids: set[str] = set()
    for index, entry in enumerate(diagrams):
        if not isinstance(entry, dict):
            errors.append(f"invalid diagrams entry at index {index}")
            continue
        chapter = entry.get("chapter")
        if effective_mode == "targeted" and chapter not in required_chapters:
            continue
        active_entries.append(entry)
        diagram_id = entry.get("id")
        if not isinstance(diagram_id, str) or not DIAGRAM_ID_RE.fullmatch(diagram_id):
            errors.append(f"diagram id must be lowercase kebab-case at index {index}")
        elif diagram_id in seen_ids:
            errors.append(f"duplicate diagram id: {diagram_id}")
        else:
            seen_ids.add(diagram_id)

        if chapter not in CHAPTERS:
            errors.append(f"invalid diagram chapter for {diagram_id!r}: {chapter!r}")
        role = entry.get("role")
        diagram_type = entry.get("type")
        if role not in DIAGRAM_ROLES:
            errors.append(f"invalid diagram role for {diagram_id!r}: {role!r}")
        elif diagram_type not in DIAGRAM_ROLES[role]:
            errors.append(f"diagram type {diagram_type!r} is incompatible with role {role!r}: {diagram_id!r}")
        status = entry.get("status")
        if status not in DIAGRAM_STATUSES:
            errors.append(f"invalid diagram status for {diagram_id!r}: {status!r}")
        purpose = entry.get("purpose")
        if not isinstance(purpose, str) or not purpose.strip():
            errors.append(f"diagram requires a purpose: {diagram_id!r}")

        sources = entry.get("sources")
        node_count = entry.get("node_count")
        edge_count = entry.get("edge_count")
        if status == "not_applicable":
            if not isinstance(entry.get("reason"), str) or not entry["reason"].strip():
                errors.append(f"not_applicable diagram requires a reason: {diagram_id!r}")
            if sources != [] or node_count != 0 or edge_count != 0:
                errors.append(f"not_applicable diagram must have empty sources and zero counts: {diagram_id!r}")
            continue

        if not isinstance(sources, list) or not sources:
            errors.append(f"diagram requires source files: {diagram_id!r}")
        else:
            declared = {
                source.replace("\\", "/")
                for source in chapter_sources.get(chapter, [])
                if isinstance(source, str)
            } if isinstance(chapter_sources, dict) else set()
            for source in sources:
                if not isinstance(source, str) or not (repo / source).is_file():
                    errors.append(f"missing diagram source for {diagram_id!r}: {source!r}")
                elif source.replace("\\", "/") not in declared:
                    errors.append(f"diagram source not declared in chapter_sources for {diagram_id!r}: {source}")
        if not isinstance(node_count, int) or isinstance(node_count, bool) or not 1 <= node_count <= 12:
            errors.append(f"diagram node_count must be between 1 and 12: {diagram_id!r}")
        if not isinstance(edge_count, int) or isinstance(edge_count, bool) or not 0 <= edge_count <= 18:
            errors.append(f"diagram edge_count must be between 0 and 18: {diagram_id!r}")

    blocks: dict[str, tuple[str, str]] = {}
    for chapter in required_chapters:
        chapter_path = book / chapter
        if not chapter_path.is_file():
            continue
        for diagram_id, body in _mermaid_blocks(chapter_path.read_text(encoding="utf-8-sig")):
            if diagram_id is None:
                errors.append(f"unregistered Mermaid block in {chapter}")
                continue
            if not DIAGRAM_ID_RE.fullmatch(diagram_id):
                errors.append(f"Mermaid diagram id must be lowercase kebab-case in {chapter}: {diagram_id}")
            if diagram_id in blocks:
                errors.append(f"duplicate Mermaid diagram id: {diagram_id}")
            else:
                blocks[diagram_id] = (chapter, body)

    entry_by_id = {
        entry["id"]: entry
        for entry in active_entries
        if isinstance(entry.get("id"), str) and DIAGRAM_ID_RE.fullmatch(entry["id"])
    }
    for diagram_id, (chapter, body) in blocks.items():
        entry = entry_by_id.get(diagram_id)
        if entry is None:
            errors.append(f"Mermaid block missing manifest entry: {diagram_id}")
            continue
        if entry.get("status") == "not_applicable":
            errors.append(f"not_applicable diagram must not have a Mermaid block: {diagram_id}")
        if entry.get("chapter") != chapter:
            errors.append(f"diagram chapter does not match Mermaid block: {diagram_id}")
        detected_type = _mermaid_type(body)
        expected_type = entry.get("type")
        if detected_type is None:
            errors.append(f"unsupported Mermaid directive: {diagram_id}")
        elif detected_type == "flowchart":
            if expected_type not in {"context", "component", "deployment"}:
                errors.append(f"Mermaid directive does not match diagram type: {diagram_id}")
        elif detected_type != expected_type:
            errors.append(f"Mermaid directive does not match diagram type: {diagram_id}")

    for entry in active_entries:
        diagram_id = entry.get("id")
        if entry.get("status") != "not_applicable" and isinstance(diagram_id, str) and diagram_id not in blocks:
            errors.append(f"diagram manifest entry missing Mermaid block: {diagram_id}")

    roles = {entry.get("role") for entry in active_entries}
    for role in sorted(REQUIRED_DIAGRAM_ROLES[effective_mode] - roles):
        errors.append(f"{effective_mode} mode missing required diagram role: {role}")
    actual_count = sum(entry.get("status") != "not_applicable" for entry in active_entries)
    if effective_mode == "fast" and actual_count > 2:
        warnings.append("fast mode should normally contain no more than two actual diagrams")


def validate(repo: Path, book: Path, *, mode: str | None = None, targets: list[str] | None = None) -> Result:
    repo = repo.resolve()
    book = book.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    manifest_path = book / ".learning-manifest.json"
    manifest: dict = {}
    manifest_is_object = False

    if not manifest_path.is_file():
        errors.append("missing project-book/.learning-manifest.json")
    else:
        try:
            loaded_manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"invalid manifest JSON: {error}")
        else:
            if isinstance(loaded_manifest, dict):
                manifest = loaded_manifest
                manifest_is_object = True
            else:
                errors.append("manifest root must be a JSON object")

    if manifest_is_object:
        missing_keys = sorted(REQUIRED_MANIFEST_KEYS - manifest.keys())
        if missing_keys:
            errors.append(f"manifest missing keys: {', '.join(missing_keys)}")
        if manifest.get("schema_version") != 2:
            errors.append("manifest schema_version must be 2")
        manifest_mode = manifest.get("mode")
        if manifest_mode not in {"full", "fast", "targeted"}:
            errors.append("mode must be full, fast, or targeted")
            effective_mode = mode or "full"
        else:
            effective_mode = manifest_mode
            if mode is not None and mode != manifest_mode:
                errors.append(f"CLI mode {mode!r} does not match manifest mode {manifest_mode!r}")
    else:
        effective_mode = mode or "full"

    manifest_targets = _normalize_targets(manifest.get("targets", [])) if manifest_is_object else []
    cli_targets = _normalize_targets(targets or [])
    if manifest_is_object and targets is not None and set(cli_targets) != set(manifest_targets):
        errors.append("CLI targets do not match manifest targets")
    requested_targets = manifest_targets if manifest_is_object else cli_targets
    if effective_mode == "targeted":
        if not requested_targets:
            errors.append("targeted mode requires chapter targets")
        required_chapters = requested_targets
    else:
        required_chapters = CHAPTERS

    if manifest_is_object and effective_mode == "targeted":
        preservation = manifest.get("preservation")
        preserved_chapters = preservation.get("chapters") if isinstance(preservation, dict) else None
        if not isinstance(preserved_chapters, dict):
            errors.append("targeted mode requires preservation.chapters baseline")
        else:
            current_snapshot = snapshot_chapters(book)
            for chapter in CHAPTERS:
                if chapter in required_chapters:
                    continue
                if chapter not in preserved_chapters:
                    errors.append(f"missing preservation baseline for {chapter}")
                    continue
                expected = preserved_chapters[chapter]
                current = current_snapshot[chapter]
                if expected != current:
                    errors.append(f"unrelated chapter changed during targeted update: {chapter}")

    for chapter in required_chapters:
        path = book / chapter
        if not path.is_file():
            errors.append(f"missing chapter: {chapter}")
        elif not path.read_text(encoding="utf-8-sig").strip():
            errors.append(f"empty chapter: {chapter}")

    all_text = ""
    scan_chapters = required_chapters if effective_mode == "targeted" else CHAPTERS
    for chapter in scan_chapters:
        path = book / chapter
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8-sig")
        all_text += f"\n{text}"
        if not _fences_are_balanced(text):
            errors.append(f"unbalanced Markdown fence: {path.name}")
        for placeholder in PLACEHOLDER_RE.findall(text):
            errors.append(f"unresolved placeholder in {path.name}: {placeholder}")
        evidence_references = _evidence_references(text)
        if not evidence_references:
            errors.append(f"missing inline file:line evidence in {path.name}")
        for evidence_path, line_number in evidence_references:
            if evidence_path.startswith("/") or re.match(r"^[A-Za-z]:/", evidence_path):
                errors.append(f"evidence path must be repository-relative in {path.name}: {evidence_path}")
                continue
            evidence_file = repo / evidence_path
            if not evidence_file.is_file():
                errors.append(f"missing evidence path in {path.name}: {evidence_path}")
            else:
                line_count = len(evidence_file.read_text(encoding="utf-8-sig", errors="replace").splitlines())
                if line_number > max(1, line_count):
                    errors.append(f"evidence line out of range in {path.name}: {evidence_path}:{line_number}")

    for pattern in SECRET_PATTERNS:
        if pattern.search(all_text):
            errors.append(f"possible secret matched pattern: {pattern.pattern}")
    if SECRET_URI_RE.search(all_text):
        errors.append("possible credential-bearing URL")
    for match in SECRET_ASSIGNMENT_RE.finditer(all_text):
        value = match.group(1).strip("'\"")
        if not SAFE_SECRET_VALUES.match(value):
            errors.append("possible unredacted secret assignment")

    if manifest_is_object:
        current_head = _git_head(repo)
        recorded_head = manifest.get("head_sha")
        if current_head != recorded_head:
            changed_paths = (
                _git_changed_paths(repo, recorded_head, current_head)
                if isinstance(recorded_head, str) and current_head
                else None
            )
            try:
                book_prefix = book.relative_to(repo).as_posix().rstrip("/") + "/"
            except ValueError:
                book_prefix = None
            source_changes = (
                [path for path in changed_paths if not book_prefix or not path.startswith(book_prefix)]
                if changed_paths is not None
                else None
            )
            if source_changes is None or source_changes:
                errors.append(f"manifest head_sha is stale: {recorded_head!r} != {current_head!r}")

        sources = manifest.get("chapter_sources", {})
        if not isinstance(sources, dict):
            errors.append("chapter_sources must be an object")
        else:
            for chapter in required_chapters:
                if not sources.get(chapter):
                    errors.append(f"missing chapter_sources evidence for {chapter}")
            for chapter, chapter_sources in sources.items():
                if chapter not in CHAPTERS:
                    warnings.append(f"unknown chapter_sources key: {chapter}")
                if effective_mode == "targeted" and chapter not in required_chapters:
                    continue
                if not isinstance(chapter_sources, list):
                    errors.append(f"chapter_sources for {chapter} must be a list")
                    continue
                for source in chapter_sources:
                    if not isinstance(source, str) or not (repo / source).exists():
                        errors.append(f"missing chapter source for {chapter}: {source!r}")

            for chapter in required_chapters:
                chapter_path = book / chapter
                if not chapter_path.is_file() or not isinstance(sources.get(chapter), list):
                    continue
                inline_paths = {
                    evidence_path
                    for evidence_path, _ in _evidence_references(
                        chapter_path.read_text(encoding="utf-8-sig")
                    )
                }
                declared_paths = {
                    source.replace("\\", "/")
                    for source in sources[chapter]
                    if isinstance(source, str)
                }
                if inline_paths and not inline_paths.issubset(declared_paths):
                    undeclared = ", ".join(sorted(inline_paths - declared_paths))
                    errors.append(
                        f"inline evidence not declared in chapter_sources for {chapter}: {undeclared}"
                    )

        _validate_diagrams(
            repo,
            book,
            manifest,
            effective_mode,
            required_chapters,
            sources,
            errors,
            warnings,
        )

        for entrypoint in manifest.get("entrypoints", []):
            if not isinstance(entrypoint, str) or not (repo / entrypoint).is_file():
                errors.append(f"missing manifest entrypoint: {entrypoint!r}")
        for subproject in manifest.get("subprojects", []):
            if not isinstance(subproject, dict) or not isinstance(subproject.get("path"), str):
                errors.append("invalid subprojects entry")
                continue
            if not (repo / subproject["path"]).exists():
                errors.append(f"missing subproject path: {subproject['path']!r}")
            for source_manifest in subproject.get("manifests", []):
                if not isinstance(source_manifest, str) or not (repo / source_manifest).is_file():
                    errors.append(f"missing subproject manifest: {source_manifest!r}")

        validation = manifest.get("validation", {})
        for name in ("paths", "markdown", "placeholders", "secrets", "diagrams", "examples"):
            item = validation.get(name) if isinstance(validation, dict) else None
            state = item.get("status") if isinstance(item, dict) else None
            if state not in ALLOWED_STATES:
                errors.append(f"validation.{name}.status is missing or invalid")
            elif state == "failed":
                errors.append(f"manifest records failed validation: {name}")
        example_item = validation.get("examples", {}) if isinstance(validation, dict) else {}
        example_state = example_item.get("status") if isinstance(example_item, dict) else None
        if example_state == "passed":
            command = example_item.get("command")
            exit_code = example_item.get("exit_code")
            level = example_item.get("level")
            if not isinstance(command, str) or not command.strip():
                errors.append("passed example validation requires a command")
            if not isinstance(exit_code, int) or isinstance(exit_code, bool) or exit_code != 0:
                errors.append("passed example validation requires exit_code 0")
            if level not in {"syntax", "type", "test", "runtime"}:
                errors.append("passed example validation requires level syntax, type, test, or runtime")
        if effective_mode == "fast" and example_state != "passed":
            errors.append("fast mode requires at least one syntax-validated example")
        elif example_state in {"static", "not_run"}:
            warnings.append("examples are not runtime-verified; do not call them runnable")

        diagram_item = validation.get("diagrams", {}) if isinstance(validation, dict) else {}
        diagram_state = diagram_item.get("status") if isinstance(diagram_item, dict) else None
        if diagram_state == "passed":
            command = diagram_item.get("command")
            exit_code = diagram_item.get("exit_code")
            level = diagram_item.get("level")
            if not isinstance(command, str) or not command.strip():
                errors.append("passed diagram validation requires a renderer command")
            if not isinstance(exit_code, int) or isinstance(exit_code, bool) or exit_code != 0:
                errors.append("passed diagram validation requires exit_code 0")
            if level != "render":
                errors.append("passed diagram validation requires level render")
        elif diagram_state == "static":
            if not isinstance(diagram_item.get("reason"), str) or not diagram_item["reason"].strip():
                errors.append("static diagram validation requires a reason")

    return Result(errors=list(dict.fromkeys(errors)), warnings=list(dict.fromkeys(warnings)))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", type=Path)
    parser.add_argument("--book", type=Path)
    parser.add_argument("--mode", choices=("full", "fast", "targeted"))
    parser.add_argument("--target", action="append", default=[])
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--snapshot",
        action="store_true",
        help="print chapter SHA-256 and mtime baseline for a targeted update",
    )
    args = parser.parse_args()
    book = args.book or args.repo / "project-book"
    if args.snapshot:
        print(json.dumps({"chapters": snapshot_chapters(book)}, ensure_ascii=False, indent=2))
        return 0
    result = validate(args.repo, book, mode=args.mode, targets=args.target or None)
    payload = {"ok": result.ok, **asdict(result)}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("PASS" if result.ok else "FAIL")
        for message in result.errors:
            print(f"ERROR: {message}")
        for message in result.warnings:
            print(f"WARNING: {message}")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
