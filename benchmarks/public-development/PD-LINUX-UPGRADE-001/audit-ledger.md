# Evaluator audit ledger: Linux rolling-upgrade scenario

- Artifact ID: `DOC-PUBLIC-LINUX-QA-FACTS-001`
- Scenario: `PD-LINUX-UPGRADE-001`
- Classification: `PUBLIC_DEVELOPMENT`; non-holdout; non-comparative.
- Evidence Status: `PENDING`

This is an independent audit aid, not a required participant structure or
answer sheet.  It is withheld from a later participant only until that output
is frozen.  The source documents remain public-development material.

| Source location | Visible fact, conflict, or absence | Audit expectation |
|---|---|---|
| release-notes / Change scope | Schema v1 to v2 affects service, local config and membership metadata. | Address configuration, persistent data and cluster impact. |
| release-notes / supported path and support reference table | Only two named OS/kernel/x86_64 combinations are supported. | Compatibility coverage names supported and unsupported/unknown combinations without inventing support. |
| release-notes / supported path | One upgraded plus two 2.3.6 members communicate during rolling upgrade. | Model mixed-version compatibility and one-member-at-a-time sequence. |
| release-notes / supported path | Two voting members remain ready. | Use as a preflight/readiness condition; do not invent quorum query or leader semantics. |
| release-notes / health plus support observable data | Ready is `/healthz` HTTP 200 with `ready:true`. | Name exact available observable and retain absent health observables as gaps. |
| release-notes / migration | First 2.4 start reads v1 and writes v2 copy, preserving v1 input. | Create source-bound migration/persistence case. |
| upgrade-runbook / configuration statement | It says operator must run `docsync config-migrate` before start. | Preserve the sequence ambiguity: ask whether manual migration is required, redundant or idempotent with automatic first-start migration; do not assume a sequence. |
| support reference / v2 fields | v2 requires storage.path/listen.port; missing-field rejection has no stated signal/state. | Draft field/readiness coverage and a gap for unknown rejection behavior. |
| runbook plus support reference / precedence | Environment port override wins; no default/effective-config observer. | Address precedence but retain missing observation/authorization gap. |
| release-notes / rollback | Rollback before membership-metadata migration has specified high-level steps. | Draft pre-migration rollback readiness only. |
| release-notes / rollback boundary | Post-metadata rollback, backup integrity, reconciliation and RPO/RTO are absent. | Explicit gaps; never claim durability/recovery success. |
| support reference / cluster facts | Leader/partition/replication/consistency/degraded behavior are absent. | Do not invent fault, quorum, data or retry oracles. |
| release-notes / client boundary | CLI 2.3/2.4 supported; browser/database/proxy/third-party support absent. | Support matrix and honest compatibility gaps. |
| release-notes / thresholds | No capacity, resource or NFR thresholds. | NFR planning/readiness only, no numeric pass threshold. |
| incident A | Unidentified narrative says cluster looked healthy. | Classify as unverified narrative, not result. |
| incident B | 2.4.0-rc2 and 2.3.6 logs are mixed. | Separate mixed build from final 2.4.0 fresh retest evidence. |
| incident C | Port-override statement lacks effective config/build/reproduction. | Request evidence; do not assert configuration success. |
| all source boundaries | No target, account, authorization, maintenance window, abort owner or cleanup. | All cases remain draft/not executed; execution prerequisites are gaps. |

Independent audit questions: Does the package trace all source facts/absences to
a case, conflict, gap, or justified scope decision?  Does it distinguish an
upgrade process step from a durability/recovery proof?  Does it separate mixed
or unidentified incident material from a pinned final-build retest?  Does every
proposed case state an action and an available/pending observable without
inventing an external result?
