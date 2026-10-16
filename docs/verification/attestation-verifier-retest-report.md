# TASK081 independent re-test of the repaired attestation verifier

- Artifact ID: `DOC-ATTESTATION-VERIFIER-RETEST-001`
- Proposed evidence ID: `EVD-ATTESTATION-VERIFIER-RETEST-001`
- Runtime: `work-c470817ccf7e448a82b7549de6dea9a4`, attempt 1 / version 1
- Subject: `CODE-ATTESTATION-VERIFIER-REPAIR-001` v1 at commit `362d9c1`
  (repair of `DOC-ATTESTATION-VERIFIER-REVIEW-001` findings)
- Design reference: `DES-061` v1
- Tester: independent (`/root/design_acceptance`); authored neither the
  implementation, the repair, nor the developer tests
- Date: 2026-10-16
- Classification: bounded local test observation only. No model call, pair
  run, holdout release, rating, comparison, Gate, acceptance or release
  decision is made or implied.

## Method

1. New independent re-test suite
   `tests/test_attestation_verifier_repair_retest.py` (8 cases, RT-1..RT-6),
   written against the review report's repair requests, not the developer's
   test plan.
2. Re-run of the TASK-078 independent suite and developer suite (now
   encoding the repaired behaviors).
3. Full-suite regression.
4. Retained-root verification on the real repository artifacts, not
   simulations.

## Results

| Check | Result |
|---|---|
| RT-1 R-02: all four retained run roots `inspect_run` → INTACT | PASS |
| RT-1 R-02: retained TASK-044 pilot root `grade_run` → SATISFIED (machine-fact bundle) | PASS |
| RT-2 R-01: fresh strict TEST_DOUBLE run root → INTACT, no `model` member, verdicts + marker present | PASS |
| RT-2 R-03: tampered `model` member (fake VERIFIED records) → rejected (RUN_INTEGRITY_FAILURE via INVALID_RESULT rebinding) | PASS |
| RT-3 F-01: seven registry grammar mutations → `TRUST_REGISTRY_INVALID` | PASS |
| RT-3 F-02: four attestation grammar mutations → `ATTESTATION_INVALID` | PASS |
| RT-4 F-03: trailing/leading whitespace and newline document bytes → `ATTESTATION_INVALID` | PASS |
| RT-5: exploratory default path unchanged (no strict members, TEST_DOUBLE) | PASS |
| RT-6: CLI strict validate wiring after repair | PASS |
| TASK-078 independent suite (17 cases) | PASS |
| Developer suites (19 + 17 cases) | PASS |
| Full repository suite | OK (741 tests, 8 pre-existing Windows-link skips) |

## Findings

None. All R-01/R-02/R-03 and F-01/F-02/F-03 repair behaviors match
DES-061 §6 and the review's requested repairs within the tested scope. One
tester-oracle correction during authoring: a tampered run root surfaces as
`RUN_INTEGRITY_FAILURE` (the `inspect_run` wrapper maps every `_inspect`
rejection), which is correct wrapping behavior, not a defect.

## Boundaries

1. Local synthetic-key observations only; no provider attestation existed.
2. The strict path was exercised only through the private TEST_DOUBLE port
   and `validate`; no native strict run exists.
3. This re-test does not close `REVIEW_REQUIRED` by itself; the independent
   re-review (next registered work) owns that verdict.
4. Nothing here completes REQ-011, authorizes a holdout release, or changes
   any Gate status.
