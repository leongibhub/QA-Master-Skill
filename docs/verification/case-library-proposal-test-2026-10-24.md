# CR-036 case-library proposal — independent test record

**Owner:** TASK-150 independent tester  
**Scope:** public module, proposal CLI, and frozen archive/wheel consumer path.  
**Basis:** REQ-037–040, NFR-015, DES-064/ADR-007, CR-036.  
**Source under test:** `ddb2fc2665b2b6f044eba9bf56a70de69211db7e` (frozen attempt).  
**Overall result:** `PASS` (bounded independent verification) — the frozen
Windows source/archive/wheel consumer attempt passed and corrected CI completed
on all four jobs. This is not a project Gate decision or human acceptance.

This independently maintained black-box corpus owns a small valid finite bundle
covering `boundary`, `decision_table`, `state_transition`, `pairwise`, and
`combinatorial`; it imports no developer test helpers.

| Test | Requirements | Objective / required observable evidence | Status |
| --- | --- | --- | --- |
| TC-PROP-001 | REQ-037, NFR-015 | Unchanged five-method library has draft/nonexecuted/not-applied metadata; strict nested library after-audits and hash agrees. | PASS — final run evidence below |
| TC-PROP-002 | REQ-037, REQ-039 | Source SHA churn retains vectors but requires rebinding review. | PASS — final run evidence below |
| TC-PROP-003 | REQ-039 | Requirement/source/oracle context changes preserve typed projection and prose/order with reasons. | PASS — final run evidence below |
| TC-PROP-004 | REQ-038 | Removal, partial-case prevention and 2-old/1-new ambiguity hold whole cases; no arbitrary after ID. | PASS — final run evidence below |
| TC-PROP-005 | REQ-038 | Bad baseline and empty case remain identifiable/held; rejection codes are stable. | PASS — final run evidence below |
| TC-PROP-006 | REQ-038, REQ-040 | Obligations hold whole cases with obligation/atomicity reasons. | PASS — final run evidence below |
| TC-PROP-007 | REQ-040 | Duplicate and orphan old gap occurrences are all held. | PASS — final run evidence below |
| TC-PROP-008 | REQ-040 | Every after `MISSING` vector has exact context and reconciled counts. | PASS — final run evidence below |
| TC-PROP-009 | REQ-037, REQ-039, NFR-015 | Typed/order/locator determinism and no input aliasing; no raw-byte promise across original representations. | PASS — final run evidence below |
| TC-PROP-010 | NFR-015 | Strict parsing/size/depth/replay/cardinality/I-O/CLI error and compact-output checks. | PASS — final run and corrected CI evidence below |
| TC-PROP-011 | REQ-037, NFR-015 | Output limit, no state/apply, clean frozen archive/wheel/offline consumer/module/helper and nested audit. | PASS — final run evidence below |

## Pre-freeze collection observation

On 2026-10-24, `python -m py_compile tests/test_case_library_proposal_independent.py`
completed successfully. `python -m unittest tests.test_case_library_proposal_independent -v`
returned exit `1` before any test method: `ModuleNotFoundError: No module named
'qa_master.case_library_proposal'`. This is a RED pre-implementation observation,
not a frozen-source result or a defect. No standalone log was fabricated.

After the developer added the module, the same 11-test source suite was run once
before final freeze. It ran 11 methods and returned exit `1`: TC-PROP-001–009 and
the then-incomplete TC-PROP-011 source guard passed; TC-PROP-010 failed because its source-level subprocess used
`-I -m qa_master` from an unrelated temporary consumer directory, where an
uninstalled source package is correctly unavailable (`No module named qa_master`).
This is an independent test-fixture environment error, not a product defect. The
source-CLI check now runs from the checkout without `-I`; `-I` is retained for the
post-freeze installed-consumer check. The exact observed result is retained in
the evidence record. After correcting that fixture and making TC-PROP-011's
archive/wheel procedure conditional on the coordinator-provided freeze SHA, a
further preliminary source run returned exit `0`: TC-PROP-001–010 passed and
TC-PROP-011's generated-output boundary passed; its freeze-gated archive/wheel
delivery subprocedure was not run. It was subsequently executed once against
the frozen source described below.

## Execution controls

The final frozen consumer test used one `TemporaryDirectory` fixture and one
returned command session, recording actual command/args/exits, archive/wheel/output
hashes and installed/runtime file counts per attempt. Its marker was written only
after fixture cleanup and the actual zero tool return. Root owns full cross-platform CI.

The one final frozen attempt completed against
`ddb2fc2665b2b6f044eba9bf56a70de69211db7e`: 11/11 tests passed in 298.459 s,
including archive/wheel/offline installed module and helper execution. Durable
per-attempt evidence and the post-cleanup marker are under
`docs/verification/evidence/cr036/task150-final/`. Initial CI `40079455590`
first exposed the existing-output-symlink fixture precedence on Linux and later
confirmed it in Windows Python 3.12 job `120829761748` and Python 3.10 job
`120829761754` (each 910 passed, 1 failure, 0 errors, 3 skips). The same leaf
caused all four initial job failures. The test correction is locally source-retested;
Corrected CI `40080022358` completed PASS on all four jobs at `83afa58`: each
reported 910 tests run, 0 failures and 0 errors; Ubuntu jobs had 12 skips and
Windows jobs had 3 skips. Complete readback is retained in
`docs/verification/evidence/cr036/corrected-ci.json`.

## Defects

BUG-027 through BUG-031 were pre-freeze prototype findings, fixed and retested
before `ddb2fc2`; see `docs/08-project-management/cr036-defect-record.md`. They
do not negate the observed final attempt. The later CI fixture-precedence issue
is documented above; corrected CI `40080022358` completed PASS on all four jobs
and is retained in `docs/verification/evidence/cr036/corrected-ci.json`. It is
not a product defect.
