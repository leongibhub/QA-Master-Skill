# QA Master V1 baseline-audit reconciliation

- Artifact ID: `DOC-BASELINE-001`
- Document State: `DRAFT`
- Evaluation State: `IN_REVIEW`
- Evidence Status: `OBSERVED`
- Source report: `DOC-TEST-BASELINE-001` / `docs/verification/baseline-2026-10-14.md` (Runtime evidence `EVD-BASELINE-20261014-001`)

## What the independent baseline audit established

The audit report records actual local execution against `77e3b5d4e8be8076720ebfd2f0338db73dac2079` using Windows Python 3.13.5 from `D:\codex-rd-platform\.venv\Scripts\python.exe`.

| Evidence | Scope | Observed result | Evidence Status |
|---|---|---|---|
| EV-BASE-001 / EV-BASE-002 | Full local `unittest` regression, verbose and quiet repeat | 301 tests ran; two workflow tests errored. The initial baseline is not clean. | OBSERVED |
| EV-BASE-003 | Side-effect approval guard | 5 targeted tests passed. | OBSERVED |
| EV-BASE-004 | Python module compilation | `compileall` process succeeded. This is syntax evidence only. | OBSERVED |
| EV-BASE-005 | Workflow, side-effect, and exact-approval targeted retest after test correction | 25 targeted tests passed. | OBSERVED |
| EV-BASE-006 / EV-BASE-007 / EV-BASE-010 | Continuation safety, artifact attribution, and typed-receipt persistence checks | 40 targeted tests passed against the observed continuation worktree. Test-only fixtures do not authenticate a human or remote executor. | OBSERVED |
| EV-BASE-008 | Continuation local regression | 375 tests completed with `OK`; a subprocess `ResourceWarning` was emitted. | OBSERVED |
| EV-BASE-009 | Wheel build, clean temporary-venv installation, package-resource and CLI smoke | The observed wheel installed and the bounded smoke checks passed. | OBSERVED |

EV-BASE-006 through EV-BASE-010 were run against a shared, dirty continuation worktree with the fingerprint retained in the source report. They do not establish a final Git revision, CI success, external-service validation, release readiness, a Gate decision, or product acceptance.

## Observed defect and disposition

`BUG-001` is an observed stale test-expectation defect in `tests/test_workflow.py`. The initial full suite failed because legacy side-effect completion now deliberately raises `PermissionError`, while two old tests expected or used the prior legacy completion contract. The test correction changed no production implementation and EV-BASE-005 passed the bounded retest.

EV-BASE-008 supplies an observed full continuation retest after the test correction. It establishes that the corrected tests passed in that fingerprinted worktree, but does not close `BUG-001`: later concurrent changes need a fresh regression result against the final revision, and the initial executions were not pre-registered Runtime test cases/executions. Creating a retrospective lifecycle closure would fabricate the required chain.

`BUG-002` is an observed medium-severity reliability finding from EV-BASE-008: the successful 375-test run emitted a still-running-subprocess `ResourceWarning`. Its root cause is not attributed. It remains open pending owner investigation and a deterministic cleanup regression.

## Resulting gaps

- `TC-INT-001` and `TC-INT-002`: the continuation report adds mock-level and local redirect checks, but provider-backed GitLab reader/artifact transport integration remains `NOT_EXECUTED`.
- `TC-INT-003`: local runner Windows/recovery integration is `NOT_EXECUTED` because the dedicated disposable-run permit was not part of this audit.
- `TC-E2E-001`: GitLab staging E2E is `NOT_EXECUTED`; no authorized target, account, or token was supplied or accessed.
- Performance, load, stress, reliability, and compatibility evidence remains `NOT_EXECUTED`.

The next verification action is an independent full regression execution against the exact final revision, including deterministic resolution or classification of `BUG-002`, followed by defect reclassification from actual results. No Gate is eligible to pass from this audit alone.
