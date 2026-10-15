# Semantic-quality repair CI readback — run 38734307476

- Evidence Status: OBSERVED
- Local subject: `9085c5fdb2df72303ecd478542037c98637d3a6c`
- Remote subject: `4f70ab65abbd287c2ed54900d838cd2de6d0539f`
- Equal Git tree: `10681e10c0e2271caa2db7ec8a0b84da0bdbc943`
- Method: GitHub API job status and decoded log readback by root.

| Job | Platform / Python | Result | Log observation |
|---|---|---|---|
| 116419579478 | Ubuntu / 3.10 | completed / success | 676 tests, 52.485s, OK, one Windows-only skip |
| 116419579731 | Ubuntu / 3.12 | completed / success | 676 tests, 44.154s, OK, one Windows-only skip |
| 116419579677 | Windows / 3.10 | completed / success | 676 tests, 153.240s, OK |
| 116419579538 | Windows / 3.12 | completed / success | 676 tests, 132.628s, OK |

This is regression evidence for this exact tree. Subsequent independent review
and reproduction found residual repeated validation when one artifact maps to
multiple obligations. These successful CI jobs do not close that P2 finding or
establish independent acceptance, a Gate decision, release readiness or quality
superiority. A later repair requires its own source-bound verification.
