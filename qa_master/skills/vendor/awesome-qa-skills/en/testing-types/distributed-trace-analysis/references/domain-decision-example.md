# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Single clock:root R[0,100]ms; synchronous children A[10,70], B[40,90], both parent=R. X-1 claims end-to-end210ms by100+60+50. X-2 asks for observed exclusive time of R. X-3 asynchronous C links to R, no timing, asserted as root cause. X-4 queue enqueue20/dequeue35ms. Decide WRONG/CALCULABLE/UNKNOWN; show interval union and queue calculation without root-cause inference from duration.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| X-1 | WRONG |
| X-2 | CALCULABLE |
| X-3 | UNKNOWN |
| X-4 | CALCULABLE |

| METRIC | VALUE |
| --- | --- |
| observed_exclusive_ms | 20 |
| queue_ms | 15 |

## Verification Method

1. Fix trace/span IDs, parent IDs, asynchronous links, service/deployment versions, timestamps, and sampling scope. Check nesting and clock skew; a link is not automatically synchronous parentage.
2. Within one clock domain, subtract the union of synchronous child intervals to obtain observed exclusive time; overlapping children are not additive. Missing spans limit this to observed intervals, not true exclusive work.
3. Derive critical paths from actual dependency/blocking order. Queue time requires enqueue/dequeue evidence; unexplained gaps are not automatically queues.
4. A longest span is an investigation candidate; causation needs logs/metrics/controlled faults. State separate missing-span, sampling, and clock limitations.
