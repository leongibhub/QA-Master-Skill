# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

T1 arrives at0min, waits for environment0–40, executes40–50, reworks50–60, completes60; runner is idle while waiting. B1 identifies the largest phase. Matched daily tasks:concurrency2 completes10/hour withWIP4;concurrency4 completes6/hour withWIP8 and increasedDB lock waits. B2 claims more concurrency always helps. B3 calls40min waiting proof of understaffing. B4 proposes DB contention requiring controlled confirmation. Decide DEPENDENCY_WAIT/UNSUPPORTED/HYPOTHESIS, separating10min execution and10min rework from60min cycle.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| B1 | DEPENDENCY_WAIT |
| B2 | UNSUPPORTED |
| B3 | UNSUPPORTED |
| B4 | HYPOTHESIS |

| METRIC | VALUE |
| --- | --- |
| dependency_wait_minutes | 40 |
| execution_minutes | 10 |
| rework_minutes | 10 |

## Verification Method

1. Fix window, work IDs/complexity, arrival/completion, and state events. Separate queue/dependency waiting, execution, rework, handoffs, and blockers; total cycle time is not labor.
2. WIP counts unfinished items; throughput counts completed items per matching window. Measure cycle/stage times separately and disclose missing events/sampling; averages alone establish no cause.
3. Identify the limiting stage/upstream dependency using utilization, arrivals, and completions. Idle resources may be blocked on materials/environment; more concurrency may increase contention and reduce throughput.
4. Propose small measurable interventions, matched before/after metrics, and rollback signals. Staffing shortage is a hypothesis, not a conclusion from waiting time or a personal ranking.
