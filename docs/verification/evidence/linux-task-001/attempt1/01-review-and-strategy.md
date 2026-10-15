# 01 — Requirements/source review and QA strategy

Classification: `PUBLIC_DEVELOPMENT`; `DRAFT_UNAPPROVED`; `NOT_EXECUTED`.

Task: offline QA design package for a proposed DocSync Server 2.3.6 → 2.4.0
three-member rolling upgrade, produced from five supplied input documents using
the installed QA Master Skill. No command was run against any host or service;
no upgrade, recovery, defect, security finding, approval, result, acceptance,
release, comparison, or superiority conclusion is claimed anywhere in this
package. Everything below is draft material for human review.

---

## 1. Source notation and evidence status

Citations in this package are natural citations of the form
`(document › "section heading")` referring to the supplied input documents.
File identity (full path + SHA256 of actual bytes) is recorded in
`read-audit.md` and `handoff.json`; the content hashes above were computed from
the actual files read.

| Document | Declared classification | Role in this package | Evidence limits declared by the source itself |
|---|---|---|---|
| `participant-task.md` | `PUBLIC_DEVELOPMENT`; `DRAFT_UNAPPROVED`; `NOT_EXECUTED` | Task instructions; defines allowed scope (offline design only) and forbidden actions | Prohibits host/service contact, SSH/systemctl/package/migration/backup/restore/traffic/network/disk/fault commands, credentials, and any result claims |
| `release-notes.md` | `PUBLIC_DEVELOPMENT`; execution state `NOT_EXECUTED` | Primary statement of change scope, supported upgrade path, migration/rollback boundary, client boundary | "Not a record of a deployed release, an approved production change, or operational evidence"; explicitly does not authorize any SSH command, restart, config write, backup restore, traffic drain, network partition, disk-fill exercise, or test result |
| `upgrade-runbook.md` | `PUBLIC_DEVELOPMENT`; `DRAFT_UNAPPROVED`; `NOT_EXECUTED` | Operational sequence, config-migrate statement, env precedence, access boundary | "Ordinary operational source material, not an approved production runbook"; supplies no target, account, host list, SSH credential, maintenance window, abort owner, backup location, data classification, stop condition, or operator authorization |
| `support-and-config.md` | `PUBLIC_DEVELOPMENT`; execution state `NOT_EXECUTED` | Support matrix, cluster shape, v2 config fields, observable service data | Explicitly does not specify leader election, partition behavior, replication factor, write consistency, membership metadata format, capacity limits, or degraded-service behavior |
| `incident-excerpts.md` | `PUBLIC_DEVELOPMENT`; `SYNTHETIC_SCENARIO_MATERIAL`; `NOT_OPERATIONAL_EVIDENCE`; `NOT_EXECUTED` | Synthetic scenario material only | "Do not describe a real incident, customer, host, build, outage, test execution, defect, recovery, or release" |

No source supplies an owner, document date, or approved baseline version. All
five documents are scenario material for offline design; none of them is
approved, deployed, or executed. No code, pinned revision, deployed system, or
build identity was supplied or inspected.

Installed QA Master Skill guidance used (files under
`.agents/skills/qa-master/`, hashes in `read-audit.md`): `SKILL.md`,
`references/work-protocol.md`, `references/domains.md`,
`references/design-methods.md`, and the professional guides
`requirements-review.md`, `functional-api.md`, `structural-integration.md`,
`nonfunctional-compatibility.md`, `security-recovery.md`,
`regression-evidence.md` (under `scripts/qa_master/skills/professional/`).

---

## 2. Atomic candidate facts and rules extracted from the sources

Every row below is a **candidate** rule or fact, not an approved requirement.
"Stated" rows restate what a source says; "not stated" rows record gaps the
sources themselves declare. Kind: `FACT` = explicitly stated by a source;
`ABSENCE` = the source explicitly states this is not stated/defined/supplied.

### 2.1 From `release-notes.md`

