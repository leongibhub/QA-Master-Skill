# Windows multi-host installation requirements

- Artifact ID: `DOC-WINDOWS-MULTIHOST-INSTALLATION-REQ-001`
- Version: `v1`
- Document State: `DRAFT`
- Evaluation State: `IN_REVIEW`
- Evidence Status: `VERIFIED`
- Change: `CR-031`
- Date: 2026-10-20

## Context and boundary

QA staff need a short Windows installation route that works both when Python is
already available and when it is absent or too old. A checkout alone does not
put the `qa-master` executable on `PATH`; documentation must therefore provide
a module invocation which remains usable without `PATH` changes or a virtual
environment.

This change documents use of the existing self-contained package and installer.
It does not configure an LLM provider, model, API token, VS Code extension, or
agent account. A successful copy, command exit, directory check, or helper
output does not establish that any agent host has discovered the Skill or that a
model has followed it.

## REQ-028 — Windows multi-host, no-PATH installation route

| Item | Requirement |
| --- | --- |
| Expected behaviour | The Windows documentation shall provide a preflight and two explicit routes: (1) a checkout route for an existing supported Python (3.10 or newer), using `py -3 -m qa_master` with `python -m qa_master` as the fallback; and (2) a Python-absent or unsupported-Python route using an official `uv` installation method and `uv tool install --python 3.13`, with `uv tool run --from . --python 3.13 qa-master` as the immediate no-PATH fallback. Neither route requires activation of a virtual environment or the `qa-master` executable to be on `PATH`. |
| Host and scope matrix | The documented module command shall calculate the deterministic existing-installer target: Codex/OpenCode global `%USERPROFILE%\\.agents\\skills\\qa-master` via `--user`, project `<project>\\.agents\\skills\\qa-master` via `--project`; Claude global `%USERPROFILE%\\.claude\\skills\\qa-master` and project `<project>\\.claude\\skills\\qa-master` via `--target`; TRAE CN global `%USERPROFILE%\\.trae-cn\\skills\\qa-master` and project `<project>\\.trae\\skills\\qa-master` via `--target`. |
| Measurable acceptance | (1) Each supported Windows host/scope route is shown with a no-PATH module invocation. (2) Existing-Python users can complete the documented installer action from a checkout without `venv` activation. (3) Python-absent/old users are directed to an official `uv` bootstrap and isolated tool installation, rather than being told to run an unavailable `qa-master` command. (4) Documentation provides a target/manifest/helper check and labels it as filesystem/package evidence only. |
| Scope boundary | This requirement neither changes the installer target semantics nor proves an actual Python download, installation on a Python-absent computer, host Skill discovery, model behaviour, or external test execution. |
| Current verification state | `TC-INSTALL-001` through `TC-INSTALL-003` have bounded independent `PASS` evidence; `TC-INSTALL-004` is independently reviewed at repaired subject `6c56c43`. The actual Python-absent/old-machine installation and host UI discovery remain `NOT_EXECUTED`. |

## NFR-012 — deterministic paths and host/provider separation

| Item | Requirement |
| --- | --- |
| Expected behaviour | Every Windows route shall use a deterministic host/scope target, retain the existing installer containment/update safeguards, and state the module invocation fallback when `qa-master` is unavailable on `PATH`. Documentation and commands shall not request, print, write, or retain provider credentials, model selection, API endpoints, passwords, cookies, private keys, or agent-account configuration. |
| Measurable acceptance | (1) The six host/scope targets are unambiguous and point to the same `SKILL.md` bundle shape. (2) The no-PATH command is usable from a checkout with an existing supported Python. (3) The bootstrap route separates installation tooling from provider/model configuration. (4) Target existence, manifest inspection, helper output, and exit status are never described as host discovery or conversation evidence. |
| Current verification state | `VERIFIED` for the bounded no-PATH documentation and ordinary-length package-target checks, with independent review at `6c56c43`. `NOT_EXECUTED`: actual Python-absent/old-machine bootstrap and install; actual Codex, OpenCode, Claude Code, and TRAE CN UI/session discovery. |

## Planned work and test cases

| ID | Work / check | Owner role | Current state |
| --- | --- | --- | --- |
| TASK-127 | Implement and document the Windows preflight, existing-Python module route, Python-absent/old `uv` route, and six host/scope target commands. | developer / documentation_manager | `DONE`, `VERIFIED`: implemented at `027ca50`; no-PATH update correction at `6c56c43` is independently reviewed. |
| TASK-128 | Independently validate the frozen documentation and installer/package route against the declared no-PATH and target contracts. | tester | `DONE`, bounded `PASS`: `EVD-WINDOWS-MULTIHOST-INSTALLATION-001` verifies the existing-Python no-PATH route, six ordinary-length package targets, and the `uv` documentation/no-PATH contract. Actual Python-absent/old-machine bootstrap/install remains `NOT_EXECUTED`. |
| TASK-129 | Independently review claim accuracy, target mapping, no-PATH fallback, credential/model separation, and evidence labels. | reviewer | `DONE`: attempt 1 `CHANGES_REQUESTED` at `ee3ecd6` is retained; attempt 2 is `PASS WITH P3 FOLLOW-UP` at `6c56c43`. P2-001/P3-001 are resolved. P3-002 is resolved by this governance reconciliation; `BUG-015` remains the open P3 follow-up. |
| TC-INSTALL-001 | From a checkout with supported Python, run the documented `py -3 -m qa_master` route without `qa-master` on `PATH`; validate a selected target and helper output. | tester | `PASS`: `EVD-WINDOWS-MULTIHOST-INSTALLATION-001` observes disposable user/project `.agents` targets, 5,882 manifest entries and helper `330/165/165`. |
| TC-INSTALL-002 | Validate the six declared host/scope targets, installed manifest/assets, target containment, and the explicit distinction from host discovery. | tester | `PASS` for six ordinary-length disposable targets in attempt 2 of `EVD-WINDOWS-MULTIHOST-INSTALLATION-001`; `BUG-015` remains open as a P3 long-nested-target limitation from retained attempt 1. Actual host UI/session discovery is `NOT_EXECUTED`. |
| TC-INSTALL-003 | Check the Python-absent/old route's official `uv` bootstrap, Python-version selection, and no-venv/no-PATH wording. | tester | `PASS` for documentation/no-PATH contract in `EVD-WINDOWS-MULTIHOST-INSTALLATION-001`; real bootstrap/download/install on a Python-absent or old-Python machine is `NOT_EXECUTED`. |
| TC-INSTALL-004 | Independently review source and documentation for path correctness, unsupported installation/discovery claims, and credential/model configuration exposure. | reviewer | `PASS WITH P3 FOLLOW-UP` on attempt 2 at `6c56c43`: P2-001 and P3-001 are resolved; no P0/P1/P2 or new P3 remains. Attempt-1 `CHANGES_REQUESTED` is retained; its P3-002 lifecycle-governance follow-up is resolved here. `BUG-015` remains open. |

## Change impact

CR-031 changes onboarding documentation and its verification contracts only. It
reuses the existing package, `qa_master` module, installer options, target
containment controls, and manifest/helper checks. It adds no new host adapter,
provider integration, credential flow, model configuration, remote operation,
Gate decision, release evidence, or acceptance claim.
