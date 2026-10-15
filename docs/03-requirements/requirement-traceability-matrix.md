# QA Master V1 requirement traceability matrix

- Artifact ID: `DOC-RTM-001`
- Document State: `DRAFT`
- Evaluation State: `IN_REVIEW`
- Baseline source: `DOC-CONTEXT-001` and current user direction, 2026-10-14
- Evidence boundary: all requirements below are a continuation baseline. They are `INFERRED` until a human approves a versioned product/requirement baseline.

## Traceability rules

`COMPLETE` requires a current link through design, implementation task/change, test case, and execution/review evidence. Existing source files and historical Markdown assertions provide only `OBSERVED` or `INFERRED` implementation context. They do not prove a release, customer acceptance, external integration, or comparison outcome.

| ID | Requirement and measurable acceptance | Design / source context | Planned task | Test case family | Current traceability | Evidence Status |
|---|---|---|---|---|---|---|
| BG-001 | Deliver one original, installable QA Master product that safely guides a test request from analysis through report. | `README.md`, `AGENTS.md` | TASK-001 | TC-001 | PARTIAL | OBSERVED |
| PRD-001 | Provide one product entry point and installed package; it must not require a separate QA-Skill repository. | `README.md`, `skills/qa-master/` | TASK-004 | TC-001 | PARTIAL | INFERRED |
| REQ-001 | The product shall preserve a project/campaign state and resume it after a process restart without silently dropping recorded decisions. | `DES-019` v3; schema-v2 service | TASK-004, TASK-019–025 | TC-001, TC-SM-001/002/004 | PARTIAL | OBSERVED |
| REQ-002 | The product shall ask only the next material unanswered scope question, retain an answered response, and avoid repeating it in the same project state. | `DES-019` v3; canonical questions projection | TASK-004, TASK-019–025 | TC-002, TC-SM-004/007 | PARTIAL | OBSERVED |
| REQ-003 | When a request says to design or generate cases only, the product shall plan without starting tests, external writes, or execution-result records. | `DES-019` v3; application service controls | TASK-004, TASK-009, TASK-018–025 | TC-003, TC-SM-003/006 | PARTIAL | OBSERVED |
| REQ-004 | The product shall label source-derived behavior as a candidate and shall require human approval before it becomes a formal requirement or test oracle. | `qa_master/reverse_requirements.py`, review packet | TASK-004 | TC-004 | PARTIAL | INFERRED |
| REQ-005 | The product shall create a risk-based draft test model covering functional, API, white-box, integration, performance, load, stress, stability, compatibility, negative, security, recovery, and regression dimensions; omissions must name their reason. | Coverage and campaign modules | TASK-005, TASK-010 | TC-005 | PARTIAL | INFERRED |
| REQ-006 | The product shall support pause and resume for a campaign, preserve invalidation history, and reject stale completion attempts. | `DES-019` v3; `CODE-SCHEMA-MIGRATION-REPAIR-001` v1 | TASK-019–025 | TC-SM-004/005/010 | PARTIAL | OBSERVED |
| REQ-007 | Enterprise adapters shall default to read-only behavior; write-capable operations shall require exact scope, artifact-bound authorization, and observable readback. | Enterprise and GitLab modules | TASK-006, TASK-009, TASK-011, TASK-015, TASK-016 | TC-007 | PARTIAL | INFERRED |
| REQ-008 | The product shall schedule and monitor an authorized remote runner only after target, command scope, timeout, artifact retention, and execution authorization are recorded. | Local runner; remote runner gap | TASK-006, TASK-010, TASK-011, TASK-014, TASK-017 | TC-008 | GAP | INFERRED |
| REQ-009 | The product shall maintain requirement-to-case-to-execution-to-defect-to-regression-to-report links and shall not close a defect without fresh retest and independent review evidence. | JUnit/release/workflow modules | TASK-005, TASK-009, TASK-010, TASK-011, TASK-013, TASK-016 | TC-009 | PARTIAL | INFERRED |
| REQ-010 | The product shall provide a usable configuration UI and documented installation path for supported local deployment; invalid configuration must show a remediable error. | `docs/CONFIGURATION.md`, `docs/verification/config-browser-smoke.md` | TASK-007, TASK-012 | TC-010 | PARTIAL | INFERRED |
| REQ-011 | The product shall not claim superiority over Awesome QA Skills unless both are evaluated with the same model, identical input set, fixed scoring protocol, expert ratings, and preserved execution artifacts. | `docs/V1_ACCEPTANCE.md` | TASK-008, TASK-012 | TC-011 | PARTIAL | INFERRED |
| REQ-012 | The product shall provide a local reproducible contract/integration environment that exercises its supported interfaces without contacting enterprise systems. | Current local test layout | TASK-004, TASK-010 | TC-012 | PARTIAL | INFERRED |
| NFR-001 | The product shall never infer approval, test execution, deployment, defect closure, or acceptance from a generated draft or process exit code. | `AGENTS.md`, acceptance tracker | TASK-005 | TC-013 | PARTIAL | INFERRED |
| NFR-002 | Evidence shall name the subject version, environment, executor, observed time, and provenance status; missing information shall be `PENDING`, `NOT_AVAILABLE`, or `NOT_EXECUTED`. | Existing evidence docs; governance baseline | TASK-001 | TC-014 | PARTIAL | INFERRED |
| NFR-003 | Configuration and artifacts shall not store passwords, tokens, cookies, private keys, or customer secrets in repository files or reports. | `DES-019` v3; repaired status projection | TASK-006, TASK-009, TASK-015, TASK-017–025 | TC-015, TC-SM-013 | PARTIAL | OBSERVED |
| NFR-004 | Network, load, destructive, and external-write operations shall require explicit operation-specific authorization; planning and dry-run output shall remain distinguishable from execution. | `DES-019` v3; application service controls | TASK-006, TASK-009, TASK-015, TASK-017–025 | TC-016, TC-SM-003/012 | PARTIAL | OBSERVED |

## Current gaps and next evidence

CR-007 has a bounded local canonical-state result: `1c35b25` repair, independent fixed-subject retest (13 focused and 411 strict tests, compileall and fresh-wheel smoke), and independent review `PASS WITH P3 FOLLOW-UP`. The earlier `830d231` independent failure (BUG-003–005) remains retained. P3 follow-up remains: a dedicated scope/approval replacement subcase for TC-SM-010, and independent POSIX directory-fsync fault/power-loss qualification. This does not complete the inferred requirements baseline, full V1, a Gate, production authority, remote execution, or enterprise E2E.

The V1 acceptance tracker cannot turn local evidence into a release conclusion. `TASK-002` records historical strict 385-test evidence at `73a86bb`; CR-007 separately records 411-test independent retest evidence at `1c35b25`, bounded review, and current CI. The installed CLI is now unified behind the canonical service, while old Python APIs remain compatibility facades. The trace remains incomplete because requirements are inferred, lifecycle artifacts/design baselines are not complete, and full product capability still lacks authenticated authority, remote execution, enterprise validation, professional depth and paired evaluation. Enterprise E2E remains `NOT_EXECUTED` by scope, rather than a precondition for local product development.