| ID | Candidate fact / rule | Citation | Kind |
|---|---|---|---|
| RN-01 | DocSync Server 2.4.0 changes the on-disk service configuration from schema v1 to schema v2 | release-notes › "Change scope" | FACT |
| RN-02 | The change affects the `docsyncd` service process, its local configuration files, and clustered membership metadata | release-notes › "Change scope" | FACT |
| RN-03 | The release is for three-member clusters only; it does not describe a single-node procedure | release-notes › "Change scope" | FACT |
| RN-04 | Upgrade is supported from 2.3.6 to 2.4.0 on x86_64 Ubuntu 22.04 with kernel 5.15 | release-notes › "Supported upgrade path" | FACT |
| RN-05 | Upgrade is supported from 2.3.6 to 2.4.0 on x86_64 Rocky Linux 9 with kernel 5.14 | release-notes › "Supported upgrade path" | FACT |
| RN-06 | Two remaining 2.3.6 members may communicate with one 2.4.0 member while a three-member rolling upgrade is in progress | release-notes › "Supported upgrade path" | FACT |
| RN-07 | Compatibility with any other server version combination is not stated | release-notes › "Supported upgrade path" | ABSENCE |
| RN-08 | Upgrade order: take one member out of service, upgrade it, wait for it to report ready, return it to service, before beginning the next member | release-notes › "Supported upgrade path" | FACT |
| RN-09 | At least two voting members must remain ready during the procedure | release-notes › "Supported upgrade path" | FACT |
| RN-10 | A ready upgraded member exposes `GET /healthz` with HTTP 200 and JSON member `ready: true` | release-notes › "Supported upgrade path" | FACT |
| RN-11 | No latency, error-rate, disk, inode, memory, CPU, or network threshold is supplied | release-notes › "Supported upgrade path" | ABSENCE |
| RN-12 | At first 2.4.0 start, the service reads `config/doc-sync.yaml` schema v1 and writes a schema-v2 copy at `data/config-v2.yaml` | release-notes › "Migration and rollback boundary" | FACT |
| RN-13 | The v1 input file (`config/doc-sync.yaml`) is preserved | release-notes › "Migration and rollback boundary" | FACT |
| RN-14 | Whether other local files are changed is not stated | release-notes › "Migration and rollback boundary" | ABSENCE |
| RN-15 | Rolling back an upgraded member is supported only before that member has migrated membership metadata | release-notes › "Migration and rollback boundary" | FACT |
| RN-16 | Rollback procedure: the operator restores the saved v1 configuration, reinstalls 2.3.6, and restarts that member | release-notes › "Migration and rollback boundary" | FACT |
| RN-17 | Rollback after membership metadata migration is not defined | release-notes › "Migration and rollback boundary" | ABSENCE |
| RN-18 | No backup integrity verification, data reconciliation query, or RPO/RTO is defined | release-notes › "Migration and rollback boundary" | ABSENCE |
| RN-19 | The 2.4.0 server supports DocSync CLI 2.3 and 2.4 on the listed operating systems | release-notes › "Client and evidence boundary" | FACT |
| RN-20 | Browser, database, proxy and third-party client support is not stated | release-notes › "Client and evidence boundary" | ABSENCE |
| RN-21 | The release note does not authorize an SSH command, restart, config write, backup restore, traffic drain, network partition, disk-fill exercise, or a test result | release-notes › "Client and evidence boundary" | FACT |

### 2.2 From `upgrade-runbook.md`

