# Windows multi-host installation — independent review

- Artifact ID: `EVD-WINDOWS-MULTIHOST-INSTALLATION-REVIEW-001`
- Change / requirements: `CR-031`; `REQ-028`; `NFR-012`
- Reviewed subject: `ee3ecd6b8590eaefe363f7171fff3be1364b8ceb`
- Reviewer: `/root/install_matrix_final_review`
- Date: 2026-10-20
- Attempt 1 conclusion: `CHANGES_REQUESTED`

## Findings

### P2-001 — the direct-Python TRAE update example requires an executable that this route does not install

- Affected: `REQ-028`, `NFR-012`, `TASK-127`, `TC-INSTALL-004`.
- Location: `docs/GETTING_STARTED.md`, update section, the TRAE CN example after the text for an existing-Python direct-run user.
- Failure mode: the section correctly introduces `py -3 -m qa_master ... --update` for a direct checkout, but its next TRAE example changes back to `qa-master install-codex ... --update`. A user who followed the supported no-PATH route can receive the same “command not found / 不是内部或外部命令” failure that CR-031 is meant to prevent.
- Impact: TRAE CN updates are not copyable for one of the two primary Windows installation states. The host/scope matrix and first installation remain correct.
- Validation: the independent test record explicitly exercised a child `PATH` with no discoverable `qa-master`; both `py -3 -m qa_master --help` and the documented `python -m qa_master --help` fallback executed successfully in this review environment.
- Remediation: use `py -3 -m qa_master install-codex --target "%USERPROFILE%\.trae-cn\skills\qa-master" --update` in that direct-Python example, with the already documented `python` substitution when the launcher is absent. Keep the uv/PATH fallback for uv users.

### P3-001 — route-contract tests do not assert the `python -m` launcher fallback or update examples

- Affected: `REQ-028`, `NFR-012`, `TC-INSTALL-004`.
- Location: `tests/test_installation_docs.py`.
- Failure mode: the tests assert `py -3 -m qa_master`, uv fallback strings and target paths, but do not assert `python -m qa_master` or that direct-Python update examples avoid a bare `qa-master` command.
- Impact: the P2 regression above passed all three documentation tests.
- Remediation: add focused assertions for launcher absence and direct-Python update commands after P2-001 is corrected.

### P3-002 — lifecycle status sources still describe committed CR-031 work as nonexistent or pending

- Affected: `CR-031`, `TASK-127`, `TASK-128`.
- Locations: `docs/08-project-management/change-register.md` CR-031 row; the TASK-127/TASK-128 initial-state rows and document-level evidence status in `docs/03-requirements/windows-multihost-installation-2026-10-20.md`.
- Failure mode: the change register says no implementation or independent result exists, while frozen commit `ee3ecd6` contains the implementation and `EVD-WINDOWS-MULTIHOST-INSTALLATION-001`; other fields remain `PENDING` despite the bounded observed results.
- Impact: runtime behavior is unaffected, but the lifecycle record is internally stale and cannot support a final Gate decision as written.
- Remediation: after remediation/re-review, have the documentation manager reconcile CR-031, TASK-127/128, evidence status and RTM without changing the retained `NOT_EXECUTED` boundaries.

No P0 or P1 finding was identified.

## Conformance checks that passed

- Existing Python 3.10+ is covered by `py -3 -m qa_master`, with the `python -m qa_master` launcher fallback stated in both onboarding documents. No venv activation is required.
- The Python-absent/old route uses the current official uv WinGet package, `uv tool install --python 3.13`, `uv tool update-shell`, and `uv tool run --from . --python 3.13 qa-master`. Astral's [installation](https://docs.astral.sh/uv/getting-started/installation/) and [tool](https://docs.astral.sh/uv/guides/tools/) documentation supports these commands.
- Codex and OpenCode global/project `.agents/skills` paths agree with the current [Codex](https://developers.openai.com/codex/skills) and [OpenCode](https://opencode.ai/docs/skills) documentation.
- Claude Code personal/project `.claude/skills` paths and `/qa-master` invocation agree with Anthropic's current [Skill documentation](https://code.claude.com/docs/en/skills).
- TRAE CN Windows global `%USERPROFILE%/.trae-cn/skills`, project `.trae/skills`, and natural-language invocation agree with TRAE's current [Skill documentation](https://docs.trae.cn/ide_skills).
- Windows examples are labelled `cmd`; the PowerShell `%USERPROFILE%` to `$env:USERPROFILE` substitution is explicit.
- Package verification reads the installed `SKILL.md` and helper, and offers a uv-managed-Python command when system Python is absent.
- Model, endpoint, password and API-token configuration remain outside QA Master. Filesystem/package success is not presented as host discovery.

## Verification evidence

- `py -3 -m unittest tests.test_installation_docs -v`: `3/3 PASS`.
- `py -3 -m qa_master --help`: exit `0`.
- `python --version`: `3.13.5`; `python -m qa_master --help`: exit `0`.
- `uv tool run --from . --python 3.13 qa-master --help`: exit `0`.
- `git diff --check 0113658..ee3ecd6`: exit `0`.
- `pytest` was `NOT_AVAILABLE` in the selected system interpreter (`No module named pytest`); the same focused cases were executed successfully with their native `unittest` runner.

The tester's `EVD-WINDOWS-MULTIHOST-INSTALLATION-001` and `BUG-015` are consistent: six ordinary-length package targets passed, the failed deliberately long target remains an open P3, and neither record claims actual host discovery. A physical Python-absent/old-Python installation and Codex/OpenCode/Claude Code/TRAE CN UI-session discovery remain `NOT_EXECUTED`.

## Attempt 2 — repaired no-PATH update route

- Reviewed subject: `6c56c43685df0b80154abf46cb11d95a9441bf59`.
- Conclusion: `PASS WITH P3 FOLLOW-UP`.
- Open findings from this attempt: P0 `0`; P1 `0`; P2 `0`; P3 `0` new. Attempt-1 P3-002 remains assigned to lifecycle governance and is not reclassified or closed by this reviewer-owned update.

### Resolution readback

- P2-001: `RESOLVED`. The existing-Python TRAE CN update example now uses `py -3 -m qa_master ... --update`, and explicitly supplies `python -m qa_master ... --update` when the `py` launcher is absent. The direct-Python path no longer requires the `qa-master` executable on `PATH`.
- P3-001: `RESOLVED`. `tests/test_installation_docs.py` now asserts the `python -m qa_master` launcher fallback and the Claude/TRAE direct-Python update commands.
- P3-002: remains `OPEN` as the retained lifecycle-governance follow-up from attempt 1. Per review scope, no non-reviewer governance state was changed in this attempt.

### Attempt 2 verification

- `py -3 -m unittest tests.test_installation_docs -v`: `4/4 PASS`.
- `python --version`: `3.13.5`; `python -m qa_master --help`: exit `0`.
- `uv tool run --from . --python 3.13 qa-master --help`: exit `0`.
- `git diff --check ee3ecd6..6c56c43`: exit `0`.

The first `CHANGES_REQUESTED` conclusion remains part of this record. Attempt 2 supersedes it only for the repaired frozen subject `6c56c43`; it does not change `BUG-015`, the physical Python-absent/old-machine `NOT_EXECUTED` boundary, or the host UI/session discovery `NOT_EXECUTED` boundary.
