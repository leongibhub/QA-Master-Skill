# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Team-v1 requires one owner and commit per task_id, accepts only the current shared-state version and reassigns or escalates failed work. A-1 lets W1 and W2 claim T and write separately. A-2 rejects a stale v2 delegation while state is v3, with no effects. A-3 completes the parent despite a failed child whose unfinished work has no owner or escalation. A-4 receives a duplicate message after commit, reads completed T and ACKs without another write. Decide PASS/FAIL with ownership, version and handoff evidence.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| A-1 | FAIL |
| A-2 | PASS |
| A-3 | FAIL |
| A-4 | PASS |

## Verification Method

1. Trace task/message/correlation IDs, sender/receiver, parent delegation, scope, owner, shared-state version, and ACK using actual acceptance/rejection/termination rules.
2. Claim/commit follows the project's atomic ownership or fencing protocol. Stale/duplicate messages must not regain ownership or duplicate writes; never assume exactly-once delivery.
3. Reconcile completed, unfinished, and indeterminate effects on partial failures before reassignment. One child's failure/timeout cannot silently discard unresolved tasks.
4. Check stop propagation, ACKs, terminal states, and remaining owners; expired leases cannot commit. Include valid single claims/handoffs so message redelivery alone is not a false defect.
