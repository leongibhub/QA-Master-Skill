# TASK-119 independent review of CR-028 continuation repairs

- Artifact ID: `DOC-CR028-FINAL-REVIEW-001`
- Proposed Evidence ID: `EVD-CR028-FINAL-REVIEW-001`
- Change: `CR-028`
- Requirements: `REQ-003`, `REQ-005`, `REQ-010`, `REQ-017`, `REQ-025`; `NFR-001`, `NFR-003`, `NFR-004`, `NFR-005`, `NFR-008` in the bounded mappings declared by CR-028
- Reviewer: `/root/glm_delta_review`
- Runtime work: `work-ba09d09a204f4cee9175acbdfa34c3a1`, attempt 1
- Review result: `PASS WITH P3 FOLLOW-UP`
- Finding counts: `P0=0`, `P1=0`, `P2=0`, `P3=1`
- Document State: `DRAFT`
- Evidence Status: `OBSERVED`
- Date: 2026-10-19

This is the formal independent review of the bounded CR-028 repair. It does not
decide a project Gate, complete any whole RTM requirement, approve a release,
accept the product, authorize execution or external writes, provide human
ratings, or establish superiority over Awesome QA Skills.

## Frozen review subject

| Subject | Revision / SHA-256 |
|---|---|
| Corrected product source | commit `6907fd4819daf931061fbbc69bcbdead51026208` |
| Original reviewed baseline | commit `c52f34c1a30f278e44ef483bb6cfdb5c7bfba130` |
| First repair subject | commit `0ff9ad47ab0d442dff2157f6bf7d10e322a83f75` |
| TASK-118 final report | `docs/verification/continuation-repair-independent-2026-10-19.md`, `dd58b6c0972b23059886a03d30f348aedfad5a3216ad89bb9406f351d011c6b9` |
| TASK-118 evidence manifest | `docs/verification/evidence/continuation-repair-independent-2026-10-19/manifest.json`, `2c116d33ddf3a92fc7bc2460a1a944e55a5c4c81d9b796861fad1432ca77dbe3` |
| Final CI | run `39211999256`, four successful jobs, 799 tests per job |

The first independent attempt is part of the review record. On `0ff9ad4`, the
fresh wheel omitted five inventoried hidden `.gitignore` assets and standalone
installation failed with `SKILL_VENDOR_RESOURCE_INVALID`. The same attempt's
strict run executed 798 tests and ended with one failure because a legacy test
incorrectly required there to be only one recursively discoverable `SKILL.md`.
Those failures remain retained and are not relabelled as passes.

The corrected subject adds the hidden-file package declaration and a clean-wheel
regression that requires the wheel vendor set to equal the 5,819-entry inventory
exactly and verifies every byte. The legacy update test now requires the exact
managed root-plus-vendor entry set, exactly one immediate QA Master entry, and a
complete isolated backup. Static review found no weakening of traversal,
symlink/reparse, overwrite-preservation or rollback checks.

## Disposition of the four reproduced findings

### Original P1 — standalone delivery omitted the breadth library: resolved

`qa_master/codex_skill.py` reads a fixed packaged inventory, rejects unsafe path
forms and linked filesystem resources, copies each listed asset, and includes the
inventory in the standalone bundle. `pyproject.toml` now explicitly includes the
five hidden vendor assets that setuptools' broad wildcard omitted.

TASK-118 attempt 2 built a fresh copied-source wheel, installed it without
dependency or network resolution, then installed the standalone Skill outside
the checkout. Source, wheel and standalone sets and bytes matched for all 5,819
vendor files. Discovery returned 330 language entries representing 165 canonical
skills, with imported and selected paths contained within their respective fresh
installations. The retained wheel SHA-256 is
`af2a4b9a7da20d695afcd36ba39436887632411ae62095a76a6e0459ce445fce`.

### Original P2 — negated requests introduced execution/regression: resolved

`qa_master/intent.py` separates positive and negative mentions with a bounded
lexical grammar, removes denied stages, and keeps execution and external-write
scope independent. Defect-submission words no longer act as unconditional
execution aliases.

Independent parser and persisted-campaign checks cover the three original
Chinese reproductions, English denials, mixed requests and positive controls.
Denied execution/regression stages remain absent and saved `no_execution` /
`no_external_writes` restrictions remain true. Positive execution planning
still does not grant executable capability or perform a test.

