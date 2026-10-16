# TASK082 independent re-review of the repaired attestation verifier

- Artifact ID: `DOC-ATTESTATION-VERIFIER-REREVIEW-001`
- Proposed evidence ID: `EVD-ATTESTATION-VERIFIER-REREVIEW-001`
- Runtime: `work-dfb36573ebc5444cac6747e4c3b35f6b`, attempt 1 / version 1
- Subjects: `CODE-ATTESTATION-VERIFIER-REPAIR-001` v1 at `362d9c1` (repair),
  `DOC-ATTESTATION-VERIFIER-RETEST-001` v1 at `5c19726` (re-test)
- Reviewer: independent (`/root/workflow_review`); same reviewer role that
  issued the TASK-079 `REVIEW_REQUIRED` verdict, re-examining the repair
- Date: 2026-10-16
- Classification: `AGENT_REVIEW_ONLY`. Bounded code/document review with
  reproduction. No model call, pair run, holdout release, rating, comparison,
  Gate, acceptance or release decision is made or implied.

## Method

1. Read the full repair diff (`00caba6..362d9c1`) line by line.
2. Verified each TASK-079 / TASK-078 finding is resolved in code, not merely
   in tests.
3. Re-executed independent probes on the repaired code, including a new probe
   the previous rounds did not attempt: differing per-arm attested values.
4. Confirmed the TASK-081 re-test suite covers the repair requests.

## Resolution status of prior findings

| Prior finding | Status | Evidence in code |
|---|---|---|
| R-01 (P2) strict TEST_DOUBLE roots rejected by own inspect | RESOLVED | `_run` no longer emits `model` for TEST_DOUBLE; `_inspect` accepts verdicts/marker on TEST_DOUBLE results and rejects them on non-strict NATIVE results; written-root inspect regression test present |
| R-02 (P1) retained roots not inspectable, grade blocked | RESOLVED | `trust_registry_sha256` optional-absent for pre-CR-015 roots; required non-null when the retained manifest is strict-profile; retained roots INTACT and `grade_run` SATISFIED (re-verified) |
| R-03 (P3) unvalidated `model` member | RESOLVED | Shape-validated, VERIFIED-state required, every record rebound to the arm-A verdict by value and evidence digest |
| F-01/F-02 (P3) dedicated §6 codes | RESOLVED | Registry and attestation grammar failures wrapped to `TRUST_REGISTRY_INVALID`/`ATTESTATION_INVALID` |
| F-03 (P3) non-canonical document bytes | RESOLVED | `document_raw != canonical(document)` rejected; TASK-081 verified leading/trailing/newline variants |
| R-04 concurrence | RESOLVED | via F-01..F-03 resolution |

## New finding (reproduced)

| ID | Severity | Observation |
|---|---|---|
| NR-1 | P2 | The strict-eligibility conjunction (DES-061 §5 and its implementation) never compares the two arms' attested values. A strict manifest with validly signed attestations where arm A attests provider revision R1 and arm B attests a different R2 still derives `STRICT_COMPARABILITY_CANDIDATE` on a native run (TEST_DOUBLE reproduction shows both verdicts accepted, `INTACT` inspection). This defeats the port's core same-model purpose (REQ-011 identical model; DES-040 `EXPLORATORY_CONFIGURED_SAME_MODEL` exists precisely because sameness was unverified). The manifest declares a single `runtime.model`, so the verifier should require both arms' attested values per subject to be equal (and, where the manifest declares a non-null value, to match it). This is primarily a design gap — DES-061 §5's conjunction lacks the equality clause — so the repair needs a bounded DES-061 §5 amendment plus the code check. |

No other new defects were identified: fail-closed ordering, drift detection,
exploratory invariance, and the no-promotion guarantees all hold in the
repaired code.

## Verdict

`REVIEW_REQUIRED` remains open, now with a single narrow request:

1. NR-1 (P2): amend DES-061 §5 with the cross-arm attested-value equality
   clause (and declared-value consistency where declared), implement it in the
   strict derivation, and add tests for differing-arm and declared-mismatch
   cases.

Everything else from TASK-079 is resolved and independently re-tested. This
re-review authorizes no merge, release, Gate, holdout release or comparison
step; the strict path still cannot be exercised natively until the separate
REQ-011 holdout/human protocol exists.
