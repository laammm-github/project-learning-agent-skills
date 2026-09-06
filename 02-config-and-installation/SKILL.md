---
name: 02-config-and-installation
description: Analyze safe installation, configuration precedence, and environment-variable names, then create project-book/02-installation.md without exposing secrets.
---

# Configuration and installation

Explain how to prepare and start the project without treating unexecuted commands as verified.

## Preparation

Read `../references/output-contract.md` and `../references/evidence-and-safety.md`. Require repository discovery or perform its lightweight preflight first.

## Analysis

1. Derive runtime versions and package-manager commands from manifests, lockfiles, tool-version files, containers, and CI.
2. Prefer documented setup commands that agree with build scripts and Compose/Make/task configuration.
3. Inspect configuration templates, settings schemas, and loader code. Do not print real `.env` contents or process environments.
4. Describe precedence from defaults through files, environment, CLI, and remote configuration when supported by code.
5. List variable names by required/optional category, source, consumer, and safe description. Never reproduce sensitive values or credential-bearing URLs.
6. Execute only safe, in-scope verification. Label every command `已运行`, `静态验证`, or `未运行`, with reason.

## Output

Write `project-book/02-installation.md` covering prerequisites, recommended setup, alternative setup when documented, configuration loading, variable names, startup/health checks, cleanup, and troubleshooting. Use valid syntax in configuration examples and redact values as `<redacted>`.

Update `chapter_sources` and the relevant manifest validation statuses.

## Acceptance

- Commands match authoritative project sources and have explicit status.
- No secret value, private key, cookie, token, password, or credential URL appears.
- Configuration precedence and consumers are supported by `path:line` evidence.
- No dependency installation, migration, container startup, or external call occurs without scope.
