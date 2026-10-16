# TASK086 independent re-review of the NR-1 equality implementation

- Artifact ID: `DOC-ATTESTATION-VERIFIER-CLOSURE-001`
- Proposed evidence ID: `EVD-ATTESTATION-VERIFIER-CLOSURE-001`
- Runtime: `work-627e3566cd234081897667d3daa1e833`, attempt 1 / version 1
- Subjects: `CODE-ATTESTATION-VERIFIER-EQUALITY-001` v1 at `547c6e6`,
  `DES-061` v2 at `17f808f`, `DOC-ATTESTATION-VERIFIER-EQUALITY-RETEST-001`
  v1 at `4afb03a`
- Reviewer: independent (`/root/workflow_review`); the reviewer role that
  issued the open `REVIEW_REQUIRED` verdict (TASK-079, reaffirmed TASK-082)
- Date: 2026-10-16
- Classification: `AGENT_REVIEW_ONLY`. Bounded code/document review with
  reproduction. No model call, pair run, holdout release, rating, comparison,
  Gate, acceptance or release decision is made or implied.

## Method

1. Read the NR-1 implementation diff (`1f9f81b..547c6e6`) and the DES-061 v2
   amendment (`17f808f`) line by line.
2. Verified the code matches the amended §3 step 6 / §5 step 3 semantics.
3. Re-executed a reviewer probe (both subjects differing across arms) plus
   the tester's six re-test cases.
4. Checked for new defects introduced by the change.

## Resolution check

| Item | Status |
|---|---|
| NR-1: cross-arm attested-value equality per subject, enforced before any participant call | RESOLVED (`STRICT_ATTESTATION_VALUE_MISMATCH` in `_verify_attestations`, pre-materialization) |
| NR-1: declared-value consistency where the manifest declares a non-null value | RESOLVED (declared `VERIFIED` states are left to `_runtime`'s dedicated `ATTESTATION_NOT_SUPPORTED`, preserving the TASK-079 boundary) |
| Reviewer probe: both subjects differing across arms | Correctly rejected with the new code |
| TEST_DOUBLE boundary preserved (no promoted `model`, marker, INTACT root) | RESOLVED (re-tested PASS) |
| Exploratory default path unchanged | RESOLVED (re-tested PASS) |
| Full-suite regression | 756 tests OK, 8 pre-existing Windows-link skips |

No new defects were identified. One observation, not a defect: the equality
check runs after all four signature verifications, so a run with both a bad
signature and differing values reports the signature failure first —
fail-closed either way, ordering immaterial.

## Verdict

`REVIEW_REQUIRED` is **closed** for CR-015's development increment. All
findings from TASK-078 (F-01..F-03), TASK-079 (R-01..R-04) and TASK-082
(NR-1) are resolved, independently re-tested, and now re-reviewed.

Standing boundaries (unchanged, restated):

1. Closing this review is not a quality verdict, acceptance, Gate result or
   release decision; every output remains `DRAFT_UNAPPROVED` /
   `NOT_EXECUTED` where applicable.
2. No native strict run has occurred; the strict path has been exercised only
   through `validate` and the private TEST_DOUBLE port.
3. `STRICT_COMPARABILITY_CANDIDATE` remains eligibility for the separate
   REQ-011 holdout/human protocol only — never fairness proof, never a
   superiority conclusion, and never holdout-release authorization.
4. A future native strict run still requires: administrator-issued registry
   and provider-signed attestations (which do not exist), the explicit local
   run command per NFR-006, and the separate holdout procedure's release
   gate.
