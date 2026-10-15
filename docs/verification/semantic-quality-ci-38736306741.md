# Semantic-quality fanout repair CI — run 38736306741

- Evidence Status: OBSERVED
- Local subject: `a9df28513d4ae808d687718bfc4f6069a32ee767`
- Remote subject: `ff7915ea77be66c5b99426b68317cb9a01e06829`
- Equal Git tree: `d4c6d70d6e9ebbbd38e386d029be3f0bd081fc66`
- Method: root read back GitHub API job status and decoded logs.

| Job | Platform / Python | Result | Log observation |
|---|---|---|---|
| 116426367834 | Ubuntu / 3.10 | completed / success | 686 tests, 52.491s, OK, one Windows-only skip |
| 116426367795 | Ubuntu / 3.12 | completed / success | 686 tests, 53.869s, OK, one Windows-only skip |
| 116426367357 | Windows / 3.10 | completed / success | 686 tests, 163.806s, OK |
| 116426367862 | Windows / 3.12 | completed / success | 686 tests, 132.500s, OK |

This run includes the retained TC027 regression and repaired evaluator. Later
independent test additions are outside this exact tree and require separate
verification. The result does not replace independent testing/review and does
not establish a Gate, human acceptance, release or comparative quality result.
