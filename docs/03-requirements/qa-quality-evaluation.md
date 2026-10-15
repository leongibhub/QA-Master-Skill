# QA quality evaluation and workflow-use requirements

- Artifact ID: `DOC-QA-QUALITY-EVALUATION-REQ-001`
- Document State: `DRAFT`
- Evaluation State: `IN_REVIEW`
- Evidence Status: `OBSERVED`
- Change: `CR-013`
- Work: `TASK-054` / `work-67c9f0ae30514ccd9c89103dcc207ca3` v3, attempt 1
- Date: 2026-10-15

## Purpose and evidence boundary

The product goal is useful QA work and, only with adequate evidence, a future
comparison with Awesome QA Skills.  The first CR-011 public-development pilot
completed six real calls, but `DOC-PAIRED-PILOT-SEMANTIC-AUDIT-001` found that
its exact JSON grade is not a valid QA-quality measurement.  Five exact-shape
violations can retain the visible rule semantics; the grader does not inspect
empty `cases`; and one state-transition oracle demands an archive side effect
that the visible facts do not establish.  The audit is an observed input to
this prospective contract.  It does not change the retained raw run, public
oracle, exact grade, assertion statuses, or their hashes.

This document creates two **DRAFT proposal IDs**, not approved or baselined
requirements:

- `REQ-025` defines quality evidence for an actual QA product output and an
  eventual whole-product comparison.
- `NFR-009` defines provenance, evaluator determinacy, retention, and
  invalidity controls for that evidence.

The contract is deliberately broader than the three public boundary,
decision-table, and state-transition fixtures.  Those fixtures may be used as
visible development examples under a new contract; they cannot alone establish
professional QA quality, product usefulness, fairness, or superiority.

Nothing here authorizes a model call, test execution, enterprise action,
external write, release, acceptance, or automatic winner claim.  A local
offline draft is still `DRAFT_UNAPPROVED` and `NOT_EXECUTED`.

## Definitions and shared assessment contract

An **obligation ledger** is a versioned, evaluator-owned list of each fact or
rule that the visible scenario makes determinable.  Each row has a stable ID,
the visible fact reference(s), the required interpretation, the applicable
quality dimension, and exactly one result: `SATISFIED`, `VIOLATED`,
`ORACLE_MISSING`, or `UNSCORABLE`.  `ORACLE_MISSING` means the source lacks a
required expected fact.  `UNSCORABLE` means a valid evaluation rule cannot be
applied to the retained participant output or evidence.  Neither is a pass,
failure, zero, or inferred value.

A **semantic projection** is either (a) a published typed per-check schema or
(b) a published deterministic normalization from a neutral response envelope
to the fields that are compared.  It defines members, types, enum meanings,
identity and ordering, required/optional fields, and permitted extension
locations.  Transport/shape conformance is assessed separately from the
projection.  Correct extra detail outside a permitted extension location does
not make a semantic obligation violated.

A **usable case** has all of the following, each source-linked where the source
supplies it: a stable case ID; covered obligation IDs; applicability and
readiness; precondition or setup; concrete data/action; observable expected
outcome; cleanup or a declared reason it is not applicable; and typed missing
source/oracle fields.  Analysis, coverage prose, or a model observation does
not substitute for a usable case.  A case is **executable** only if the source
also supplies a target interface, setup/fixture contract, observable locator,
and any needed cleanup/side-effect inventory.  A draft or static-review case
must say why it is not executable; it must never invent an API/UI or rejection
signal.

Quality is reported as a profile, never as a hidden aggregate.  The four core
dimensions are:

1. **Response/shape conformance** — whether the neutral envelope and the
   published projection can be processed.
2. **Semantic obligation fulfillment** — whether source-determined rules,
   values, exclusions, transitions, guards, and effects are correct.
3. **Case usability and completeness** — whether each obligation has a usable
   case or an explicit typed gap, and whether the case can be reviewed or
   executed at its stated readiness.
4. **Provenance and gap honesty** — whether claims cite visible facts and
   missing/conflicting/unsupported facts remain gaps rather than assumptions.

The whole-product assessment additionally records, separately, requirement
and conflict analysis; selection and actual application of appropriate
professional methods; functional/API/negative/security/recovery/regression
coverage as applicable; integration/structural concerns as applicable;
non-functional categories with stated thresholds or a stated missing-threshold
gap; scope and no-execution discipline; and output usability for the requested
deliverable.  A task may mark a category `NOT_APPLICABLE` only with a concrete
reason.  It may mark a source-dependent category `ORACLE_MISSING` or
`UNSCORABLE`; it must not silently omit it.

