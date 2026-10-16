# CR-023 Convention-Regression Module — Independent Verification (TASK-102)

- **Status**: PUBLIC_DEVELOPMENT / DRAFT_UNAPPROVED
- **Verified commit**: `a007345` (`tests/test_skill_instruction_conventions.py`, 11 tests)
- **Tester**: `/root/design_acceptance` (TASK-102, work `work-5f6de7863ee744f7b9b586e1f5592700`)
- **Method**: All checks executed against a disposable copy of the repository tree (`TemporaryDirectory`, `.git`/`.qa-master`/caches excluded). The working tree was never mutated. Mutation anchors use `\s+`-tolerant regexes because clauses wrap across lines in the Markdown source — the same lesson that drove whitespace-normalized matching in the module under test.

## Results

| # | Check | Result |
|---|-------|--------|
| V1 | Pristine copy: module 11/11 pass | PASS |
| V2 | Mutation kill: CR-021 family-consistency clause (R-01 repair) removed → suite red; restored → green | PASS |
| V2 | Mutation kill: CR-021 engine vocabulary `CONFLICT` wording corrupted → red; restored → green | PASS |
| V2 | Mutation kill: CR-021 engine-discipline wiring in `SKILL.md` (`mirror`→`ignore`) → red; restored → green | PASS |
| V2 | Mutation kill: CR-018 scale-violation clause in `functional-api.md` deleted → red; restored → green | PASS |
| V3 | OA-3 guard: `GRANTED` injected into `typed-observations.md` → suite red | PASS |
| V4 | Wheel-safety: `skill_bundle()` resolves `SKILL.md`, `references/typed-observations.md`, professional assets under isolated `-I` import (60 assets) | PASS |
| V5 | Coverage cross-check: every clause TASK-092/TASK-097 verified is asserted by the module (14/14 anchors present) | PASS |

**Total: 12/12 PASS.**

## Findings

- **F-1 (observation, no action)**: The module's whitespace-normalized matching (`' '.join(text.split())`) is what makes both the green-path assertions and this verification's restore-green checks robust; raw substring guards would false-fail on any future re-wrapping. Verified the design, not just the current bytes.
- **F-2 (verification-tooling note, no action)**: One verification-script iteration was needed — the first kill-test run used raw substrings as mutation anchors and false-failed on a line-wrapped clause; the first V4 probe embedded `\n` inside a raw `-c` string. Both are bugs in the throwaway verification harness, not in the module under test; corrected and re-run as recorded above.
- **F-3 (scope note)**: The module pins **clause presence** (delivered state). It cannot and does not claim the clauses produce the behavioural effect — that remains the quota-blocked CR-022 fresh-set run. No overlap with CR-022 precommitted materials: this verification used only repo-committed assets and the disposable tree copy; no `.qa-master/` run trees were touched.

## Verdict

The regression guard is real: every tested mutation of a CR-018/CR-021 clause is detected, the OA-3 non-goal guard fires on oracle-token injection, asset resolution is wheel-safe, and clause coverage matches the TASK-092/TASK-097 acceptance lists. TASK-101's deliverable is **verified**.
