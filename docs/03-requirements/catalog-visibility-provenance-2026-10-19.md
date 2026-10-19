# Catalog visibility and vendor provenance requirements — 2026-10-19

- Artifact: `DOC-CATALOG-VISIBILITY-PROVENANCE-REQ-001`
- Change: `CR-029`
- Document State: `DRAFT`
- Evaluation State: `IN_REVIEW`
- Evidence Status: `PENDING`

## Purpose and boundary

The user requested a complete, readable presentation of the currently delivered QA
skill catalogue after observing that the product README did not expose the content
visible in the upstream catalogue.  This document defines a bounded documentation
and provenance increment.  It does not assert that every listed Skill has been
executed, is equally capable, or is superior to another product.

The current installed bundle is the only delivery subject for the visibility work.
Current upstream contents and the identity of the imported snapshot must be
investigated separately before any refresh or parity statement.  CR-028 recorded
the absence of independently established package provenance as P3.  A concurrent
candidate provenance file may be examined under TASK-121, but it is not treated as
independently verified until its retrieval basis and digest are checked.

## REQ-026 — complete user-facing catalogue visibility

| Item | Requirement |
| --- | --- |
| Priority | P1 |
| Input | The installed vendor inventory and the physical English/Chinese Skill entries included by the current package. |
| Expected behaviour | The README provides a navigable, hierarchical catalogue of every logical Skill delivered by the current package.  Each entry states a concise purpose and links to the corresponding Chinese and English installed source where both are delivered.  A stable path-oriented index may remain in `docs/SKILL_CATALOG.md`, but it must point readers to the README's complete catalogue. |
| Scope boundary | A listed entry means the source asset is included in the delivered catalogue.  It does not mean an Agent selected it, an instruction was applied correctly, a test ran, a domain result passed, or that the product has a quality or comparison ranking. |
| Measurable acceptance | (1) Every logical canonical name represented by the package inventory occurs exactly once in the README catalogue. (2) Each listed logical Skill has working Chinese and English entry links when both language entries are packaged. (3) Readers can reach the catalogue from the README navigation and can locate an entry through headings or the README's in-page search. (4) The README and stable index agree on the set and logical count. (5) The catalogue uses only the current shipped asset paths and does not imply missing assets or unverified capabilities. |
| Verification | `TC-CAT-001` through `TC-CAT-006`; independent validation is required before any bounded completion statement. |

## NFR-010 — immutable vendor provenance and refresh discipline

| Item | Requirement |
| --- | --- |
| Priority | P1 |
| Expected behaviour | The vendored catalogue records machine-readable provenance for the exact packaged snapshot: source repository URL, immutable source revision, retrieval or refresh date, applicable licence reference, and a deterministic snapshot digest over the declared asset set.  A record may explicitly use `NOT_AVAILABLE` for a fact that cannot be established; it must never borrow a revision from a different checkout, historical comparison arm, or current network state. |
| Refresh rule | A future update first records the candidate upstream revision and retrieval date, produces a source-to-package path/digest diff, retains notices and licence obligations, and keeps the previous package recoverable by the existing installer contract.  The update is a new scoped change with fresh test and review evidence. |
| Scope boundary | Provenance proves the identity of packaged bytes.  It does not prove upstream completeness, present-day upstream parity, licence interpretation beyond the retained notice, product quality, or permission to change third-party content. |
| Measurable acceptance | (1) The immutable revision, date, source URL, licence reference and snapshot digest are present or each absent fact is explicitly marked `NOT_AVAILABLE`. (2) A verifier can recompute the snapshot digest from the packaged inventory without network access. (3) A refresh report identifies added, removed and changed paths and preserves the previous provenance record. (4) No README claim calls the delivered set current, complete relative to upstream, or superior unless separately evidenced. |
| Verification | `TC-CAT-007` and `TC-CAT-008`; no upstream retrieval, package mutation or licence decision has occurred under this requirement draft. |

## Planned work and test cases

| ID | Work / check | Owner role | Expected evidence state |
| --- | --- | --- |
| TASK-120 | Build the README catalogue and align the stable index to REQ-026; retain a local structural check. | documentation_manager | `PENDING` |
| TASK-121 | Inspect the current upstream catalogue, including Playwright-related entries, and establish or explicitly retain the exact vendor provenance record before proposing any package refresh. | researcher / developer | `PENDING` |
| TASK-122 | Independently test the frozen documentation and provenance implementation. | tester | `PENDING` |
| TASK-123 | Independently review scope, catalogue truthfulness, path integrity, provenance treatment and licence-boundary claims. | reviewer | `PENDING` |
| TC-CAT-001 | Enumerate logical canonical names from the packaged inventory and compare the exact set with README catalogue markers. | tester | `NOT_EXECUTED` |
| TC-CAT-002 | Resolve every Chinese and English README catalogue link against the frozen package. | tester | `NOT_EXECUTED` |
| TC-CAT-003 | Check catalogue navigation, headings and entry discoverability from README. | tester | `NOT_EXECUTED` |
| TC-CAT-004 | Compare README logical count and name set with `docs/SKILL_CATALOG.md`. | tester | `NOT_EXECUTED` |
| TC-CAT-005 | Check that each catalogue description and boundary statement is compatible with the linked asset and contains no execution, quality, release or superiority claim. | tester | `NOT_EXECUTED` |
| TC-CAT-006 | Fresh-install check: resolve sampled and exhaustive catalogue paths within an installed package rather than the source checkout. | tester | `NOT_EXECUTED` |
| TC-CAT-007 | Validate required vendor-provenance fields and recompute the snapshot digest offline from the declared inventory. | tester | `NOT_EXECUTED` |
| TC-CAT-008 | For a proposed refresh only, independently compare the recorded upstream revision and retrieval evidence with the candidate path/digest diff; otherwise record no refresh as `NOT_EXECUTED`. | tester | `NOT_EXECUTED` |

## Change impact

Documentation and packaged vendor metadata are in scope.  A future upstream sync may
affect package contents, installer manifests, attribution, routing coverage, tests
and the README; those effects require a separate source diff and verification.
No Gate, release, external operation, product acceptance, comparison result, or
superiority conclusion follows from this draft.
