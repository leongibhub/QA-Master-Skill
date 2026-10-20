# TASK-123 independent review of CR-029 catalogue visibility and provenance

- Artifact ID: `DOC-CR029-INDEPENDENT-REVIEW-001`
- Proposed Evidence ID: `EVD-CR029-INDEPENDENT-REVIEW-001`
- Change: `CR-029`
- Requirements: `REQ-026`, `NFR-010`
- Reviewer: `/root/catalog_visibility_review`
- Review result: `PASS WITH P3 FOLLOW-UP`
- Finding counts: `P0=0`, `P1=0`, `P2=0`, `P3=1`
- Document State: `DRAFT`
- Evidence Status: `OBSERVED`
- Date: 2026-10-19

This review covers the bounded README catalogue, pinned bilingual vendor snapshot,
package delivery and provenance contract. It does not decide a project Gate,
approve a release, accept the whole product, prove the semantic quality of every
Skill, or establish comparative superiority.

## Frozen review subject and evidence

| Subject | Revision / result |
| --- | --- |
| Final product and test source | `523ec344112f03ea350e1fa13c16d5ddc755277e` |
| README/catalogue implementation | introduced at `024505bd5e59df62be7b46bf4dbf0681e0911aad`; unchanged by the three provenance corrections |
| Pinned upstream source | `547fbcd9c417ab8afbde1cd9f18b40ecbae0333b`, tree `694cf0b677cb90cee101e7806657537b016c356c` |
| Independent test | `EVID-CATALOG-VISIBILITY-INDEPENDENT-2026-10-19`; `TC-CAT-001` through `TC-CAT-008` PASS on the final subject within their stated boundaries |
| Local reviewer check | 13 focused tests PASS; independent digest recomputation `01c9414f426e36b8659aa08ac73d8db2042e2e1769aace4269881f7cb2c05799` |
| CI at review time | two Ubuntu jobs for `523ec34` successful; two Windows jobs still in progress and therefore not counted as PASS evidence |

The failed and superseded attempts remain part of the evidence chain. Attempt 1
(`024505b`) failed on Linux because its raw-byte digest depended on checkout line
endings. Attempt 2 (`5996ace`) normalized binary bytes and overstated verification.
Attempt 3 (`598a979`) separated text and binary treatment but retained
platform-dependent path ordering. None of those outcomes is relabelled as a pass.

## Requirement and architecture assessment

### REQ-026 — complete catalogue visibility: PASS in bounded scope

The README exposes 165 logical Skills through 330 English/Chinese links. The
hierarchy matches the delivered inventory exactly: 10 workflows, 28 Core QA, 100
Engineering QA, 4 Production Quality, 18 AI Native QA and 5 Skill Engineering
entries. Each language entry occurs once, all linked package paths resolve, and
`docs/SKILL_CATALOG.md` has the same logical and physical set.

The user flow retains one QA Master entry for single-stage, combined and complete
QA work. The catalogue does not introduce separate required installations. The
main README does not copy the upstream multi-tool installer table or community
recommendations and does not claim those integrations. It distinguishes asset
presence and routing from execution, output quality, acceptance and release.

### NFR-010 — vendor provenance: PASS in pinned-snapshot scope

The package records the source repository, immutable commit and tree, retrieval
date, licence path, declared 5,816-file scope and deterministic digest. The final
algorithm uses UTF-8 bytewise ordering of relative POSIX paths, strict UTF-8 and
CRLF-to-LF canonicalization for an exhaustive declared text-extension set, and raw
bytes for the declared `.docx` binary set. Unknown extensions and invalid declared
text fail the regression rather than being silently reclassified.

Independent source-archive and fresh-wheel recomputation produced the declared
digest. A pinned Git-object comparison found 5,816 upstream blobs and 5,816
committed vendor blobs with no missing, extra or changed paths. The upstream and
vendored licence blobs also matched.

Canonical text provenance is kept separate from installed-byte integrity. A wheel
built from a clean archive was installed into an isolated environment and then to
a separate consumer directory. Its 5,820-entry vendor inventory had no missing or
changed files, and `.qa-master-install.json` matched all 5,882 installed
non-manifest files. Generated `__pycache__` files were correctly excluded from the
declared vendor source set and installer manifest.

The earlier CR-028 provenance P3 is therefore closed only for the pinned `en/` and
`zh/` snapshot at the stated upstream revision. This does not prove later upstream
currency, repository-wide parity outside those subtrees, licence interpretation,
Skill behaviour, product quality or superiority.

## Compatibility, security and regression assessment

The catalogue expansion changes documentation and links; it does not add another
runtime entry or weaken execution and external-write gates. The two Playwright
runner files now equal their pinned upstream blobs and pass `bash -n`; static checks
confirm their JSON-output environment variable and reporter list. Browser execution
was not performed, so no browser-runtime result is claimed.

Attribution and the PolyForm Noncommercial licence remain packaged. The retained
upstream README is clearly identified as upstream material; its third-party tool
and community statements are not presented as QA Master support claims. No secret,
credential or external-write path was introduced by this change.

## Finding

### P3 — embedded independent-verification status has ambiguous lifetime

`qa_master/skills/vendor/awesome-qa-skills/SOURCE_PROVENANCE.json` records
`verification_status: OBSERVED` and `independent_verification_status: PENDING`.
Those values were truthful when `523ec34` was frozen, and the external independent
report now verifies that exact commit. A consumer reading only the immutable
package metadata, however, cannot tell that `PENDING` is a freeze-time status and
may treat it as the current evidence state.

This does not invalidate the revision, tree, licence, file set, digest or fresh
install evidence. Recommended follow-up: in the next metadata-schema revision,
name the field as status-at-freeze or replace the mutable status with an external
attestation reference. Do not rewrite the tested snapshot merely to make it
self-assert `VERIFIED`.

## Bounded conclusion

No unresolved P0, P1 or P2 finding remains on `523ec34`. The README now makes the
complete delivered catalogue visible without adding unsupported multi-tool,
community, execution or superiority claims. The pinned bilingual snapshot and its
fresh installed delivery are reproducible within the declared text/binary and
package-manifest boundaries.

The result is `PASS WITH P3 FOLLOW-UP`. It is not a project Gate decision, release
approval, human acceptance or evidence that QA Master is better than another
product.
