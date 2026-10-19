# Evaluator-held holdout register and release-after-freeze procedure

- Artifact ID: `DOC-HOLDOUT-REGISTER-PROCEDURE-001`
- Proposed evidence ID: `EVD-HOLDOUT-REGISTER-PROCEDURE-001`
- Change: `CR-014`
- Work: `TASK-075` / `work-60ab5357d90949658fec32b90ceb85b6`, attempt 1
- Related requirements: `REQ-011`, DRAFT `REQ-025`/`NFR-009` (readiness only;
  completes none of them)
- Document State: `DRAFT`
- Evaluation State: `IN_REVIEW`
- Evidence Status: `PENDING`
- Date: 2026-10-16
- Classification: `PUBLIC_DEVELOPMENT` planning document. No holdout material
  has been created, moved, hashed, released or exposed by this document.

## Purpose and boundary

`REQ-011` requires that any superiority claim over the upstream skill library rests on a
same-model, same-input evaluation with a fixed scoring protocol, expert ratings
and preserved artifacts.  Phase 3 of the quality contract
(`DOC-QA-QUALITY-EVALUATION-REQ-001`) additionally requires an independently
held representative holdout before a controlled comparison run, and states that
a human, not a script or agent, makes any comparison decision.

The paired evaluation plan (`DOC-PAIRED-EVALUATION-PLAN-001`, recommendation 6)
calls for "an evaluator-held holdout register with a public commitment hash and
release-after-freeze procedure, but no answer keys in the shared repository".
The semantic-quality design (`DES-060` §12/§13) requires that holdout material
"stays in a separately governed location" and that the evaluator "reports this
declared class and never promotes development data to a holdout".  No such
procedure document exists yet.

This document defines that procedure.  It is a governance procedure for a
future evaluation owner.  It creates no holdout, performs no run, invokes no
model, records no rating, and supports no comparison, Gate, acceptance or
release decision.

## Owner identity and independence boundaries

1. The evaluation owner must be a registered Runtime identity whose role is not
   `developer` and who did not implement, test or review the product subjects
   being compared.  In Runtime terms the owner registers as a distinct agent
   identity (for example a future `/root/evaluation_owner`), distinct from
   `/root/qa_linux_trial`, `/root/design_acceptance`, `/root/workflow_review`
   and all developer identities.
2. The owner must not have authored or tuned participant prompts, templates,
   fixtures, grading code or answer material for either arm.
