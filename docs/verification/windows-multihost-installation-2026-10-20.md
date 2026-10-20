# Windows multi-host installation — independent test record

- Artifact ID: `EVD-WINDOWS-MULTIHOST-INSTALLATION-001`
- Change / requirement: `CR-031`; `REQ-028`; `NFR-012`
- Subject: `027ca50f2a0ba52558286872edfd351f64ac0887`
- Executor: tester `/root/install_matrix_independent_test`
- Date: 2026-10-20
- Environment: Windows; Python `3.13.5` (`C:\\WINDOWS\\py.exe`); uv `0.11.6`; repository checkout `D:\\QA-Master-Install-Docs`.

## Results

| Case | Result | Observable evidence |
| --- | --- | --- |
| `TC-INSTALL-001` | PASS | With the child `PATH` limited to `C:\\Windows;C:\\Windows\\System32`, where `qa-master` was not discoverable, `C:\\WINDOWS\\py.exe -3 -m qa_master install-codex` installed both disposable Codex/OpenCode user and project targets. Each retained `SKILL.md`, a 5,882-file manifest and helper output `vendor.count=330`, `en=165`, `zh=165`. The first two routes also completed the tester's per-file SHA-256 manifest comparison before the next route started. |
| `TC-INSTALL-002` | PASS (bounded, attempt 2) | Attempt 1 retained a long-path `SKILL_INSTALL_IO_ERROR` as `BUG-015`. Attempt 2 used ordinary-length disposable roots and completed the remaining Claude Code and TRAE CN user/project shapes. Together with the two Codex/OpenCode targets, all six documented ordinary-length target shapes passed package checks. No real host UI was operated. |
| `TC-INSTALL-003` | PASS (documentation contract) | [uv's official installation page](https://docs.astral.sh/uv/getting-started/installation/) documents `winget install --id=astral-sh.uv -e`; the guide points to it and uses `uv tool install --force --python 3.13 .`. With `qa-master` removed from `PATH`, `C:\\Users\\leon.wang\\.local\\bin\\uv.exe tool run --from . --python 3.13 qa-master --help` exited 0 and printed the CLI usage. A physical Python-absent/old-Python machine was not supplied, so bootstrap/download/install on one remains `NOT_EXECUTED`. |
| `TC-INSTALL-004` | PENDING | Assigned to the independent reviewer in `TASK-129`; this tester did not make a review conclusion. |

## Target and content checks

The completed disposable targets were below `C:\\Users\\leon.wang\\AppData\\Local\\Temp\\qa-master-cr031-independent-7be7c507524b4ef8a3f12eba21c2084a`:

| Target shape | `SKILL.md` | Manifest entries | Helper catalog |
| --- | --- | ---: | --- |
| User `.agents\\skills\\qa-master` via `--user` | present | 5,882 | 330 / 165 English / 165 Chinese |
| Project `.agents\\skills\\qa-master` via `--project` | present | 5,882 | 330 / 165 English / 165 Chinese |

The installer result declared `execution: NOT_EXECUTED`; that property and the filesystem checks are package-delivery evidence only. Codex, OpenCode, Claude Code and TRAE CN session discovery, model selection and conversation behavior are all `NOT_EXECUTED`.

## Documentation and regression checks

- `tests.test_installation_docs` completed: 3 passed. It asserts the existing-Python and uv routes, six documented target strings, no virtual-environment activation requirement, provider/token boundary, catalog check and retained Linux/macOS instructions.
- A larger selected suite (`tests.test_codex_skill` and `tests.test_readme_catalog`) was intentionally stopped after its documented installation checks began to keep this independent run bounded. It is `NOT_EXECUTED` as a complete suite; its partial output is not counted as a pass.
- TRAE's official Skill guide identifies Windows global `%userprofile%/.trae-cn/skills` and project `.trae/skills/` locations. It also describes host-side enablement/import options; this test did not interact with them.

## Defect

### BUG-015 — installer reports generic I/O error for a long nested explicit target

- Linked requirement/tests: `REQ-028`, `NFR-012`, `TC-INSTALL-002`.
- Reproduction: invoke `C:\\WINDOWS\\py.exe -3 -m qa_master install-codex --target <long-disposable-path>\\profile\\.claude\\skills\\qa-master` from the frozen subject. The prior `.agents` user/project copies completed; the Claude target then returned `{"error": "SKILL_INSTALL_IO_ERROR"}` during bundle staging.
- Expected: an explicit documented target should install or return a stable, actionable length/target error before a partial staging attempt.
- Actual: generic `SKILL_INSTALL_IO_ERROR`; no host directory was published at the requested target. A temporary staging directory remained.
- Severity: P3 pending developer triage. The test root is substantially longer than an ordinary `%USERPROFILE%` target, so this does not prove ordinary user-path installation fails. Attempt 2 subsequently passed all six ordinary-length documented target shapes; this retained finding is outside that bounded PASS and should be reproduced with a controlled length boundary before closure.

No password, token, API endpoint, account configuration, provider setting or external system was read or written during this test.

## Attempt 2 — ordinary-length Claude and TRAE targets

- Subject: unchanged, `027ca50f2a0ba52558286872edfd351f64ac0887`.
- Environment: same Windows / Python `3.13.5`; the child `PATH` was again limited to `C:\\Windows;C:\\Windows\\System32`, with no discoverable `qa-master` executable.
- Test root: disposable `D:\\qmi-61cc31fe`, deliberately short and representative of the documented ordinary `%USERPROFILE%` and project target shapes.

| Route | Result | Observable package evidence |
| --- | --- | --- |
| Claude Code global `u\\.claude\\skills\\qa-master` | PASS | `py -3 -m qa_master install-codex --target ...` returned `INSTALLED`, 5,882 files and a 5,882-entry manifest; required bundle entries were present; helper returned 330 / 165 / 165. |
| Claude Code project `pclaude\\.claude\\skills\\qa-master` | PASS | Same checks and counts passed. |
| TRAE CN global `u\\.trae-cn\\skills\\qa-master` | PASS | Same checks and counts passed. |
| TRAE CN project `ptrae\\.trae\\skills\\qa-master` | PASS | Same checks and counts passed. |

Combined with the two completed `.agents` routes in attempt 1, the six ordinary-length documented target shapes have package-level `PASS` evidence. `TC-INSTALL-002` is therefore `PASS` in that bounded ordinary-path scope. `BUG-015` remains open as a P3 long-nested-path limitation: attempt 2 does not erase the retained attempt-1 failure.

The test also checked each installed file path remained beneath its requested target. It did not run a host UI or conversation, so Codex, OpenCode, Claude Code and TRAE CN discovery and behavior remain `NOT_EXECUTED`.

### Cleanup record

The tester attempted a scoped cleanup only after resolving the exact `D:\\qmi-61cc31fe` target and confirming its `D:\\qmi-` prefix. The execution environment rejected the recursive removal before it ran. Cleanup is therefore `NOT_EXECUTED`; the disposable directory remains at that exact path for subsequent manual deletion. No user profile, project checkout or host Skill directory was touched.
