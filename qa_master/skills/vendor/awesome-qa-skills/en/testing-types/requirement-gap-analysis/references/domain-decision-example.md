# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

G1 refund requirement defines roles, amounts, duplicate IDs, failures, and closure when the ledger succeeds and balances reconcile. G2 permits pausing tasks but defines no terminal/closure condition. G3 references missing appendix B. G4 same-version rules give both7 and14 days. G5 scope is web-only and explicitly excludes native push. Decide COMPLETE/MISSING_RULE/MISSING_MATERIAL/CONFLICT/N/A; show G2's impact and closure evidence without false findings on G1.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| G1 | COMPLETE |
| G2 | MISSING_RULE |
| G3 | MISSING_MATERIAL |
| G4 | CONFLICT |
| G5 | N/A |

## Verification Method

1. Build a versioned checklist of applicable roles, states, rules, exceptions, and closure conditions, tied to supplied sources. Do not force irrelevant checklist items onto a product.
2. Separate MISSING_RULE (relevant but undefined behavior), MISSING_MATERIAL (referenced evidence absent), CONFLICT, N/A (evidenced scope exclusion), and COMPLETE.
3. Give requirement ID, missing content, affected scenarios, blockage, owner, and minimal clarification. An unseen field or empty document does not by itself prove a product defect.
4. Close only with authoritative added rules/source version and testable expectations, updating traceability. Unapproved suggestions remain proposals; complete controls must not receive invented gaps.