### Original P2 — long-tail catalog requests were unreachable: resolved

`qa_master/skill_registry.py` supports exact canonical names, documented curated
Chinese/English aliases, language selection, explicit unavailable-name gaps,
negated specialist exclusion and visible ambiguity. The application passes the
actual prompt into that selector.

TASK-118 independently addressed all 165 canonical names in both languages and
the documented property-based, chaos, Playwright and ambiguous RAG examples from
wheel and standalone installations. Ambiguous RAG remains visible rather than
silently guessed. This establishes catalog reachability only; it does not prove
the professional quality of outputs in 165 domains.

### Original P2 — interaction coverage mixed rows and interactions: resolved

`qa_master/design_methods.py` now counts the union of selected t-way
interactions for the interaction denominator. Candidate rows and missing-oracle
rows are separate analysis fields. Without an oracle, required interactions are
reported as unresolved oracle obligations and never as executed or ready cases.

Independent enumeration confirms 16/16 interactions for the packaged six-row
pairwise example, supported three-way combinations, and missing-oracle variants.
The deterministic generator remains bounded and draft-only.

## README and usability assessment

The rewritten README provides Windows and Linux installation commands, a
project-local entry, single-stage, combined, full-flow and specialist examples,
an explicit separation between 165 logical skills and 330 language directories,
and boundaries between deterministic helpers, Agent-applied guidance and actual
execution. It does not claim whole-product superiority, release readiness or
automatic quality from catalog size.

TASK-118 executed the documented local CLI examples and standalone lifecycle
commands. Planning retained no-execution scope; deterministic design remained
`DRAFT_UNAPPROVED` / `NOT_EXECUTED`; discovery returned 165 English plus 165
Chinese entries. All 366 repository-local link targets in README, Getting
Started and Skill Catalog existed. Interactive Agent output quality, remote
links and a Linux shell transcript were not verified and are not claimed.

## Independent evidence assessment

The attempt-2 test design covers the installed boundary that the original source
tests missed. It uses separate isolated processes for wheel and standalone
behavior, validates import and selected-path provenance, independently enumerates
combinatorial interactions, preserves the failed first attempt, and keeps skips
distinct from passes.

Final CI run `39211999256` completed successfully on Ubuntu and Windows with
Python 3.10 and 3.12. Each job ran 799 tests with zero failures and errors.
Ubuntu jobs recorded nine skips and Windows jobs three skips. The jobs checked
out merge `791e599`, which incorporates source `6907fd4` into base `c52f34c`;
the evidence does not describe that as a direct source-head checkout.

The reviewer also independently executed the clean-wheel inventory regression
on the corrected subject: one test passed in 226.149 seconds. The managed
update/backup regression separately passed in 117.705 seconds. These focused
checks supplement rather than replace TASK-118 and CI.

## Finding

### P3 — packaged vendor provenance does not identify its upstream revision

`qa_master/skills/vendor/awesome-qa-skills/README.md` records the upstream
repository, license and catalog counts. `qa_master/skills/vendor-files.json`
records the fixed 5,819 paths. Neither packaged artifact records an independently
verified upstream commit/tree, retrieval date or whole-snapshot digest.

Local Git and the generated standalone install manifest bind the delivered
bytes, so this is not a current runtime-integrity or installation failure. It
does leave the packaged third-party source provenance incomplete for future
updates and source-to-upstream reconciliation. Repository research documents
refer to an older comparison pin, but this review does not infer that the full
vendored import is byte-identical to that revision.

Recommended follow-up: after independently establishing the actual import
source, package its upstream commit/tree, retrieval date and snapshot digest (or
an equivalent per-file source manifest), and regression-test that metadata with
the delivered inventory. Until then, the upstream revision is `NOT_AVAILABLE`.

## Bounded conclusion

No unresolved P0, P1 or P2 finding remains in the reviewed CR-028 repair. The
four original defects are resolved on the fixed source and installed-delivery
boundary, and the README improvement is usable within the verified local scope.
The remaining P3 is a provenance follow-up and does not invalidate the bounded
repair result.

This result does not cover external systems, enterprise adapters, production
execution, customer acceptance, every specialist's semantic output, release
readiness, or comparative superiority. Those claims require their own current
requirements and evidence.
