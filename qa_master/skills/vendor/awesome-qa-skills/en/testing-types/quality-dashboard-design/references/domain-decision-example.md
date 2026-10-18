# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Project gates: an open P0 blocks; data older than 24h is STALE; tests without execution are NOT_RUN. D-1 has 99/100 passes and one open P0. D-2 uses a 48-hour-old green source. D-3 shows zero failures and green despite no test run. D-4 has current 100/100 evidence, no P0, drill-down to run17 and a complete definition/window. Decide BLOCKED/STALE/NOT_RUN/PASS with decision/source/action mapping; missing data is not zero.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| D-1 | BLOCKED |
| D-2 | STALE |
| D-3 | NOT_RUN |
| D-4 | PASS |

## Verification Method

1. Map audience decisions to metrics, definitions/windows, source versions, actions and owners; available data alone must not decide what matters.
2. Show numerator/denominator, refresh time and source status. Distinguish zero, null, NOT_RUN, BLOCKED and stale data; never fill gaps with zero or reuse stale green.
3. Preserve P0 blockers and small high-risk groups in summaries. Overall pass rates cannot override individual blockers; aggregation follows project rules.
4. Provide drill-down to run/obligation/defect evidence, refresh contracts and action triggers. Missing sources or gates yield design and gaps, not a current pass.