3. The owner must hold holdout material outside the product repository, outside
   any participant workspace, outside any arm root, and outside any directory
   exposed to an agent during a run.  Recommended location shape:
   a dedicated directory on the evaluation host outside all working trees
   (for example `<drive>:\qa-holdout\CR-014\`), with access limited to the
   owner identity.
4. The owner must not be the person who later performs the blinded human
   rating, and must not disclose holdout content to raters until after freeze.

## Holdout classes and what may be registered

Only material whose judging approach is already declared by
`DOC-PAIRED-EVALUATION-PLAN-001` §"Scenario policy" may be registered:

| Class | Content boundary | Judging approach |
|---|---|---|
| Method holdout set | Different values, rule shapes, conflict patterns, transition graphs and missing-input cases from the declared input grammar. No reuse of any visible development fixture values. | Versioned script checks held with the owner. |
| Narrative holdout set | Realistic but de-identified QA planning, evidence, scope, reporting and routing problems, including incomplete and adversarially ambiguous inputs. No real customer or private data. | Blind human review using a pre-registered rubric. |

Prohibited registrations: any scenario already used as visible development
material (the twelve `benchmarks/scenarios.json` scenarios, the three
`PE-*` public-development fixtures, and the `PD-API-COLLAB-001` /
`PD-LINUX-UPGRADE-001` public trials); any expected answer, oracle value,
rating rubric detail or grading code placed in the shared repository; any
material copied from either participant's assets.

## Registration record (repository-visible, content-free)

The owner publishes, in this repository, one content-free commitment record per
holdout set.  The record contains **no holdout content, no answer key, no
expected value and no rating**.  Required fields:

| Field | Content |
|---|---|
| `holdout_set_id` | Stable ID, e.g. `HOLDOUT-METHOD-001`. |
| `class` | `METHOD_HOLDOUT` or `NARRATIVE_HOLDOUT`. |
| `declared_input_grammar` | Reference to the grammar declaration the items follow (e.g. the DES-040 scenario object for method items). |
| `item_count` | Whole number of holdout items. |
| `item_sha256_list_commitment` | SHA-256 over the canonical concatenation of per-item SHA-256 values, in a stable order. A per-item list of hashes is acceptable only if the items themselves remain unreleased; the concatenation commitment is always required. |
| `created_at_utc` | RFC 3339 UTC, whole seconds, literal `Z`. |
| `owner_agent_id` | Registered Runtime identity of the evaluation owner. |
| `freeze_criteria_ref` | Pointer to the freeze criteria this set waits on (see below). |
| `release_policy` | `RELEASE_AFTER_FREEZE_ONLY`. |

The record's own SHA-256 is registered in Runtime as DRAFT planning evidence.
The record is intentionally inspectable: a reviewer can confirm the commitment
hash exists and matches nothing in the shared repository, without learning any
item content.

## Freeze criteria

A holdout set is frozen (and only then releasable to the evaluation run
pipeline) when **all** of the following are DONE in Runtime and recorded:

1. Both participant subjects for the intended comparison are frozen at pinned
   commits with all visible asset hashes recorded (materialization verified).
2. The provider-pinned exact model revision and system baseline are attested,
   or the run is explicitly labeled `EXPLORATORY_CONFIGURED_SAME_MODEL` and
   cannot support strict comparison anyway (in which case holdout release is
   pointless and must not occur — see "Release gating" below).
3. All development-set-visible participant work that could have tuned toward
   the holdout grammar is complete and registered.

Until all criteria are DONE, the holdout set status is `PENDING_FREEZE`.

## Release-after-freeze procedure

1. The owner verifies the freeze criteria against Runtime records, and records
   the verification as evidence with locator pointing at this procedure and the
   Runtime work/artifact IDs that constitute the freeze.
2. Only for a strict-comparison-eligible run (profile
   `STRICT_COMPARISON_CANDIDATE` under DES-040, or its successor contract): the
   owner releases the holdout items **only** to the evaluation run pipeline's
   evaluator-only locations (outside both arm roots and outside any manifest
   directory), never into participant-visible material, prompts, response
   contracts or ledgers.
3. For an exploratory run the holdout must NOT be released; exploratory runs
   use only visible development material.  Releasing a holdout into an
   exploratory run consumes it irrevocably and is prohibited.
4. After the run bundle (outputs, traces, ratings, adjudication, limitations)
   is retained, the owner may publish the holdout items themselves with their
   per-item hashes, so the public commitment becomes verifiable end-to-end.
5. A holdout set may be released at most once.  Any post-release change
   requires a new holdout set ID and a new commitment.

## Leakage prohibitions

1. No holdout item, answer key, expected value, rating, rubric detail or
   grading code may enter: the product repository, any participant workspace,
   any arm root, any prompt or response contract, any manifest directory, or
   any agent-visible directory during a run.
2. The owner's commitment record contains only the fields listed above; it is
   content-free by construction.
3. Development material may never be reported or registered as holdout
   (`DES-060`: the evaluator reports the declared class and never promotes
   development data to a holdout).
4. The DES-040 evaluator-exclusion registry (`forbidden_locators`,
   `forbidden_sha256`, `fixture_markers`) is the run-time enforcement point:
   before any strict run, the owner's holdout per-item hashes and locators are
   added to that registry so the preflight can detect accidental copying into
   arm roots, prompts or response contracts.
5. If any leakage is detected or suspected, the affected holdout set is
   invalidated: its status becomes `INVALIDATED_BY_LEAKAGE`, a new set must be
   created under a new ID, and the event is recorded in Runtime evidence.

## Evidence-class boundaries

- This procedure and any commitment records are DRAFT planning evidence for
  `REQ-011`/Phase 3 **readiness only**.  They do not complete REQ-011, do not
  create comparison evidence, and do not alter any Gate status.
- A registered, unreleased holdout set does not make any past or future
  exploratory run strictly comparable.
- No human rating, adjudication, aggregate score, winner or superiority
  statement may be derived from the existence of this procedure or any
  commitment record.
- Holdout release without an eligible strict run, or any attempt to release
  into an exploratory run, is a procedure violation to be recorded as a defect
  candidate in the gap register.

## Open items for the eventual strict evaluation owner

1. Representative workload mix and minimum sample size remain `PENDING` per
   `DOC-QA-QUALITY-EVALUATION-REQ-001`; the holdout item count must be chosen
   only after that decision.
2. Rater qualifications, rubric ownership and adjudication rules remain
   `NOT_AVAILABLE` until humans are named.
3. The strict-profile provider attestation path (DES-040
   `STRICT_PROFILE_NOT_SUPPORTED` unless a trusted verifier validates provider
   revision and system baseline) has no implementation yet; until it exists,
   no strict run and therefore no holdout release can occur.

## Current conclusion

`NOT_EXECUTED`.  This procedure defines how a future evaluation owner creates,
registers, freezes and releases evaluator-held holdout material.  No holdout
exists, no commitment record has been issued, no run is authorized by this
document, and no comparison, Gate, acceptance or release decision follows.
