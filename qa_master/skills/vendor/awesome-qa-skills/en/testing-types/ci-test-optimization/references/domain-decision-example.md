# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Same commit/test-set/runner:baseline queue20s, install30s, parallel test jobs60s/40s, report5s, no retries. CI-1 valid cache cuts install to10s, identical other phases and fault detection. CI-2 removes money regression job, misses the fault. CI-3 uses || true after job failure and reports green. CI-4 reuses old cache after lockfile change without validation. Decide ACCEPT/REJECT/UNKNOWN, showing baseline/CI-1 end-to-end time and critical path.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| CI-1 | ACCEPT |
| CI-2 | REJECT |
| CI-3 | REJECT |
| CI-4 | UNKNOWN |

| METRIC | VALUE |
| --- | --- |
| baseline_seconds | 115 |
| candidate_seconds | 95 |

## Verification Method

1. Fix commit/run/runner/config/test-set identities. Decompose events into queue, checkout/install, setup, execute, retry, and report; separate end-to-end waiting from runner busy time.
2. Compute the actual DAG critical path without summing overlapping jobs. Preserve retry counts and original failures; retry green cannot erase first failure.
3. Cache keys include relevant lockfile/toolchain/config identity. Compare cold/warm runs, hits, and invalidation evidence; mismatched cache cannot bypass dependency validation.
4. Match before/after protection obligations, tests, fault detection, resources, and windows. Reject speedups through dropped tests/swallowed failures; propose measurable gains and rollback signals.