## REQ-025 — prospective QA-quality contract and reachable product workflow

| Item | Requirement |
|---|---|
| Source / rationale | User goal; `REQ-005`, `REQ-011`, `REQ-013`–`REQ-018`; `DOC-COMPARISON-RESEARCH-001`; `DOC-PAIRED-PILOT-SEMANTIC-AUDIT-001` / `EVD-PAIRED-PILOT-SEMANTIC-AUDIT-001`.  The audit shows that exact JSON equality is neither semantic correctness nor usable QA delivery. |
| Priority | P1 |
| Preconditions | Before participant output is generated, an evaluator freezes the visible scenario, response-envelope version, obligation ledger, semantic projection, dimension applicability rules, and comparison profile.  A product-workflow claim also identifies the installed entry point, applicable professional guides, and the claimed deterministic design-method route. |
| Inputs | A non-secret QA request; source facts and source IDs; declared scope; target/observable facts when available; a versioned neutral envelope; evaluation profile; and, for a comparison, two content-addressed participant contexts receiving equal visible input.  A design-method invocation additionally receives the existing strict campaign/design-model input described by `REQ-013`–`REQ-018`. |
| Expected behavior / output | Produce a quality profile with one result and evidence pointer per obligation and dimension.  Produce usable draft cases for every determinable obligation, or typed gaps.  When the product claims to use bundled professional guidance or deterministic method synthesis, the installed user-facing workflow exposes the selected guide/source mapping and the resulting draft method output.  It does not relabel analysis-only output as cases, draft work as execution, or unavailable facts as expected results. |
| Normal flow | (1) Freeze the assessment inputs. (2) Derive an obligation ledger only from visible facts. (3) Process neutral participant output through the published semantic projection. (4) assess shape, semantic, usability/completeness, and provenance/gaps independently. (5) record professional-method applicability and source-to-output mapping. (6) retain a quality profile and limitations without an aggregate or winner. |
| Error / exception flow | Missing or conflicting source facts, absent target/observable facts, unsupported output, invalid projection, unbound guide/method asset, empty `cases`, or an uncovered obligation prevents the affected claim.  The result is a typed gap, `ORACLE_MISSING`, `UNSCORABLE`, or a conformance/semantic/usability violation as applicable.  It must not be repaired by guessed facts, forced JSON shape, automatic case synthesis, an inferred score, or a substitution of a different participant/model. |
| Boundary conditions | A source-provided state invariant is distinct from an unprovided side-effect invariant.  For example, a source saying an invalid archive event remains `DRAFT` cannot require unchanged persisted data without a visible fact.  Extra correct annotations may be retained outside the projection.  A complete rule analysis with `cases: []` remains analysis-only.  Existing historical run/oracle/grade records are immutable and cannot be reclassified by this requirement. |
| Dependencies / constraints | `REQ-003`, `REQ-005`, `REQ-011`, `REQ-013`–`REQ-018`, `REQ-019`–`REQ-024`, `NFR-003`, `NFR-004`, and `NFR-009`.  `REQ-013`–`REQ-018` already define the deterministic engine and offline campaign draft; they do **not** prove that the installed Codex Skill reaches them.  The first implementation must therefore make that claimed route discoverable and testable rather than merely adding a grader. |
| Measurable acceptance criteria | (1) Every evaluated check has a published projection or is `UNSCORABLE`; hidden inner-member names, enum labels, ordering, or `additionalProperties` rules cannot determine a semantic violation. (2) Every expected field maps to one or more visible source fact IDs; an unsupported field becomes `ORACLE_MISSING`/`UNSCORABLE`. (3) Every ledger obligation maps to one usable case or an explicit typed gap; an empty case collection or analysis-only observation cannot satisfy case coverage. (4) Each usable case contains the fields in the shared contract, and no case is called executable without the declared target/observable contract. (5) The evaluation suite covers more than boundary/decision/state fixtures: it includes requirements/conflict and gap handling, at least one requested functional/API or integration concern where applicable, safety/scope/no-execution behavior, recovery/regression evidence handling, and an explicitly classified non-functional request. (6) The installed QA Master workflow has a documented single offline `design --input --output` path that reuses the existing campaign draft behavior, packages the strict input reference and non-secret example, exposes selected guide/source mapping, and invokes the method route when valid `design_models` are supplied.  If no source/model is supplied it emits a gap and never marks a requirement approved. (7) A fresh isolated installed package can run that path with `python -I <skill-root>/scripts/qa.py design ...`, with no repository, `PYTHONPATH`, external package, network, adapter, state/approval mutation, or process-runner dependency. (8) Invalid input leaves a pre-existing output sentinel unchanged and all successful output remains `DRAFT_UNAPPROVED`/`NOT_EXECUTED`. (9) No criterion produces an automatic rating, aggregate, fairness, winner, or superiority conclusion. |
| Verification method | Independent tests use evaluator-owned fixtures and side-effect sentinels for the projection/ledger, source binding, unsupported-oracle, empty-case, extension-detail, readiness, and atomic-output boundaries.  An independent tester executes the isolated fresh-wheel/installed-Skill workflow and a representative offline QA task.  An independent reviewer audits the source-to-guide-to-method-output path and retained profile.  Agent review is recorded as `AGENT_REVIEW_ONLY`, not human assessment.  A later blinded human review is separately required for narrative quality and any comparison conclusion. |