| ID | Candidate fact / rule | Citation | Kind |
|---|---|---|---|
| RB-01 | Step 1: record the cluster member name, installed server version, supported OS/kernel version, and the identity of the available v1 configuration backup for the selected member | upgrade-runbook › "Intended sequence" | FACT |
| RB-02 | Step 2: confirm that two other voting members are ready before removing the selected member from service | upgrade-runbook › "Intended sequence" | FACT |
| RB-03 | No command, traffic-drain mechanism, quorum query, or leader-election observer is defined for that confirmation | upgrade-runbook › "Intended sequence" | ABSENCE |
| RB-04 | Step 3: install 2.4.0 on the selected member and start `docsyncd` | upgrade-runbook › "Intended sequence" | FACT |
| RB-05 | Step 4: a member is treated as ready only after its documented `/healthz` response is HTTP 200 with `ready: true`; then return it to service and proceed to the next member | upgrade-runbook › "Intended sequence" | FACT |
| RB-06 | Step 5 rollback trigger: if the member cannot reach the documented ready state before membership metadata migration, restore the saved v1 configuration, reinstall 2.3.6, and restart the member | upgrade-runbook › "Intended sequence" | FACT |
| RB-07 | No post-rollback health or data reconciliation oracle is given | upgrade-runbook › "Intended sequence" | ABSENCE |
| RB-08 | The operational team must run `docsync config-migrate` before starting a 2.4.0 member | upgrade-runbook › "Configuration statement" | FACT |
| RB-09 | `docsync config-migrate` is said to create `data/config-v2.yaml` from `config/doc-sync.yaml` | upgrade-runbook › "Configuration statement" | FACT |
| RB-10 | The runbook does not state whether `docsyncd` performs the same migration automatically | upgrade-runbook › "Configuration statement" | ABSENCE |
| RB-11 | How `docsync config-migrate` is authorized, its exit-code meaning, and what happens after a partial migration are not stated | upgrade-runbook › "Configuration statement" | ABSENCE |
| RB-12 | For an upgraded member, `DOCSYNC_LISTEN_PORT` takes precedence over `listen.port` in `config/doc-sync.yaml` | upgrade-runbook › "Configuration precedence and access boundary" | FACT |
| RB-13 | No default port is specified | upgrade-runbook › "Configuration precedence and access boundary" | ABSENCE |
| RB-14 | No source states how environment values are supplied, who may change them, or how the effective configuration is observed | upgrade-runbook › "Configuration precedence and access boundary" | ABSENCE |
| RB-15 | No target, account, host list, SSH credential, maintenance window, abort owner, backup location, data classification, stop condition, or operator authorization is supplied; no listed activity may be executed from this document | upgrade-runbook › "Configuration precedence and access boundary" | FACT |

### 2.3 From `support-and-config.md`

| ID | Candidate fact / rule | Citation | Kind |
|---|---|---|---|
| SC-01 | Supported combinations: 2.3.6 and 2.4.0 each on Ubuntu 22.04 / kernel 5.15 / x86_64 and on Rocky Linux 9 / kernel 5.14 / x86_64 | support-and-config › "Supported platform and service facts" (table) | FACT |
| SC-02 | The cluster has exactly three voting members | support-and-config › "Supported platform and service facts" | FACT |
| SC-03 | Leader election, network-partition behavior, replication factor, write consistency, membership metadata format, capacity limits, and degraded-service behavior are not specified | support-and-config › "Supported platform and service facts" | ABSENCE |
| SC-04 | Schema v2 requires `storage.path` and `listen.port` | support-and-config › "Configuration v2 fields" | FACT |
| SC-05 | Schema v2 accepts an optional `metrics.enabled` boolean | support-and-config › "Configuration v2 fields" | FACT |
| SC-06 | 2.4.0 rejects a configuration that omits either required field | support-and-config › "Configuration v2 fields" | FACT |
| SC-07 | The resulting log, error code, service state, or whether the prior configuration remains usable after rejection is not stated | support-and-config › "Configuration v2 fields" | ABSENCE |
| SC-08 | `DOCSYNC_LISTEN_PORT`, if set, takes precedence over `listen.port` (consistent with RB-12) | support-and-config › "Configuration v2 fields" | FACT |
| SC-09 | No default value and no inspection command for the effective value are defined | support-and-config › "Configuration v2 fields" | ABSENCE |
| SC-10 | Config-file ownership, file permissions, SELinux policy, storage free-space/inode requirements, and migration locking when two operators act concurrently are not stated | support-and-config › "Configuration v2 fields" | ABSENCE |
| SC-11 | `GET /healthz` returns HTTP 200 and `{"ready": true}` only for a ready member | support-and-config › "Observable service data" | FACT |
| SC-12 | No endpoint or log format is documented for schema version, membership metadata, configuration migration progress, persisted documents, backup contents, or client protocol negotiation | support-and-config › "Observable service data" | ABSENCE |

