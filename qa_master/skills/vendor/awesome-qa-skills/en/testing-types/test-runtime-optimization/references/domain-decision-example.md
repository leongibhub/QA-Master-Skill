# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Matched commit, obligations, and2-worker limit. Baseline setup20s, tests A60s/B40s sequentially, teardown10s. T1 isolates data and runs A/B in parallel; setup/teardown unchanged, same amount fault still detected. T2 shares an account and misses the fault. T3 uses a different test set and takes10s. T4 is only an unexecuted estimate. Decide ACCEPT/REJECT/NOT_COMPARABLE/ESTIMATE and compute baseline/T1 critical-path time with cold/warm cache context.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| T1 | ACCEPT |
| T2 | REJECT |
| T3 | NOT_COMPARABLE |
| T4 | ESTIMATE |

| METRIC | VALUE |
| --- | --- |
| baseline_seconds | 130 |
| candidate_seconds | 90 |

## Verification Method

1. Profile setup, execution, teardown, and retries with matched commit, obligations, data, resources, and windows. Derive DAG critical paths without adding overlapping jobs.
2. Separate cold/warm cache, runner limits, concurrency, isolated data, and contention. Record changed factors; different test volumes/environments cannot prove speedups.
3. Recheck the same business fault against effective assertions while retaining failures/logs/traces. Parallelism cannot share conflicting accounts or swallow errors; faster time cannot offset lost protection.
4. Give baseline/candidate duration, resource cost, percentage gain, and rollback signals. Comparable actual runs establish observed gains; estimates remain candidates, not production guarantees.
