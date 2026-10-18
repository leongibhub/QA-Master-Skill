# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Dictionary v1 counts new defects by distinct defect_id and first-attempt pass rate by each distinct test_id's first attempt. Events: D1 created/closed/reopened, D2 created, D1 imported twice. T1 first FAIL then rerun PASS; T2 first PASS; T3 planned without execution. K-1 claims four new defects. K-2 replaces the first failure with a rerun and claims 100% first-pass. K-3 recomputes both metrics. K-4 calls T3 passed. Decide WRONG/CALCULABLE/UNKNOWN with entity deduplication, the first-attempt denominator and missing execution.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| K-1 | WRONG |
| K-2 | WRONG |
| K-3 | CALCULABLE |
| K-4 | UNKNOWN |

| METRIC | VALUE |
| --- | --- |
| new_defects | 2 |
| first_attempt_pass_numerator | 1 |
| first_attempt_pass_denominator | 2 |

## Verification Method

1. Define purpose, statistical unit, numerator/denominator, window/timezone, filters, deduplication, missing-data handling, version, source and lineage.
2. Separate defect entities from state events, first attempts from reruns, and closure from reopening. Aggregate supplied IDs/event times; duplicates are not new defects and retries cannot inflate first-pass rates.
3. Recompute samples and check denominator coverage, delays and exclusions. Missing records remain unknown. Treat flawed records as measurement issues until product-quality evidence exists.
4. Provide worked calculations, interpretation limits, sourced action thresholds and comparability rules. Correlation does not establish cause.
