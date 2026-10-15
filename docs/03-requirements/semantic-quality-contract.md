# Semantic QA quality evaluator sub-contract

- Artifact ID: `DOC-SEMANTIC-QUALITY-CONTRACT-001`
- Document State: `DRAFT`
- Evaluation State: `IN_REVIEW`
- Evidence Status: `PENDING`
- Change: `CR-013`
- Work: `TASK-059` / `work-132abdca7cbe4db4ad838f12c5ecaa1c` v1, attempt 1
- Requirements: `REQ-025` v1 and `NFR-009` v1; no new requirement ID is allocated
- Design input: `DES-055` v1 and `DOC-PAIRED-PILOT-SEMANTIC-AUDIT-001` v1
- Date: 2026-10-15

## Scope and nonclaims

This Phase 2 sub-contract assesses retained QA responses against published,
source-bound facts with a local process-free evaluator. It is separate from
`qa_master.paired_evaluation.grade_run`, which keeps its existing exact typed
assertion comparison. It does not change or regrade CR-011 raw output, public
oracle, legacy grade, assertion statuses, run identity, or retained bytes.

The evaluator never calls a model, launches a process, reaches a network target,
synthesizes cases, makes an external write, or turns a draft into execution
evidence. It emits no aggregate, numeric score, rating, winner, fairness,
superiority, acceptance, Gate, or release result.

Human narrative ratings, holdouts, evaluator qualifications, thresholds,
sample-size rules, and comparison interpretation are `NOT_AVAILABLE`. A local
default cannot supply them.

## Published evaluator bundle

Before output assessment, an owner freezes one non-secret, content-addressed
bundle:

| Item | Required contract |
|---|---|
| Visible facts | Stable fact IDs, exact determinate value/type, source locator/digest, and scope. An absent fact is not an expected value. |
| Typed semantic projection | Per-check schema or deterministic normalization from the neutral envelope. It specifies members, types, controlled enums, identity/order, required/optional fields, and extension locations. Shape parsing stays separate from semantic comparison. |
| Obligation ledger | Stable ID; visible fact IDs; required interpretation; applicable category/dimension; and declared expected state. Unbound fields are excluded. |
| Category applicability | Every broad category below is `APPLICABLE`, `NOT_APPLICABLE` with reason, `ORACLE_MISSING`, or `UNSCORABLE`; none may be silently omitted. |
| Case/gap schema | Published case and gap members, source/gap binding, and readiness vocabulary. A natural response is accepted only with a deterministic projection. |
| Evaluator identity | Contract, projection, normalizer, and result-schema SHA-256 values. Missing identity prevents evaluation. |

A changed fact, projection, ledger, normalizer, category rule, participant
artifact, or declared input creates a new result identity. Prior bytes remain
historical evidence.

## Result profile

The normalized profile has an independent row for each applicable
`(obligation_id, dimension)` pair, an evidence pointer, and fact/contract IDs.
Its only outcomes are:

| Outcome | Meaning |
|---|---|
| `SATISFIED` | Valid projected field plus required source binding meets a published obligation. |
| `VIOLATED` | Valid projected field contradicts a source-bound obligation, or a required usable-case member is demonstrably absent. |
| `ORACLE_MISSING` | Visible source lacks a required expected value, target, observable, or side-effect invariant. |
| `UNSCORABLE` | Projection, response, category, required evidence, or a legitimate deterministic rule is unavailable or unsupported. |

An empty case list cannot satisfy usability. Correct extension detail outside the
projection cannot alone create a semantic violation. A hidden JSON member,
ordering rule, enum, or `additionalProperties` rule cannot create a semantic
obligation. Rows are never collapsed across dimensions, scenarios, participants,
or categories.

| Dimension | Assessment boundary |
|---|---|
| `SHAPE` | Envelope/projection parseability and declared transport members. |
| `SEMANTIC` | Source-determined values, rules, exclusions, guards, states, effects, and conflicts. |
| `USABILITY` | Case/gap delivery and stated consumer readiness. |
| `PROVENANCE` | Visible-fact binding and honest missing/ambiguous/conflicting/unsupported gaps. |

## Case and gap artifact

A case requires a stable `case_id`, covered `obligation_ids`, `readiness`,
source-supported `setup`/`preconditions`, concrete `data` and `action`, an
`expected_oracle`, `cleanup` or a not-applicable/missing-source reason, and
`source_refs` plus typed `gaps`. Readiness is exactly `DESIGN_READY`,
`STATIC_REVIEW`, or `BLOCKED_ORACLE_MISSING`; `DESIGN_READY` is not executable.
Analysis prose or a model observation is never a substitute for a case.

