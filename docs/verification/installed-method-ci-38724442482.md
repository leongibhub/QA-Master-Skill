# Installed-method CI readback — run 38724442482

- Artifact ID: `DOC-INSTALLED-METHOD-CI-002`
- Evidence ID: `EVD-INSTALLED-METHOD-CI-002`
- Change / subject: `CR-013` / `TASK-056` attempt 3
- Remote commit: `787ec257b3357f7b9781210d3f6607ab6319f4c6`
- Local implementation commit: `8b5017af42c7675cd32f941b71c85cf79b30d499`
- Tree relation: root GitHub API readback reported the remote tree equal to local `8b5017a`.
- Evidence Status: `OBSERVED`
- Date: 2026-10-15

## Observed GitHub Actions matrix

| Job | Platform / Python | Result | Observed test output |
|---|---|---|---|
| `116386696270` | Ubuntu / 3.10 | completed / success | 605 tests, 31.380 seconds, `OK`, one Windows-only skip |
| `116386696649` | Ubuntu / 3.12 | completed / success | 605 tests, 22.262 seconds, `OK`, one Windows-only skip |
| `116386696591` | Windows / 3.10 | completed / success | 605 tests, 117.037 seconds, `OK` |
| `116386696761` | Windows / 3.12 | completed / success | 605 tests, 87.601 seconds, `OK` |

This CI record is distinct from the prior 598-test run at the earlier
`f62932b` subject. It is remote regression evidence only. TASK-057 attempt 3 later supplied separately scoped independent fresh-install and
actual-task evidence, and TASK-058 independently reviewed it. This CI record is
still remote regression evidence only; it is not a semantic quality evaluation,
comparison, Gate, acceptance or release decision.
