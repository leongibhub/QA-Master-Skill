# Catalog visibility and vendor provenance requirements — 2026-10-19

- Artifact: `DOC-CATALOG-VISIBILITY-PROVENANCE-REQ-001`
- Change: `CR-029`
- Document State: `DRAFT`
- Evaluation State: `IN_REVIEW`
- Evidence Status: `OBSERVED` — failed and superseded attempts are retained.
  Attempt 4 has bounded independent test and review evidence; the review retains
  one P3 metadata-lifetime follow-up. No Gate, release, or acceptance result exists.

## Purpose and boundary

The user requested a complete, readable presentation of the currently delivered QA
skill catalogue after observing that the product README did not expose the content
visible in the upstream catalogue.  This document defines a bounded documentation
and provenance increment.  It does not assert that every listed Skill has been
executed, is equally capable, or is superior to another product.

The current installed bundle is the only delivery subject for the visibility work.
CR-028 recorded the absence of independently established package provenance as P3.
TASK-121 attempt 1 committed a candidate snapshot at `024505b`: it added a source
record, updated the retained upstream README, and aligned the bilingual Playwright
runner.  An independent check confirmed the declared 5,816 `en/` and `zh/` paths
and their upstream blobs for the pinned source revision.  That narrow equivalence
does not make a general present-day-upstream, quality, or release claim.

`TC-CAT-007` nevertheless failed in attempt 1: the declared raw-byte snapshot
digest did not recompute in the Windows worktree because CRLF conversion changed
eligible file bytes. Attempt 2 made a local normalized-text assertion pass but was
not accepted because its blanket normalization touched binary `.docx` files and its
metadata overstated verification. Attempt 3 (`598a979`) separated text and binary
handling but was a reviewer P2 NON-PASS because its non-ASCII path ordering did not
meet the stated UTF-8 bytewise digest contract. Attempt 4 (`523ec34`) defines
canonical UTF-8 bytewise relative POSIX sorting and digest `01c9414f…`.
Independent source-archive, fresh-wheel, install-manifest, upstream-blob and
focused catalogue checks passed in their bounded scope. The final review is `PASS
WITH P3 FOLLOW-UP`: the embedded `independent_verification_status: PENDING` was
truthful at freeze time but has an ambiguous lifetime for later package readers.
It is retained rather than rewritten; two Windows CI jobs were still in progress
at the last observation and are not counted as passing evidence.

## REQ-026 — complete user-facing catalogue visibility

| Item | Requirement |
| --- | --- |
| Priority | P1 |
| Input | The installed vendor inventory and the physical English/Chinese Skill entries included by the current package. |
| Expected behaviour | The README provides a navigable, hierarchical catalogue of every logical Skill delivered by the current package.  Each entry states a concise purpose and links to the corresponding Chinese and English installed source where both are delivered.  A stable path-oriented index may remain in `docs/SKILL_CATALOG.md`, but it must point readers to the README's complete catalogue. |
| Scope boundary | A listed entry means the source asset is included in the delivered catalogue.  It does not mean an Agent selected it, an instruction was applied correctly, a test ran, a domain result passed, or that the product has a quality or comparison ranking. |
| Measurable acceptance | (1) Every logical canonical name represented by the package inventory occurs exactly once in the README catalogue. (2) Each listed logical Skill has working Chinese and English entry links when both language entries are packaged. (3) Readers can reach the catalogue from the README navigation and can locate an entry through headings or the README's in-page search. (4) The README and stable index agree on the set and logical count. (5) The catalogue uses only the current shipped asset paths and does not imply missing assets or unverified capabilities. |
| Verification | `TC-CAT-001` through `TC-CAT-006`; bounded independent validation is retained for `523ec34`. It does not decide a Gate, release, or acceptance. |

## NFR-010 — immutable vendor provenance and refresh discipline

| Item | Requirement |
| --- | --- |
| Priority | P1 |
| Expected behaviour | The vendored catalogue records machine-readable provenance for the declared vendor snapshot: source repository URL, immutable source revision, retrieval or refresh date, applicable licence reference, and a deterministic snapshot digest over the declared asset representation. For declared UTF-8 text extensions, that representation is strict UTF-8 content with `CRLF` normalized to `LF`; declared binary extensions use raw file bytes. The digest therefore identifies canonical text content and declared-binary bytes, not the original raw worktree bytes of declared text files. Exact installed delivery bytes are a separate installer concern: `.qa-master-install.json` records per-file SHA-256 values over the written bytes and the installer validates those values. A record may explicitly use `NOT_AVAILABLE` for a fact that cannot be established; it must never borrow a revision from a different checkout, historical comparison arm, or current network state. |
| Refresh rule | A future update first records the candidate upstream revision and retrieval date, produces a retained source-to-package path/digest diff (including added, removed, changed, text-canonicalization, and declared-binary-byte classifications), retains notices and licence obligations, and keeps the previous package recoverable by the existing installer contract. The report location is `docs/verification/catalog-provenance-refresh-2026-10-19.md`; it identifies the source revision, baseline, verifier digest rule, result, unresolved paths, and whether installed-byte validation was executed. The update is a new scoped change with fresh test and review evidence. |
| Scope boundary | The source snapshot digest establishes canonical text-content identity for declared text paths and raw-byte identity for declared binary paths only. It does not establish raw worktree-byte identity for text files or exact bytes in an installed delivery; the latter requires a successful `.qa-master-install.json` manifest validation. It also does not prove upstream completeness, present-day upstream parity, licence interpretation beyond the retained notice, product quality, or permission to change third-party content. |
| Measurable acceptance | (1) The immutable revision, date, source URL, licence reference and snapshot digest are present or each absent fact is explicitly marked `NOT_AVAILABLE`. (2) A verifier can recompute the snapshot digest from the packaged inventory without network access using the declared canonical-text/raw-binary rule, without asserting raw worktree-byte identity for text paths. (3) A refresh report identifies added, removed, changed, text-canonicalized, and declared-binary-byte paths, preserves the previous provenance record, and states whether installer-manifest validation of installed bytes ran. (4) When exact installed-byte identity is asserted, the installer must validate `.qa-master-install.json` against the installed files. (5) No README claim calls the delivered set current, complete relative to upstream, or superior unless separately evidenced. |
| Verification | `TC-CAT-007` attempt 1 is `FAIL`: a 5,816-path/upstream-blob check passed, but the raw-byte digest mismatched after CRLF conversion. Attempt 2 (`5996ace`) is NON-PASS: it applied that normalization to binary files and recorded an inconsistent verification state. Attempt 3 (`598a979`) is reviewer P2 NON-PASS for non-canonical non-ASCII path ordering. Attempt 4 (`523ec34`) passed bounded independent source-archive/fresh-wheel/installed-manifest checks and reran `TC-CAT-008` as bounded PASS. Final review is `PASS WITH P3 FOLLOW-UP` for the embedded freeze-time independent-verification status; its remediation is a future metadata-schema change, not a rewrite of this tested snapshot. The initial upstream retrieval and package mutation are retained at `024505b`; no licence decision, release, quality, or superiority conclusion follows. |

