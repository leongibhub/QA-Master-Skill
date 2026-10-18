# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

A 20-minute refund charter uses recoverable order O1; one refund_id must refund 20 only once. M-1 executed two submissions and observed cumulative refund 40, evidence E1. M-2 executed a normal order view with correct amount, E2. M-3's planned weak-network retry has not started. M-4 cannot read back state because the environment disconnected. Cleanup restored O1's original amount, E3. Decide FAIL/PASS/NOT_RUN/BLOCKED with concrete steps, a charter and unfinished work.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| M-1 | FAIL |
| M-2 | PASS |
| M-3 | NOT_RUN |
| M-4 | BLOCKED |

## Verification Method

1. Give each time-box a charter: task/risk, environment/build, data, exploration scope, deadline, and evidence. Track scripted execution and exploration separately within authorization.
2. Record precondition→action→expected→actual→evidence ID→state. Not started is NOT_RUN, interrupted is INCOMPLETE, environment prevention is BLOCKED; a checklist is no execution log.
3. Prepare recoverable data/checkpoints and restore accounts/orders/config according to policy, checking residuals. Unauthorized deletion is not cleanup.
4. Under limited time complete the critical risk loop first, then preserve unfinished work, owners, and restart points. Conclusions cover observations only; missing oracles stay open.
