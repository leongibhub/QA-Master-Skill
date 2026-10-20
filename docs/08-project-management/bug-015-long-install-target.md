# BUG-015 — long nested Windows Skill target reports a generic I/O error

- Change: `CR-031`
- Requirement: `REQ-028`, `NFR-012`
- Found by: `TASK-128`, `TC-INSTALL-002` attempt 1
- Evidence: `EVD-WINDOWS-MULTIHOST-INSTALLATION-001`
- Severity: `P3`
- Status: `OPEN`

An explicit Claude-style target beneath a deliberately long disposable Windows
path returned `SKILL_INSTALL_IO_ERROR` while staging the self-contained bundle.
No final host target was published, but a staging directory remained. The same
frozen subject subsequently installed all six documented host/scope shapes when
tested under ordinary-length disposable paths, so this finding does not show a
failure for the documented `%USERPROFILE%` or normal project routes.

Future work should reproduce the exact length boundary and return an actionable
target-length error before staging, or support the longer path safely. This
defect is not closed by the ordinary-path PASS and does not establish host Skill
discovery, model behavior, release readiness, or acceptance.
