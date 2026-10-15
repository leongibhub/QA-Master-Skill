# TASK-053 paired-pilot semantic audit

- Artifact ID: `DOC-PAIRED-PILOT-SEMANTIC-AUDIT-001`
- Evidence ID: `EVD-PAIRED-PILOT-SEMANTIC-AUDIT-001`
- Document State: `DRAFT`
- Evidence Status: `OBSERVED`
- Reviewer: `/root/workflow_review`
- Runtime work: `work-d02516a2870b4befa3e4e53e0b329d54` v1 / attempt 1
- Source commit: `4c30faa233eb60cea3fa6a9122d7d85baf6af18d`
- Date: 2026-10-15
- Finding count: **P0 0 / P1 0 / P2 3 / P3 1**

## Scope and evidence boundary

This audit reads the six retained pilot envelopes, their unchanged final bytes,
the three public visible inputs, the three public oracle bundles, and the
existing exact grade. It compares source rules with the generated cases,
steps, expected results, gaps, and typed observations.

The capture index is
`docs/verification/evidence/paired-pilot-001/index.json`, SHA-256
`3CE6BBBE08AC4504C58F115D27EC63752A76C6A6E72B3B02BED2F3335E06EA11`.
It binds result SHA-256
`B2CB38FA826184BE698EBB2DD4C04FB6587F91FE559150DCA69671DB4C004FFE`
and grade SHA-256
`8CFB753182DB0EC0C325F3C0F0F8AC739A40E832A0E21165E23CF2BA3FDA2C6B`.
All six envelope hashes match that index.

Arm A is `QA-Master-current-packaged` at source commit
`96926a282739865f90bcedf9eab2ec6c5ada6176`; Arm B is
`Awesome-QA-Skills-pinned` at source commit
`1a8c57c0e1c31b80aea5cb85dd830387dee09c9f`, as bound by the frozen run
manifest. These identities help locate the observations; they do not turn this
single public-development run into a controlled product comparison.

No model was called for this audit. It did not rerun or reinterpret the pilot,
change source, fixtures, raw capture, oracle, or grade, and did not create a
human rating or aggregate score.

The public semantic inputs reviewed were:

| Scenario | Visible-input SHA-256 | Public-oracle SHA-256 |
|---|---|---|
| `PE-BND-001` | `FADE63DF9F6809BF110E0576E5BD5A64689484F180DF14DF48B610334DADBC80` | `2CED8951C7FBCE2B8830FA90DF20F4B3E6ABE9B067721B15EFEF21CA617A6A12` |
| `PE-DTT-001` | `42D2EFE819481B61576342BA589CEB25CA61E7EA180CAA74A697BDB70127DB77` | `CE63E126DED22E18FCF740054059CF7205B9A1A46E0FDDC33D5F6612CC722081` |
| `PE-STT-001` | `8B28A1A3721366A452019DEF87F49722894CE26C31FDF0349A05457E6F20FB51` | `50916D0D622854BC4D3057855B4DD3CD9FE6DDF5D6AC050E2870D38FC67299FD` |

## Findings

### P2-001 — the hidden exact JSON shape is not a semantic quality oracle

The existing grade reports seven `SATISFIED` and five `VIOLATED` assertions.
All six source-provenance assertions are satisfied. Of the six primary JSON
assertions, only Boundary Arm A exactly equals its bundle; the other five are
`VIOLATED`.

The visible questions request a JSON observation but do not define its inner
property names, classification vocabulary, ordering, optional annotations, or
`additionalProperties` policy. Concrete evidence of the mismatch follows:

- Boundary Arm B returns the same accepted set `[1,2,8,9]` and rejected set
  `[0,10]` as the oracle, adding only `step: 1` and an expectation-scope note.
- Both decision-table arms enumerate the same three legal combinations, the
  same excluded combination, the two defined fees, and the unresolved
  MEMBER/DOMESTIC conflict. Their labels and supporting detail differ from the
  compact oracle.
