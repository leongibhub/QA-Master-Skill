# Semantic-quality CI readback — run 38732162170

- Artifact ID: `DOC-SEMANTIC-QUALITY-CI-001`
- Evidence ID: `EVD-SEMANTIC-QUALITY-CI-001`
- Change / subject: `CR-013` / `TASK-061`
- Local commit: `6905e0209b1159c8a8fd2b5799a74cf22adea240`
- Remote commit: `6fab7ea07ca14495109b981c43ebaad813f8b645`
- Tree relation: root GitHub API readback reported remote tree equal to local tree `37f5cc9915bff5f7e0136156e13aa7779a8e363e`.
- Evidence Status: `OBSERVED`

| Job | Platform / Python | Result | Observed output |
|---|---|---|---|
| `116412317917` | Ubuntu / 3.10 | completed / success | 648 tests, 38.556 seconds, `OK`, one Windows-only skip |
| `116412317605` | Ubuntu / 3.12 | completed / success | 648 tests, 40.017 seconds, `OK`, one Windows-only skip |
| `116412317893` | Windows / 3.10 | completed / success | 648 tests, 120.896 seconds, `OK` |
| `116412317994` | Windows / 3.12 | completed / success | 648 tests, 146.720 seconds, `OK` |

This root-reported GitHub API readback is remote regression evidence only. It does
not substitute for the active TASK-062 independent test, TASK-063 review, semantic
quality assessment, Gate, acceptance, release, model, process, network or enterprise
result.