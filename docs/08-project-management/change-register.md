# QA Master V1 change register

- Artifact ID: `DOC-CHANGE-001`
- Document State: `DRAFT`
- Evaluation State: `IN_REVIEW`

| Change | Reason and impact | Approval | Current evidence | Follow-up work |
|---|---|---|---|---|
| CR-001 | Review-directed enterprise Jira journal/readback and GitLab HTTP correction. Affects REQ-007, REQ-009 and NFR-001–004. Prior enterprise output is retained as history. | NOT_AVAILABLE | Current frozen-candidate test/review scope includes this local correction; no external system operation is claimed. | TASK-013 / work-7448e268b6a044dd807c35b81c606e8c |
| CR-002 | Review-directed local-runner absolute executable and minimal-environment binding correction. Affects REQ-008 and NFR-001–004. Prior runner output is retained as history. | NOT_AVAILABLE | Current frozen-candidate test/review scope includes this local correction; no remote runner execution is claimed. | TASK-014 / work-b218a56587ed452792c168a0ab0d049f |
| CR-003 | Post-work API generated-test credentialed-HTTP and explicit authorization-guard correction. Affects REQ-007 and NFR-001/003/004. | NOT_AVAILABLE | `CODE-ROOT-SECURITY-001` v3 pins `18e92b1`; local strict test and review cover the source. No host authority or API execution is claimed. | TASK-015 |
| CR-004 | Post-work Jira typed-subset readback correction. Affects REQ-007, REQ-009 and NFR-001–004. | NOT_AVAILABLE | `CODE-JIRA-RECOVERY-001` v2 pins the frozen source. Local contract evidence exists; no Jira system was accessed. | TASK-016 |
| CR-005 | Final runner output-destination/timeout binding, replay and secret-argv rejection. Affects REQ-008 and NFR-001–004. | NOT_AVAILABLE | `CODE-LOCAL-RUNNER-HARDENING-002` v2 pins `18e92b1`; local strict test/review cover the source. No remote execution is claimed. | TASK-017 |
| CR-006 | Cross-platform CLI JSON and synthetic runner-fixture correction after CI run `38573216585` failed. Affects REQ-003 and NFR-003/004. | NOT_AVAILABLE | Local `73a86bb` / remote-equivalent `d0ff0a` has strict local test, fresh-wheel portability review, and two successful GitHub CI API-readback runs. This does not provide enterprise execution or release evidence. | TASK-018 |
| CR-007 | Current-direction planning record for canonical CLI/Campaign/Workflow schema migration and durable pause/resume. Candidate impact on REQ-003/004/005/006 and NFR-001/003/004 is pending architecture analysis; no requirement baseline has changed. | NOT_AVAILABLE | Direction observed and design→development→independent-test→independent-review work chain registered. There is no implementation, test, approval, or Gate evidence for this change. | TASK-019–022 / `docs/08-project-management/schema-migration-continuation-plan.md` |

CR-001 through CR-006 are late registrations for corrections already observed in the worktree. CR-007 is a new, forward-looking continuation record created before design and implementation. The current frozen candidate has independent local test and review evidence; it has no human approval, release decision, enterprise E2E, or remote-execution evidence. The review's full-V1 conclusion remains `FAIL`.
