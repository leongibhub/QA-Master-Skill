# TASK079 independent review of the strict-profile attestation verifier port

- Artifact ID: `DOC-ATTESTATION-VERIFIER-REVIEW-001`
- Proposed evidence ID: `EVD-ATTESTATION-VERIFIER-REVIEW-001`
- Runtime: `work-1acf0f0add1f4977aa1a72ece64b30b1`, attempt 1 / version 1
- Subjects under review: `DES-061` v1 (`51a058a`), `CODE-ATTESTATION-VERIFIER-001` v1
  (`7721dc2`), `DOC-ATTESTATION-VERIFIER-TEST-001` v1 (`4c02618`)
- Reviewer: independent (`/root/workflow_review`); the reviewer authored none of
  the design, implementation or tests
- Date: 2026-10-16
- Classification: `AGENT_REVIEW_ONLY`. This is a bounded code/document review
  with reproduction. No model call, pair run, holdout release, rating,
  comparison, Gate, acceptance or release decision is made or implied, and this
  report is not a quality verdict.

## Method

1. Read DES-061 end-to-end against the DES-040 contract it extends.
2. Read the full implementation diff (`42d5069..7721dc2`:
   `qa_master/paired_evaluation.py`, `tests/test_attestation_verifier.py`).
3. Re-executed targeted reproductions for each suspected defect (scripts
   retained in the session log; synthetic keys only).
4. Re-inspected every retained run root under `.qa-master/` with the new code.
5. Reviewed the TASK-078 independent test report and its three findings.

## Review findings (typed, bounded, all reproduced)

| ID | Severity | Observation | Reproduction |
|---|---|---|---|
| R-01 | P2 | Emitter/inspector inconsistency for strict TEST_DOUBLE runs: `_run` emits `attestation_verdicts`, `strict_eligibility` and `model` whenever a strict manifest passed the verifier, regardless of backend, but `_inspect` rejects any non-`STRICT_COMPARABILITY_CANDIDATE` result carrying those members. A strict manifest run through the private test port therefore produces a run root that its own `inspect_run` rejects with `RUN_INTEGRITY_FAILURE`. The developer test asserts the result dict but never inspects the written root, so this was not caught. | Private-port strict run with synthetic attestations → `inspect_run(root)` → `RUN_INTEGRITY_FAILURE` |
| R-02 | P1 | Retained-evidence verifiability break: `_inspect` now requires `trust_registry_sha256` in `preflight.json`, but every pre-CR-015 run root lacks the key. All four retained roots fail: `paired-pilot/observed-v4-final-freeze/CR011-EXPLORATORY-PUBLIC-DEV-001` (the TASK-044 public-development pilot evidence), and the three `cr011-independent` preview roots. `grade_run` calls `inspect_run` first, so grading of retained evidence is also blocked. DES-040 §1 requires the existing contract to remain compatible; this is a regression of that compatibility for already-retained evidence. | `inspect_run` on all four retained roots → `RUN_INTEGRITY_FAILURE` (missing `trust_registry_sha256`) |
| R-03 | P3 | `model` member is accepted in results without shape validation and without cross-checking against `attestation_verdicts`: a tampered `result.json` could carry an arbitrary `model` object, and for genuine strict runs the VERIFIED records in `model` are not re-bound to the verdict list. | Code read of `_inspect` optional-key handling |
| R-04 | P3 | Reviewer concurrence with TASK-078 F-01/F-02 (DES-061 §6 dedicated codes surface contract-layer codes for grammar failures) and F-03 (non-canonical document bytes with trailing whitespace tolerated; `evidence_sha256` binds file bytes, not the signed canonical bytes). | Confirmed by reading and by TASK-078 reproductions |

## Confirmed positive properties (within reviewed scope)

1. Fail-closed ordering is correct: registry load → attestation verification →
   materialization → per-call recheck (`EXECUTABLE_DRIFT`, registry drift,
   `MATERIALIZED_DRIFT`) → launch. No participant call can precede
   verification.
2. The default runtime remains verifier-free: no flags → strict manifests
   still fail `STRICT_PROFILE_NOT_SUPPORTED`; exploratory manifests never
   enter the new path and produce byte-identical validate results with and
   without `None` flags (TASK-078 INDEP-4 confirmed; reviewer re-read).
3. Declared `VERIFIED` without the verifier is still rejected
   (`ATTESTATION_NOT_SUPPORTED` retained in `_runtime`).
4. Registry consumption is opt-in and single-purpose: registry + exploratory
   profile fails `STRICT_PROFILE_MISMATCH` — no silent upgrade path.
5. A strict TEST_DOUBLE run can never derive `STRICT_COMPARABILITY_CANDIDATE`
   (backend conjunction in `_run`).
6. No rating, winner, superiority, Gate or holdout-release semantics exist in
   the port; `claim_status`/`human_rating_status` stay `NOT_ASSERTED`/
   `NOT_EXECUTED`; the `HOLDS_FOR_HOLDOUT_PROTOCOL_ONLY` marker states the
   separate REQ-011 holdout protocol remains required.
7. Mid-run registry drift stops the run and records `TRUST_REGISTRY_DRIFT` as
   an infrastructure failure on the stopped attempt (reproduced in TASK-078
   and re-read by the reviewer).

## Verdict

`REVIEW_REQUIRED` — changes requested before this port may be considered for
any further CR-015 lifecycle step:

1. R-02 (P1) must be repaired: historical run roots must remain inspectable
   (treat `trust_registry_sha256` as optional-absent for pre-v2 preflights, or
   version the preflight schema) and `grade_run` on retained evidence must
   work again.
2. R-01 (P2) must be repaired: either strict TEST_DOUBLE results stop emitting
   the strict members, or `_inspect` accepts them for `TEST_DOUBLE`
   `execution_backend`; the two components must agree by construction and a
   test must inspect the written root.
3. R-03 and the concurred F-01/F-02/F-03 (P3) are requested, not blocking.

The repair belongs in a new work order under CR-015 following the existing
`*-REPAIR-001` pattern. This review authorizes no merge, release, Gate,
holdout release or comparison step.
