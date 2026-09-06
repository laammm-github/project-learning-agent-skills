---
name: 08-learning-review
description: Semantically review project learning material, generate the FAQ and checklist, and run deterministic book validation.
---

# Learning review

Read `../references/output-contract.md` and `../references/evidence-and-safety.md`. Review chapter meaning and evidence; keyword presence is not proof of coverage.

## Review workflow

1. Build a coverage matrix from the detected subsystem types and chapter acceptance criteria.
2. For each criterion record `covered`, `partial`, `unknown`, or `not_applicable`, with the chapter and source evidence.
3. Cross-check architecture against at least one flow, contracts against examples, installation against manifests, and all cited paths against the repository.
4. Identify contradictions, unsupported certainty, stale Git baselines, missing failure paths, unverified commands, and secret exposure.
5. Generate `project-book/09-faq.md` from real points of confusion and known gaps.
6. Generate `project-book/10-learning-checklist.md` with coverage, validation results, known unknowns, contribution-readiness tasks, and next learning steps.
7. Update all manifest validation statuses, then run `../scripts/validate_book.py <repo> --mode <mode>`. Fix deterministic errors or report them explicitly.

## Output rules

- Full and fast modes check all ten chapters plus `.learning-manifest.json`.
- Targeted mode checks the manifest and target chapters while preserving unrelated files.
- FAQ answers need evidence or an explicit inference/unknown label.
- A file existing or containing a word does not satisfy a learning objective.

## Acceptance

- Chapters 09 and 10 are included in completeness checks.
- The checklist distinguishes documented knowledge from learner-completed practice.
- Every remaining validation failure and unknown has a concrete next action.
- Final delivery does not claim success when the validator reports errors.
