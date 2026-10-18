# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Matched team/window/complexity: baseline 100 accepted tasks in 100h with one escape. A candidate splits cases into 200 rows but still delivers 100 tasks in 100h with five escapes. P-1 claims doubled productivity and better quality. P-2 is a separate candidate: the same 100 tasks in 80h, one escape, comparable rework and complete acceptance evidence. P-3 ranks a payment team against a copy team by case count alone. Decide UNSUPPORTED/SUPPORTED/NOT_COMPARABLE using balanced input/output/quality/flow evidence.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| P-1 | UNSUPPORTED |
| P-2 | SUPPORTED |
| P-3 | NOT_COMPARABLE |

## Verification Method

1. Balance effort/cost, accepted output, defects/escapes and waiting/rework with explicit windows, team/task units, complexity and product risk.
2. Deduplicate split or merged cases and verify acceptance. Case/commit counts do not equal value; missing quality/rework evidence prevents productivity claims.
3. Compare only matched tasks, complexity, tools and windows. Different team work mixes cannot support direct ranking or personal performance evaluation; expose context and uncertainty.
4. Check dropped hard tests, unreported defects, deferred time and rerun counts. Metrics trigger investigations and experiments, not automatic causal or reward decisions.
