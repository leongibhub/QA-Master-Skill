# Public-development API QA task evaluation plan

- Artifact ID: `DOC-PUBLIC-API-QA-PLAN-001`
- Work: `TASK-065` / `work-ca9683f4130e4f7c830311429bed3a79`, attempt 1
- Related requirements: DRAFT `REQ-025`, `NFR-009`; informs but does not
  complete `REQ-011`.
- Document State: `DRAFT`
- Evaluation State: `IN_REVIEW`
- Evidence Status: `OBSERVED` (TASK-066 participant output, TASK-069 fixture
  audit/reconciliation and TASK-067 practical review executed and retained; see
  "Completion status" below — no quality, comparison or acceptance conclusion)
- Date: 2026-10-15

## Completion status (added by TASK-074 linkage)

The planned trial chain has executed in the registered bounded scope.  The
freeze was delivered by TASK-065 (commit `962637b`); the participant trial by
TASK-066 (output retained at `52bff03`); the independent reconciliation and
coverage audit by TASK-069; and the practical review by TASK-067 with an
`AGENT_REVIEW_ONLY` conclusion of
`REVIEWABLE_SOURCE_GROUNDED_DRAFT_WITH_EXPLICIT_GAPS`, P0/P1/P2/P3=0.  The
originally suggested evidence IDs were issued with bounded statuses only:
`EVD-PUBLIC-API-QA-PARTICIPANT-001` (OBSERVED, participant output),
`EVD-PUBLIC-API-QA-RECONCILIATION-001` and `EVD-PUBLIC-API-QA-COVERAGE-001`
(OBSERVED, TASK-069 independent reconciliation/coverage) and
`EVD-PUBLIC-API-QA-PRACTICAL-REVIEW-001` (VERIFIED, TASK-067 review delivery
linkage), plus the freeze/participant delivery records.  These
are bounded observations only: they are not a quality PASS, score, comparison,
execution, holdout/human assessment, Gate, acceptance or release result.

## Purpose and boundary

This plan evaluates a real use of the installed QA Master Skill on an ordinary
requirements document and an ordinary OpenAPI document.  It tests whether the
Skill, with a participant actually applying the installed guidance, can create
a useful, source-grounded *draft* API QA design.  It does not assume that a
deterministic generator is necessary or sufficient for that work.

The scenario is `PUBLIC_DEVELOPMENT`, not a holdout.  It is not a model
comparison, benchmark score, human quality assessment, requirement approval,
executed test, enterprise integration, release or Gate decision.  No
participant call is made by this planning work.

## Frozen input set

The proposed trial reads exactly these paths:

| Path | Role | Participant read access |
|---|---|---|
| `benchmarks/public-development/PD-API-COLLAB-001/requirements.md` | Ordinary change-request source | Allowed |
| `benchmarks/public-development/PD-API-COLLAB-001/openapi.yaml` | Ordinary API interface source | Allowed |
| `benchmarks/public-development/PD-API-COLLAB-001/participant-task.md` | Plain-language task instruction | Allowed |
| Installed QA Master Skill root selected by the later runner | Product subject, guides and references | Allowed, exact manifest/hash retained |
| `benchmarks/public-development/PD-API-COLLAB-001/audit-ledger.md` | Evaluator audit aid | Not allowed during participant work |
| `benchmarks/public-development/PD-API-COLLAB-001/expected-review-checklist.md` | Independent audit aid | Not allowed during participant work |

The audit documents do not make this a holdout: the source scenario remains
public development material and the audit aids are released after the trial.
They are withheld from the participant only to avoid giving a ready-made
coverage answer to the task under review.

Before a trial begins, the execution owner must record the SHA-256 and byte
count of each source document, task instruction, installed Skill manifest and
every installed Skill file actually read.  A changed byte requires a new
scenario revision; it may not be mixed into a trial already in progress.

## Participant procedure

The later participant receives the plain Markdown instruction and the two
ordinary sources, then works from the installed QA Master Skill.  It may select
and apply guides and may use the installed offline design helper when useful.
It must not be asked to submit a special contract DSL, a fixed JSON response
shape, or fixed source-fact IDs.

The deliverable is ordinary Markdown under a predeclared trial output root.
It includes natural source citations, a source/guide read audit, scope and
method discussion, reviewable draft cases, explicit gaps and a no-execution
limitation.  The output must use no credentials and cannot access a service or
make a product change.  Its content remains `DRAFT_UNAPPROVED` and
`NOT_EXECUTED`.

