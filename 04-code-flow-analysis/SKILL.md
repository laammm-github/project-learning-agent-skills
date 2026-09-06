---
name: 04-code-flow-analysis
description: Trace representative end-to-end code and data flows with transformations, persistence, and failures, then create project-book/04-core-flow.md.
---

# Code flow analysis

Read `../references/output-contract.md`; require repository discovery and architecture context before selecting a flow.

## Flow selection

- Full mode: trace one to three flows covering the primary user journey and materially different asynchronous or privileged paths.
- Fast mode: trace one representative primary flow.
- Targeted mode: trace the requested flow only.

Choose flows from real entrypoints and call sites, not generic Controller/Service templates.

## Trace method

For every hop record:

- concrete `path:line` and symbol;
- input type/shape and origin;
- validation, normalization, enrichment, routing, or serialization;
- output type/shape and consumer;
- state read/written and transaction boundary;
- synchronous/asynchronous boundary;
- authentication, authorization, tenancy, retries, timeout, cancellation, and error translation when applicable.

Follow alternate and failure paths far enough to explain externally visible behavior. Use tests to confirm non-obvious branches. Do not infer runtime order solely from directory layout.

## Output

Write `project-book/04-core-flow.md` with selection rationale, sequence diagram, step-by-step transformations, persistence/events, key context propagation, error/cancellation paths, evidence, and known unknowns. Update `chapter_sources`.

## Acceptance

- Each arrow maps to a real call, message, event, or persisted transition.
- Input → transformation → output is explicit at every important boundary.
- At least one failure path is covered per flow.
- Static-only conclusions are labeled `静态推断`.
