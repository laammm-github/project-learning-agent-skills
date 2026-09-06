---
name: 03-architecture-analysis
description: Analyze module boundaries, runtime processes, dependencies, deployment, cross-cutting concerns, decisions, and risks, then create project-book/03-architecture.md.
---

# Architecture analysis

Turn the repository inventory into a verified static, runtime, and deployment model. Read `../references/output-contract.md` and `../references/evidence-and-safety.md` first.

## Analysis workflow

1. **Boundaries**: identify components from manifests, entrypoints, package boundaries, public interfaces, persistence adapters, and ownership rules. Record responsibility and data owned by each component.
2. **Static dependencies**: trace imports, API clients, shared libraries, schemas, and generated contracts. State dependency direction and flag cycles or boundary leaks only when evidenced.
3. **Runtime processes**: start from confirmed entrypoints and map request handlers, workers, schedulers, queues, event buses, databases, caches, and external services.
4. **Deployment topology**: verify process/container names, ports, health checks, volumes, networks, scaling units, and startup ordering from deployment configuration.
5. **Cross-cutting concerns**: locate authentication/authorization, tenancy, configuration, observability, retries, idempotency, transactions, caching, billing, and error translation when present.
6. **Decisions and risks**: distinguish explicit decisions from `静态推断`. Link each tradeoff or risk to concrete implementation evidence and explain impact rather than guessing intent.
7. **Representative verification**: cross-check the model against at least one real route, command, job, or library call and its tests.

## Output

Write `project-book/03-architecture.md` with:

- scope and analysis baseline;
- subsystem/context map;
- module responsibilities and owned data;
- dependency direction and contracts;
- runtime process and deployment diagrams;
- cross-cutting capability map;
- architectural decisions, tradeoffs, risks, and known unknowns;
- evidence index.

Use Mermaid only when it materially clarifies relationships and keep node names identical to source/deployment names. Update `chapter_sources`.

## Acceptance

- Every component shown exists and every important edge has `path:line` evidence.
- Static structure, runtime interaction, and deployment are not conflated.
- Hybrid repositories show subsystem-specific architecture plus integration points.
- Unknowns and inferred intent are labeled rather than presented as fact.
