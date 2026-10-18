# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Loop-v4: escalate after 3 consecutive no-progress cycles; hard cost budget 1 unit stops at exhaustion. B-1: same search arguments/observation repeat 3 times without change, followed by a fourth call. B-2: only 2 repetitions but cost reaches 1; no further call, terminal budget_stop. B-3: each of 3 calls obtains new relevant records, advances the goal, cost=0.6; work continues. Decide PASS/FAIL and explain deduplication and budget precedence.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| B-1 | FAIL |
| B-2 | PASS |
| B-3 | PASS |

## Verification Method

1. Record task/run/step IDs, plan, tool and normalized arguments, observation identity/digest, business state delta, and cumulative time/cost; redact sensitive values while preserving deduplication evidence.
2. Progress requires new goal-relevant evidence or state advancement. Repeated action/observation with no advancement counts as a no-progress cycle; successful calls or repeated prose do not establish progress.
3. Apply supplied no-progress limits, retry policy, and time/cost budgets. Safety/cancellation stops immediately; any exhausted hard budget precedes more planning. Ask for missing limits rather than invent numbers.
4. Repetition takes the project-authorized change-strategy, stop, or escalation branch. Report trigger step, termination class, remaining work, and absence of extra effects.