## Pre-registered assessment approach

An independent tester first checks the evidence boundary and source coverage
using the separate audit ledger and checklist.  The tester does not grade prose
or calculate a quality score.  It records whether each source fact or source
absence is represented by a natural citation to a case, a gap, a conflict, or
a justified scope decision; it records missing/unsupported links as findings.

An independent reviewer then assesses source-to-case/gap traceability and
practical usability.  A usable draft case tells a later tester what must be
true first, which data/action is proposed, what observable is expected, what
is missing, and why it is not executable if target details are absent.  The
reviewer must preserve uncertainty rather than rewarding elaborate but
unsupported prose.  This is `AGENT_REVIEW_ONLY`, not a human rating.

Neither review may infer an API pass/failure, product bug, security weakness,
enterprise compatibility, performance value, user approval, score, aggregate,
winner, or comparison conclusion.

## Completeness and negative checks

The later independent assessment must check all of the following:

1. The participant used only allowed paths; the audit ledger/checklist and any
   private comparator/holdout paths were unread.
2. Source hashes and installed-Skill hashes are retained, and participant
   source citations resolve to the two supplied documents.
3. The role/tenant, schema/boundary, state/version, optimistic-concurrency,
   idempotency and request-ID facts receive source-grounded case or gap
   treatment.
4. The `403` versus `404` cross-tenant contradiction is explicit and no fixed
   outcome is guessed.
5. Missing cleanup, target, error-body, timeout/retry, SLO/rate, client
   support, delivery/recovery and regression-baseline facts remain explicit
   gaps or deferrals rather than invented assertions.
6. Each proposed case is reviewable: it names an action, observable expected
   result, setup/precondition, data, readiness and cleanup or an honest reason
   that cleanup cannot be stated.
7. The output preserves draft/no-execution wording and makes no approval,
   rating, security, result, release, comparison or superiority claim.

The assessment may identify a concrete product defect only where the installed
workflow or guidance causes a reproducible, source-grounded failure.  Examples
could be failure to expose a source conflict, systematic omission of a required
case field, or substitution of helper candidates for usable cases.  A generic
claim that a new API generator would be helpful is not a defect finding.

## Decision after observation

After independent testing and review, route each observed issue to the smallest
supported remedy:

| Observation | Candidate next work, subject to requirements/design |
|---|---|
| Relevant guide was not discoverable or did not prompt a necessary fact/gap | Guide, routing, or output-template repair |
| Skill cannot keep a source citation through its user-facing workflow | Traceability/UI contract repair |
| Repeated, well-specified API patterns cannot be represented without loss | Evaluate a deterministic helper or generator proposal |
| Source lacks a target, cleanup, SLO, recovery or policy fact | Record a source gap; do not change product to guess it |

No remedy is selected by this plan.  The trial evidence determines whether a
product implementation task is justified.

## Remaining dependencies

1. Governance must bind the final source/task/plan hashes to TASK-065 and
   establish a later participant work record.
2. A runner must install and freeze the exact QA Master Skill subject and
   define a disposable output root with an allowed-path audit.
3. A separate participant may perform the later task only after that work is
   registered; this plan performs no participant call.
4. Independent tester and reviewer work must be separately registered and
   receive the frozen subject plus the audit aids after participant output is
   frozen.
5. Any eventual model/comparator claim still requires the independent
   provider/holdout/human controls in `REQ-011`; TASK-065 does not supply them.

## Proposed evidence identifiers

The planning and source artifacts use `DOC-PUBLIC-API-QA-PLAN-001`,
`DOC-PUBLIC-API-QA-FACTS-001`, and `DOC-PUBLIC-API-QA-CHECKLIST-001`.
Suggested future, unissued identifiers were
`EVD-PUBLIC-API-QA-PARTICIPANT-001`, `EVD-PUBLIC-API-QA-TEST-001`, and
`EVD-PUBLIC-API-QA-REVIEW-001`.  They were later issued or superseded by the
executed trial chain with bounded statuses only (see "Completion status"
above); `EVD-PUBLIC-API-QA-TEST-001` was not carried as a separate ID, and the
independent work registered its own reconciliation/coverage/review records.
No quality, comparison or acceptance conclusion follows from their issuance.
