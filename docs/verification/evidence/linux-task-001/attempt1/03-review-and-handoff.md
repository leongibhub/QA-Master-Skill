# 03 — Self-review and handoff

Classification: `PUBLIC_DEVELOPMENT`; `DRAFT_UNAPPROVED`; `NOT_EXECUTED`.

Self-review of the draft package (`01-review-and-strategy.md`,
`02-draft-cases.md`, this file) against the participant task and the installed
QA Master Skill guidance (`SKILL.md`, `references/work-protocol.md`,
`references/domains.md`, and the professional guides). This review critiques
the draft; it does not approve it.

---

## 1. Interpretation limits

1. **All four technical sources are unapproved scenario material.** Every input
   declares itself `PUBLIC_DEVELOPMENT` and `NOT_EXECUTED`; the runbook is
   `DRAFT_UNAPPROVED`; the incident excerpts are `SYNTHETIC_SCENARIO_MATERIAL`
   and `NOT_OPERATIONAL_EVIDENCE`. Nothing in this package rests on a deployed
   system, a pinned build, executed tests, or an approved baseline. Every
   "candidate fact" in `01` §2 is a candidate for human review, not a
   requirement.
2. **No owner, date, or approval status was supplied for any document.** The
   conflict register cannot be prioritized by document authority because no
   document claims precedence; both sides of the migration-trigger conflict
   (G-01) were therefore drafted as equal-status variants (TC-LU-006 vs
   TC-LU-009).
3. **The only service observable is `GET /healthz`.** Every case's expected
   result is ultimately anchored to the readiness contract (HTTP 200 +
   `ready: true`, support-and-config › "Observable service data"). Cases whose
   subject is not readiness (migration boundary, rejection behavior, effective
   port, client operations) have their observables marked pending rather than
   inferred from plausibility.
4. **Deliberate non-inventions.** No quorum query, leader-election oracle,
   RPO/RTO number, default port, capacity threshold, fault outcome, CLI
   command, error code, or synthetic config/port/document value was invented.
   Where a setup needed such a value, the case references the member's
   *recorded* data (per upgrade-runbook step 1) and records the placeholder as
   a gap (G-22). TC-LU-011's post-rollback `/healthz` check is labeled a
   *candidate* observable for review precisely because the runbook states no
   post-rollback oracle exists.
5. **`/healthz` on which port?** A subtle circularity is preserved rather than
   resolved: readiness is checked via `/healthz`, but no default port or
   effective-config inspection method exists (G-09), and TC-LU-010 tests port
   precedence itself. The package flags this; it does not paper over it.
6. **Incident excerpts are quarantined.** TC-LU-015 uses them only as scenario
   motivation, states no expected result from them, and excludes them from any
   final-build evidence base (G-18); `build=2.4.0-rc2` is noted as unmappable
   to any supported build (G-19).
7. **Method table honesty.** Performance/load/stress/stability are marked not
   applicable with the missing-input reason (no thresholds, workload,
   duration, monitoring, or authorization), per `nonfunctional-compatibility.md`
   ("Do not translate 'fast', 'many users' or 'all browsers' into numbers") and
   the sources' explicit absence statements (RN-11, SC-03).

## 2. Self-identified weaknesses of the draft

- TC-LU-002's expected result depends on "out of service / return to service",
  which no source defines; the case is kept but its service-state transitions
  are conditional (G-08). A reviewer may reasonably ask whether the case
  should be split once a drain mechanism is defined.
- TC-LU-008's "acceptance" observable collapses to readiness; whether
  `metrics.enabled` has any observable effect is genuinely unknown (no metrics
  endpoint documented, SC-12), so the case may be weaker than it appears.
- The regression impact map (§3 of `02`) cannot be evidence-backed because no
  pinned before/after revisions exist (G-20); it is a stated-reason selection
  only.
- Case priority was not assigned: the sources give no risk ranking and the
   work-protocol advises priority with reason; assigning P0–P3 without a risk
   basis would be invention, so all cases remain unprioritized pending human
   review.
- Cleanup statements are mostly "none stated"; this is accurate to the sources
  (no revert/reset procedures exist beyond the pre-metadata rollback) but
  leaves a future execution packet under-specified.

## 3. Pending decisions (for a human reviewer / source owner)