## Planned work and test cases

| ID | Work / check | Owner role | Expected evidence state |
| --- | --- | --- |
| TASK-120 | Build the README catalogue and align the stable index to REQ-026; retain a local structural check. | documentation_manager | `024505b` implementation is `OBSERVED`. On frozen `523ec34`, the independent 13-test focused suite passed the 165 logical-name/330 bilingual-leaf, link, navigation, index and boundary checks; the fresh delivery check also passed. No completion, release, or Gate conclusion follows. |
| TASK-121 | Inspect the current upstream catalogue, including Playwright-related entries, and establish or explicitly retain the declared vendor-provenance record before proposing any package refresh. | researcher / developer | Attempt 1 `FAIL` at `024505b`; attempt 2 `NON-PASS` at `5996ace`; attempt 3 P2 `NON-PASS` at `598a979`; attempt 4 `523ec34` bounded PASS with a P3 metadata-lifetime follow-up. |
| TASK-122 | Independently test the frozen documentation and provenance implementation. | tester | Attempts 1–3 are retained. For `523ec34`, `TC-CAT-001`–`008` passed within their declared scope: 13 focused tests, clean archive and wheel provenance, upstream 5,816/5,816 blob comparison, fresh 5,820-file vendor inventory and 5,882-file installer-manifest validation. |
| TASK-123 | Independently review scope, catalogue truthfulness, path integrity, provenance treatment and licence-boundary claims. | reviewer | `PASS WITH P3 FOLLOW-UP`, P0/P1/P2=0: the embedded `independent_verification_status: PENDING` is freeze-time state with ambiguous lifetime. Do not rewrite this tested package; address it in a future metadata-schema revision. |
| TC-CAT-001 | Enumerate logical canonical names from the packaged inventory and compare the exact set with README catalogue markers. | tester | Attempt 1 `PASS`; final `523ec34` focused suite `PASS`. |
| TC-CAT-002 | Resolve every Chinese and English README catalogue link against the frozen package. | tester | Attempt 1 `PASS`; final `523ec34` focused suite `PASS`. |
| TC-CAT-003 | Check catalogue navigation, headings and entry discoverability from README. | tester | Attempt 1 `PASS`; final `523ec34` focused suite `PASS`. |
| TC-CAT-004 | Compare README logical count and name set with `docs/SKILL_CATALOG.md`. | tester | Attempt 1 `PASS`; final `523ec34` focused suite `PASS`. |
| TC-CAT-005 | Check that each catalogue description and boundary statement is compatible with the linked asset and contains no execution, quality, release or superiority claim. | tester | Attempt 1 `PASS`; final `523ec34` focused suite `PASS`. |
| TC-CAT-006 | Fresh-install check: resolve sampled and exhaustive catalogue paths within an installed package rather than the source checkout. | tester | Attempt 1 `NOT_EXECUTED`; final `523ec34` `PASS` from clean-archive wheel through separate consumer installation (5,820 vendor entries, 0 missing/changed; 5,882 manifest files matched). |
| TC-CAT-007 | Validate required vendor-provenance fields and recompute the declared canonical-text/raw-binary snapshot digest offline. When exact installed bytes are asserted, separately validate the installer manifest against the installed files. | tester | Attempt 1 `FAIL`; attempt 2 `NON-PASS`; attempt 3 P2 `NON-PASS`; final `523ec34` `PASS` with matching source-archive and wheel digest `01c9414f…` plus separate installed-manifest validation. |
| TC-CAT-008 | Independently compare the recorded upstream revision and retrieval evidence with the candidate path/digest diff, including canonical-text and raw-declared-binary treatment; otherwise record no refresh as `NOT_EXECUTED`. | tester | Attempt 1 bounded `PASS`; attempts 2–3 `NOT_EXECUTED`; final `523ec34` bounded `PASS` (5,816/5,816 upstream/vendor blobs, zero diffs and matching licence blob). |

## Change impact

Documentation and packaged vendor metadata are in scope.  A future upstream sync may
affect package contents, installer manifests, attribution, routing coverage, tests
and the README; those effects require a separate source diff and verification.
No Gate, release, external operation, product acceptance, comparison result, or
superiority conclusion follows from this draft.
