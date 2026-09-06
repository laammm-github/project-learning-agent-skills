# Evidence and safety

Read this reference before configuration inspection, command execution, or incremental updates.

## Evidence levels

Use the strongest available label:

- **已运行**: the command or example completed successfully during this run; include the exact command.
- **静态验证**: supported by source, manifest, test, or configuration evidence but not executed.
- **静态推断**: a reasoned conclusion that is not directly declared; state the supporting files.
- **未运行**: execution was unsafe, unavailable, expensive, or outside user scope; state why.

README prose is a lead, not final proof. Confirm important claims against manifests, entrypoints, routes, tests, container definitions, or implementation code.

## Secret handling

- Prefer `.env.example`, `.env.default`, schema definitions, and settings code.
- Read variable names, defaults known to be non-sensitive, and precedence rules. Do not copy values from real `.env` files, credential stores, shell environments, or CI secrets.
- Redact suspicious values as `<redacted>`. Never include API keys, tokens, private keys, passwords, cookies, or connection strings containing credentials.
- Do not print an entire environment or configuration file merely to discover names.

## Safe execution

- Static analysis is the default.
- Dependency installation, containers, migrations, external API calls, paid model calls, and writes outside `project-book/` require explicit user scope or an already-authorized workflow.
- Prefer syntax checks and existing focused tests. Record the command, result, and limitations.
- Never report an illustrative snippet as runnable. A runnable example must contain no unresolved placeholders and must pass at least a language-native syntax/type check.

## Existing books and incremental updates

1. Inspect Git status and the existing book before writing.
2. If the book has no manifest, treat it as legacy: preserve useful text, establish a manifest, and change only claims verified against the current repository.
3. If the manifest HEAD differs, obtain the changed file list with Git and exclude changes under `project-book/`. The manifest SHA identifies the analyzed source baseline, so book-only commits do not require regeneration. Map remaining source changes through `chapter_sources`; also update dependent chapters when a public contract changed.
4. In targeted mode, capture `validate_book.py <repo> --snapshot` before writing, store it under manifest `preservation`, and preserve unrelated chapter bytes and timestamps. Do not regenerate this baseline after edits.
5. If generated and user-authored text cannot be distinguished safely, stop and ask before overwriting the affected chapter.

## Scale controls

- Prefer `rg --files`; fall back to a cross-platform filesystem walk.
- Exclude dependency, VCS, cache, build, coverage, generated, and binary-heavy directories.
- Discover all manifests first, then sample entrypoints and boundaries per subproject.
- Do not use arbitrary `head -N` results as proof of importance.
- For very large repositories, document excluded areas and analyze the user-relevant subsystems first.
