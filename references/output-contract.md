# Output contract

Read this reference for every orchestrated run and whenever a child skill writes a chapter.

## Stable output interface

All output lives directly under `project-book/`:

```text
project-book/
├── .learning-manifest.json
├── 01-project-overview.md
├── 02-installation.md
├── 03-architecture.md
├── 04-core-flow.md
├── 05-core-concepts.md
├── 06-source-code-guide.md
├── 07-extension-guide.md
├── 08-examples.md
├── 09-faq.md
└── 10-learning-checklist.md
```

Full and fast runs require all ten chapters. A targeted run requires the manifest and the chapter files named in `targets`; it must preserve unrelated existing chapters.

A targeted manifest also contains the pre-write snapshot from `validate_book.py <repo> --snapshot`:

```json
{
  "preservation": {
    "captured_at": "ISO-8601 timestamp",
    "chapters": {
      "01-project-overview.md": {"sha256": "hex digest", "mtime_ns": 123456789},
      "02-installation.md": null
    }
  }
}
```

Include all ten chapter keys; `null` means the chapter did not exist before the targeted update. Never refresh this snapshot after writing.

## Manifest schema

Write valid JSON with this shape:

```json
{
  "schema_version": 2,
  "repo_root": ".",
  "head_sha": "40-character Git SHA or null",
  "generated_at": "ISO-8601 timestamp",
  "mode": "full",
  "targets": [],
  "subprojects": [{"path": ".", "manifests": ["pyproject.toml"]}],
  "project_types": [{"path": ".", "types": ["web", "library"]}],
  "entrypoints": ["src/app.py"],
  "chapter_sources": {
    "01-project-overview.md": ["README.md", "pyproject.toml"]
  },
  "validation": {
    "paths": {"status": "passed", "reason": null},
    "markdown": {"status": "passed", "reason": null},
    "placeholders": {"status": "passed", "reason": null},
    "secrets": {"status": "passed", "reason": null},
    "examples": {
      "status": "passed",
      "reason": "Python syntax validation",
      "command": "python -m py_compile examples/hello.py",
      "exit_code": 0,
      "level": "syntax"
    }
  }
}
```

Allowed validation states are `passed`, `failed`, `static`, and `not_run`. A passed example validation must record `command`, integer `exit_code: 0`, and `level` (`syntax`, `type`, `test`, or `runtime`). A null `head_sha` is valid outside Git. In Git repositories, `head_sha` is the analyzed source baseline; later commits that change only `project-book/` do not invalidate it. Use repository-relative POSIX-style paths even on Windows; paths may contain spaces.

## Evidence format

- Cite a concrete symbol or claim as ``path/to/file.py:42``.
- Use a tight line anchor, not a directory or guessed line range.
- Paths are relative to the repository root and must exist at validation time.
- Put chapter evidence in prose and repeat the source paths in `chapter_sources`.
- Every generated chapter must contain at least one inline evidence citation, and every inline evidence path must be declared in that chapter's `chapter_sources` entry.
- Label inference as `静态推断`; label unexecuted commands as `未运行`.

## Chapter acceptance

1. Overview: repository shape, subsystem types, manifests, entrypoints, technology stack, and reading route.
2. Installation: prerequisites, official commands, configuration precedence, variable names, and verification status.
3. Architecture: module boundaries, dependency direction, runtime processes, deployment, cross-cutting concerns, decisions, and risks.
4. Core flow: one to three representative flows with input, transformation, output, persistence, and failures.
5. Concepts: real abstractions, contracts, invariants, extension points, and code evidence.
6. Source guide: goal-oriented reading paths from entrypoint to contract to implementation.
7. Extension guide: project-specific steps, registration, tests, and compatibility constraints.
8. Examples: project-native illustrative and runnable examples with explicit validation status.
9. FAQ: questions derived from real architecture, setup, and validation gaps.
10. Checklist: semantic coverage matrix, validation results, known unknowns, and practice tasks.

Fast mode keeps the same chapters but may shorten each to the evidence needed for one main subsystem. Targeted mode does not create empty placeholder chapters.
