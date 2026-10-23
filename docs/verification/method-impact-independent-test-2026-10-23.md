# CR-034 independent test record

- Evidence ID: EVD-CR034-INDEPENDENT-TEST-001
- Scope: REQ-032 through REQ-036 and NFR-014; DES-063; TASK-140.
- Tester: independent test owner, separate from TASK-138 implementation owner.
- Source under test: frozen `5c516a66b82d51d9473e149a426421f003e4dc95`.
- Environment: Windows, CPython 3.13 local test runner; one isolated archive/venv
  delivery test completed against the final frozen source.
- Overall status: `PASS` for the executed offline test scope. This is not a
  project Gate or a statement that any proposed application test was executed.

| Test case | Requirement | Objective | Status | Evidence |
| --- | --- | --- | --- | --- |
| TC-IMPACT-001 | REQ-032 | All five finite methods retain exact vectors in an unchanged comparison. | PASS | `tests/test_method_impact_independent.py` |
| TC-IMPACT-002 | REQ-032, REQ-034 | Source-descriptor-only ID churn retains vectors and requests rebinding. | PASS | same |
| TC-IMPACT-003 | REQ-032, NFR-014 | Boolean/integer and decimal changes remain typed differences. | PASS | same |
| TC-IMPACT-004 | REQ-034 | Requirement, oracle and source context changes select review. | PASS | same |
| TC-IMPACT-005 | REQ-032, REQ-035 | Model rename/new model becomes explicit added/removed work; no guessed pair. | PASS | same |
| TC-IMPACT-006 | REQ-033 | Stale input rejects; duplicate and undocumented/orphan cases stay visible. | PASS | same |
| TC-IMPACT-007 | REQ-035 | Obligations, unknown requirements and known/orphan declared gaps become followups. | PASS | same |
| TC-IMPACT-008 | REQ-033, NFR-014 | Scenario ordering and declared reference-set ordering produce stable identities/actions. | PASS | same |
| TC-IMPACT-009 | NFR-014, REQ-036 | Strict parser, no-clobber, junction/reparse protection, non-mutation and hostile Markdown values. | PASS; symlink subcheck SKIPPED | same and `evidence/cr034/delivery/delivery-metadata.json` |
| TC-IMPACT-010 | REQ-036 | One clean archive wheel, offline venv, module CLI and installed helper run from a consumer directory. | PASS | `evidence/cr034/delivery/delivery-metadata.json` |

## Executed evidence

`python -W error::ResourceWarning -m unittest` executed TC-IMPACT-001 through
009 plus the Windows junction check: **11 run, 10 PASS, 1 SKIPPED, 0 failures,
0 errors**. The only skip was the optional symbolic-link test because this Windows
test account lacks link privilege; the native junction test passed.

TC-IMPACT-010 ran once against the clean Git archive of `5c516a6`: archive,
wheel build, virtual-environment creation, offline wheel install, Skill install,
module CLI and installed helper all exited `0`. The wheel SHA-256 was
`873d45fcd383f49dd188806feeff73a4b06700ffa4fad34817a5765ae41df6a6`.
The installed Skill copied 5,888 files. Module and helper both produced
`DRAFT_UNAPPROVED` / `NOT_EXECUTED` reports with `review_case_count` 9. Exact
stdout/stderr and report hashes are retained in
`evidence/cr034/delivery/delivery-metadata.json`; it records the normal pip
upgrade notice and the Windows redirected-path warning as warnings, not failures.
Across the two executions, the independent suite ran **12 test methods: 11 PASS,
1 SKIPPED, 0 failures, 0 errors**.

The product archive used by TC-IMPACT-010 is exactly `5c516a6`. The test runner
contained only an uncommitted, TASK-140-owned opt-in evidence wrapper controlled
by `QA_MASTER_IMPACT_EVIDENCE_DIR`; it captures command metadata outside the
temporary consumer directory and is not part of the archive or installed product.

## Method and evidence rules

The suite calls the public Python boundary, the module CLI, and the installed
Skill helper. It does not import TASK-138 test helpers. It uses
`python -W error::ResourceWarning -m unittest tests.test_method_impact_independent -v`.
The archive delivery test ran once after source, docs and tests were committed;
it captured subprocess output as UTF-8 with replacement and recorded exact exits
under `docs/verification/evidence/cr034/`. A successful report only means an
offline draft/proposal was created. It is not test execution, acceptance or
permission to skip regression.

## Defects

No defect is closed by this document or by the local test run.

- `BUG-016` — on pre-repair `ebfc947`, pass a baseline library with the valid
  gap `{"candidate_id":"TC-MD-UNKNOWN","reason_code":"OTHER"}` to
  `analyze_method_impact`. The baseline correctly reported an orphan candidate,
  but `gap_followups` was empty, losing the declared reason/action required by
  REQ-035. The repair preserves a `REVIEW_GAP` entry with empty after IDs.
- `BUG-017` — on pre-repair `ebfc947`, make an M-BOUND oracle obligation and
  change the `SRC-REQ` descriptor. Affected row actions retained only
  `UNRESOLVED_MODEL_OBLIGATION`, hiding `SOURCE_DESCRIPTORS_CHANGED`. The repair
  keeps the dominant action and unions the declared reasons.

Both defects were reproduced before the product freeze, repaired before
`5c516a6`, and independently retested by TC-IMPACT-007. Their project-level
disposition is recorded separately; this bounded retest is neither external
defect closure nor a Gate decision. The symbolic-link privilege skip is an
environment limitation, not a product defect; the equivalent Windows junction
test passed.
