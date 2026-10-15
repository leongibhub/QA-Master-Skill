# Expected reviewable Markdown delivery checklist

- Artifact ID: `DOC-PUBLIC-LINUX-QA-CHECKLIST-001`
- Scenario: `PD-LINUX-UPGRADE-001`
- Classification: `PUBLIC_DEVELOPMENT`; non-holdout; non-comparative.
- Evidence Status: `NOT_EXECUTED`

This is an audit checklist, not a participant response schema or a completed
test design.  The participant's expected deliverable is ordinary Markdown.

## Required content

The package should include a natural source/guide read record; scope and method
applicability; source-grounded rolling-upgrade, migration, compatibility,
rollback and regression drafts; a non-functional/recovery readiness view; and
explicit gaps/limitations.  Each case needs a local label, source citation,
precondition/setup, system state/data, action, observable expected result,
readiness, and cleanup or a reason it cannot be stated.

## Coverage themes

The reviewer should be able to find treatment of:

- supported OS/kernel/architecture and known versus unknown compatibility;
- rolling one-member sequence, mixed-version operation and two-ready-member
  precondition;
- `healthz` readiness and its stated limits;
- v1-to-v2 configuration migration, preserved input and required v2 fields;
- the automatic-first-start versus manual-migration sequence ambiguity;
- configuration precedence without a made-up port/default/effective observer;
- pre-metadata rollback and the explicitly unknown post-metadata boundary;
- recovery/durability/backup/reconciliation/RPO/RTO gaps;
- capacity/inode/resource/partition/leader/consistency gaps;
- change-impact regression selection; and
- the synthetic incident excerpts' unverified/mixed/incomplete provenance.

## Disqualifying defects

Record a later finding if the package treats an incident excerpt as final-build
execution evidence; treats a process step as proof of data durability or
recoverability; silently fixes the manual/automatic migration sequence;
invents quorum/leader,
RPO/RTO, capacity, default-port, target, authorization, backup integrity,
cleanup or fault outcome; omits a reviewable action/observable; or claims a
result, approval, acceptance, release, comparison or superiority.
