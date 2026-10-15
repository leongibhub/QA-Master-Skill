# 02 — Draft test case families, upgrade/rollback readiness view, and regression impact map

Classification: `PUBLIC_DEVELOPMENT`; `DRAFT_UNAPPROVED`; `NOT_EXECUTED`.

All cases below are **design-only drafts for human review**. No case was
executed, and none may be executed from this package: no target, account, host
list, credential, maintenance window, abort owner, or operator authorization
exists (upgrade-runbook › "Configuration precedence and access boundary"), and
the release note "does not authorize an SSH command, restart, config write,
backup restore, traffic drain, network partition, disk-fill exercise, or a test
result" (release-notes › "Client and evidence boundary").

Labels are local draft labels (`TC-LU-###`, Linux Upgrade) for review
convenience only; they are not external test-management IDs. Citations are
natural citations (document › section). Where an expected result is conditional
or blocked, the blocking gap ID from `01-review-and-strategy.md` §3 is noted and
the gap is preserved — never silently resolved.

Common setup notes that apply to every case (stated once, cited per case):
- Cluster shape: exactly three voting members (support-and-config › "Supported
  platform and service facts"). Single-node procedures are not described
  (release-notes › "Change scope").
- Baseline platform: one of the four supported combinations in
  support-and-config › "Supported platform and service facts" (table).
- The only documented service observable is `GET /healthz` returning HTTP 200
  and `{"ready": true}` for a ready member (support-and-config › "Observable
  service data").
- No synthetic configuration file contents, port numbers, document workloads,
  or member names are invented (G-22): setups reference "the member's actual
  recorded v1 configuration" per upgrade-runbook › "Intended sequence" step 1.

---

## 1. Draft case families

### TC-LU-001 — Supported platform / kernel / arch combination is on the support matrix before upgrade

| Field | Value |
|---|---|
| Family | Compatibility / pre-upgrade verification |
| Source citation | release-notes › "Supported upgrade path" ("Upgrade is supported from DocSync Server 2.3.6 to 2.4.0 on x86_64 Ubuntu 22.04 with kernel 5.15, and on x86_64 Rocky Linux 9 with kernel 5.14"); support-and-config › "Supported platform and service facts" (table) |
| Precondition / setup | A three-member DocSync cluster with all members at 2.3.6 on one supported OS/kernel/arch combination; member name, installed server version, and OS/kernel version recorded per upgrade-runbook › "Intended sequence" step 1. Offline step for this draft: no host contact. |
| Selected system state / data | Each member's recorded OS, kernel, architecture, and server version, compared against the four-row matrix in support-and-config. |
| Proposed action (future, authorized execution only) | For each member, compare its recorded platform identity against the support matrix, and the (2.3.6 → 2.4.0) pair against the upgrade-path statement, before selecting it for upgrade. |
| Observable expected result | Every member matches a (2.3.6, Ubuntu 22.04, 5.15, x86_64) or (2.3.6, Rocky Linux 9, 5.14, x86_64) row, so the 2.3.6→2.4.0 upgrade pair is a supported combination. A member on any other OS/kernel/arch/version is out of stated support scope — the source states compatibility with no other server version (release-notes › "Supported upgrade path"). |
| Readiness | DRAFT / NOT_EXECUTED |
| Cleanup | None required — comparison of recorded metadata only; no system change proposed. |

### TC-LU-002 — Rolling upgrade proceeds one member at a time with readiness gating between members

| Field | Value |
|---|---|
| Family | Functional / sequence |
| Source citation | release-notes › "Supported upgrade path" ("Take one member out of service, upgrade it, wait for it to report ready, and return it to service before beginning the next member. At least two voting members must remain ready during this procedure."); upgrade-runbook › "Intended sequence" steps 3–4 |
| Precondition / setup | Three-member cluster at 2.3.6 on a supported platform; v1 configuration backup identity recorded for each member (upgrade-runbook step 1); two other voting members confirmed ready (upgrade-runbook step 2). |
| Selected system state / data | Cluster with member M1 selected first; M2, M3 remain at 2.3.6 in service. |
| Proposed action (design) | Sequence design: (a) take M1 out of service; (b) install 2.4.0 and start `docsyncd` (upgrade-runbook step 3); (c) wait until M1's documented `/healthz` is HTTP 200 with `ready: true` (upgrade-runbook step 4); (d) return M1 to service; (e) only then begin M2; repeat for M3. The proposed action is the sequence definition itself, for review — no command set exists to attach to it (see G-08). |
| Observable expected result | At every point between starting one member's upgrade and returning it to service, the two not-currently-upgrading members remain ready (observable via their documented `/healthz` = 200 + `ready: true`), satisfying "at least two voting members must remain ready". The upgraded member reports `/healthz` 200 + `ready: true` before the next member begins. **Note:** "out of service" and "return to service" have no defined mechanism or observable (no traffic-drain mechanism, upgrade-runbook step 2) — this part of the expected result is conditional on a future definition (G-08). |
| Readiness | DRAFT / NOT_EXECUTED (cluster-level readiness oracle pending, G-08) |
| Cleanup | None stated: no source defines a return-to-service or drain mechanism to undo (G-08). Any cleanup beyond "return the member to service" cannot be stated from these sources. |

### TC-LU-003 — Mixed-version window: two 2.3.6 members operate with one 2.4.0 member mid-upgrade

| Field | Value |
|---|---|
| Family | Integration / compatibility |
| Source citation | release-notes › "Supported upgrade path" ("Two remaining 2.3.6 members may communicate with one 2.4.0 member while a three-member rolling upgrade is in progress. The document does not state compatibility with any other server version.") |
| Precondition / setup | Mid-rolling-upgrade state of TC-LU-002: M1 upgraded and ready at 2.4.0; M2, M3 still at 2.3.6 and ready. |
| Selected system state / data | One 2.4.0 member in service with two 2.3.6 members in service (the only mixed-version combination the sources support). |
| Proposed action (design) | During the window between M1 returning to service and M2 beginning its upgrade, observe each member's documented `/healthz` and record whether the members remain ready. |
| Observable expected result | Members remain ready per their `/healthz` responses. **Limit preserved:** the sources state only that the members "may communicate"; they specify no replication, consistency, or degraded-behavior contract (support-and-config › "Supported platform and service facts"), so no data-consistency or communication-correctness assertion is designable — only readiness. Any version combination other than {2×2.3.6, 1×2.4.0} is outside stated compatibility (G-15). |
| Readiness | DRAFT / NOT_EXECUTED |
| Cleanup | None required — observation-only design during a state that the upgrade sequence itself resolves. |

### TC-LU-004 — Two-ready-member precondition check before removing a member from service

| Field | Value |
|---|---|
| Family | Functional / precondition |
| Source citation | upgrade-runbook › "Intended sequence" step 2 ("Confirm that two other voting members are ready before removing the selected member from service. The source does not define a command, traffic-drain mechanism, quorum query, or leader-election observer."); release-notes › "Supported upgrade path" ("At least two voting members must remain ready") |
| Precondition / setup | Member selected for upgrade; its v1 backup identity recorded (upgrade-runbook step 1). |
| Selected system state / data | The two other members' readiness state, as observable through their documented `/healthz` endpoints (the only readiness observable any source provides, support-and-config › "Observable service data"). |
| Proposed action (design) | Before removing the selected member, check each of the two other members' `/healthz`; proceed to removal only if both return HTTP 200 with `ready: true`. |
| Observable expected result | Both remaining members return `/healthz` 200 + `{"ready": true}` before the selected member is removed. **Limits preserved:** this verifies per-member readiness only; no quorum query or leader-election observer exists to verify cluster-level voting readiness (G-08), and "removing from service" has no defined mechanism (G-08). |
| Readiness | DRAFT / NOT_EXECUTED (cluster-level readiness oracle pending, G-08) |
| Cleanup | None — observation gate; no state change proposed. |

### TC-LU-005 — Upgraded member readiness via `GET /healthz`

| Field | Value |
|---|---|
| Family | Functional / API observable |
| Source citation | release-notes › "Supported upgrade path" ("A ready upgraded member exposes `GET /healthz` with HTTP 200 and JSON member `ready: true`"); support-and-config › "Observable service data" ("`GET /healthz` returns HTTP 200 and `{\"ready\": true}` only for a ready member"); upgrade-runbook › "Intended sequence" step 4 |
| Precondition / setup | One member upgraded to 2.4.0, `docsyncd` started (upgrade-runbook step 3). |
| Selected system state / data | A single upgraded member's `/healthz` response (status code and JSON body). |
| Proposed action (design) | Issue `GET /healthz` against the upgraded member and inspect status code and body. |
| Observable expected result | For a ready member: HTTP 200 with JSON body containing `ready: true`. Per support-and-config, the 200/`ready: true` response occurs **only** for a ready member, so a non-ready member must not produce this exact response — though what it does produce is not documented (no error contract, SC-12/G-03 adjacent), so the negative side of this case is design-blocked. |
| Readiness | DRAFT / NOT_EXECUTED |
| Cleanup | None — read-only observation. |

### TC-LU-006 — Automatic migration at first 2.4.0 start (variant A of the migration-trigger conflict)

| Field | Value |
|---|---|
| Family | Functional / config migration |
| Source citation | release-notes › "Migration and rollback boundary" ("At first 2.4.0 start, the service reads `config/doc-sync.yaml` schema v1 and writes a schema-v2 copy at `data/config-v2.yaml`. It preserves the v1 input file and does not state whether other local files are changed.") |
| Precondition / setup | Member at 2.3.6 with a v1 `config/doc-sync.yaml` present; 2.4.0 installed; `docsyncd` started for the first time. **This variant assumes no prior manual `config-migrate` was run** — see TC-LU-009 and conflict G-01. |
| Selected system state / data | The member's actual recorded v1 configuration file (upgrade-runbook step 1), its content hash captured before start; the `data/config-v2.yaml` path. |
| Proposed action (design) | After first 2.4.0 start, check for existence of `data/config-v2.yaml` and compare `config/doc-sync.yaml` content against its pre-start capture. |
| Observable expected result | `data/config-v2.yaml` exists (a schema-v2 copy was written), and `config/doc-sync.yaml` is unchanged (v1 input preserved). Whether other local files changed is **unknown** — the source explicitly does not state it (G-21); no expected result is invented for other files. |
| Readiness | DRAFT / NOT_EXECUTED (variant A of an unresolved SOURCE_CONFLICT, G-01) |
| Cleanup | None stated — the sources define no post-migration state reset; the v1 file is preserved by design, and whether `data/config-v2.yaml` should be removed on any revert is not stated (post-metadata rollback undefined, G-06). |

### TC-LU-007 — Schema v2 rejects a configuration missing a required field

| Field | Value |
|---|---|
| Family | Negative / configuration validation |
| Source citation | support-and-config › "Configuration v2 fields" ("Schema v2 requires `storage.path` and `listen.port`. It accepts an optional `metrics.enabled` boolean. The reference says 2.4.0 rejects a configuration that omits either required field, but it does not state the resulting log, error code, service state, or whether the prior configuration remains usable.") |
| Precondition / setup | An upgraded 2.4.0 member environment with a v2 configuration that omits `storage.path`, and (as a separate variant) one that omits `listen.port`. |
| Selected system state / data | A v2 config candidate lacking exactly one required field per variant. Test file contents cannot be invented from the sources (G-22); the variant is defined by the omission, not by specific values. |
| Proposed action (design) | Present each omission variant to the 2.4.0 configuration path (at start or via config validation, whichever a future contract defines) and observe the outcome. |
| Observable expected result | The configuration is rejected (stated). **Observable pending (G-03):** the log output, error code, resulting service state, and whether the prior configuration remains usable are not stated by any source — these sub-observables are marked awaiting a source, not guessed. |
| Readiness | DRAFT / NOT_EXECUTED (observable partially ORACLE_MISSING, G-03) |
| Cleanup | None stated — whether the rejected config leaves any state to clean up is itself unknown (G-03: "whether the prior configuration remains usable" is unstated). |

### TC-LU-008 — Schema v2 accepts a configuration with both required fields, with and without optional `metrics.enabled`

| Field | Value |
|---|---|
| Family | Functional / configuration validation |
| Source citation | support-and-config › "Configuration v2 fields" ("Schema v2 requires `storage.path` and `listen.port`. It accepts an optional `metrics.enabled` boolean.") |
| Precondition / setup | Upgraded 2.4.0 member environment; v2 configuration candidates containing both required fields. |
| Selected system state / data | Two candidates: (a) `storage.path` + `listen.port` present, `metrics.enabled` absent; (b) `storage.path` + `listen.port` present, `metrics.enabled` present as a boolean. Specific values not invented (G-22). |
| Proposed action (design) | Start (or validate, per a future contract) with each candidate and observe service behavior. |
| Observable expected result | Candidate (a) is accepted (optional field absent is valid); candidate (b) is accepted. The success observable available from the sources is the readiness contract: a ready member serves `/healthz` 200 + `ready: true` (TC-LU-005). Whether `metrics.enabled` has any observable effect is **not stated** — no metric endpoint is documented (SC-12) — so no metrics-behavior expectation is asserted. |
| Readiness | DRAFT / NOT_EXECUTED |
| Cleanup | None stated — the sources define no reset procedure for configuration state; reverting a member is only defined pre-metadata-migration (G-06). |

### TC-LU-009 — Manual `docsync config-migrate` before start (variant B of the migration-trigger conflict) — CONFLICT PRESERVED

| Field | Value |
|---|---|
| Family | Functional / config migration / conflict |
| Source citation | upgrade-runbook › "Configuration statement" ("The operational team must run `docsync config-migrate` before starting a 2.4.0 member. The command is said to create `data/config-v2.yaml` from `config/doc-sync.yaml`. The runbook does not state whether `docsyncd` performs the same migration automatically, how the command is authorized, its exit-code meaning, or what happens after a partial migration.") — **conflicts with** release-notes › "Migration and rollback boundary" (automatic migration at first start, TC-LU-006). |
| Precondition / setup | Member at 2.3.6 with v1 `config/doc-sync.yaml`; v1 backup identity recorded; 2.4.0 installed but **not yet started**. |
| Selected system state / data | Pre-start state: `data/config-v2.yaml` absent (per this variant's premise). |
| Proposed action (design) | Run `docsync config-migrate` (authorization, invocation method, and exit-code meaning all unstated, G-12), then start `docsyncd`. |
| Observable expected result | `data/config-v2.yaml` is created from `config/doc-sync.yaml` ("is said to create" — the runbook itself hedges). **Open conflict, kept open (G-01):** this runbook sequence ("must run before starting") is inconsistent with release-notes' automatic-at-first-start description of the same artifact. Both variants are drafted; neither is baselined; no resolution is proposed or implied. The runbook's own acknowledged unknowns (authorization, exit codes, partial migration) remain gaps (G-11, G-12). |
| Readiness | DRAFT / NOT_EXECUTED (SOURCE_CONFLICT G-01 preserved; authorization and exit-code oracle missing, G-12) |
| Cleanup | None stated — partial-migration behavior is unknown (G-11), so whether an incomplete `data/config-v2.yaml` requires removal before retry cannot be stated. |

### TC-LU-010 — `DOCSYNC_LISTEN_PORT` takes precedence over `listen.port`

| Field | Value |
|---|---|
| Family | Functional / configuration precedence |
| Source citation | upgrade-runbook › "Configuration precedence and access boundary" ("For an upgraded member, `DOCSYNC_LISTEN_PORT` takes precedence over `listen.port` in `config/doc-sync.yaml`. No default port is specified. No source states how environment values are supplied, who may change them, or how the effective configuration is observed."); support-and-config › "Configuration v2 fields" (same precedence rule; no default value or inspection command) |
| Precondition / setup | Upgraded 2.4.0 member with a v2 config containing `listen.port`, and the environment variable `DOCSYNC_LISTEN_PORT` set. **Setup details pending (G-10):** how environment values are supplied and who may change them is not stated, so the exact setup mechanism cannot be specified. No specific port values are invented (no default port exists in any source, G-09; G-22). |
| Selected system state / data | A member where the env var value differs from the config-file `listen.port` value (the two values must be distinct for precedence to be observable; the values themselves come from the member's actual environment, not from invented defaults). |
| Proposed action (design) | With both set to distinct values, start the upgraded member and determine which port it listens on. |
| Observable expected result | The member listens on the `DOCSYNC_LISTEN_PORT` value, not the config-file `listen.port` value. **Observation method pending (G-09):** no source defines how the effective configuration is observed (no inspection command, no default port, and no documented port-bearing endpoint other than `/healthz` on an unspecified port) — the practical observation mechanism is an open question, not an invented command. |
| Readiness | DRAFT / NOT_EXECUTED (observation method ORACLE_MISSING, G-09; setup policy pending, G-10) |
| Cleanup | None stated — the sources do not define an effective-config reset or inspection, so no cleanup beyond "unset the environment variable in the member's environment" (mechanism itself unspecified, G-10) can be stated. |

### TC-LU-011 — Pre-membership-metadata rollback of a not-ready member

| Field | Value |
|---|---|
| Family | Recovery (design only) |
| Source citation | release-notes › "Migration and rollback boundary" ("Rolling back an upgraded member is supported only before that member has migrated membership metadata. The operator restores the saved v1 configuration, reinstalls 2.3.6, and restarts that member."); upgrade-runbook › "Intended sequence" step 5 (same procedure when the member "cannot reach the documented ready state before membership metadata migration"; "The source gives no post-rollback health or data reconciliation oracle.") |
| Precondition / setup | A member upgraded to 2.4.0 that has **not yet migrated membership metadata** and cannot reach the documented ready state; the member's saved v1 configuration backup identity recorded in step 1. **Blocking note (G-02):** no observable exists for "has migrated membership metadata" — the boundary condition of this entire case is unobservable in the supplied sources. |
| Selected system state / data | One not-ready upgraded member; its recorded v1 configuration backup. |
| Proposed action (design) | Restore the saved v1 configuration, reinstall 2.3.6, restart the member (the three stated steps; no commands exist for any of them). |
| Observable expected result | **Conditional (G-02, G-04):** the only candidate observable available from the sources is the readiness contract — after restart, the member serves `/healthz` 200 + `ready: true` under 2.3.6. This is offered as a candidate post-rollback observable for review, **not** as a stated source oracle: the runbook explicitly says no post-rollback health or data-reconciliation oracle is given, and no data reconciliation query or backup integrity verification exists (RN-18). The rollback boundary precondition itself (pre-metadata) cannot be verified (G-02). |
| Readiness | DRAFT / NOT_EXECUTED (oracle partly ORACLE_MISSING, G-04; boundary observation missing, G-02; authorization missing, G-07) |
| Cleanup | None stated — a rollback **is** the recovery action; the sources define no procedure beyond the three stated steps and no reconciliation check afterward (G-04). |

### TC-LU-012 — Post-membership-metadata rollback — BLOCKED GAP (not a designable case)

| Field | Value |
|---|---|
| Family | Recovery — blocked |
| Source citation | release-notes › "Migration and rollback boundary" ("The release does not define rollback after membership metadata migration, backup integrity verification, a data reconciliation query, or an RPO/RTO.") |
| Precondition / setup | Not designable: a member that has migrated membership metadata. |
| Selected system state / data | Not designable. |
| Proposed action | None — recorded as a typed gap (`PROCEDURE_UNDEFINED`, G-06; `RECOVERY_OBJECTIVE_UNCONFIRMED`, G-05). |
| Observable expected result | None exists in any source; inventing one is prohibited. |
| Readiness | BLOCKED GAP (kept as a gap, not a case) |
| Cleanup | Not applicable — no procedure exists. |

### TC-LU-013 — Client compatibility: DocSync CLI 2.3 and 2.4 against a 2.4.0 member

| Field | Value |
|---|---|
| Family | Compatibility / client |
| Source citation | release-notes › "Client and evidence boundary" ("The 2.4.0 server supports DocSync CLI 2.3 and 2.4 on the listed operating systems. Browser, database, proxy and third-party client support is not stated."); support-and-config › "Observable service data" ("No endpoint or log format is documented for… client protocol negotiation") |
| Precondition / setup | An upgraded, ready 2.4.0 member on a supported OS; CLI 2.3 and CLI 2.4 available. **Contract gap (G-13):** no CLI command set, arguments, or output contract is documented in any supplied source, so no concrete client operation can be specified without inventing it. |
| Selected system state / data | A ready 2.4.0 member; the two stated supported CLI versions. |
| Proposed action (design, scenario level) | From each CLI version, perform an ordinary client operation against the 2.4.0 member and observe success. The specific operation cannot be named from the sources (G-13) — candidate operations await a CLI contract. |
| Observable expected result | Both CLI 2.3 and CLI 2.4 operate successfully against the 2.4.0 server on the listed operating systems (as stated). The precise success observable (command output shape) is pending a CLI contract; no protocol-negotiation log or endpoint is documented to check (SC-12). Browser/database/proxy/third-party client behavior is explicitly out of stated scope — no expectation is drafted for them (RN-20). |
| Readiness | DRAFT / NOT_EXECUTED (operations CONTRACT_MISSING, G-13) |
| Cleanup | None stated — client operations are not defined, so whether any create state (e.g., synced documents) is unknown; no cleanup can be specified without inventing client behavior. |

### TC-LU-014 — Regression impact selection for the 2.3.6 → 2.4.0 change scope

| Field | Value |
|---|---|
| Family | Regression (design) |
| Source citation | release-notes › "Change scope" ("changes the on-disk service configuration from schema v1 to schema v2… affects the `docsyncd` service process, its local configuration files, and clustered membership metadata"); regression-evidence.md (installed guide) method: trace changed components to direct requirements, consumers, data migration paths and critical journeys |
| Precondition / setup | None (analysis case over the stated change scope). |
| Selected system state / data | The three stated change surfaces: service process, configuration files/schema, membership metadata; plus the stated client matrix and env precedence rules. |
| Proposed action (design) | Apply the regression impact map in §3 of this document: for each changed surface, select the direct-impact cases (TC-LU-006/007/008/009/010 for config; TC-LU-002/003/011 for service/membership) and the stated client-coverage case (TC-LU-013), with the stated reason recorded per row. |
| Observable expected result | Each recheck area maps to at least one draft case or an explicit typed gap (as tabulated in §3); no changed surface is left unassigned without a recorded reason. This is a design-completeness check, not a test result. |
| Readiness | DRAFT / NOT_EXECUTED |
| Cleanup | None — analysis only. |

### TC-LU-015 — Incident-excerpt-derived scenarios (synthetic provenance — separated from evidence)

| Field | Value |
|---|---|
| Family | Regression / evidence handling (scenario motivation only) |
| Source citation | incident-excerpts › header ("These are original synthetic excerpts for an offline regression/evidence-design exercise. They do not describe a real incident, customer, host, build, outage, test execution, defect, recovery, or release."); Excerpts A, B, C |
| Precondition / setup | None. These excerpts are **declared synthetic, `NOT_OPERATIONAL_EVIDENCE`**, with unverified/mixed provenance (an operator note, a log fragment naming `build=2.4.0-rc2` — a version absent from all supported matrices, G-19 — and a ticket note). |
| Selected system state / data | The three excerpts as motivation material only. |
| Proposed action (design) | Record what each excerpt would *motivate checking* if a real build and authorization existed: Excerpt A (restart during upgrade; "cluster looked healthy afterwards") motivates a mid-upgrade restart readiness check — already covered in design terms by TC-LU-002/003 readiness observables. Excerpt B (v2 migration log followed by a 2.3.6 start) motivates checking migration-then-rollback sequencing — adjacent to TC-LU-011, whose boundary is unobservable (G-02). Excerpt C ("configuration appeared to use port override") motivates the precedence check TC-LU-010, whose observation method is itself pending (G-09). |
| Observable expected result | None. **These excerpts cannot ground any expected result, defect, or observed behavior** (G-18): they are synthetic scenario material and must remain separated from any final-build evidence base. No defect, incident, or behavior claim is derived from them here, and `build=2.4.0-rc2` cannot be mapped to any supported build (G-19). |
| Readiness | DRAFT / NOT_EXECUTED — provenance-limited; excluded from any evidence report |
| Cleanup | Not applicable — no execution, no state touched. |

### TC-LU-016 — Partial migration behavior — BLOCKED GAP

| Field | Value |
|---|---|
| Family | Failure handling — blocked |
| Source citation | upgrade-runbook › "Configuration statement" ("The runbook does not state… what happens after a partial migration.") |
| Precondition / setup | Not designable: no definition of "partial migration" state, trigger, or observable exists. |
| Selected system state / data | Not designable. |
| Proposed action | None — recorded as typed gap (`ORACLE_MISSING`, G-11). |
| Observable expected result | None stated by any source; not invented. |
| Readiness | BLOCKED GAP |
| Cleanup | Not applicable. |

### TC-LU-017 — Concurrent migration by two operators — BLOCKED GAP

| Field | Value |
|---|---|
| Family | Concurrency — blocked |
| Source citation | support-and-config › "Configuration v2 fields" ("It does not state… migration locking when two operators act concurrently.") |
| Precondition / setup | Not designable: no locking behavior, serialization contract, or conflict observable is stated. |
| Selected system state / data | Not designable. |
| Proposed action | None — recorded as typed gap (`CONCURRENCY_POLICY_MISSING`, G-17). |
| Observable expected result | None stated; not invented. |
| Readiness | BLOCKED GAP |
| Cleanup | Not applicable. |

### TC-LU-018 — Whether other local files change during migration — EXPLORATORY DRAFT

| Field | Value |
|---|---|
| Family | Exploratory / change-surface inventory |
| Source citation | release-notes › "Migration and rollback boundary" ("It preserves the v1 input file and does not state whether other local files are changed.") |
| Precondition / setup | Member at 2.3.6 with its local file state inventoried (paths and content hashes) before first 2.4.0 start. |
| Selected system state / data | The member's local file tree before and after first start. |
| Proposed action (design) | After first 2.4.0 start, compare the local file inventory against the pre-start capture and record differences (expected: `data/config-v2.yaml` added; `config/doc-sync.yaml` unchanged — the two stated facts). |
| Observable expected result | **Unknown by design (G-21):** the source explicitly does not state whether other local files change, so this case's expected result is deliberately left open for a human decision or a future source; it is an information-gathering draft, not an assertion. |
| Readiness | DRAFT / NOT_EXECUTED (exploratory; expected result open, G-21) |
| Cleanup | None stated — no source defines which files may be created or how to revert them (post-metadata rollback undefined, G-06). |

---

## 2. Upgrade/rollback readiness view

Everything in this view is design-stage readiness of the **documentation**, not
of any real system. No upgrade or rollback was performed, attempted, or
assessed against a real host.

| Readiness aspect | Status | Source basis | What is missing before execution could ever be considered |
|---|---|---|---|
| Supported platform matrix | **Stated (ready for review)** | support-and-config › "Supported platform and service facts" | — |
| Upgrade path (version pair) | **Stated (ready for review)** | release-notes › "Supported upgrade path" | Compatibility beyond 2.3.6→2.4.0 is unstated (RN-07) |
| Rolling sequence definition | **Stated at intent level** | release-notes › "Supported upgrade path"; upgrade-runbook › "Intended sequence" | No command, drain mechanism, quorum query, or leader-election observer (G-08); readiness observable exists only per member |
| Readiness gate observable | **Stated** (`/healthz` 200 + `ready: true`) | release-notes; upgrade-runbook step 4; support-and-config | Non-ready responses undefined (no error contract) |
| Two-ready-member precondition | **Stated as a rule**; verification method partial | upgrade-runbook step 2; release-notes | Cluster-level readiness unobservable (G-08) |
| Mixed-version window | **Stated as permitted** | release-notes ("Two remaining 2.3.6 members may communicate with one 2.4.0 member") | No consistency/replication contract (G-15) |
| Config migration trigger | **CONFLICT — NOT READY** | release-notes (automatic at first start) vs upgrade-runbook (manual `config-migrate` required before start) | Conflict G-01 must be resolved by a source owner; authorization and exit codes for `config-migrate` also missing (G-12) |
| Config migration artifact & input preservation | **Stated** | release-notes ("writes a schema-v2 copy at `data/config-v2.yaml`… preserves the v1 input file") | Other local files unknown (G-21) |
| v2 required-field rejection | **Stated as a rule**; observables missing | support-and-config | Log, error code, service state, prior-config usability (G-03) |
| Env port precedence | **Stated as a rule**; observation method missing | upgrade-runbook; support-and-config | Default port, effective-config inspection, env supply mechanism (G-09, G-10) |
| Pre-metadata rollback procedure | **Stated at intent level**; oracle missing | release-notes; upgrade-runbook step 5 | Post-rollback health/reconciliation oracle (G-04); boundary unobservable (G-02); backup integrity verification and RPO/RTO (G-05, RN-18) |
| Post-metadata rollback | **NOT READY — undefined** | release-notes ("does not define rollback after membership metadata migration") | Entire procedure (G-06) |
| Authorization to execute anything | **ABSENT** | upgrade-runbook ("No target, account, host list, SSH credential, maintenance window, abort owner, backup location, data classification, stop condition, or operator authorization is supplied"); release-notes (no SSH command, restart, … authorized) | Everything execution-related (G-07) |
| Evidence base | **NOT READY** | all inputs are `NOT_EXECUTED` scenario material; incident excerpts are synthetic | A pinned build, environment identity, and executed records (G-18, G-20) |

**Overall readiness statement (design only):** the supplied sources describe *a
reviewable intent* for a rolling upgrade with a pre-metadata rollback path, but
they do not yet constitute an executable or approvable upgrade/rollback plan:
the migration trigger conflicts between documents, the rollback boundary and
post-rollback outcomes are unobservable, post-metadata rollback is undefined,
and no authorization, target, or environment exists. No upgrade, recovery, or
readiness conclusion beyond "draft produced for review" is claimed.

---

## 3. Regression impact map

Method per the installed regression-evidence guide: trace each stated change
surface to direct requirements, consumers, and recheck cases with a stated
reason. Changed surfaces are taken only from release-notes › "Change scope"
(plus the client matrix and precedence rules); nothing else is assumed to have
changed. Pinned before/after revisions do not exist (no build identity, G-20),
so this map is a design-time selection, not an evidence-backed impact analysis.

| # | Change surface (as stated) | Directly affected behavior | Recheck cases (draft) | Reason for selection | Residual gap |
|---|---|---|---|---|---|
| 1 | `docsyncd` service process (2.3.6 → 2.4.0) | Service start, readiness | TC-LU-005, TC-LU-002 | New binary version on the same host; readiness gate is the only stated observable | Non-ready responses undefined (G-03 adjacent) |
| 2 | On-disk configuration schema v1 → v2 | Config load, validation, migration | TC-LU-006, TC-LU-007, TC-LU-008, TC-LU-009, TC-LU-018 | Schema change directly changes what the service accepts and how it starts | Trigger conflict (G-01); rejection observables (G-03); other-files unknown (G-21) |
| 3 | Clustered membership metadata | Cluster membership during/after upgrade | TC-LU-003, TC-LU-011, (TC-LU-012 blocked) | Metadata format/behavior change interacts with mixed-version window and rollback boundary | Metadata format unspecified (SC-03); boundary unobservable (G-02); post-metadata rollback undefined (G-06) |
| 4 | `DOCSYNC_LISTEN_PORT` precedence rule | Effective listen port | TC-LU-010 | Explicit stated behavioral rule for upgraded members | Observation method missing (G-09) |
| 5 | Client matrix (CLI 2.3, 2.4 supported) | Client operations against 2.4.0 | TC-LU-013 | Stated support statement needs a corresponding check | CLI contract missing (G-13) |
| 6 | v1 input preservation during migration | Operator's original config | TC-LU-006 (preservation check) | Stated invariant worth an explicit check | — |
| 7 | Synthetic incident themes (restart mid-upgrade, migration-then-rollback, port override) | Motivation only | TC-LU-015 | Guide-directed risk-based adjacent selection; kept strictly separate from evidence | Synthetic provenance (G-18, G-19) |

**Smoke-level selection** (if a future authorized execution environment
existed, these would run first): TC-LU-005 (readiness), TC-LU-006 or TC-LU-009
(migration, variant per conflict resolution), TC-LU-007 (rejection rule).
**Direct-impact:** as tabulated above. **Risk-based adjacent:** mixed-version
window (TC-LU-003), rollback path (TC-LU-011). **Not selected, with reason:**
performance/load/stress/stability cases (no thresholds, G-14); security
cases (no authorization or policy, G-07/G-16); white-box cases (no source,
G-20); network-partition/disk-fill/fault-injection (no disposable target,
bounded-impact statement, or recovery procedure; design-only work must not run
these operations per domains.md; also RN-21/RB-15).

---

All cases remain `DRAFT` / `NOT_EXECUTED`. Conflicts (G-01 above all) are
preserved as conflicts. No quorum query, leader-election oracle, RPO/RTO
number, default port, capacity threshold, or fault outcome has been invented
anywhere in this document. Self-review follows in `03-review-and-handoff.md`.