- Both state-transition arms preserve the same two valid and three invalid
  candidates, guards, target/preserved states, and sourced persistence facts,
  but use richer structures and different member names.

These are exact-structure variances. The grade correctly records canonical
inequality, but that inequality is not evidence that the rule semantics are
wrong. Treating it as quality would penalize correct additional detail and
unpublished representation choices.

**Impact:** the current grade cannot rank case quality or distinguish a wrong
rule from an alternate correct representation. It may produce false semantic
negatives while missing unusable cases entirely.

**Prospective correction:** either publish an exact per-check semantic schema
in the visible input, including required/optional fields and controlled enums,
or grade a documented normalized projection. Preserve extension annotations
outside the graded projection. Report transport/shape conformance separately
from semantic fulfillment.

### P2-002 — two outputs contain analysis but no test cases

Decision-table Arm B and state-transition Arm B both have `cases: []`.
Nevertheless, their observations contain respectively all four finite
condition combinations and all five stated transition candidates. The material
is useful analysis, but it does not provide case-level preconditions, data,
steps, and expected results in the response contract's `cases` collection.

The exact grader never examines `cases`, `steps`, `expected`, or `gaps`.
Consequently it cannot specifically detect this deliverable failure. The same
grader would also not distinguish an empty case set from an executable one if
the observations were canonical.

**Impact:** the two outputs cannot be directly reviewed, imported, or executed
as case artifacts without a second transformation. A consumer could mistake a
complete rule analysis for a complete test design.

**Prospective correction:** derive visible coverage obligations and require
each obligation to map to a nonempty case or an explicit, typed gap. Every case
must carry source, precondition/setup, concrete action/input, observable
expected outcome, and readiness state. An analysis record is not a substitute
for a case record.

### P2-003 — the state-transition oracle invents an archive side-effect invariant

Visible fact `F-STT-005` says that `archive` is undefined, the request is
invalid, and the state remains DRAFT. It does not say that persisted data or
other side effects remain unchanged. The public oracle nevertheless requires
the archive row to contain `side_effect_expectation: "UNCHANGED"`, separately
from `state_expectation: "DRAFT"`.

Both arms preserve the sourced state invariant and explicitly say that effects
beyond state are unspecified. Arm A records `G-STT-001`; Arm B records the same
gap. This is evidence-safe behavior, not a participant omission.

**Impact:** the hidden oracle encourages fabrication of an invariant that is
not in the visible source and contributes to both state-transition primary
assertions being `VIOLATED`.

**Prospective correction:** remove the unsupported effect expectation or add a
visible source fact. Until then, grade that field as `ORACLE_MISSING` or
`UNSCORABLE`; do not retroactively change the retained pilot grade.

### P3-001 — execution readiness is only free-text and remains source-limited

The public inputs intentionally describe rules, not a concrete API/UI, data
fixture, environment, response schema, or observable rejection signal. The
generated cases are therefore logical draft designs, not runnable cases:

- Boundary Arm A correctly records that the validation entry point and concrete
  accept/reject signals are missing. Boundary Arm B leaves `gaps` empty and says
  no additional assumptions are needed even though its action only says to
  evaluate the values "in future validation".
- Decision-table Arm A correctly makes the conflicting combination a static
  rule-mapping case and records that excluded-input runtime behavior is unknown.
- State-transition Arm A covers all five candidates. Its SUBMITTED/cancel case
  names SUBMITTED as a precondition but does not state the source-defined setup
  path (`submit` from DRAFT with `owner=true`). Arm B records that reachability
  path in analysis but still emits no case.
- The phrases "no side effect" and "persisted data remains unchanged" are not
  tied to an enumerated persisted-field or external-effect inventory. Neither
  participant can derive that inventory from the visible source.

This is mainly an input and response-contract limitation. The neutral case
schema also lacks a typed per-case readiness/block reason, setup/teardown,
cleanup, target interface, and observable locator. Prose gaps are honest, but a
machine consumer cannot reliably separate design-ready, static-review, and
blocked cases.

