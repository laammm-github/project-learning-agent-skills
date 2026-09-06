---
name: 06-tutorial-writer
description: Convert project-book chapters 01-05 into evidence-backed source navigation and extension guides without rewriting the source chapters.
---

# Tutorial writer

Read `../references/output-contract.md`. Inputs are `project-book/01-project-overview.md` through `05-core-concepts.md`; never read or write `docs/analysis/`.

## Source guide

Create `project-book/06-source-code-guide.md` around reader goals, not filesystem order:

- fastest path: entrypoint → central contract → representative implementation;
- module paths: responsibility, key files/symbols, callers, dependencies, and tests;
- task paths: where to read for API, execution, persistence, UI, configuration, or other detected subsystems;
- deeper comparisons between simple and advanced implementations;
- `path:line` evidence and next practice task.

## Extension guide

Create `project-book/07-extension-guide.md` only from real extension points established in chapter 05:

- supported extension type and compatibility contract;
- files to add/change, registration/discovery path, configuration, and tests;
- smallest project-native illustrative snippet, labeled `示意`;
- validation command and expected observable behavior;
- failure modes, security/tenancy rules, and migration concerns when applicable.

Do not promise copy-paste execution here; runnable artifacts belong in chapter 08. Preserve chapters 01-05 and update `chapter_sources` for chapters 06-07.

## Acceptance

- All reading and extension paths resolve to real files/symbols.
- Guidance follows project conventions and applicable repository instructions.
- No generic plugin/tool template is used when the project lacks that extension model.
- Chapters end with a concrete next reading or practice task.
