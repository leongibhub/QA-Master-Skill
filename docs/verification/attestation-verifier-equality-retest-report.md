# TASK085 independent re-test of the NR-1 equality implementation

- Artifact ID: `DOC-ATTESTATION-VERIFIER-EQUALITY-RETEST-001`
- Proposed evidence ID: `EVD-ATTESTATION-VERIFIER-EQUALITY-RETEST-001`
- Runtime: `work-7b6baf043cf34a8db382aa8c21f56809`, attempt 1 / version 1
- Subject: `CODE-ATTESTATION-VERIFIER-EQUALITY-001` v1 at commit `547c6e6`
- Design reference: `DES-061` v2 (NR-1 amendment)
- Tester: independent (`/root/design_acceptance`); authored neither the
  implementation nor the developer tests
- Date: 2026-10-16
- Classification: bounded local test observation only. No model call, pair
  run, holdout release, rating, comparison, Gate, acceptance or release
  decision is made or implied.

## Method

New independent suite `tests/test_attestation_verifier_equality_retest.py`
(6 cases) authored against the NR-1 amendment, plus full-suite regression.

## Results

| Check | Result |
|---|---|
| Differing provider revision across arms → `STRICT_ATTESTATION_VALUE_MISMATCH` | PASS |
| Differing system baseline across arms → `STRICT_ATTESTATION_VALUE_MISMATCH` | PASS |
| Declared-value mismatch rejected; declared match passes | PASS |
| Declared `VERIFIED` keeps the dedicated `ATTESTATION_NOT_SUPPORTED` code | PASS |
| Equal-values strict TEST_DOUBLE run bounded (no `model`, marker intact, root INTACT) | PASS |
| Exploratory default path unchanged after the equality change | PASS |
| Full repository suite | OK (756 tests, 8 pre-existing Windows-link skips) |

## Findings

None. The NR-1 behavior matches DES-061 v2 within the tested scope.

## Boundaries

1. Local synthetic-key observations; no provider attestation existed.
2. The strict path was exercised only through `validate` and the private
   TEST_DOUBLE port; no native strict run exists.
3. This re-test does not close `REVIEW_REQUIRED`; the TASK-086 re-review owns
   that verdict.
