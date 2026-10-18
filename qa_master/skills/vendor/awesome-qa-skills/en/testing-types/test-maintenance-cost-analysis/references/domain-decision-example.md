# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Same month,20h each. A:16h duplicated selector implementations,4h product change. B:16h runner outage/wait/retry,4h product change. C:20h without causes. M1 recommends deduplication for A while retaining business assertions. M2 prioritizes environment reliability for B. M3 infers identical root causes from equal totals. M4 labels C personally inefficient. Decide SUPPORTED/UNSUPPORTED/UNKNOWN for recommendations, with source-based cost groups and no performance ranking from total hours. M5: C has no cause records; classify its maintenance cause UNKNOWN.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| M1 | SUPPORTED |
| M2 | SUPPORTED |
| M3 | UNSUPPORTED |
| M4 | UNSUPPORTED |
| M5 | UNKNOWN |

## Verification Method

1. Fix assets, sample window, unit, and time sources. Separate product change, test defect, infrastructure, data, duplication, and unclassified costs; do not double-count one event across causes.
2. Link trigger, change frequency, time ranges, review/rework, and failure impact. Separate one-time build from recurring maintenance; one sample cannot predict precise long-term costs.
3. Explain sample size, representativeness, outliers, and interval formulas. Without monetary rates report labor; unknown causes remain UNKNOWN and are no personal-performance rating.
4. Equal totals may require different interventions: change decoupling, test repair, environment stability, isolation, or deduplication. Validate gains and retained protection in matched follow-up samples.
