# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Baseline passes99/100. Controlled F1 duplicates a debit; title-only T1 stays green. F2 changes amount; T2 ledger assertion fails. F3 disconnects environment; T3 fails startup without reaching business assertion. F4 is not injected. Separate historical one-week data has1 duplicate-debit escape. Decide MISSED/DETECTED/INCONCLUSIVE/NOT_RUN with injection denominator separate from historical escape;99% pass rate is no effectiveness proof.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| F1 | MISSED |
| F2 | DETECTED |
| F3 | INCONCLUSIVE |
| F4 | NOT_RUN |

## Verification Method

1. Map obligation/fault class→test ID→real production behavior→effective assertion→escaping defect. Pass/coverage rates are signals, not fault-detection proof.
2. Historical escapes retain observation window, exposure, detection/misses, and sources. Controlled fault injections use separate denominators, controls, environment, and mutation identity; do not pool them into production-defect rates.
3. Verify failures came from the intended business assertion; environment errors/timeouts are not automatically valid detections. Give candidate causes/minimal independent checks without claiming causation from correlation.
4. Report detected/missed/unexecuted faults by class with residual uncertainty, prioritizing critical oracles. Without fault/escape data deliver an evaluation plan, not effectiveness proof.
