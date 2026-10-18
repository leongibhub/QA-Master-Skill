# TASK108 independent test report: CR-025 third-round instruction upgrades

- Artifact ID: `DOC-SKILL-INSTRUCTION-OPTIMIZATION-TEST-003`
- Proposed evidence ID: `EVD-SKILL-INSTRUCTION-OPTIMIZATION-TEST-003`
- Subject: `CODE-SKILL-INSTRUCTION-OPTIMIZATION-003` v1 at commit `fb4f2d3`
- Tester: independent (`/root/design_acceptance`); not the implementing developer
- Date: 2026-10-18
- Classification: `SOURCE_TRACE_ONLY_NO_QUALITY_VERDICT`

## Method

Read the committed bytes at `fb4f2d3` via `git show` (not the working tree),
checked each upgrade against its mapped CR-022/CR-024 residual class, verified
the OA-3 non-goal and the absence of CR-022-material coupling, and confirmed
the commit touches only the one instruction asset plus the regression guard.
The full test suite was re-run independently: 765 OK (skipped=8).

## Results

| ID | Check | Result |
|---|---|---|
| T1 | Clause 1 explicit-scope discipline present: "list exactly those stated items", "do not derive additional candidates from general rules" | PASS |
| T2 | Clause 2 exhaustive-universe provenance present: "exhaustive-universe fact", "enumeration provably complete" | PASS |
| T3 | OA-3 non-goal respected: `GRANTED`/`ALLOWED` appear nowhere in any arm instruction asset | PASS |
| T4 | Commit `fb4f2d3` touches only `typed-observations.md` + `tests/test_skill_instruction_conventions.py`; no engine/contract/schema file changed | PASS |
| T5 | No CR-022-material coupling in the new clauses: no `F-FS-`/`Q-FS-`/`FS-0x` IDs and no CR-022 state tokens (`ISSUED`/`IDLE`/`QUEUED`/…) in the added lines | PASS |
| T6 | Regression guard extended with `CR025Conventions` (2 tests: explicit-scope clause, exhaustive-universe provenance clause) | PASS |
| T7 | Full suite independently re-run: 765 OK, 8 skipped (pre-existing Windows symlink branch skips); convention subset 13 OK | PASS |

## Failure-mode mapping verification

| CR-022/CR-024 residual class | Upgrade | Mapped |
|---|---|---|
| Q-FS-052 over-generation: both arms list 7 derived invalid candidates vs oracle 1 explicitly-stated (renewal request from a terminal state) | explicit-scope discipline | yes |
| Transition-list provenance: arm A omits the `F-FS-0x1` "only states" universe fact (0/3 vs arm B 1/3) on the valid-transition checks | exhaustive-universe provenance | yes |

## Boundary observation

The upgrades are instruction-layer only; behavioural effect is unproven by
this test. Per TASK-097, the verification must NOT reuse the recorded CR-022
fixtures (they would reward third-round tuning on the same material without
isolation). The verifier requires a second fresh pre-registered scenario set
exercising the same two failure classes (explicitly-stated invalid candidates;
"only states" transition provenance), executable on never-graded material.

## Verdict

7/7 checks PASS. The two upgrades are present, mapped, packaged, free of
oracle-token tuning and free of CR-022-material coupling. Content and
packaging verified only; behavioural effect deferred to the second fresh-set
verification run.
