# TASK097 independent test report: CR-021 second-round instruction upgrades

- Artifact ID: `DOC-SKILL-INSTRUCTION-OPTIMIZATION-TEST-002`
- Proposed evidence ID: `EVD-SKILL-INSTRUCTION-OPTIMIZATION-TEST-002`
- Runtime: `work-ea053d845d634f52902451acc14372a8`, attempt 1 / version 1
- Subject: `CODE-SKILL-INSTRUCTION-OPTIMIZATION-002` v1 at commit `a68bffa`
- Tester: independent (`/root/design_acceptance`); not the implementing developer
- Date: 2026-10-16
- Classification: `SOURCE_TRACE_ONLY_NO_QUALITY_VERDICT`

## Method

Read the committed bytes at `a68bffa` via `git show` (not the working tree),
checked each upgrade against its mapped CR-019 residual class, verified the
OA-3 non-goal, and confirmed the commit touches only the two instruction
assets. An initial T4 assertion failure was diagnosed as a line-wrap artifact
in the test script itself (content confirmed present after whitespace
normalization); recorded here for transparency.

## Results

| ID | Check | Result |
|---|---|---|
| T1 | Multi-part completeness clause present: one member per asked kind, missing asked-for member declared incomplete, exact row keys with no extra fields or renames | PASS |
| T2 | Label minimality clause present: shortest source-faithful form, no qualifier stacking (`WRONG_PASSWORD` example), guards in their own field | PASS |
| T3 | Universe discipline present in both files: enumerate exactly the fact-defined combinations, correct-but-extra rows to the case table | PASS |
| T4 | Engine vocabulary alignment present in both files: `CONFLICT`/`EXCLUDED`/`GAP` definitions mirroring the deterministic engine, with the anti-patterns named (`CONFLICTING`, `UNSUPPORTED_EXCLUDED`, `UNRESOLVED`) | PASS |
| T5 | OA-3 non-goal respected: the strings `GRANTED` and `ALLOWED` appear nowhere in either asset — no tuning to the oracle's arbitrary token choice | PASS |
| T6 | Commit `a68bffa` touches only the two instruction assets; no `.py` engine/contract/schema file changed | PASS |
| T7 | Full test suite independently re-run: 752 tests OK, 8 skipped (pre-existing Windows symlink branch skips) | PASS |

## Failure-mode mapping verification

| CR-019 residual class (CR-020 audit taxonomy) | Upgrade | Mapped |
|---|---|---|
| Q-DTT-001 missing `excluded_combinations` member; Q-STT-001 missing valid+invalid split | multi-part completeness | yes |
| Q-STT-011 `WRONG_PASSWORD_BEFORE_…`; Q-STT-021 `CONFIRMED_PAYMENT`, guard-qualified rows | label minimality | yes |
| Q-DTT-021 extra `FINAL_SALE` rows beyond the fact-defined universe | universe discipline | yes |
| Q-DTT-001 `CONFLICTING` vs the engine's `CONFLICT` | engine vocabulary alignment | yes |

## Boundary observation

The upgrades are instruction-layer only; behavioural effect is unproven by
this test. Unlike CR-018, the verification must NOT reuse the recorded
CR-019 fixtures (they would reward second-round tuning on the same material
without isolation). The verifier requires a fresh pre-registered scenario
set exercising the same failure classes, executable after the upstream model
quota recovers (2026-10-22). The OA-3 finding guarantees arm instructions
were not tuned to oracle-synthesized tokens, but the fresh-set design must
also avoid re-introducing that coupling.

## Verdict

7/7 checks PASS. The four upgrades are present, mapped, packaged and free of
oracle-token tuning. Content and packaging verified only; behavioural effect
deferred to the fresh-set verification run.
