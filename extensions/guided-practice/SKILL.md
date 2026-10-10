---
name: guided-practice
description: Guide a learner through safe, evidence-backed exercises using an existing project-book. Use only when the user asks for practice, a learning plan, or a knowledge check; never add a default chapter.
---

# Guided practice

Turn the repository's existing learning material into concrete practice with observable outcomes. This is an **optional extension**, not a ninth core phase or an eleventh project-book chapter.

## Required reading and entry conditions

1. Read [the output contract](../../references/output-contract.md) and [evidence and safety rules](../../references/evidence-and-safety.md).
2. Resolve the **target repository** independently from this skill's installation directory. Inspect Git status and `project-book/.learning-manifest.json` without changing either.
3. Read `project-book/10-learning-checklist.md` first, then the relevant parts of chapters 03-08 and the actual cited source/tests. Do not assume that a chapter statement is true merely because it exists.
4. If the book is missing, explain that `project-learning-agent` must generate the needed chapters first; offer a read-only, clearly provisional source-based practice path if the user wants to proceed.
5. If the book's source `head_sha` differs from HEAD, check whether the intervening changes are only in `project-book/`. For source changes, verify affected evidence against current code or mark exercises `待复核`. If a diff is unavailable, treat freshness as unknown, not confirmed.
6. Do not invoke this extension in a normal `full`, `fast`, or `targeted` documentation run unless practice is also explicitly requested.

## Design an exercise

Select tasks based on the user's stated goal and available time; if unspecified, choose one representative core flow and propose a short three-step sequence. Each exercise must include:

- **Goal and prerequisites**: the capability being learned, assumed background, and relevant chapter(s).
- **Evidence trail**: a real repository-relative `path:line` anchor for the entrypoint, central contract, and test or observable behavior where available.
- **Learner action**: a precise read / explain / predict / verify task. Start with read-only inspection, then a project-native safe command only if appropriate.
- **Expected observation and pass criteria**: externally checkable behavior, plus one failure path or edge case; distinguish expectations from results actually observed.
- **Hints and stretch task**: offer one progressively more revealing hint and one optional deeper extension.

Use the progression **locate → explain → predict → verify → reflect**. Do not invent commands, imports, APIs, tests, output, or passing results.

## Execution and feedback

1. Present the exercise and expected evidence. When coaching interactively, allow the learner to attempt it before revealing the model answer; when asked for a complete self-study plan, provide the whole sequence at once.
2. For each attempted step, compare the learner's explanation or observed output with the source contracts, cited tests, and stated acceptance criteria. Explain gaps with evidence, not just a score.
3. Track steps as `planned`, `attempted`, `validated`, or `blocked`. Mark `validated` only when the user's supplied evidence or a tool result actually demonstrates the acceptance criteria. Reading a page alone does not prove mastery.
4. Label observations using the existing vocabulary: `已运行`, `静态验证`, `静态推断`, or `未运行`. Show exact commands only when they were executed and report failures honestly.
5. Finish with a concise recap of demonstrated learning, unresolved questions, and the next most useful exercise.

## Safety and output boundaries

- **Read-only by default.** Never modify source, install dependencies, run services, contact external APIs, execute migrations, or write practice answers into the repository without explicit user authorization. Never reveal real `.env` values or credentials.
- Safe test execution must follow [evidence and safety rules](../../references/evidence-and-safety.md); an example with side effects is presented as `未运行` unless explicitly authorized.
- Default output is **the conversation**, not a file. Only when the user requests a persistent session record, write `project-book/practice-session.md` (new file or carefully reviewed update). Keep all ten stable chapter names and `.learning-manifest.json` unchanged; never rewrite learner-authored notes silently.
- An optional practice-session file is **not** an additional target chapter and must not be inserted into `targets` or `chapter_sources`. Its status is not a substitute for `scripts/validate_book.py` validation.

## Acceptance

- Every exercise traces to real source evidence or is explicitly marked provisional.
- An assessment separates source knowledge, learner attempts, and observed verification.
- Normal documentation modes still use the same eight child skills and ten book chapters.
- No unapproved writes or unsafe executions occur.
