# Catalog provenance refresh evidence — 2026-10-19

- Artifact: `DOC-CR029-CATALOG-PROVENANCE-REFRESH-001`
- Change: `CR-029`
- Related work: `TASK-121`, `TC-CAT-007`, `TC-CAT-008`
- Document State: `DRAFT`
- Evaluation State: `IN_REVIEW`
- Evidence Status: `OBSERVED`

## Attempt register

### Attempt 1 — `024505b` — FAIL

Implementation commit `024505bd5e59df62be7b46bf4dbf0681e0911aad` added
`SOURCE_PROVENANCE.json`, updated the retained upstream README, and changed the
bilingual Playwright runner.  The candidate source record names upstream commit
`547fbcd9c417ab8afbde1cd9f18b40ecbae0333b`, retrieval date `2026-10-19`, and a
5,816-file `en/`/`zh/` snapshot scope.

Independent checking confirmed that the declared 5,816 relative paths and the
corresponding upstream blobs match the pinned revision.  This is a bounded
source-to-package observation; it does not assert that the package is generally
current, complete beyond the stated scope, released, or superior.

`TC-CAT-007` is **FAIL** for this attempt.  The candidate metadata specifies a
digest over raw eligible file bytes, but recomputing it in the Windows worktree
encountered CRLF-converted bytes and produced a different digest.  Therefore the
declared snapshot digest is not yet a cross-worktree verifier contract.

### Attempt 2 — `5996ace` — NON-PASS

The first corrective candidate made a local normalized-text assertion pass, but
independent review found two disqualifying issues: its blanket `CRLF -> LF`
transformation also changed the raw bytes of 12 declared-binary `.docx` assets, and
its `verification_status: VERIFIED` field contradicted the still-pending
independent verification. `TC-CAT-008` was not re-executed for this rejected
candidate. Attempt 2 is retained as a non-pass and does not close
`BUG-CR029-001`.

### Attempt 3 — `598a979` — NON-PASS / P2

Commit `598a979fc1a7db6b57a5247a246482c81a9df7ed` declares separate text and
binary hashing, a strict text-extension registry, UTF-8 decoding for declared text
and byte preservation for declared binaries. Review found a P2 digest-contract
defect: its path ordering did not make the claimed UTF-8 bytewise relative POSIX
ordering explicit and reproducible for non-ASCII paths. The candidate is
superseded and is retained as a non-pass; no earlier PASS is transferred to it.

### Attempt 4 — `523ec34` — PASS WITH P3 FOLLOW-UP

Commit `523ec344112f03ea350e1fa13c16d5ddc755277e` specifies UTF-8 bytewise
relative POSIX path ordering and records snapshot digest
`01c9414f426e36b8659aa08ac73d8db2042e2e1769aace4269881f7cb2c05799`. It is the
frozen/pushed corrective subject. The independent source-archive and fresh-wheel
recomputation both produced the declared digest; the declared 5,816-path upstream
and vendor Git-blob sets had zero differences; and clean-archive installation
validated 5,820 vendor entries plus 5,882 installed non-manifest files against
`.qa-master-install.json`. `TC-CAT-001` through `TC-CAT-008` therefore passed
within their stated boundaries. The reviewer recorded `PASS WITH P3 FOLLOW-UP`,
P0/P1/P2=0: `independent_verification_status: PENDING` is accurate freeze-time
metadata but has ambiguous lifetime for a later package-only reader. The tested
snapshot is not rewritten; a future metadata-schema revision must name the
freeze-time state or reference external attestation. At the observation time two
Ubuntu CI jobs succeeded and two Windows jobs remained in progress, so Windows CI
is not counted as passing evidence.

## Future refresh evidence requirement

Any future refresh must recompute the complete declared manifest offline,
apply the declared canonical-text/raw-binary rule, and retain a path/digest diff
with `added`, `removed`, `changed`, `text-canonicalized`, and
`declared-binary-byte` categories. It must state that this snapshot digest does
not prove raw worktree bytes for text paths. If it asserts exact installed delivery
bytes, it must also validate `.qa-master-install.json` against the installed files
and retain that result separately. It must re-run `TC-CAT-007`, `TC-CAT-008`, fresh
wheel/standalone delivery (`TC-CAT-006`), and review the evidence-state fields.
Attempt 4's bounded PASS does not decide a Gate, release, acceptance, or
superiority claim.