**Prospective correction:** provide a declared execution target and observable
contract when executable cases are expected. Add a case readiness field such as
`DESIGN_READY` or `BLOCKED_ORACLE_MISSING`, and structured setup, observable,
cleanup, and missing-oracle fields. Do not require participants to invent an
interface or denial response.

## Scenario-by-scenario semantic audit

| Scenario | Source-determinable obligations | Arm A observation | Arm B observation | Exact-grade interpretation |
|---|---|---|---|---|
| `PE-BND-001` | Whole-number step 1; accept `1,2,8,9`; reject `0,10`; cite both facts. Exact inner JSON shape is not specified. | Two parameterized cases cover all six points with correct outcomes. The interface/observable gap is explicit. | Two parameterized cases cover all six points with correct outcomes. The interface gap is not recorded. | A primary and provenance assertions satisfy. B provenance satisfies; primary violation is extra correct metadata, not a semantic error. |
| `PE-DTT-001` | Three legal combinations, one excluded combination, fees 15/5, MEMBER/DOMESTIC conflict, and conflict-source pair are determinable. Runtime reaction for the excluded input is not. Exact object/enums are not specified. | Four case records cover the full finite universe. Defined fees, conflict, exclusion, and both missing-oracle gaps are preserved. | The observation covers the same universe and outcomes, but `cases` is empty. | Both provenance assertions satisfy; both primary violations are representation differences, not observed rule errors. |
| `PE-STT-001` | Two valid and three invalid candidates, guards, target/preserved states, submitted-at persistence, and unchanged persisted data for two invalid candidates are determinable. Archive side effects, concrete denial responses, timestamp value semantics, and other events from CANCELLED are not. | Five case records cover all stated candidates and avoid inventing archive side effects. Setup for the SUBMITTED pre-state is implicit. | Analysis covers the same candidates and gives useful reachability detail, but `cases` is empty. | Both provenance assertions satisfy. Both primary violations combine hidden shape differences with the oracle's unsupported archive-effect field. |

## Limited product observations

For these exact public fixtures, Arm A produced reviewable case records for all
three methods: two boundary groups, four decision-table rows, and five
state-transition candidates. Arm B produced equally usable boundary groups and
substantive decision/state analysis, but no decision-table or state-transition
case records. Arm B's state analysis is stronger on explicit reachability;
Arm A is stronger on deliverable case structure and on exposing missing runtime
oracles.

Those are case-specific observations. They do not establish an overall winner
or superiority: there is one public run, no holdout, no repeatability sample,
no verified provider revision/system baseline, no blinded review, and no human
rating.

## Prospective executable-quality contract

The next contract should be additive and non-retroactive:

1. Publish a typed semantic projection for every graded check. Define member
   names, types, enum meanings, identity/order rules, required fields, and where
   extension annotations may appear.
2. Build an obligation ledger from visible facts. Boundary points, every legal
   and excluded decision combination, and every stated transition/guard/effect
   must map to a case or a typed gap.
3. Grade four dimensions independently: response/shape conformance, semantic
   obligation fulfillment, case usability/completeness, and provenance/gap
   honesty. Do not collapse them into a score or winner.
4. Require each case to identify source, readiness, setup/preconditions,
   concrete data/action, observable expected result, cleanup, and any missing
   oracle. Empty cases or analysis-only findings cannot satisfy case coverage.
5. Bind every expected field to visible facts. Unsupported expectations become
   `ORACLE_MISSING` / `UNSCORABLE`; extra correct detail outside the projection
   does not become a semantic failure.
6. Require concrete target and observable contracts before calling a case
   executable. Preserve draft/static cases when those contracts are absent.
7. Keep the old raw outputs and exact grade immutable. Validate the new contract
   with new fixtures and independent tests before using it for any future
   comparison.

## Nonclaims

This audit does not alter the twelve retained assertion statuses. It does not
claim execution success for any generated test, strict comparability, fairness,
human preference, aggregate quality, superiority, acceptance, release, or a
Gate result. It is bounded evidence for future requirements and evaluator
design only.
