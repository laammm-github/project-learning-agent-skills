---
name: 01-repo-discovery
description: Discover a repository's shape, subprojects, technology stacks, and real entrypoints, then create project-book/01-project-overview.md.
---

# Repository discovery

Produce an evidence-backed map of the repository, including hybrid and monorepo structures.

## Preparation

Read `../references/output-contract.md`. If configuration or an existing book is involved, also read `../references/evidence-and-safety.md`. Reuse Phase 00 inventory from the parent skill or run `../scripts/inventory_repo.py <repo>`.

## Analysis

1. Read applicable repository instructions and contributor documentation.
2. Use build and workspace manifests, container definitions, package scripts, executable declarations, and imports to identify subprojects. Directory names alone are insufficient.
3. Classify the repository shape and assign multiple applicable types to each subsystem, such as web, CLI, library, service, worker, agent runtime, storage, or infrastructure.
4. Treat inventory `entrypoint_candidates` only as leads. Confirm `entrypoints` from executable declarations, framework configuration, container commands, or direct call sites; do not promote candidates merely by filename.
5. Derive versions and dependencies from authoritative manifests rather than README prose.
6. Record exclusions and unknown areas for repositories too large to inspect completely.

## Output

Write `project-book/01-project-overview.md` with:

- analysis baseline and repository shape;
- one-sentence purpose and principal user journeys;
- subsystem inventory with types and responsibilities;
- annotated top-level tree;
- confirmed entrypoints and startup path;
- technology stack and authoritative manifests;
- shortest useful reading route;
- unknown or excluded areas.

Every material entrypoint, version, and subsystem claim needs repository-relative `path:line` evidence. Update manifest fields `subprojects`, `project_types`, `entrypoints`, and `chapter_sources`.

## Acceptance

- Supports more than one subsystem and project type.
- Contains no guessed entrypoint or version.
- Uses cross-platform discovery and excludes dependencies/build artifacts.
- Separates confirmed facts from `静态推断`.
