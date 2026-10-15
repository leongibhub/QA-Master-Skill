# Final semantic-quality evidence-tree CI — run 38737995019

- Evidence Status: OBSERVED
- Local subject: `c93b41ecad142666c4480181d86a043404461a1b`
- Remote subject: `f9d6f7f64baf6265774c90bf3644ca7d17b7b9dd`
- Equal Git tree: `f66424daf3d4756e480422cedfc9294742ab2242`
- Method: root read back GitHub API job status and decoded logs.

| Job | Platform / Python | Result | Log observation |
|---|---|---|---|
| 116432100300 | Ubuntu / 3.10 | completed / success | 689 tests, 52.422s, OK, one Windows-only skip |
| 116432101912 | Ubuntu / 3.12 | completed / success | 689 tests, 53.396s, OK, one Windows-only skip |
| 116432101009 | Windows / 3.10 | completed / success | 689 tests, 103.833s, OK |
| 116432100605 | Windows / 3.12 | completed / success | 689 tests, 137.825s, OK |

The tested tree includes all 30 independent regression tests and the retained
attempt3 evidence/final review. This record was written after that run and is
not part of its tested tree. The evaluator source remains the independently
reviewed `a9df285` implementation. The bounded review retains one P3 follow-up
for evaluator-specific link/reparse fixtures; Runtime defect closure records
remain incomplete. No overall V1, Gate, release or quality-superiority result
follows from these successful jobs.