## NFR-009 — deterministic evaluation provenance, retention, and invalidation

| Item | Requirement |
|---|---|
| Source / rationale | `NFR-001`, `NFR-002`, `NFR-006`–`NFR-008`; `DOC-PAIRED-EVALUATION-PLAN-001`; `DOC-PAIRED-PILOT-SEMANTIC-AUDIT-001`.  An evaluator must be able to distinguish an output defect from an ambiguous oracle, implementation drift, or an unavailable comparison condition. |
| Priority | P1 |
| Preconditions | An evaluation owner creates a new evidence root before a quality run or review.  The owner identifies whether each scenario is visible development material, independently held holdout material, or a non-comparison product test. |
| Inputs | Participant/asset/source hashes; scenario and source hashes; response-envelope/projection/ledger/rubric/normalizer/grader hashes; evaluator role and review mode; runtime/model policy and observed identity facts; raw/redacted output artifact hashes; and previous-result references where relevant. |
| Expected behavior / output | Retain a content-addressed evidence manifest that binds inputs, evaluation versions, output artifacts, every per-obligation outcome, evaluator type, limitations, and invalidation dependencies.  Preserve raw evidence and prior grades unchanged.  A changed participant, source, scenario, projection, oracle, tool policy, model/runtime fact, or assessment rule creates a new result rather than silently updating an old one. |
| Normal flow | Freeze the bundle before output generation; retain every included scenario/outcome and any excluded/failed case with its reason; report automatic checks, independent agent review, and human review in separate fields.  Development fixtures and holdouts are identified separately.  A claim has the narrowest evidence class supported by the retained bundle. |
| Error / exception flow | Missing hash, unknown evaluator/rubric/projection version, unavailable required output, mixed participant versions, changed input after freeze, inability to blind a narrative packet, or a requested human rating without completed human records invalidates the affected evaluation claim.  The system records `PENDING`, `NOT_AVAILABLE`, `NOT_EXECUTED`, or `UNSCORABLE` as appropriate; it never fills a missing datum from a prior run. |
| Boundary conditions | An agent-generated audit can find defects but is not a human rating, acceptance, or adjudication.  A deterministic checker may establish a declared projection fact but cannot judge unstated semantics.  A successful process, parsed JSON, or all-green fixture test is not a quality profile or comparison result.  Older exact grades remain historical even when a later contract exposes their limits. |
| Dependencies / constraints | Evidence is local and secret-safe under `NFR-003`; evaluation remains non-executing unless an explicitly authorized runner is used under `REQ-021` and `NFR-006`.  Holdout material, answer keys, and anonymization maps stay outside participant prompts, product tuning material, and shared source until their declared release rule. |
| Measurable acceptance criteria | (1) An independent reconciler can verify every retained artifact and all source/projection/ledger hashes from the manifest. (2) A one-byte change to any frozen participant asset, visible fact, oracle/projection, or rubric invalidates the result and requires a new run ID; prior evidence remains addressable. (3) The report identifies all scenarios considered and every excluded, failed, or unscorable case; no post-hoc subset can be presented as the whole result. (4) Development material is never reported as a holdout. (5) Automatic, agent-review, and human-review evidence classes cannot be substituted for one another. (6) A superiority statement is impossible until `REQ-011` strict-comparison preconditions, independently held representative holdout, completed blinded human ratings/adjudication, and a separate human decision are all evidenced. |
| Verification method | Independent manifest-reconciliation, mutation/invalidation, missing-field, replay, holdout-leakage, evidence-class, and historical-record-immutability tests.  An independent reviewer checks a sampled complete bundle against its ledger and raw hashes.  Human-rating/adjudication requirements remain `NOT_EXECUTED` until actual independent people complete them. |

