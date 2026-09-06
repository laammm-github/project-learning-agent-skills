---
name: 07-example-generator
description: Generate project-native illustrative and runnable examples with explicit verification status in project-book/08-examples.md.
---

# Example generator

Read `../references/output-contract.md` and `../references/evidence-and-safety.md`. Require a confirmed contract or extension point from chapter 05 or 07.

## Example classes

- **示意示例** explains a concept and may omit setup, but must say it is not directly runnable.
- **可运行示例** has no unresolved placeholders, uses only project languages and supported APIs, includes exact prerequisites, and passes at least a native syntax/type check.

Generate other language variants only when the repository actually exposes supported interfaces in those languages or the user asks for them.

## Workflow

1. Select the smallest official invocation or extension pattern and verify imports, signatures, registration, configuration, and expected output.
2. Prefer existing test fixtures and documented examples as structural references without copying large passages.
3. Put complete files in an `examples/` directory only when the user requests physical example files; otherwise keep them in chapter 08.
4. Run a safe syntax/type check or focused test. Record the exact command and result.
5. If execution is unavailable, downgrade the snippet to `示意示例` or mark it `未运行`; never call it runnable.

## Output

Write `project-book/08-examples.md` with a minimal usage example, relevant extension example, configuration example using valid syntax, registration/testing steps, expected behavior, and per-example verification status. Update `chapter_sources` and `validation.examples`.

## Acceptance

- No `[placeholder]`, fake import, invented API, or commented JSON remains in runnable material.
- Every runnable example has a successful validation command.
- Examples follow repository conventions and do not require unsafe side effects by default.
- Secret values are redacted.
