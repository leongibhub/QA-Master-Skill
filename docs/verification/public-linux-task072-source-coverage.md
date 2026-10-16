# TASK072 source-coverage supplement after participant freeze

Artifact: DOC-PUBLIC-LINUX-QA-COVERAGE-001. Evidence: EVD-PUBLIC-LINUX-QA-TEST-001 (proposed for governance registration). Runtime work-bef340f1e1c7417d90e96f228b607bbd, attempt 1. This is an independent document/source trace audit, not a quality PASS, score, comparison, acceptance, Gate, release or product-validity decision.

The TASK071 retained output remains OUTPUT_RETAINED_NOT_ASSESSED for quality verdict purposes; this supplement adds source-coverage observations without relabeling it as a quality success. TASK070 freeze `2f9ec205446b03f1871dc5e5784e8d3724c90ad3`, participant output commit `c3a52ff83ae6c520866046fc36409e957a7f5dc8`, original manifest `04BBAFACBF69D930AC483F2DCBA48B432924C5EA778836780BD8792D21019C50` superseded by the provenance-corrected manifest `D59C93AE8810B4F9BB0F20A824592796A0B32733C00741F7B254FBCBE2445E21` at `cd4a7d97bb86ff85891db7f410e17fad91b0f53c` (recorded by EVD-PUBLIC-LINUX-QA-PARTICIPANT-MANIFEST-CORRECTION-001; participant file bytes unchanged — the five participant output hashes are identical in both manifest versions).

## Method and released audit material

After participant output was frozen, governance released audit-ledger.md and expected-review-checklist.md for this follow-up audit. Tester read both in full, all five frozen input sources in full, and all five retained participant output files in full. Ledger SHA `3DABC312A4D11ED7AA329C3DD39AB815313810FEBFBCFEDF824CA6282DAEF353`; checklist SHA `F9E0019CA54D173FC318498CFF1EABCC165039EAA25288B3029F33F50AE26BF5`; both byte-identical to the TASK070 freeze record. They are source-location/check themes, not hidden JSON, mandatory F-IDs, ordering, case-count or scoring rules. Labels below are auditor navigation aids only.

S = retained `01-review-and-strategy.md`; C = retained `02-draft-cases.md`; H = retained `03-review-and-handoff.md`; RA = retained `read-audit.md`; HO = retained `handoff.json`. TC-LU/G/RN/RB/SC/IE identifiers are the participant's existing natural Markdown labels. All retained files are under `docs/verification/evidence/linux-task-001/attempt1` and their hashes were rechecked unchanged against the retained manifest before this audit. No participant output was edited or rerun.

## Integrity reconciliation (retained bytes, preparation, inputs, postcheck)

| Reconciliation item | Result | Evidence |
|---|---|---|
| Five participant output files byte-identical between `.qa-master\linux-task-001\participant\output` and retained attempt1 directory | Confirmed (SHA256 pairwise equal; five hashes match manifest) | F9200527…B86B38, A0C43D7E…75E35, 5E597295…DC4ED, B48F6B5C…B4BD6, DE5827D5…D098A |
| Manifest eight-file hash table matches actual bytes in attempt1 | Confirmed (8/8) | corrected manifest `D59C93AE…2445E21` (original `04BBAFAC…919C50` superseded; five participant-file entries identical in both) |
| Five participant inputs match TASK070 frozen SHA256/bytes | Confirmed (5/5) | source-freeze.md table |
| Installed Skill 59 files match install stamp and current a9df285 source | Confirmed (59/59; `references/design-methods.md` and `examples/design-methods.json` differ from repo blob only by LF/CRLF normalization, content identical; `scripts/qa.py` matches the deterministic generator in `codex_skill.py` byte-for-byte; remaining 56 files byte-identical to `a9df285` tree) | `.qa-master-install.json` SHA `9c1c9ea7…467d7`, wheel `cfd10bcd…e3d163` |
| Install stamp = preparation `manifest_sha256`; wheel = preparation `wheel_sha256` | Confirmed | preparation.json |
| Output directory contains exactly the five declared files | Confirmed | directory listing |
| postcheck claims (`sources_unchanged`, `installed_bundle_unchanged`, 59 files) | Re-verified independently during this audit | postcheck.json |
| Manifest field-provenance correction | Recorded; participant bytes unaffected; correction evidence VERIFIED with scope limited to provenance | EVD-PUBLIC-LINUX-QA-PARTICIPANT-MANIFEST-CORRECTION-001 |

