# Catalog provenance refresh evidence — 2026-10-19

- Artifact: `DOC-CR029-CATALOG-PROVENANCE-REFRESH-001`
- Change: `CR-029`
- Related work: `TASK-121`, `TC-CAT-007`, `TC-CAT-008`
- Document State: `DRAFT`
- Evaluation State: `IN_REVIEW`
- Evidence Status: `OBSERVED`

## Attempt 1 retained facts

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

## Corrective retry placeholder

Status: `PENDING`.

The retry must freeze its source revision and package revision, choose one explicit
digest representation (raw Git blob bytes or an exact line-ending normalization
rule), recompute the complete 5,816-path manifest offline, and retain a path/digest
diff with `added`, `removed`, `changed`, and `line-ending-normalized` categories.
It must also re-run `TC-CAT-007` and `TC-CAT-008` independently.  No PASS result,
package refresh conclusion, Gate decision, release, or superiority claim exists.
