#!/usr/bin/env python3
"""Emit a safe, cross-platform repository inventory as JSON."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Iterable


EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".cache",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "venv",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "coverage",
    ".coverage",
    ".next",
    ".nuxt",
    "target",
    "__pycache__",
}

MANIFEST_NAMES = {
    "pyproject.toml",
    "requirements.txt",
    "package.json",
    "pnpm-workspace.yaml",
    "Cargo.toml",
    "go.mod",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "Gemfile",
    "composer.json",
    "docker-compose.yml",
    "docker-compose.yaml",
    "Makefile",
}

RULE_NAMES = {"AGENTS.md", "CONTRIBUTING.md", "CLAUDE.md", "README.md"}
ENTRY_NAMES = {
    "app.py",
    "main.py",
    "__main__.py",
    "manage.py",
    "index.ts",
    "index.tsx",
    "server.ts",
    "server.js",
    "main.go",
    "main.rs",
    "Program.cs",
}


def _is_included(relative: Path) -> bool:
    lowered = {part.lower() for part in relative.parts}
    return not lowered.intersection({part.lower() for part in EXCLUDED_DIRS})


def _is_manifest(path: Path) -> bool:
    name = path.name
    return (
        name in MANIFEST_NAMES
        or name == "Dockerfile"
        or (name.startswith("docker-compose.") and name.endswith((".yml", ".yaml")))
        or (name.startswith("compose.") and name.endswith((".yml", ".yaml")))
    )


def _rg_files(repo: Path) -> list[Path] | None:
    if not shutil.which("rg"):
        return None
    result = subprocess.run(
        ["rg", "--files", "--hidden"],
        cwd=repo,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    if result.returncode not in (0, 1):
        return None
    return [Path(line) for line in result.stdout.splitlines() if line.strip()]


def _walk_files(repo: Path) -> list[Path]:
    files: list[Path] = []
    for current, dirs, names in os.walk(repo):
        dirs[:] = [name for name in dirs if name.lower() not in {d.lower() for d in EXCLUDED_DIRS}]
        current_path = Path(current)
        files.extend((current_path / name).relative_to(repo) for name in names)
    return files


def collect_files(repo: Path, *, prefer_rg: bool = True, max_files: int = 20_000) -> tuple[list[Path], bool, str]:
    raw = _rg_files(repo) if prefer_rg else None
    source = "rg" if raw is not None else "filesystem"
    raw = raw if raw is not None else _walk_files(repo)
    unique = sorted({path for path in raw if _is_included(path)}, key=lambda p: p.as_posix().lower())
    return unique[:max_files], len(unique) > max_files, source


def _git_value(repo: Path, args: list[str]) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args], cwd=repo, text=True, encoding="utf-8", errors="replace", capture_output=True, check=False
        )
    except OSError:
        return None
    value = result.stdout.strip()
    return value if result.returncode == 0 and value else None


def _resolve_module_entrypoint(manifest: Path, module: str, files: set[str]) -> str | None:
    module = module.strip().split(":", 1)[0]
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.]*", module):
        return None
    base = manifest.parent / Path(*module.split("."))
    for candidate in (base.with_suffix(".py"), base / "__init__.py"):
        value = candidate.as_posix()
        if value in files:
            return value
    return None


def _declared_entrypoints(repo: Path, manifests: list[Path], files: list[Path]) -> list[Path]:
    """Resolve only conventional or manifest-declared executable source files."""
    file_names = {path.as_posix() for path in files}
    confirmed: set[str] = {
        path.as_posix()
        for path in files
        if path.name in {"__main__.py", "main.go", "main.rs", "Program.cs"}
        and not {"test", "tests", "fixtures", "examples"}.intersection({part.lower() for part in path.parts})
    }

    manifest_roots = {path.parent for path in manifests}
    for path in files:
        if path.name in {"app.py", "main.py", "manage.py"} and path.parent in manifest_roots:
            confirmed.add(path.as_posix())

    for manifest in manifests:
        try:
            text = (repo / manifest).read_text(encoding="utf-8-sig", errors="replace")
        except OSError:
            continue
        if manifest.name == "pyproject.toml":
            in_scripts = False
            for line in text.splitlines():
                stripped = line.strip()
                if stripped.startswith("[") and stripped.endswith("]"):
                    in_scripts = stripped in {"[project.scripts]", "[tool.poetry.scripts]"}
                    continue
                if not in_scripts or "=" not in stripped:
                    continue
                value_match = re.match(r"[^=]+\s*=\s*['\"]([^'\"]+)['\"]", stripped)
                if value_match and (resolved := _resolve_module_entrypoint(manifest, value_match.group(1), file_names)):
                    confirmed.add(resolved)
        elif manifest.name == "package.json":
            try:
                package = json.loads(text)
            except json.JSONDecodeError:
                continue
            declared: list[str] = []
            for field in (package.get("main"), package.get("module"), package.get("browser")):
                if isinstance(field, str):
                    declared.append(field)
            package_bin = package.get("bin")
            if isinstance(package_bin, str):
                declared.append(package_bin)
            elif isinstance(package_bin, dict):
                declared.extend(value for value in package_bin.values() if isinstance(value, str))
            for value in declared:
                candidate = (manifest.parent / value).as_posix()
                if candidate in file_names:
                    confirmed.add(candidate)

    return [Path(path) for path in sorted(confirmed, key=str.lower)]


def _declares_cli(repo: Path, files: Iterable[Path]) -> bool:
    for path in files:
        if path.name == "pyproject.toml":
            try:
                text = (repo / path).read_text(encoding="utf-8-sig", errors="replace")
            except OSError:
                continue
            if re.search(r"(?m)^\[(?:project\.scripts|tool\.poetry\.scripts)\]\s*$", text):
                return True
        elif path.name == "package.json":
            try:
                package = json.loads((repo / path).read_text(encoding="utf-8-sig"))
            except (OSError, json.JSONDecodeError):
                continue
            if package.get("bin"):
                return True
    return False


def _subsystem_types(repo: Path, root: Path, files: Iterable[Path]) -> list[str]:
    relative_files = list(files)
    names = {path.name for path in relative_files}
    parts = {part.lower() for path in relative_files for part in path.parts}
    types: set[str] = set()
    if "package.json" in names and ({"app", "pages", "frontend", "web"} & parts):
        types.add("web")
    if {"app.py", "server.ts", "server.js", "main.go"} & names:
        types.add("service")
    if {"__main__.py", "manage.py"} & names or "cmd" in parts or "cli" in parts or _declares_cli(repo, relative_files):
        types.add("cli")
    if {"pyproject.toml", "Cargo.toml", "go.mod", "package.json"} & names:
        types.add("library")
    if "worker" in parts or "workers" in parts or "executor" in parts:
        types.add("worker")
    if "agent" in parts or "agents" in parts or "tools" in parts:
        types.add("agent-runtime")
    if any(name.startswith("docker-compose") for name in names) or "Dockerfile" in names:
        types.add("infrastructure")
    return sorted(types or {"unknown"})


def build_inventory(repo: Path, *, prefer_rg: bool = True, max_files: int = 20_000) -> dict:
    repo = repo.resolve()
    if not repo.is_dir():
        raise ValueError(f"Repository directory does not exist: {repo}")

    files, truncated, source = collect_files(repo, prefer_rg=prefer_rg, max_files=max_files)
    manifests = [path for path in files if _is_manifest(path)]
    rules = [path for path in files if path.name in RULE_NAMES]
    entrypoint_candidates = [
        path
        for path in files
        if path.name in ENTRY_NAMES and not {"test", "tests", "fixtures", "examples"}.intersection({p.lower() for p in path.parts})
    ]
    entries = _declared_entrypoints(repo, manifests, files)

    roots = sorted({path.parent for path in manifests}, key=lambda p: (len(p.parts), p.as_posix()))
    subproject_roots = roots or [Path(".")]
    subprojects = []
    project_types = []
    for root in subproject_roots:
        scoped = [path for path in files if root == Path(".") or root in path.parents or path == root]
        scoped_manifests = [path.as_posix() for path in manifests if path.parent == root]
        subprojects.append({"path": root.as_posix(), "manifests": scoped_manifests})
        project_types.append({"path": root.as_posix(), "types": _subsystem_types(repo, root, scoped)})

    head_sha = _git_value(repo, ["rev-parse", "HEAD"])
    status = _git_value(repo, ["status", "--short"])
    return {
        "repo_root": str(repo),
        "repository_shape": "monorepo" if len(subproject_roots) > 1 else "single-project",
        "head_sha": head_sha,
        "dirty": bool(status),
        "discovery_source": source,
        "file_count": len(files),
        "truncated": truncated,
        "excluded_directories": sorted(EXCLUDED_DIRS),
        "rules": [path.as_posix() for path in rules],
        "manifests": [path.as_posix() for path in manifests],
        "subprojects": subprojects,
        "project_types": project_types,
        "entrypoints": [path.as_posix() for path in entries],
        "entrypoint_candidates": [path.as_posix() for path in entrypoint_candidates],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", type=Path)
    parser.add_argument("--max-files", type=int, default=20_000)
    parser.add_argument("--no-rg", action="store_true", help="Force the filesystem fallback")
    args = parser.parse_args()
    try:
        inventory = build_inventory(args.repo, prefer_rg=not args.no_rg, max_files=args.max_files)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(inventory, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
