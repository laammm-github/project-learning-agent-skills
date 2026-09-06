---
name: project-learning-agent
description: Analyze an unfamiliar code repository and create or incrementally update an evidence-backed project-book. Use for full, fast, or targeted repository learning; not for one-off code questions.
---

# Project Learning Agent

Create trustworthy learning material from the repository as it exists now. Preserve the eight child skill names and the `project-book/01-10` chapter interface.

## Required references

- Read [references/output-contract.md](references/output-contract.md) before creating or validating output.
- Read [references/evidence-and-safety.md](references/evidence-and-safety.md) before inspecting configuration, running commands, or updating an existing book.
- Read only the child skills needed by the selected mode. A full or fast run uses all eight; a targeted run uses the requested child and its dependencies.

## Modes

- **full**: default when the user asks to learn, document, or understand a whole repository. Produce all ten detailed chapters.
- **fast**: use when the user explicitly asks for a quick overview. Produce all ten concise chapters, one representative flow, and at least one project-native syntax-validated example.
- **targeted**: use when the user names a topic or child skill. Update only requested chapters and required dependencies; do not rewrite unrelated existing chapters.

Record the selected mode and targets in `project-book/.learning-manifest.json`.

## Phase 00: preflight

Before analysis or writes:

1. Resolve the repository root and inspect Git HEAD/status without changing it.
2. Read applicable `AGENTS.md`, `CONTRIBUTING.md`, README files, and build manifests.
3. Run `scripts/inventory_repo.py <repo>` when available. It emits a cross-platform JSON inventory without emitting source contents or secret values; distinguish manifest-confirmed `entrypoints` from filename-based `entrypoint_candidates`.
4. Identify the repository shape (`single-project` or `monorepo`) and every relevant subsystem type. Do not force a hybrid repository into one label.
5. Inspect an existing manifest and book. Treat a book without a manifest as legacy; preserve its content and establish a baseline before updating it.
   For targeted mode, run `scripts/validate_book.py <repo> --snapshot` before any writes and copy the result plus `captured_at` into manifest `preservation`; do not recapture it after writing.
6. Treat manifest `head_sha` as the analyzed source baseline. If HEAD changed, use the previous manifest plus `git diff <old>..HEAD --name-only`, excluding `project-book/`, to select affected chapters. A commit containing only the generated book does not stale the source baseline. Never silently replace user-authored material.

## Dependency graph

Use this ordering even when work is targeted:

```text
00 preflight
 └─ 01 discovery
     ├─ 02 configuration
     └─ 03 architecture
         ├─ 04 code flow
         └─ 05 concepts and contracts
             ├─ 06 source and extension guide
             └─ 07 runnable examples
                 └─ 08 review
```

Dependencies may be analyzed in memory during a targeted run, but only requested output files may be changed unless a dependency chapter is missing or factually incompatible. Report any additional chapter update.

## Execution

1. Run the selected child skills in dependency order.
2. Write every chapter directly under `project-book/`; never use `docs/analysis/`.
3. Cite material claims with repository-relative `path:line` evidence. Mark unsupported conclusions `静态推断` and commands not executed `未运行`.
4. Update the manifest after chapter generation. `chapter_sources` must list the evidence files used by each changed chapter. In targeted mode, retain the pre-write `preservation` baseline unchanged so validation can detect unrelated edits.
5. Run `scripts/validate_book.py <repo> --mode <mode>` and fix deterministic failures before delivery.
6. Report validation failures that cannot safely be fixed. Do not claim the book or an example is verified when it was not run.

## Child skill routing

- [01-repo-discovery](01-repo-discovery/SKILL.md): repository and subsystem inventory.
- [02-config-and-installation](02-config-and-installation/SKILL.md): installation and configuration.
- [03-architecture-analysis](03-architecture-analysis/SKILL.md): static and runtime architecture.
- [04-code-flow-analysis](04-code-flow-analysis/SKILL.md): representative end-to-end flows.
- [05-concept-extraction](05-concept-extraction/SKILL.md): real abstractions and contracts.
- [06-tutorial-writer](06-tutorial-writer/SKILL.md): source navigation and extension guidance.
- [07-example-generator](07-example-generator/SKILL.md): project-native runnable examples.
- [08-learning-review](08-learning-review/SKILL.md): semantic coverage, FAQ, checklist, and final validation.

## Completion

A run is complete only when required chapters and the manifest exist, changed claims have evidence, secrets are absent, examples have explicit validation status, and the validator has no errors. Keep automatic discovery behavior unchanged; this skill does not create `agents/openai.yaml`.

For skill maintenance, run `python scripts/self_check.py`; it validates the root plus eight child skills and executes the cross-platform script tests.