## Ledger-by-ledger source mapping

| Ledger row (source location / visible fact) | Actual participant mapping | Trace observation and remaining source limit |
|---|---|---|
| release-notes / Change scope: schema v1→v2 affects service, local config, membership metadata | S RN-01/02/03; C TC-LU-014 rows 1–3; H §2 | All three stated change surfaces are extracted as FACT and drive the regression map. Cluster-only scope (RN-03) is retained; no single-node procedure is invented. |
| release-notes / supported path + support table: only two named OS/kernel/x86_64 combinations | S RN-04/05/07, SC-01; C TC-LU-001 | The four-row support matrix and upgrade-path pair are used exactly; unsupported/unknown combinations are out-of-scope by citation, no support invented. |
| release-notes / supported path: one upgraded plus two 2.3.6 members communicate during rolling upgrade | S RN-06; C TC-LU-003 | Mixed-version window modeled at the stated combination only; no other version pair asserted. |
| release-notes / supported path: two voting members remain ready | S RN-09, RB-02; C TC-LU-002/004 | Used as precondition/readiness gate; per-member `/healthz` only; no quorum query or leader semantics invented (G-08). |
| release-notes / health + support observable: Ready is `/healthz` HTTP 200 `ready:true` | S RN-10, SC-11; C TC-LU-005 and readiness anchors throughout | Exact observable named; absent health observables (non-ready contract) retained as gap (G-03 adjacent, SC-12). |
| release-notes / migration: first 2.4 start reads v1, writes v2 copy, preserves v1 input | S RN-12/13; C TC-LU-006 (variant A) | Source-bound migration/persistence case drafted with input-preservation check; "other local files" absence kept open (G-21, TC-LU-018 exploratory). |
| upgrade-runbook / configuration statement: operator must run `docsync config-migrate` before start | S RB-08/09/10, G-01; C TC-LU-009 (variant B) | The sequence ambiguity is preserved as SOURCE_CONFLICT G-01: both variants drafted, neither baselined, no resolution assumed. Runbook's own unknowns (authorization, exit codes, partial migration) are gaps G-11/G-12. |
| support reference / v2 fields: storage.path/listen.port required; missing-field rejection has no stated signal/state | S SC-04/05/06/07, G-03; C TC-LU-007/008 | Field/readiness coverage drafted; rejection result stated, all rejection observables marked pending, not guessed. |
| runbook + support / precedence: env port override wins; no default/effective-config observer | S RB-12/13/14, SC-08/09, G-09/G-10; C TC-LU-010 | Precedence rule addressed; observation method and env-supply policy retained as gaps; no default port invented. |
| release-notes / rollback: pre-membership-metadata rollback has specified high-level steps | S RN-15/16, RB-06; C TC-LU-011 | Pre-migration rollback readiness drafted only; post-rollback `/healthz` offered as candidate observable, explicitly labeled not-a-source-oracle. |
| release-notes / rollback boundary: post-metadata rollback, backup integrity, reconciliation, RPO/RTO absent | S RN-17/18, G-04/G-05/G-06; C TC-LU-012 blocked | Explicit gaps; no durability/recovery success claimed anywhere. |
| support reference / cluster facts: leader/partition/replication/consistency/degraded absent | S SC-03, G-15; C TC-LU-003 limit note | No fault, quorum, data or retry oracle invented; mixed-version case limited to readiness observables. |
| release-notes / client boundary: CLI 2.3/2.4 supported; browser/db/proxy/third-party absent | S RN-19/20, G-13; C TC-LU-013 | Support matrix honored; honest compatibility gaps; scenario-level case only pending CLI contract. |
| release-notes / thresholds: no capacity/resource/NFR thresholds | S RN-11, SC-03, G-14; C §1 method table | NFR planning/readiness only; no numeric pass threshold set. |
| incident A: unidentified narrative "cluster looked healthy" | S IE-02, G-18; C TC-LU-015 | Classified as unverified synthetic narrative; used as motivation only; no result derived. |
| incident B: 2.4.0-rc2 and 2.3.6 logs mixed | S IE-03, G-19; C TC-LU-015 | Mixed build separated from any final-build retest evidence; rc2 noted as absent from all supported matrices. |
| incident C: port-override statement lacks effective config/build/reproduction | S IE-04; C TC-LU-015 | Evidence requested via TC-LU-010 pending-observation framing; no configuration success asserted. |
| all source boundaries: no target/account/authorization/maintenance window/abort owner/cleanup | S RB-15, RN-21, G-07/G-20; C opening boundary statement; H §1.1, §4.4 | All cases remain draft/NOT_EXECUTED; execution prerequisites retained as gaps. |

