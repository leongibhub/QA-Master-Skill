# CR-032 provenance status independent review

- Review task: `TASK-131`
- Requirement: `NFR-010`
- Frozen implementation: `93f0d32c6b279908b4bd015f0fc830a8dd7b1d59`
- Frozen reviewed subject: `2db9fa9a78057581451569dbf1269850c9bf5f0d`
- Document State: DRAFT
- Evidence Status: OBSERVED
- Verdict: **PASS**
- Final findings: **P0 0 / P1 0 / P2 0 / P3 0**

## Scope

This review covers only the schema-v2 provenance metadata, its offline regression
contract, and the CR-032 follow-up report. It does not refresh the upstream
snapshot or establish current-upstream parity, Skill behaviour, host discovery,
acceptance, release, comparative quality, or a lifecycle Gate result.

## Independent observations

1. The v2 record keeps the historical freeze-time state as
   `independent_verification_status_at_freeze: PENDING` and gives the later
   verification its own bounded `independent_verification` object. Its scope text
   explicitly excludes this metadata revision and broader product claims.
2. Git object `cbff0bc0af4922ee75522f313cda10a646e70c7a` exists, is an ancestor of the
   recorded remote `main`, and contains both referenced reports. The report blobs
   recomputed, after the declared CRLF-to-LF normalization, to:
   - `f65866f8c344cd0afcd9e775d4afb090716ba5e69d4bb657b5fc457f42262f4d`
   - `1a209dedc5df76be542fca5d3d23463e9b0614c6ccd19ffe6868462749887e4c`
   These exactly match the metadata. The same evidence commit still contains the
   schema-v1 `PENDING` metadata, so the v2 record does not use itself as evidence.
3. No file under the pinned `en/` or `zh/` source snapshot differs from verified
   subject `523ec344112f03ea350e1fa13c16d5ddc755277e`. The focused provenance test
   independently recomputed the declared 5,816-file digest as
   `01c9414f426e36b8659aa08ac73d8db2042e2e1769aace4269881f7cb2c05799`.
4. `python -m unittest -v tests.test_vendor_skills tests.test_readme_catalog`
   completed **13 tests with OK** on `2db9fa9`.
5. A negative test changed both `evidence_commit` and its matching report URLs to
   a fake 40-hex revision. The regression test rejected the modified record at the
   independently pinned evidence-commit assertion.
6. `git diff --check HEAD^ HEAD` passed for the final repair commit.

## Finding history

### P2-001 — resolved before final verdict

The initial implementation test hashed the current checkout's report paths but
did not independently pin the immutable evidence commit or report tuples. Matching
edits to metadata and working-tree reports could therefore retarget the asserted
evidence chain while the test remained green.

Commit `2db9fa9` resolves this by independently pinning the evidence commit and
both artifact/path/hash tuples in the offline test. This remains usable in source
archives and installed-package checks that have neither Git metadata nor network
access. The independent Git-object comparison above establishes the correctness
of those initial pinned values. The negative tampering check confirms the repaired
test rejects a coordinated fake revision and URL change. No P2 remains.

## Delivery boundary

The reviewer started an additional wheel/standalone experiment, but its result was
not retained by the tool session and is not counted as independent evidence.
Its outcome is `NOT_AVAILABLE`; no independent wheel/standalone pass is claimed.
The implementation record's separate 16-check author validation, including
installed inventory and consumer discovery, remains an author observation and is
not relabelled here.

Within the reviewed metadata-only scope, the stale-status ambiguity is corrected
without changing the verified source snapshot or overstating the evidence. No
completion, release, acceptance, superiority, or Gate decision follows.
