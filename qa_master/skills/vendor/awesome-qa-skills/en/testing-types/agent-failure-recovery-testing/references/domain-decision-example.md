# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Protocol R-v2: one debit per operation_id; query state before retrying uncommitted steps; permanent permission errors stop and escalate. F-1: pay-1 debit commits, response times out, retry debits again, two entries for the same op. F-2: steps 1/2 commit; recovery executes only step 3, with one entry per step. F-3: five unchanged retries follow permanent 403. Decide PASS/FAIL per trace, required recovery branch, final state, and evidence.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| F-1 | FAIL |
| F-2 | PASS |
| F-3 | FAIL |

## Verification Method

1. Build failure | confirmed write state | retryability | retry/compensate/escalate | recovered state | evidence from the project protocol. Separate transient, permanent, and indeterminate outcomes.
2. A timeout does not mean no execution: query committed effects by operation_id/idempotency key before replay. Read back an existing result or retry safely; the same key must not produce a second business write.
3. For partial success reconcile completed and remaining steps. Compensate only under the supplied protocol and authority, recording each outcome; failed compensation escalates.
4. Stop unchanged retries for permanent errors and notify the owner. Compare business state, attempt count, user-visible outcome, and resources before/after recovery; missing logs leave recovery unverified.