No ledger row lacked a trace to a case, gap, conflict or scoped limitation in this retained package. This is a finite source-trace observation, not a coverage percentage, completeness guarantee for the real product, or quality grade. Known source gaps remain gaps even when linked.

## Checklist reconciliation

| Released checklist item | Retained location / observation |
|---|---|
| Natural source/guide read record | RA lists all 15 files read with byte hashes (5 inputs + 10 installed guides); S §1 source notation table; HO `sources` array carries the same 15 hashes. |
| Scope and method applicability | S §4 method table for 13 methods with source-grounded applicability reasons; helper noted-not-used §4; H §1.7. |
| Source-grounded rolling-upgrade, migration, compatibility, rollback, regression drafts | C TC-LU-001..005 (upgrade/compatibility), TC-LU-006..010 (migration/config), TC-LU-011/012 (rollback), TC-LU-014 + §3 map (regression); §2 readiness view. |
| Non-functional/recovery readiness view | C §2 readiness table (14 rows, each with what-is-missing column); recovery limited to design (TC-LU-011) with G-04/G-05 gaps; NFR targets explicitly not set (G-14). |
| Explicit gaps/limitations | S §3 typed register G-01..G-22 (15 distinct types); blocked gaps recorded as non-cases (TC-LU-012/016/017); H §2 self-identified weaknesses; HO `open_questions`. |
| Per-case fields: label, citation, precondition/setup, state/data, action, observable expected result, readiness, cleanup-or-reason | Every TC-LU-001..018 row carries all eight fields; blocked gaps state "not designable" per field with the reason; cleanup "none stated" is accurate to sources, not an omission. |
| Supported OS/kernel/arch known vs unknown compatibility | TC-LU-001 (four-row matrix + out-of-scope rule RN-07); S RN-04/05/07, SC-01. |
| Rolling one-member sequence, mixed-version, two-ready precondition | TC-LU-002, TC-LU-003, TC-LU-004; readiness gating observable RN-10/SC-11. |
| healthz readiness and stated limits | TC-LU-005 (positive contract only; negative side design-blocked per SC-12). |
| v1→v2 migration, preserved input, required v2 fields | TC-LU-006 (variant A), TC-LU-007 (rejection), TC-LU-008 (acceptance ± metrics.enabled). |
| Automatic-first-start vs manual-migration ambiguity | G-01 preserved; TC-LU-006 vs TC-LU-009 as equal-status variants; D-01 pending decision; readiness row marked CONFLICT—NOT READY. |
| Config precedence without made-up port/default/effective observer | TC-LU-010 with G-09/G-10 pending; no default port invented; H §1.5 flags the /healthz-port circularity. |
| Pre-metadata rollback and unknown post-metadata boundary | TC-LU-011 (conditional oracle, candidate observable labeled as such); TC-LU-012 BLOCKED GAP. |
| Recovery/durability/backup/reconciliation/RPO/RTO gaps | G-04/G-05; RN-18 absence extracted; no drill plan thresholds invented. |
| Capacity/inode/resource/partition/leader/consistency gaps | G-14 (thresholds), G-16 (storage/permissions), G-15 (leader/consistency); corresponding method rows N/A with reasons. |
| Change-impact regression selection | C §3 seven-surface map with per-row reason and residual gap; smoke/direct/risk-adjacent/not-selected-with-reason classes. |
| Synthetic incident excerpts' unverified/mixed/incomplete provenance | IE-01..04 declared synthetic; TC-LU-015 motivation-only with no expected result; G-18/G-19; excluded from any evidence base. |

