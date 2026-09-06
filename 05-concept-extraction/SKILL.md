---
name: 05-concept-extraction
description: Extract real abstractions, contracts, invariants, and extension points from source code, then create project-book/05-core-concepts.md.
---

# Concept and contract extraction

Read `../references/output-contract.md`. Use architecture and flow evidence to select concepts that explain how the project is designed.

## Analysis

1. Identify central domain types, interfaces, schemas, protocols, registries, lifecycle abstractions, and state machines from real code.
2. For each concept capture purpose, contract, required behavior, optional behavior, invariants, failure behavior, and extension mechanism.
3. Quote only short signatures or minimal real excerpts with `path:line`; never substitute a generic sample class for the project's contract.
4. Verify usage through implementations and tests. Note divergent implementations and compatibility constraints.
5. Add an analogy only when it preserves the important constraints; state where the analogy stops applying.

## Output

Write `project-book/05-core-concepts.md` with key concepts, contracts/invariants, concept relationships, extension points, common misconceptions, and evidence index. Update `chapter_sources`.

## Acceptance

- Every named abstraction and method exists in the repository.
- “Must” requirements are enforced by an interface, validation, test, or call site.
- Illustrative pseudocode is clearly labeled and never presented as source.
- Concepts explain design decisions rather than paraphrasing implementation line by line.