### 2.4 From `incident-excerpts.md`

| ID | Candidate material | Citation | Kind |
|---|---|---|---|
| IE-01 | All three excerpts are synthetic scenario material, not operational evidence; they do not describe a real incident, customer, host, build, outage, test execution, defect, recovery, or release | incident-excerpts › header classification | FACT (provenance declaration) |
| IE-02 | Excerpt A (operator note, synthetic): "member restarted during upgrade; cluster looked healthy afterwards" at 2026-09-18 02:10Z, host=lab-node-b | incident-excerpts › "Excerpt A — maintenance note" | SYNTHETIC |
| IE-03 | Excerpt B (log fragment, synthetic): build=2.4.0-rc2 line "migrated configuration to v2" at 02:12Z followed by build=2.3.6 line "service started" at 02:13Z | incident-excerpts › "Excerpt B — log fragment" | SYNTHETIC |
| IE-04 | Excerpt C (ticket note, synthetic): ticket=SIM-42, "configuration appeared to use port override" at 02:20Z | incident-excerpts › "Excerpt C — ticket note" | SYNTHETIC |

Consistency note (observation, not a resolution): the support matrix in
`support-and-config.md` and the upgrade path in `release-notes.md` agree on the
OS/kernel/arch combinations (RN-04/05 vs SC-01), and the runbook and the
reference agree on env-var precedence (RB-12 vs SC-08). Excerpt B's
`build=2.4.0-rc2` is a version that appears nowhere in the supported-matrix or
upgrade-path sources (see gap G-19).

---

## 3. Conflicts-and-gaps register (typed)

Types follow the installed professional guides (`requirements-review.md`,
`functional-api.md`, `nonfunctional-compatibility.md`, `security-recovery.md`,
`regression-evidence.md`). Conflicts are preserved as conflicts; nothing below
is resolved by plausibility.