## Disqualifying-defect check

| Checklist disqualifier | Finding in retained output |
|---|---|
| Incident excerpt treated as final-build execution evidence | Not found. TC-LU-015 states no expected result from excerpts; G-18/G-19 quarantine them; H §4.5 keeps them out of any future evidence report. |
| Process step treated as proof of durability/recoverability | Not found. TC-LU-011 conditional oracle explicitly disclaims reconciliation; G-04/G-05 retain RPO/RTO/backup-integrity absences. |
| Silent fix of manual/automatic migration sequence | Not found. G-01 is a typed SOURCE_CONFLICT; both variants kept open; D-01 pending; readiness row NOT READY. |
| Invented quorum/leader, RPO/RTO, capacity, default-port, target, authorization, backup-integrity, cleanup or fault outcome | Not found. G-08/G-09/G-14/G-16/G-07 gaps; cleanup fields say "none stated" with reason; fault/partition/disk-fill explicitly not selected (C §3). |
| Omitted reviewable action/observable | Not found. All 18 TC-LU rows have action + observable-or-explicitly-pending; blocked rows state why design is impossible. |
| Claimed result, approval, acceptance, release, comparison or superiority | Not found. Every file header carries PUBLIC_DEVELOPMENT/DRAFT_UNAPPROVED/NOT_EXECUTED; HO `execution: NOT_EXECUTED`, `scope` all false; H §5 claims-deliberately-not-made. |

## Independent audit questions (ledger footer)

- **Does the package trace all source facts/absences to a case, conflict, gap, or justified scope decision?** Yes within the audited set: 18/18 ledger rows map (table above); 43 candidate facts (RN×21, RB×15, SC×12 minus overlaps noted by participant) each carry a citation; every ABSENCE row lands in a typed gap.
- **Does it distinguish an upgrade process step from a durability/recovery proof?** Yes: TC-LU-002/003 sequence steps are readiness-observation designs; durability/recovery proofs are absent by design (G-04/G-05) and TC-LU-011's candidate observable is labeled a review candidate, not a source oracle.
- **Does it separate mixed or unidentified incident material from a pinned final-build retest?** Yes: G-18/G-19 + TC-LU-015; no build identity exists (G-20) so no retest evidence is asserted.
- **Does every proposed case state an action and an available/pending observable without inventing an external result?** Yes: available observables anchor to `/healthz` and file existence/content; pending observables are marked with gap IDs; no external result is invented.

## Additional observations (not defects)

- H §5 states "counts approximate for review convenience only" for the 43-fact tally; actual table counts (RN 21, RB 15, SC 12, IE 4 = 52 rows including overlaps and provenance notes) differ from the narrative "22 FACT, 14 ABSENCE, 3 SYNTHETIC" because the participant counts its own §2.1–2.4 kinds, not table rows. This is a labeling convenience inconsistency, not a source-trace defect; no fact row is unsupported.
- The deliberate non-invention of port values means TC-LU-010's setup references "distinct values from the member's actual environment" — executable only after D-06; correctly blocked rather than fabricated.
- H §1.5's `/healthz`-port circularity observation (readiness checked on a port whose default is undefined while TC-LU-010 tests precedence) is itself source-faithful: the sources create this circularity, and the participant flags it rather than resolving it.

## Boundaries and evidence

No participant rerun, output rewrite, helper execution, host/service access, credential use or product test occurred during this audit. Releasing audit aids after freeze does not retroactively grant participant access or establish host isolation. Prompt-scope/read-audit limits (`PROMPT_SCOPED_NOT_OS_ENFORCED`, `PARTICIPANT_DECLARED_NOT_HOST_ACCESS_ATTESTATION`) from the retained record remain in force. This supplement is source coverage only; it preserves OUTPUT_RETAINED_NOT_ASSESSED for the final quality verdict and makes no score, comparison, acceptance, Gate or release decision. A separate reviewer may assess practical drafting usability and identify further findings.

Evidence directory `docs/verification/evidence/linux-task-001/coverage-task072` holds input/output hashes and this supplement's manifest with text transformations disabled.
