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
| REQ-001 | The product shall preserve a project/campaign state and resume it after a process restart without silently dropping recorded decisions. | `qa_master/workflow.py` | TASK-004 | TC-001 | PARTIAL | INFERRED |
| REQ-002 | The product shall ask only the next material unanswered scope question, retain an answered response, and avoid repeating it in the same project state. | `qa_master/intent.py` | TASK-004 | TC-002 | PARTIAL | INFERRED |
| REQ-003 | When a request says to design or generate cases only, the product shall plan without starting tests, external writes, or execution-result records. | `qa_master/intent.py`, workflow controls | TASK-004, TASK-009 | TC-003 | PARTIAL | INFERRED |
| REQ-004 | The product shall label source-derived behavior as a candidate and shall require human approval before it becomes a formal requirement or test oracle. | `qa_master/reverse_requirements.py`, review packet | TASK-004 | TC-004 | PARTIAL | INFERRED |
| REQ-005 | The product shall create a risk-based draft test model covering functional, API, white-box, integration, performance, load, stress, stability, compatibility, negative, security, recovery, and regression dimensions; omissions must name their reason. | Coverage and campaign modules | TASK-005, TASK-010 | TC-005 | PARTIAL | INFERRED |
| REQ-006 | The product shall support pause and resume for a campaign, preserve invalidation history, and reject stale completion attempts. | Workflow core | TASK-005 | TC-006 | GAP | INFERRED |
| REQ-007 | Enterprise adapters shall default to read-only behavior; write-capable operations shall require exact scope, artifact-bound authorization, and observable readback. | Enterprise and GitLab modules | TASK-006, TASK-009, TASK-011 | TC-007 | PARTIAL | INFERRED |
| REQ-008 | The product shall schedule and monitor an authorized remote runner only after target, command scope, timeout, artifact retention, and execution authorization are recorded. | Local runner; remote runner gap | TASK-006, TASK-010, TASK-011 | TC-008 | GAP | INFERRED |
| REQ-009 | The product shall maintain requirement-to-case-to-execution-to-defect-to-regression-to-report links and shall not close a defect without fresh retest and independent review evidence. | JUnit/release/workflow modules | TASK-005, TASK-009, TASK-010, TASK-011 | TC-009 | PARTIAL | INFERRED |
| REQ-010 | The product shall provide a usable configuration UI and documented installation path for supported local deployment; invalid configuration must show a remediable error. | `docs/CONFIGURATION.md`, `docs/verification/config-browser-smoke.md` | TASK-007, TASK-012 | TC-010 | PARTIAL | INFERRED |
| REQ-011 | The product shall not claim superiority over Awesome QA Skills unless both are evaluated with the same model, identical input set, fixed scoring protocol, expert ratings, and preserved execution artifacts. | `docs/V1_ACCEPTANCE.md` | TASK-008, TASK-012 | TC-011 | PARTIAL | INFERRED |
| REQ-012 | The product shall provide a local reproducible contract/integration environment that exercises its supported interfaces without contacting enterprise systems. | Current local test layout | TASK-004, TASK-010 | TC-012 | PARTIAL | INFERRED |
| NFR-001 | The product shall never infer approval, test execution, deployment, defect closure, or acceptance from a generated draft or process exit code. | `AGENTS.md`, acceptance tracker | TASK-005 | TC-013 | PARTIAL | INFERRED |
| NFR-002 | Evidence shall name the subject version, environment, executor, observed time, and provenance status; missing information shall be `PENDING`, `NOT_AVAILABLE`, or `NOT_EXECUTED`. | Existing evidence docs; governance baseline | TASK-001 | TC-014 | PARTIAL | INFERRED |
| NFR-003 | Configuration and artifacts shall not store passwords, tokens, cookies, private keys, or customer secrets in repository files or reports. | Repository contract | TASK-006 | TC-015 | PARTIAL | INFERRED |
| NFR-004 | Network, load, destructive, and external-write operations shall require explicit operation-specific authorization; planning and dry-run output shall remain distinguishable from execution. | Existing module boundaries | TASK-006 | TC-016 | PARTIAL | INFERRED |

## Current gaps and next evidence

The V1 acceptance tracker cannot turn local evidence into a release conclusion. `TASK-002` recorded the failing `77e3b5d` source baseline and a later observed 375-test continuation run plus wheel smoke for an explicit shared-worktree fingerprint; its subprocess warning remains open and a final-revision independent run is still required. `TASK-003` remains the independent gap/review audit. Late-registered tasks record current development scope only. Enterprise E2E remains `NOT_EXECUTED` by scope, rather than a precondition for local product development.