| ID | Type | Description | Citations | Impact on draft cases |
|---|---|---|---|---|
| G-01 | `SOURCE_CONFLICT` | **Migration trigger: automatic vs manual.** release-notes says migration happens automatically: "At first 2.4.0 start, the service reads `config/doc-sync.yaml` schema v1 and writes a schema-v2 copy at `data/config-v2.yaml`" (RN-12). The runbook says the operational team **must** run `docsync config-migrate` **before** starting a 2.4.0 member (RB-08), and itself acknowledges it "does not state whether `docsyncd` performs the same migration automatically" (RB-10). The two documents describe different mandatory sequences for the same artifact (`data/config-v2.yaml`). Not resolvable from the supplied sources. | release-notes › "Migration and rollback boundary"; upgrade-runbook › "Configuration statement" | TC-LU-006 and TC-LU-009 are drafted as variants; both kept; neither can be baselined until a source owner resolves the conflict |
| G-02 | `ORACLE_MISSING` | No documented observable for "membership metadata migrated" — the rollback boundary (RN-15) cannot be observed. No endpoint or log documents schema version, membership metadata, or migration progress (SC-12) | release-notes › "Migration and rollback boundary"; support-and-config › "Observable service data" | TC-LU-011 blocked at the boundary check; TC-LU-012 undefined |
| G-03 | `ORACLE_MISSING` | Rejection observables for a v2 config missing required fields: no log, error code, service state, or statement whether the prior configuration remains usable (SC-07) | support-and-config › "Configuration v2 fields" | TC-LU-007 drafted; expected observable conditional/pending |
| G-04 | `ORACLE_MISSING` | No post-rollback health or data reconciliation oracle (RB-07); no backup integrity verification, data reconciliation query, or RPO/RTO (RN-18) | upgrade-runbook › "Intended sequence" step 5; release-notes › "Migration and rollback boundary" | TC-LU-011 expected result conditional; no reconciliation check designable |
| G-05 | `RECOVERY_OBJECTIVE_UNCONFIRMED` | No RPO/RTO, no recovery objectives, no recovery owner, no backup identity beyond "saved v1 configuration" | release-notes › "Migration and rollback boundary"; upgrade-runbook › "Configuration precedence and access boundary" | Recovery work limited to design; no drill plan thresholds may be invented |
| G-06 | `PROCEDURE_UNDEFINED` | Rollback after membership metadata migration is not defined (RN-17) | release-notes › "Migration and rollback boundary" | TC-LU-012 recorded as blocked gap, not a case |
| G-07 | `AUTHORIZATION_MISSING` | No target, account, host list, SSH credential, maintenance window, abort owner, backup location, data classification, stop condition, or operator authorization (RB-15); the release note authorizes no SSH command, restart, config write, backup restore, traffic drain, network partition, disk-fill exercise, or test result (RN-21) | upgrade-runbook › "Configuration precedence and access boundary"; release-notes › "Client and evidence boundary" | All execution blocked; every case is design-only |
| G-08 | `ORACLE_MISSING` | No command, traffic-drain mechanism, quorum query, or leader-election observer to confirm "two other voting members are ready" (RB-03); only per-member `/healthz` is documented (SC-11) | upgrade-runbook › "Intended sequence" step 2 | TC-LU-004 limited to per-member `/healthz`; cluster-level readiness unverifiable |
| G-09 | `ORACLE_MISSING` | No default port (RB-13, SC-09) and no inspection command for the effective configuration value (RB-14, SC-09) | upgrade-runbook › "Configuration precedence and access boundary"; support-and-config › "Configuration v2 fields" | TC-LU-010 observation method pending; no default-port case designable |
| G-10 | `POLICY_UNCONFIRMED` | How environment values are supplied and who may change them is not stated (RB-14) | upgrade-runbook › "Configuration precedence and access boundary" | TC-LU-010 setup details pending |
| G-11 | `ORACLE_MISSING` | Behavior after a partial migration is not stated (RB-11) | upgrade-runbook › "Configuration statement" | TC-LU-016 blocked |
| G-12 | `AUTHORIZATION_MISSING` | How `docsync config-migrate` is authorized and what its exit codes mean are not stated (RB-11) | upgrade-runbook › "Configuration statement" | TC-LU-009 variants cannot be baselined or executed |
| G-13 | `CONTRACT_MISSING` | Browser, database, proxy, third-party client support not stated (RN-20); no client protocol negotiation observable (SC-12); no CLI command set or output contract documented anywhere | release-notes › "Client and evidence boundary"; support-and-config › "Observable service data" | TC-LU-013 drafted at scenario level only; concrete operations pending a CLI contract |
| G-14 | `THRESHOLD_UNCONFIRMED` | No latency, error-rate, disk, inode, memory, CPU, or network threshold (RN-11); no capacity limits (SC-03) | release-notes › "Supported upgrade path"; support-and-config › "Supported platform and service facts" | No performance/load/stress/stability target may be set; corresponding method rows N/A for target-setting |
| G-15 | `BEHAVIOR_UNSPECIFIED` | Leader election, network-partition behavior, replication factor, write consistency, membership metadata format, and degraded-service behavior are not specified (SC-03) | support-and-config › "Supported platform and service facts" | Mixed-version window (TC-LU-003) limited to documented per-member readiness; no consistency assertions |
| G-16 | `SECURITY_POLICY_UNCONFIRMED` | Config-file ownership, file permissions, SELinux policy, storage free-space/inode requirements not stated (SC-10) | support-and-config › "Configuration v2 fields" | No security/permissions case designable; recorded as gap |
| G-17 | `CONCURRENCY_POLICY_MISSING` | Migration locking when two operators act concurrently is not stated (SC-10) | support-and-config › "Configuration v2 fields" | TC-LU-017 blocked |
| G-18 | `EVIDENCE_UNVERIFIED` | Incident excerpts are declared `SYNTHETIC_SCENARIO_MATERIAL` / `NOT_OPERATIONAL_EVIDENCE`; they cannot ground any expected result, defect, or observed behavior (IE-01) | incident-excerpts › header | TC-LU-015 derived as scenario motivation only; excluded from any final-build evidence base |
| G-19 | `VERSION_PROVENANCE_UNCONFIRMED` | Excerpt B references `build=2.4.0-rc2`, a version absent from the supported matrix (SC-01) and the upgrade path (RN-04/05) | incident-excerpts › "Excerpt B"; support-and-config › "Supported platform and service facts" | Excerpt B cannot be mapped to any supported build; noted, not resolved |
| G-20 | `ENVIRONMENT_UNIDENTIFIED` | No test environment, build identity, or pinned revision is supplied by any source; all five inputs are `NOT_EXECUTED` scenario material | all input headers | Every case is design-only; no execution environment exists to bind cases to |
| G-21 | `ORACLE_MISSING` | Whether other local files change during migration is not stated (RN-14); no file-level diff oracle exists in the sources | release-notes › "Migration and rollback boundary" | TC-LU-018 exploratory draft with unknown expected result |
| G-22 | `TEST_DATA_MISSING` | No representative v1 configuration file, v2 file example, document workload, or port values are supplied; inventing field contents would exceed the sources | (absence across all four technical sources) | Case setups reference "the member's actual recorded v1 configuration" rather than synthetic file contents |

