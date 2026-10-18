# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

E1 two instances, fixed mix; SLO p95<=200ms. Measurements:100RPS:p95=150ms/CPU55%;150RPS:p95=260ms. K-1 claims300RPS from CPU55%. K-2 constant arrival130RPS, validated service100RPS, scaling wait60s; calculate backlog. K-3 no one-instance-loss measurements. K-4 measured100RPS satisfies SLO. Decide UNSUPPORTED/CALCULABLE/UNKNOWN/SUPPORTED with conditions/provenance.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| K-1 | UNSUPPORTED |
| K-2 | CALCULABLE |
| K-3 | UNKNOWN |
| K-4 | SUPPORTED |

| METRIC | VALUE |
| --- | --- |
| backlog_requests | 1800 |

## Verification Method

1. For each point record environment/config/instances, workload mix, arrival/completion throughput, latency percentiles, errors, CPU/memory/queues, and window. Trace measurement→SLO→candidate capacity.
2. Estimate only within measured SLO-acceptable regions. CPU percentage cannot linearly predict throughput; unmeasured points remain candidates constrained by downstream saturation/scaling delay.
3. Under supplied constant-rate/queue assumptions, scaling-wait backlog=max(0,arrivals−validated service rate)×wait seconds; check backlog latency/recovery, not only totals.
4. Use measured or explicitly conditional capacity after project-specified instance/dependency failure. Missing failure data cannot establish adequate headroom; margin, growth, cost, and acceptance come from the project.
