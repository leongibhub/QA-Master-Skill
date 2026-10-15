# Installed-method CI readback — run 38722857430

- Artifact ID: `DOC-INSTALLED-METHOD-CI-001`
- Evidence ID: `EVD-INSTALLED-METHOD-CI-001`
- Change / subject: `CR-013` / `TASK-056` attempt 2
- Remote commit: `1836ac1f2153d8bcb6c6a75191f2e3759ff20b83`
- Local implementation commit: `f62932b1cce8471c929632fced8909a7a277a2ba`
- Tree relation: root GitHub API readback reported the remote tree equal to local `f62932b`.
- Evidence Status: `OBSERVED`
- Date: 2026-10-15

## Observed GitHub Actions matrix

| Job | Platform / Python | Result | Observed test output |
|---|---|---|---|
| `116381443813` | Ubuntu / 3.10 | completed / success | 598 tests, 29.191 seconds, `OK`, one Windows-only skip |
| `116381444077` | Ubuntu / 3.12 | completed / success | 598 tests, 30.203 seconds, `OK`, one Windows-only skip |
| `116381444246` | Windows / 3.12 | completed / success | 598 tests, 108.363 seconds, `OK` |
| `116381444253` | Windows / 3.10 | completed / success | 598 tests, 110.036 seconds, `OK` |

This is an API readback of the CI workflow after the packaged-reference repair.
It provides remote regression evidence for the frozen implementation tree. It does
not execute or verify TASK-057's tester-owned fresh installed workflow,
representative offline QA task, source/projection quality, human assessment,
comparison, acceptance, release, or a Gate decision.
