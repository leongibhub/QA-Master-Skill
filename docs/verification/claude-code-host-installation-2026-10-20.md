# Independent Claude Code host-installation verification — 2026-10-20

- Evidence ID: `EVID-CLAUDE-CODE-HOST-INSTALLATION-2026-10-20`
- Change: `CR-030`
- Tester task: `TASK-125`
- Subject: `053c2870c3387c2540f1bbfda485a6de4b699c13`
- Executor: independent tester (`/root/claude_host_independent_test`)
- Observed: 2026-10-20T11:31:04+08:00 to 2026-10-20T11:34:58+08:00
- Environment: Windows 11 Professional Workstation 10.0.26200; Python 3.13.5;
  uv 0.11.6; PowerShell; installed `qa-master.exe` at
  `C:\\Users\\leon.wang\\.local\\bin\\qa-master.exe`.

This is an installer and documentation result, not a Gate, release, acceptance,
or evidence that a VS Code extension loaded the Skill.

## Results

| Test case | Result | Observable evidence |
| --- | --- | --- |
| TC-HOST-001 | PASS (bounded) | Explicit installation to separate disposable user-like and project-like `.claude/skills/qa-master` targets returned `INSTALLED`, each with `files: 5882`. Each manifest declared 5,882 files; a full SHA-256 comparison found `missing: 0` and `hash_mismatch: 0`. The user-like installed helper executed with `py -3 -I` and reported vendor `330`, `en: 165`, `zh: 165`, status `DISCOVERED`. Re-install returned `UNCHANGED`. A deliberate local edit then made `--update` return exit 2 / `SKILL_TARGET_MODIFIED`; the edit remained in place and no backup or recovery directory was created. The focused documentation and README/catalog regression run completed 7 tests with `OK`. |
| TC-HOST-002 | NOT_EXECUTED | The supplied VS Code Claude Code session was not available to this tester. No extension discovery, slash-command listing, manual `/qa-master` invocation, model behaviour, or DeepSeek configuration result is inferred from the copied files. |

## Executed method and results

The candidate checkout was clean and resolved to the subject hash above. The
following check produced no product-source diff between the parent and this
documentation-only subject:

```powershell
git diff --exit-code 053c287^ 053c287 -- qa_master
```

The installed CLI was used because the documented user workflow invokes
`qa-master`. It was directed only at a disposable root:

```text
C:\Users\leon.wang\AppData\Local\Temp\qa-master-tc-host-001-053c287\
  user-home\.claude\skills\qa-master
  project\.claude\skills\qa-master
```

For both targets, the exact invocation was:

```powershell
qa-master install-codex --target "<disposable target>"
```

Both commands returned `status: INSTALLED`, the exact supplied target path,
`files: 5882`, `backup: null`, `recovery_directory: null`, and
`execution: NOT_EXECUTED`. A recursive post-install inventory of the disposable
root found only the two expected target branches and their required parent
directories; it found no unrelated file or sibling Skill entry. This establishes
bounded containment inside the disposable root, while allowing the necessary
`.claude` and `skills` parent directories.

For each target, `.qa-master-install.json` had `schema_version: 1`, 5,882
declared entries, zero missing entries, and zero SHA-256 mismatches. Both had
`SKILL.md`, `scripts/qa.py`, `references/`, and `examples/`. The user-like
helper was then run from the installed target, not from the checkout:

```powershell
py -3 -I "<target>\scripts\qa.py" skills
```

Its parsed result was `vendor_count: 330`, `en: 165`, `zh: 165`, and
`vendor_status: DISCOVERED`.

For update safety, a second install of the unchanged user-like target returned
`UNCHANGED` with `files: 5882`. A temporary line was appended to the project
target's `references/domains.md`; the command below returned exit 2 and
`{"error": "SKILL_TARGET_MODIFIED"}`:

```powershell
qa-master install-codex --target "<project target>" --update
```

The temporary edit was retained, `qa-master.backup-*.zip` count was zero, and
no `.qa-master-recovery` directory existed. This negative result confirms that
an altered managed target is not overwritten by `--update`; it does not
exercise a real version-to-version backup because the frozen product source did
not change in CR-030.

The command help listed only `--user`, `--project`, `--target`, and `--update`.
A scoped static inspection of the two onboarding documents and the install
parser found the Claude/DeepSeek wording only in the host/model boundary text:
it says QA Master does not read or configure the endpoint, password, or API
Token. No credential value or credential-input option was supplied or observed.

The focused regression command completed successfully:

