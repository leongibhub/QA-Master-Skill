# Installed-method CI readback — run 38726341002

- Artifact ID: `DOC-INSTALLED-METHOD-CI-003`
- Evidence ID: `EVD-INSTALLED-METHOD-CI-004`
- Change / source-freeze mapping: `CR-013`; local `0dd319b`, remote `fb1ba496`; remote tree `357aa1d22731fdb4e117eaf23fb12bd193e79cc7` equals the local HEAD tree.
- Product-code boundary: the installed Phase 1 implementation remains `8b5017a`; `0dd319b` contains governance/evidence reconciliation and does not begin the DES-060 evaluator implementation.
- Evidence Status: `OBSERVED`
- Date: 2026-10-15

## Observed GitHub Actions matrix

| Job | Platform / Python | Result | Observed test output |
|---|---|---|---|
| `116393022846` | Ubuntu / 3.10 | completed / success | 606 tests, 31.556 seconds, `OK`, one Windows-only skip |
| `116393022336` | Ubuntu / 3.12 | completed / success | 606 tests, 30.988 seconds, `OK`, one Windows-only skip |
| `116393022827` | Windows / 3.10 | completed / success | 606 tests, 94.210 seconds, `OK` |
| `116393022729` | Windows / 3.12 | completed / success | 606 tests, 119.740 seconds, `OK` |

This is a root-reported GitHub API readback of the existing Phase 1 source-freeze.
It does not exercise TASK-061, evaluate semantic quality, change CR-011 retained
artifacts, close a future defect, or establish a Gate, acceptance, release, model,
process, network or enterprise result.