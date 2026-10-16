# Public-development Linux upgrade QA task evaluation plan

- Artifact ID: `DOC-PUBLIC-LINUX-QA-PLAN-001`
- Work: `TASK-070` / `work-6f1d9d2a59334e45bccea60d33540083`, attempt 1
- Related requirements: DRAFT `REQ-025`, `NFR-009`; supports local evidence
  for `REQ-005`, `REQ-009`, `NFR-001` and `NFR-004` without completing them.
- Document State: `DRAFT`
- Evaluation State: `IN_REVIEW`
- Evidence Status: `OBSERVED` (TASK-071 participant output, TASK-072 coverage audit
  and TASK-073 practical review executed and retained; see "Completion status"
  below — no quality, comparison or acceptance conclusion)
- Date: 2026-10-15

## Completion status (added by TASK-074 linkage)

The planned trial chain has executed in the registered bounded scope.  The
freeze was delivered by TASK-070 (commit `2f9ec205`); the participant trial by
TASK-071 (output retained at `c3a52ff`, manifest provenance corrected at
`cd4a7d9` with participant bytes unchanged); the independent coverage audit by
TASK-072 (`16555fd`); and the practical review by TASK-073 (`6bd7eeb`) with an
`AGENT_REVIEW_ONLY` conclusion of
`REVIEWABLE_SOURCE_GROUNDED_DRAFT_WITH_EXPLICIT_GAPS`, P0/P1/P2/P3=0.  The
originally suggested evidence IDs were issued as
`EVD-PUBLIC-LINUX-QA-PARTICIPANT-001` (OBSERVED),
`EVD-PUBLIC-LINUX-QA-TEST-001` (OBSERVED) and
`EVD-PUBLIC-LINUX-QA-REVIEW-001` (VERIFIED, delivery linkage only), plus the
free delivery/correction records.  These are bounded observations only: they
are not a quality PASS, score, comparison, execution, holdout/human assessment,
Gate, acceptance or release result.

## Purpose and boundary

This plans one actual, offline use of the installed QA Master Skill on ordinary
release, runbook, support/configuration and incident-excerpt documents.  It
checks whether the Skill can produce a useful source-grounded draft for Linux
rolling upgrade, migration, rollback and regression evidence—not whether a
generator exists or whether a real service works.

The scenario is `PUBLIC_DEVELOPMENT`, not a holdout or model comparison.  It
does not authorize an SSH/service/package/configuration/backup/restore/network
or fault operation.  It makes no participant call, quality score, acceptance,
Gate, release, or superiority conclusion.

## Frozen input and allowed paths

The later participant may read exactly these four ordinary sources and the
plain task:

- `release-notes.md`
- `upgrade-runbook.md`
- `support-and-config.md`
- `incident-excerpts.md`
- `participant-task.md`

The exact installed QA Master Skill selected by the later runner is also
allowed; its manifest and every guide/reference actually read must be retained.
`audit-ledger.md`, `expected-review-checklist.md`, this plan, the source-freeze
record, comparator material and any private holdout are excluded until the
participant output freezes.  The audit aids are not a holdout; they are later
released public-development evaluation material withheld only to avoid a
ready-made answer sheet.

Before a later task begins, record SHA-256 and byte count for every listed
source/prompt, plus the installed Skill manifest/read files.  Any changed byte
is a new scenario revision and cannot be combined with an earlier output.

## Participant delivery

The participant produces ordinary Markdown in a predeclared output root.  It
records source and guide reads with natural citations, scope/method selection,
reviewable draft cases, an upgrade/rollback readiness view, regression impact,
and gaps.  It must not be given a special DSL, fixed JSON schema, fact IDs, or
the audit answer aids.  A finite installed helper is optional for a narrow
subproblem; its candidates cannot stand in for usable Linux QA cases.

All delivery content is `DRAFT_UNAPPROVED` and `NOT_EXECUTED`.  A case is
reviewable only when it includes setup/precondition, state/data, proposed
action, observable expected result, readiness, cleanup-or-reason and natural
source citation.  Missing operator authority, target, side-effect observer or
recovery oracle remains a gap.

## Independent assessment after freeze

An independent tester uses the audit ledger and checklist after the participant
output freezes.  The tester traces each source fact, conflict and absence to a
draft case, gap, conflict or justified scope decision.  It checks that mixed or
unidentified incident material is not relabeled as final-build test evidence.

An independent reviewer assesses practical usability: could a later Linux/SRE
tester use the package to obtain the next needed source, target or approval
without guessing an upgrade command or oracle?  The reviewer verifies that
process completion, ready health, configuration migration, data durability,
rollback recovery and regression evidence remain distinct claims.  This is
`AGENT_REVIEW_ONLY`, not human assessment or scoring.

## Pre-registered checks

1. All source facts/absences map by natural citation to a case, gap, conflict,
   or justified scope decision.
2. Supported platform/mixed-version conditions, rolling sequence, ready
   observable, configuration migration/precedence, rollback boundary and
   compatibility have source-grounded treatment.
3. The manual migration versus automatic-first-start sequence ambiguity remains
   visible; the output asks whether the manual operation is required, redundant
   or idempotent instead of assuming a sequence.
4. Unknown leader/quorum observer, partition/consistency, capacity/inodes,
   RPO/RTO, backup integrity/reconciliation, target/account/authorization,
   effective config and post-migration rollback facts remain explicit gaps.
5. A regression-impact map distinguishes affected upgrade/config/client paths
   from an actual regression result, and labels incident excerpts according to
   their synthetic, mixed-build or unverified provenance.
6. No document output claims a host/service observation, durability proof,
   recovery success, test outcome, defect, approval, acceptance, release,
   comparison or superiority.

## Dependencies and later work

The governance owner must bind final hashes to TASK-070 and register a separate
participant task.  Only after participant output is frozen may separately
registered independent testing and review receive the audit aids.  Future
TASK-071 through TASK-073 may carry participant, testing and review work, but
are planned only by this document and are neither created nor executed here.

Suggested future, unissued evidence IDs were `EVD-PUBLIC-LINUX-QA-PARTICIPANT-001`,
`EVD-PUBLIC-LINUX-QA-TEST-001`, and `EVD-PUBLIC-LINUX-QA-REVIEW-001`.  They
were later issued by the executed trial chain with bounded statuses only
(OBSERVED for participant/test, VERIFIED for review delivery linkage); see
"Completion status" above.  No quality, comparison or acceptance conclusion
follows from their issuance.
