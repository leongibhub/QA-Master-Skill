# Draft QA case packet

AGENT_REVIEW_ONLY. DRAFT_UNAPPROVED. Product tests NOT_EXECUTED. All cases remain incomplete for execution due to missing interface/fixtures/observables/cleanup.

| Case | Source | Scenario | Draft expected result | Helper candidate |
|---|---|---|---|---|
| TC-DRAFT-001 | F-01 | Batch size 1 | Invalid under size policy; exact rejection signal unspecified. | TC-MD-04B44BACB9EB9D2B6FB5 |
| TC-DRAFT-002 | F-02 | Rebate member=True, settled=True | Rebate allowed. | TC-MD-2E6193A290A0FCE9FFD7 |
| TC-DRAFT-003 | F-02 | Rebate member=True, settled=False | No rebate. | TC-MD-470AF2F5DC79A8AFD11E |
| TC-DRAFT-004 | F-01 | Batch size 5 | Accepted by size policy. | TC-MD-6771DCB506C2535C2986 |
| TC-DRAFT-005 | F-01 | Batch size 7 | Invalid under size policy; exact rejection signal unspecified. | TC-MD-698787358E08672685AB |
| TC-DRAFT-006 | F-01 | Batch size 6 | Accepted by size policy. | TC-MD-70B1B5D2FB5E3E118F1C |
| TC-DRAFT-007 | F-03, F-05 | REVIEW + publish | Status becomes PUBLISHED. | TC-MD-88135DDF9FDF0F3C9938 |
| TC-DRAFT-008 | F-02 | Rebate member=False, settled=False | No rebate. | TC-MD-8C675B515478FAECC901 |
| TC-DRAFT-009 | F-03, F-04 | DRAFT + submit | Status becomes REVIEW. | TC-MD-994439C082F326506657 |
| TC-DRAFT-010 | F-02 | Rebate member=False, settled=True | No rebate. | TC-MD-A628F4A9FD0280A8840A |
| TC-DRAFT-011 | F-01 | Batch size 2 | Accepted by size policy. | TC-MD-ABB52658B9F3ACB58218 |
| TC-DRAFT-012 | F-01 | Batch size 3 | Accepted by size policy. | TC-MD-BB0330A46B4CEA05F65A |
| TC-DRAFT-013 | F-03, F-06 | DRAFT + publish | Transition invalid and status remains DRAFT; no assertion about other persisted data. | TC-MD-DA8D79BFBF3E07A9AC1B |
| TC-DRAFT-014 | F-03 | Initial lifecycle state | DRAFT. | None |

Detailed actions, preconditions, oracle, cleanup, priority rationale and gap IDs are in final-cases.json. Typed missing inputs are in typed-gaps.json.

Functional/negative finite design: six boundary points (1,2,3,5,6,7), all four admissible rebate assignments, and all three explicitly declared transitions. Interior 4 belongs to accepted partition but is not a boundary point; no exhaustive integer-domain coverage claim. Initial state is separately traced. Strict-type partitions and unspecified state/event combinations remain typed gaps.

API requires target contract. White-box/integration require source/dependency contracts. Performance/load/stress/stability/compatibility require NFR inputs. Security requires authorization policy; recovery requires objective/fault contract. Regression requires change scope. These categories are assessed for applicability but are not completed design or execution coverage. Linux/kernel and AI numerical/device-specific work are N/A for the supplied document-policy facts: no such objects are described.
