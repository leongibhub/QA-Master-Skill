# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Matched version/environment/obligations: baseline runs sequentially in 10min and detects duplicate refund in T-refund. O-1 isolates data and runs in parallel in 6min, retaining detection and no conflicts. O-2 deletes T-refund, runs in 4min and stays green under the fault. O-3 compares a differently sized project taking 3min and claims 70% gain. O-4 lacks mandatory-obligation mappings. Decide ACCEPT/REJECT/NOT_COMPARABLE/UNKNOWN with percentage benefit, retained protection and unblock conditions.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| O-1 | ACCEPT |
| O-2 | REJECT |
| O-3 | NOT_COMPARABLE |
| O-4 | UNKNOWN |

| METRIC | VALUE |
| --- | --- |
| runtime_reduction_percent | 40 |

## Verification Method

1. Match before/after versions, environment, obligations, data and windows. Source selection/order/parallel/cache inclusions and exclusions; different test volumes cannot support timing comparisons.
2. Preserve critical risks, known escapes and mandatory gates. Reject removal of sole protection; unknown mappings require conservative checks or escalation.
3. Measure duration/resources, detection, misses/escapes and flakiness separately. The same controlled fault must still fail an effective assertion for the same obligation.
4. State benefit conditions, residual risk, implementation/rollback triggers and owners. Removing protection requires authorized acceptance, not an optimization proposal alone.