## Phased implementation and verification plan

The phases are ordered so that the next increment fixes a real product-delivery
gap before investing in a more elaborate comparison scorer.

| Phase | Scope and measurable exit | Current evidence state |
|---|---|---|
| 1 — reachable offline QA product workflow | Architecture and implementation expose the installed Skill's single `design --input --output` path, package its strict input reference/example, preserve offline draft-only behavior, map selected professional guides and supplied sources to output, and connect valid `design_models` to the existing campaign draft engine.  Fresh isolated installation and independent representative-task testing prove this path; missing source/model remains a typed gap. | `OBSERVED`, bounded: `8b5017a` TASK057 attempt3 independently passed 8 focused and 8 fresh-wheel checks and a representative offline task; TASK058 review is `PASS WITH P3 FOLLOW-UP`. This does not baseline the DRAFT contract, prove all REQ-025 criteria, or decide a Gate. |
| 2 — semantic and usability evaluation contract | New versioned fixtures cover the four core dimensions and whole-product categories, with public development material plus independently held material.  Tests prove projection semantics, source binding, obligation-to-case/gap completeness, case readiness, and preservation of old evidence. | `OBSERVED`, partial: repaired evaluator `a9df285` has TASK062 attempt3 independent public-development evidence (30 focused and 30 fresh-wheel PASS; 689 strict `OK` with three Windows-link skips; supplemental gap regressions) and TASK063 `PASS WITH P3 FOLLOW-UP`, P0/P1/P2=0. The P3 semantic-evaluator-specific link/reparse fixture, independently held material, human assessment and whole-product comparison remain pending or not available. |
| 3 — controlled comparison and human decision | Freeze both participant contexts and a representative holdout before run; meet all strict-comparison conditions in `REQ-011`; retain repeats, blinded human reviews, disagreements, adjudication, and limitations.  A human, not a script or agent, makes any comparison decision. | `NOT_EXECUTED`.  The retained six-call run is only `EXPLORATORY_CONFIGURED_SAME_MODEL`. |

## Ambiguities and decisions still required

| Item | Status / required decision |
|---|---|
| Representative workload mix and minimum sample size | `PENDING`.  It must be selected before a comparison from the product's actual supported request classes, not inferred from three public fixtures. |
| Per-dimension acceptance threshold or any aggregate interpretation | `PENDING`.  This document intentionally defines no numerical quality threshold and no winner rule. |
| Exact installed wrapper argument grammar, output schema, and source-mapping structure | Bounded Phase 1 route is implemented and independently evidenced under `DES-055`; this DRAFT requirement remains unapproved and does not imply full Phase 1 or REQ-025 completion. |
| Holdout owner, retention location, rater qualifications, and adjudication rule | `NOT_AVAILABLE`.  These are required before a human-comparison conclusion, not guessed from local development evidence. |
| Provider-pinned revision/system-baseline evidence | `NOT_AVAILABLE` in the retained pilot.  Its absence prevents strict comparability under `REQ-024`. |

## Completeness and conflict check

`REQ-025` covers input/source grounding, semantic correctness, output shape,
case usability, executable readiness, professional QA applicability, real
installed workflow reachability, and whole-product comparison scope.
`NFR-009` covers pre-registration, evaluator determinacy, provenance,
retention, invalidation, holdout separation, and evidence-class boundaries.
Together they prevent a local engine unit test, a green JSON parser, a
single-fixture result, or a successful model process from being reported as
product quality or superiority.

The proposal does not conflict with the existing non-execution, approval,
secret, provenance, or strict-comparison requirements.  It adds no automatic
external operation and leaves CR-011 historical evidence unchanged.  Detailed
architecture, implementation tasks, independent test cases, and any human
quality decision remain future work.
