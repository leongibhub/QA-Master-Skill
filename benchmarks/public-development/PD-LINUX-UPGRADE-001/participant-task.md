# Draft Linux upgrade QA design task

Classification: `PUBLIC_DEVELOPMENT`; `DRAFT_UNAPPROVED`; `NOT_EXECUTED`.

Read only these ordinary source documents before responding:

1. `release-notes.md`
2. `upgrade-runbook.md`
3. `support-and-config.md`
4. `incident-excerpts.md`

Using the installed QA Master Skill and the applicable installed guidance,
prepare a reviewable Markdown QA design package for this proposed DocSync
Server rolling upgrade.  Include natural source citations, source/evidence
limits, method applicability, draft cases, an upgrade/rollback readiness view,
regression impact, and explicit gaps.  A table is welcome, but do not use or
request a special participant DSL, a fixed JSON response shape, or supplied
fact identifiers.

Make each draft case reviewable: state its precondition or setup, selected
system state/data, proposed action, observable expected result, readiness,
cleanup or a reason it cannot be stated, and natural source citation.  Keep a
conflict as a conflict.  Identify contradictions, missing facts and evidence
limits from the supplied sources without inventing results.  Treat the incident
excerpts according to their declared provenance.

Do not contact a host or service; run SSH, systemctl, package, migration,
backup, restore, traffic, network, disk, or fault command; use credentials;
or claim an upgrade, recovery, defect, security finding, approval, result,
acceptance, release, comparison, or superiority conclusion.  This is offline
design only.  If an installed offline helper is useful for a limited finite
subproblem, its output is a draft input to your review, not an executable test
or a completed rollback plan.