---

## 4. Method selection and applicability

Applicability was checked per `SKILL.md` ("Check applicability of functional,
API, white-box, integration, performance, load/stress, stability,
compatibility, negative, recovery, security and regression coverage") against
the Linux/systems guidance in `references/domains.md` ("Identify supported
distro/kernel/architecture, install/upgrade/rollback paths, services,
privileges, ports, storage/network topology and persistent data… For
distributed or storage systems, model membership, quorum/leadership where
applicable…"). A scenario counts as designed only when its actions and
observables are specified; category listings alone are not coverage.

| Method | Applicability to this Linux rolling upgrade | Reason (source-grounded) | Guide applied |
|---|---|---|---|
| Functional (sequence/state) | **Applicable (design)** | The rolling-upgrade sequence, readiness gating, and config migration are functional behaviors with a stated observable (`/healthz` 200 + `ready: true`, RN-10/SC-11) | functional-api.md |
| API / contract | **Partially applicable** | Exactly one endpoint contract exists (`GET /healthz`, SC-11). No other API contract, CLI command set, or response schema is documented (SC-12, G-13), so API coverage beyond `/healthz` is `CONTRACT_MISSING` | functional-api.md |
| Boundary | **Limited** | No numeric bounds are supplied (no port range, no capacity threshold, RN-11/SC-03). The only stated "boundaries" are the rollback boundary (pre/post membership-metadata migration, RN-15/17) and required-vs-optional v2 fields (SC-04/05) | functional-api.md |
| Negative | **Partially applicable** | One stated negative rule: 2.4.0 rejects a v2 config omitting a required field (SC-06), but its observable is `ORACLE_MISSING` (SC-07). No other negative contract (e.g., unsupported OS behavior) is stated | functional-api.md |
| White-box | **Not applicable** | No source code, pinned revision, or control-flow observation was supplied | structural-integration.md |
| Integration | **Partially applicable (design)** | Stated integrations: mixed-version member communication during the rolling window (RN-06) and CLI 2.3/2.4 client support (RN-19). Inter-member protocol, replication, and consistency contracts are unspecified (SC-03, G-15), so integration checks are limited to documented observables | structural-integration.md |
| Performance | **Not applicable (targets missing)** | No latency/error-rate threshold is supplied (RN-11); `SLA_UNCONFIRMED`/`THRESHOLD_UNCONFIRMED` — proposing numbers is forbidden by the sources and by nonfunctional-compatibility.md | nonfunctional-compatibility.md |
| Load / stress | **Not applicable (workload + authorization missing)** | No workload model, data volume, duration, abort limits, or authorization (RN-11, RB-15); stress also requires a disposable target and bounded impact per domains.md, none supplied | nonfunctional-compatibility.md |
| Stability | **Not applicable** | No duration, load, or monitoring fields are documented; nothing to hold or measure | nonfunctional-compatibility.md |
| Compatibility | **Applicable (design)** | An explicit support matrix exists (SC-01), an explicit upgrade-path matrix (RN-04/05), and an explicit client matrix (RN-19); a draft compatibility matrix can be built entirely from stated combinations | nonfunctional-compatibility.md |
| Recovery | **Applicable for design only; execution blocked** | Pre-metadata rollback procedure is stated (RN-15/16, RB-06) but has no post-rollback oracle (RB-07), no RPO/RTO (RN-18), and no authorization (RB-15). Post-metadata rollback is undefined (RN-17) | security-recovery.md |
| Security | **Not applicable (blocked)** | No authorization, accounts, threat model, or data classification exists (RB-15). Security-adjacent facts (file permissions, SELinux) are explicitly unstated (SC-10, G-16). `AUTHORIZATION_MISSING` per security-recovery.md | security-recovery.md |
| Regression | **Applicable (design)** | The change scope is stated precisely (RN-01/02: service process, config schema, membership metadata; plus client matrix RN-19 and env precedence RB-12), so a regression impact map with stated recheck reasons can be drafted; evidence state remains `NOT_EXECUTED` | regression-evidence.md |

### Installed offline helper (noted, not used for this draft)

The installed deterministic design helper
(`python -I "<skill>/scripts/qa.py" design --input bundle.json --output report.json`,
per `references/design-methods.md`) could model the member upgrade lifecycle as
a finite state-transition model (states such as: 2.3.6-ready → out-of-service →
2.4.0-starting → ready / rollback-before-metadata) for a limited finite
subproblem. It was **not run** for this package: the deliverable is reviewable
without it, and per the participant task and `references/design-methods.md` its
output would be a draft planning input only — never an executable test, an
approval, or a completed rollback plan. If a future engineer runs it, its
`method_design`/`installed_design` output must be completed into usable draft
cases or typed gaps by hand, as done here.

---

## 5. Strategy summary

**Designable now (source-grounded observables exist):**
platform/compatibility matrix checks; rolling one-member-at-a-time sequence;
mixed-version window existence; two-ready-member precondition (limited to
per-member `/healthz`); `/healthz` readiness gating; v1→v2 migration with input
preservation (as conflicting variants); v2 required-field rejection (result
stated, observable pending); optional `metrics.enabled` acceptance; env port
precedence (rule stated, observation method pending); pre-metadata rollback
sequence (conditional oracle); client compatibility scenario (operations
pending); regression impact selection.

**Blocked with typed gaps (kept as gaps, not invented):**
post-metadata rollback (G-06); partial migration (G-11); concurrent migration
locking (G-17); rejection observables (G-03); post-rollback reconciliation and
RPO/RTO (G-04/G-05); quorum/leader observation (G-08); default port and
effective-config inspection (G-09); security/permissions checks (G-16);
performance/load/stress/stability targets (G-14); CLI operation contract
(G-13); all execution (G-07, G-20).

**Hard conflict preserved:** manual-vs-automatic migration sequence (G-01) —
kept open in TC-LU-009; no resolution is proposed or implied.

Draft case families are in `02-draft-cases.md`; self-review and handoff in
`03-review-and-handoff.md`.