```powershell
py -3 -m unittest tests.test_installation_docs tests.test_readme_catalog -v
```

It ran 7 tests in 0.112 seconds with `OK`, covering the uv/no-manual-venv
Windows contract, both host path strings, token boundary wording, restart and
update wording, every catalog link, layer counts, the single-entry invariant,
and the README evidence boundary.

## Limits and defects

No new defect was established. The broad `tests.test_codex_skill` run was not
used as PASS evidence: it was stopped after it exceeded the bounded verification
time while copying the large self-contained bundle. The independently executed
target installs, full manifests, installed-helper check, idempotence, modified
target rejection, and focused regression above are the evidence for
TC-HOST-001.

The command-level exercise used the already installed user `qa-master` tool;
its package metadata does not expose an immutable Git commit. The frozen commit
was independently checked and has no `qa_master/` product-source delta from its
parent, so this is adequate for the CR-030 documentation increment but is not a
fresh-wheel-at-commit qualification. Cleanup of the disposable target root is
`NOT_EXECUTED`: the environment rejected the attempted scoped `Remove-Item`
command, so the inspected target remains at the path recorded above.

TC-HOST-002 remains `NOT_EXECUTED`. A filesystem copy, helper discovery count,
or successful CLI exit does not prove VS Code Claude Code discovery, model
selection, or a `/qa-master` conversation.

## Attempt 2 — ancestor-junction repair retest

- Subject: `7d6929bf9b45992e266f20193d40ea7be3b5529d`
- Executor: independent tester (`/root/claude_host_independent_test`)
- Observed: 2026-10-20T11:44:49+08:00 to 2026-10-20T11:45:42+08:00
- Environment: Windows 11 Professional Workstation 10.0.26200; Python 3.13.5;
  PowerShell; checkout import confirmed as `D:\\QA-Master-PR2\\qa_master\\__init__.py`.

This retest covers the P1 ancestor-link repair introduced by `7d6929b`. It
preserves the attempt-1 evidence above and does not convert TC-HOST-002 into an
executed test.

| Check | Result | Observable evidence |
| --- | --- | --- |
| TC-HOST-001A, Windows junction ancestor | PASS | A real Windows directory junction (`Directory, ReparsePoint`) from a disposable `junction-project` to a separate `external` directory was created with PowerShell. `py -3 -m qa_master install-codex --target "<junction>\\.claude\\skills\\qa-master"` returned exit 2 and `{"error": "SKILL_TARGET_CONFLICT"}`. The external directory had 0 entries both before and after; `<external>\\.claude\\skills\\qa-master` and the requested junction target did not exist. |
| TC-HOST-001B, ordinary target regression | PASS | `py -3 -m qa_master install-codex --target "<ordinary-project>\\.claude\\skills\\qa-master"` returned `INSTALLED`, `files: 5882`, and `execution: NOT_EXECUTED`. The installed manifest had schema 1 and 5,882 entries; `SKILL.md`, `scripts/qa.py`, `references/`, and `examples/` existed. The installed helper, invoked through `py -3 -I`, reported vendor 330, English 165, Chinese 165 and `DISCOVERED`. |
| Unit regression for link handling | PASS with one environment skip | `py -3 -m unittest tests.test_codex_skill.CodexSkillTests.test_linked_ancestor_is_rejected_before_install tests.test_codex_skill.CodexSkillTests.test_windows_junction_ancestor_is_rejected_before_install -v` completed `OK (skipped=1)`: the Windows junction case passed; the directory-symlink case was skipped because this user lacks the Windows symbolic-link privilege (`WinError 1314`). |
| Documentation/catalog regression | PASS | `py -3 -m unittest tests.test_installation_docs tests.test_readme_catalog -v` completed 7 tests in 0.123 seconds with `OK`. |
| TC-HOST-002, supplied VS Code Claude Code discovery/manual call | NOT_EXECUTED | No supplied VS Code Claude Code session was available. Neither junction rejection nor ordinary file installation proves host discovery, slash-command visibility, model selection, or a conversation result. |

The repaired source normalizes the requested target lexically and calls
`_assert_unlinked_ancestor_chain` before bundle construction, before parent
directory creation, and at publication/update boundaries. The independent
junction case observed the initial fail-closed boundary in the actual source
CLI and verified that no bundle content reached the junction destination.

The two attempt-2 disposable roots remain for inspection because the environment
previously rejected the scoped cleanup command. No production, user-profile
Claude directory, VS Code configuration, credential, external QA system, or
business-test target was changed.
