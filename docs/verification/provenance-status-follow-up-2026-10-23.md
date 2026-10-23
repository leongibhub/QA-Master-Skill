# CR-032 provenance metadata status follow-up

- Requirements: NFR-010; closes the metadata-lifetime P3 follow-up from TASK-123.
- Tasks: TASK-130 implementation; TASK-131 independent verification and review.
- Document State: DRAFT. Evidence Status: OBSERVED.
- Scope: metadata schema and evidence references only.

The user requested correction of the stale `PENDING` presentation. Schema v2
renames the freeze-time field to `independent_verification_status_at_freeze` and
adds a separate `independent_verification` record. Its `VERIFIED` status refers
only to the pinned bilingual snapshot tested at
`523ec344112f03ea350e1fa13c16d5ddc755277e`, not to this new metadata revision.

The record binds the upstream commit and unchanged snapshot digest to two existing
independent reports at immutable evidence commit
`cbff0bc0af4922ee75522f313cda10a646e70c7a`. Report SHA-256 hashes normalize CRLF
to LF, so Windows checkouts and repository blobs agree. These are unsigned report
references, not signed attestations. Reports remain external to the Skill bundle;
their immutable URLs and hashes travel with the package.

The prior source commit, retrieval date, snapshot algorithm, 5,816-file digest,
licence and `en/`/`zh/` bytes are unchanged. Historical reports are preserved.
Package readers of schema v1 must explicitly support schema v2 to use the new
fields. No runtime parser consumes the former status field in this repository;
the regression test is updated to validate report hashes and snapshot binding.

Acceptance: distinguish freeze-time state from subsequent verification; preserve
the source snapshot; resolve both report URLs to immutable recorded documents;
validate the unchanged snapshot digest and report hashes; independently review the
change. No new source refresh, upstream-currency, host discovery, Skill-quality,
Gate, acceptance or release conclusion is implied.

Author validation: `python -m unittest tests.test_vendor_skills tests.test_readme_catalog tests.test_vendor_install -v` completed 16 tests in 52.281 seconds with `OK`; `git diff --check` passed. This includes the 5,816-file snapshot digest, report-hash binding, complete installed inventory and isolated consumer discovery. Independent verification and review: PENDING at implementation freeze.
