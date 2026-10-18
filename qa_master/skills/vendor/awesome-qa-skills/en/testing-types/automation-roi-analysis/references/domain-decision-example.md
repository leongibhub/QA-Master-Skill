# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

All costs are Human hours; monthly window: build=12h, manual=1h/run, automation+review=0.2h/run. R-1:20 runs/month, maintenance=4h/month, horizon=3 months. R-2:5 runs/month, maintenance=4h/month. R-3:20 runs/month, change raises maintenance to20h/month. R-4:frequency missing. Decide POSITIVE/NO_BREAK_EVEN/UNKNOWN; show R-1 three-month net labor saving and whole-month break-even, without unsourced monetary conversion.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| R-1 | POSITIVE |
| R-2 | NO_BREAK_EVEN |
| R-3 | NO_BREAK_EVEN |
| R-4 | UNKNOWN |

| METRIC | VALUE |
| --- | --- |
| net_saving_h | 24 |
| break_even_months | 1 |

## Verification Method

1. Fix candidate, window, and units. Separate Human time, machine occupancy, review, maintenance, and money; conversions need sourced rates.
2. For one window, net saving = runs×(manual cost/run−automated cost/run)−maintenance−build cost. Define ROI numerator/denominator; absent monetary conversion, report labor only.
3. If recurring net saving >0, break-even windows = build cost/recurring net saving, rounding up for whole execution windows. If <=0, no break-even under those assumptions.
4. Vary frequency and change-driven maintenance in project-supplied low/base/high scenarios with sources and sign changes. Missing inputs yield formulas/conditional ranges, never precise invented returns or automatic adoption.