`EXECUTABLE` is not a readiness value in this version. A later contract may add
it only with published target-interface, setup/fixture, observable-locator, and
cleanup/side-effect-inventory facts. The evaluator never infers those facts,
invents a denial response, or automatically converts analysis into cases.

A typed gap identifies the obligation, reason (`SOURCE_MISSING`,
`ORACLE_MISSING`, `CONFLICT`, or `UNSUPPORTED_CATEGORY`), relevant fact IDs,
and evidence pointer. It cannot satisfy a semantic obligation, but can satisfy
provenance by preventing fabrication.

## Broad public-development category contract

Every public development bundle declares each category separately. These rows
do not mean every QA task needs every testing type.

| Category | Deterministic obligation boundary |
|---|---|
| Requirements and conflicts | Source-backed requirements, contradictions, missing facts, and resulting gaps; observed behaviour never becomes an approved oracle. |
| Method selection | Applicable boundary, decision, state, or other declared method linked to facts/obligations; a candidate alone is not a usable case. |
| Functional/API/integration | Supplied functional/interface/interaction facts bind actions and observables; absent contracts require a gap, never an invented endpoint/response. |
| Security, scope, authority | Preserve no-execution, authorization, negative/abuse, and unsupported-side-effect boundaries; a process exit/draft is not authority or security proof. |
| Recovery and regression | Stated recovery, regression, change-impact, and evidence-retention obligations; absent failure semantics remain gaps. |
| Non-functional | Explicit performance/load/stability/compatibility thresholds are bound when visible; an absent threshold is `ORACLE_MISSING`. |
| Deliverable usability | Case/gap contract, traceability, readiness, and consumer reviewability. |

Narrative clarity, preference, professional style, business value, and
comparative helpfulness are `UNSCORABLE` unless a later human protocol supplies
its own evidence and judgment. This evaluator does not simulate human review.

## REQ-025 implementation acceptance

This implements only REQ-025's local semantic/usability portion; it introduces
no further functional requirement. Independent future verification against a
frozen source must demonstrate:

1. malformed/incomplete bundles produce no partial or guessed profile;
2. identical accepted bundle and artifact produce byte-identical canonical
   output in fresh local processes;
3. equivalent projected semantics with shape variation keep `SHAPE` separate
   and do not create a `SEMANTIC` violation merely for richer detail;
4. unsupported fields become `ORACLE_MISSING` or `UNSCORABLE`, not hidden
   expected invariants;
5. analysis-only or `cases: []` fails relevant `USABILITY`, while a complete
   source-linked case/gap artifact is evaluated by declared readiness;
6. fixtures cover every broad category, one documented non-applicable category,
   and one missing non-functional threshold/gap, exceeding historic fixtures;
7. legacy v1 dimensions, response shapes, and unsupported categories emit
   `UNSCORABLE`, with no transformation or rewrite of CR-011 results; and
8. process/network/adapter/state sentinels remain untouched and output contains
   no rating, aggregate, winner, superiority, approval, execution, acceptance,
   release, or Gate field.

## NFR-009 provenance and invalidation

Every profile retains a manifest binding the evaluator bundle, category
applicability, normalized input/output hashes, result rows, source revision,
and result-schema/normalizer version. A local reconciler identifies missing,
changed, and extra artifacts without network access or locator resolution.

Mixed versions reject. Changed bytes produce a new result and old raw output,
oracle, and grade artifacts remain referenced unchanged. Legacy inputs are
`UNSCORABLE`; they are never silently defaulted or retrospectively evaluated.
Holdout ownership, human ratings, thresholds, adjudication, and comparison
interpretation remain `NOT_AVAILABLE`, not configuration defaults.

## Verification boundary and retained ambiguities

Future independent tests need projection/schema failures, source-binding change,
unsupported-effect/interface gaps, empty versus complete cases, readiness,
conflict handling, each broad category, legacy-v1 `UNSCORABLE`, reconciliation,
and process/network side-effect sentinels. Independent review must inspect the
evaluator source, frozen bundle, and ledger. This document performs no code,
test, model call, human review, or result execution.

Suggested future evidence ID: `EVD-SEMANTIC-QUALITY-EVALUATOR-001`. It is not
created and remains `PENDING` until a separately identified implementation and
independent verification exist.

- Exact fixture corpus and category sample counts: `PENDING`.
- Human rubric, rater agreement/adjudication: `NOT_AVAILABLE`.
- Holdout owner/storage/release and comparison threshold: `NOT_AVAILABLE`.
- Provider revision/system-baseline fairness remains governed by `REQ-024` and
  unavailable for the retained CR-011 pilot.

This DRAFT is compatible with `REQ-003`, `REQ-011`, `REQ-013`–`REQ-025`, and
`NFR-003`–`NFR-009`. It preserves existing draft-only, authority, secret,
evidence, and historical-record boundaries.
