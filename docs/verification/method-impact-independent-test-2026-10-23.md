# CR-034 independent test record

- Evidence ID: EVD-CR034-INDEPENDENT-TEST-001
- Scope: REQ-032 through REQ-036 and NFR-014; DES-063; TASK-140.
- Tester: independent test owner, separate from TASK-138 implementation owner.
- Source under test: final repair freeze `c2e795716b9b37644476978402ecf50b32d281d4`.
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
| TC-IMPACT-009 | NFR-014, REQ-036 | Strict parser, no-clobber, junction/reparse protection, non-mutation and hostile Markdown values. | PASS; symlink subcheck SKIPPED | `evidence/cr034/focused-tests-repair.txt` |
| TC-IMPACT-010 | REQ-036 | One clean archive wheel, offline venv, module CLI and installed helper run from a consumer directory. | PASS | `evidence/cr034/delivery-repair/delivery-metadata.json` |

## Executed evidence

`python -W error::ResourceWarning -m unittest` executed TC-IMPACT-001 through
009 plus the ambiguity, Windows junction and symbolic-link checks on `c2e7957`:
**12 run, 11 PASS, 1 SKIPPED, 0 failures, 0 errors**. The only skip was the
optional symbolic-link test because this Windows test account lacks link privilege;
the native junction test passed.

The initial TC-IMPACT-010 archive check remains historical evidence for
`5c516a6` at `evidence/cr034/delivery/delivery-metadata.json`. Because BUG-020
changed the pairing result, a second, justified archive check ran once against
`c2e7957`: archive, wheel build, virtual-environment creation, offline wheel
install, Skill install, module CLI and installed helper all exited `0`. Its wheel
SHA-256 was `6b5cd4e4f76b5a81deee31e63c375e12790d88e4d368e940e4589cf1331b011f`.
The installed Skill copied 5,888 files. Module and helper both produced
`DRAFT_UNAPPROVED` / `NOT_EXECUTED` reports with `review_case_count` 9. Exact
stdout/stderr and report hashes are retained in
`evidence/cr034/delivery-repair/delivery-metadata.json`; it records the normal
pip upgrade notice and the Windows redirected-path warning as warnings, not
failures. Final-repair evidence totals **13 test methods: 12 PASS, 1 SKIPPED,
0 failures, 0 errors**.

The product archive used by the final TC-IMPACT-010 is exactly `c2e7957`. The
test runner contained only a TASK-140-owned opt-in evidence wrapper controlled
by `QA_MASTER_IMPACT_EVIDENCE_DIR`; it captures command metadata outside the
temporary consumer directory and is not part of the archive or installed product.

## Method and evidence rules

The suite calls the public Python boundary, the module CLI, and the installed
Skill helper. It does not import TASK-138 test helpers. It uses
`python -W error::ResourceWarning -m unittest tests.test_method_impact_independent -v`.
Each archive delivery test ran once for its named frozen source, captured
subprocess output as UTF-8 with replacement, and recorded exact exits under
`docs/verification/evidence/cr034/`. A successful report only means an
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

- `BUG-020` — before `c2e7957`, an ambiguous formal group with two old IDs and
  one after ID populated every old row's singular `after_candidate_id`. This
  falsely suggested a one-to-one pairing. TC-IMPACT-008a retains all IDs in the
  group delta but requires `REVIEW_AMBIGUOUS` and a null singular after ID for
  each affected row. The final archive evidence is therefore a new check of the
  repaired bytes, not a relabeling of the `5c516a6` result.