| # | Decision needed | Why it is open | Affected artifacts |
|---|---|---|---|
| D-01 | Resolve the migration-trigger conflict: is `data/config-v2.yaml` created automatically at first 2.4.0 start (release-notes) or must `docsync config-migrate` run first (upgrade-runbook), or both in some order? | `SOURCE_CONFLICT` G-01; both documents describe mandatory sequences for the same artifact | TC-LU-006, TC-LU-009; readiness view row "Config migration trigger" |
| D-02 | Define an observable for "membership metadata migrated" (the rollback boundary) | `ORACLE_MISSING` G-02 | TC-LU-011, TC-LU-012 |
| D-03 | Define rejection observables for invalid v2 configs (log/error code/service state/prior-config usability) | `ORACLE_MISSING` G-03 | TC-LU-007 |
| D-04 | Approve (or supply) a post-rollback health/reconciliation oracle and RPO/RTO | `RECOVERY_OBJECTIVE_UNCONFIRMED` G-04/G-05; sources explicitly lack them | TC-LU-011; readiness view |
| D-05 | Define the mechanism for "two other voting members ready" (command/quorum query) and "out of/return to service" | `ORACLE_MISSING` G-08 | TC-LU-002, TC-LU-004 |
| D-06 | Define effective-config observation, env supply mechanism, and whether a default port exists | `ORACLE_MISSING` G-09 / `POLICY_UNCONFIRMED` G-10 | TC-LU-010 |
| D-07 | Supply a CLI command/output contract for client compatibility checks | `CONTRACT_MISSING` G-13 | TC-LU-013 |
| D-08 | Decide whether security-adjacent checks (file ownership, permissions, SELinux) are in scope, and supply policy | `SECURITY_POLICY_UNCONFIRMED` G-16 | blocked security family |
| D-09 | Decide the treatment of partial migration and concurrent-operator migration (accept risk, define locking, or declare out of scope) | `ORACLE_MISSING` G-11 / `CONCURRENCY_POLICY_MISSING` G-17 | TC-LU-016, TC-LU-017 |
| D-10 | Approve a bounded case baseline (scope + version) for this draft set, or restate/reject individual candidates | no human baseline exists yet | entire package |

## 4. Next actions for a future engineer

1. Read `handoff.json` and verify the source and artifact hashes against
   actual bytes before reusing anything (per work-protocol.md). If a source
   file changed, re-extract the affected candidate facts and invalidate
   dependent cases; do not relabel old drafts against changed sources.
2. Seek decisions D-01 through D-10 from the document owners or a human
   reviewer. D-01 (migration trigger) is the highest-leverage decision: it
   determines whether TC-LU-006 or TC-LU-009 (or a merged sequence) becomes
   the baseline case.
3. If the deterministic offline helper is desired for a limited finite
   subproblem, model the member upgrade lifecycle as a state-transition bundle
   per `references/design-methods.md` and run
   `python -I "<skill>/scripts/qa.py" design --input bundle.json --output report.json`.
   Treat its `method_design`/`installed_design` output as a draft planning
   input only: complete its candidates into usable cases or typed gaps by
   hand, exactly as done here; never present it as approval or execution.
4. When (and only when) an authorized target, environment, build identity, and
   operator authorization exist: convert the DRAFT cases into an execution
   packet with concrete commands, data, and abort conditions; execution
   requires a new bounded activity and its own authorization (work-protocol.md).
5. Keep the incident excerpts out of any evidence report regardless of later
   build availability; they are synthetic by declaration (G-18).

## 5. Deliverable boundaries — complete vs incomplete

**Complete (to draft standard, for review):**
- Source notation and evidence-status table for all five inputs.
- 43 atomic candidate facts/rules with natural citations (22 FACT, 14 ABSENCE,
  3 SYNTHETIC, 4 consistency/provenance notes — counts approximate for review
  convenience only).
- Typed conflicts-and-gaps register: 22 entries covering SOURCE_CONFLICT,
  ORACLE_MISSING, RECOVERY_OBJECTIVE_UNCONFIRMED, PROCEDURE_UNDEFINED,
  AUTHORIZATION_MISSING, POLICY_UNCONFIRMED, CONTRACT_MISSING,
  THRESHOLD_UNCONFIRMED, BEHAVIOR_UNSPECIFIED, SECURITY_POLICY_UNCONFIRMED,
  CONCURRENCY_POLICY_MISSING, EVIDENCE_UNVERIFIED,
  VERSION_PROVENANCE_UNCONFIRMED, ENVIRONMENT_UNIDENTIFIED,
  TEST_DATA_MISSING.
- Method applicability table for 13 methods with source-grounded reasons.
- 15 draft case-family entries (TC-LU-001…TC-LU-015) plus 3 blocked gaps
  recorded as gaps (TC-LU-012, TC-LU-016, TC-LU-017) and 1 exploratory draft
  with an open expected result (TC-LU-018) — each with citation, setup, state,
  action, expected result, readiness, and cleanup-or-reason.
- Upgrade/rollback readiness view (design-stage, documentation-level only).
- Regression impact map with stated reasons and explicit not-selected areas.
- Read audit and machine-readable handoff.

**Incomplete / blocked (by design, with typed gaps):**
- Any executable test, command, or procedure (no authorization, target,
  environment, or build — G-07, G-20).
- Migration-trigger resolution (G-01) and any case that depends on it being
  baselined.
- Post-metadata rollback design (G-06), partial migration (G-11), concurrent
  migration (G-17).
- Rejection observables (G-03), effective-config observation (G-09),
  cluster-level readiness (G-08), client operations contract (G-13).
- Any performance/load/stress/stability target (G-14) and any security finding
  or security case (G-07, G-16).
- Case priorities, approvals, and the human baseline decision (D-10).
- Any evidence report: no execution occurred; result state is `NOT_EXECUTED`
  throughout.

**Claims deliberately not made:** no upgrade, recovery, defect, security
finding, approval, result, acceptance, release, comparison, or superiority
conclusion; no quality-pass or completion claim beyond "draft produced for
review".
