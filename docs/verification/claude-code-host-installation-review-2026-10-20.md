# Independent review — Claude Code host installation — 2026-10-20

- Review ID: `DOC-CR030-INDEPENDENT-REVIEW-001`
- Change: `CR-030`
- Reviewer task: `TASK-126`
- Subject: `053c2870c3387c2540f1bbfda485a6de4b699c13`
- Test evidence reviewed: `EVID-CLAUDE-CODE-HOST-INSTALLATION-2026-10-20`
- Reviewer: independent reviewer (`/root/claude_host_independent_review`)
- Result: `FAIL`
- Severity count: P0 0, P1 1, P2 0, P3 1

## Findings

### P1 — Ancestor links bypass the installer's target-containment safeguard

`REQ-027` requires the project route not to write outside the named project
target and the user route not to write outside the current user's Claude Skill
target. The installer checks only the final `target` for a symlink or Windows
reparse point (`qa_master/codex_skill.py:142-146`). It does not inspect any
ancestor before creating parent directories and a staging directory
(`qa_master/codex_skill.py:156-160`) or publishing the staged tree
(`qa_master/codex_skill.py:195`). Consequently, a linked or junctioned
`.claude`, `skills`, or other ancestor can redirect the documented apparent
target to another filesystem location. This is inconsistent with the existing
explicit rejection of target and nested reparse points and leaves the stated
containment acceptance criterion unenforced.

The independent test used ordinary disposable directories. It did not exercise
a linked ancestor. A bounded Windows junction probe at the `skills` ancestor
did not complete within 30 seconds and was interrupted; it is not PASS evidence.
Add ancestor-link/junction rejection through the filesystem root, or explicitly
define and enforce a resolved-target containment policy, then independently test
both user-like and project-like routes.

### P3 — The evidence does not exercise a successful managed update

`NFR-011` says the existing update, backup and manifest controls remain
applicable. The evidence exercises initial install, idempotence, and rejection
of a locally modified target, but explicitly does not exercise a real
version-to-version update. A successful update creates staging, recovery, and
backup artifacts outside the final `qa-master` directory
(`qa_master/codex_skill.py:159-160,171-195`). This is compatible with the
documented backup design, but the literal `REQ-027` phrase "does not write
outside ... target" does not state this exception. Clarify the controlled
locations in the requirement and add a successful-update case before claiming
the whole updater safeguard is verified for the Claude route.

## Conformance observations

- The README and getting-started guide give short user and project commands for
  Windows and preserve the existing Codex/OpenCode route. The Linux/macOS path
  uses the appropriate `/` separator. No conflicting manual-venv step remains.
- The documented personal and project paths and `/qa-master` invocation agree
  with the current Claude Code Skills documentation: personal skills use
  `~/.claude/skills/<skill-name>/SKILL.md`, project skills use
  `.claude/skills/<skill-name>/SKILL.md`, and skills can be invoked by
  `/skill-name`: <https://code.claude.com/docs/en/skills>.
- The documents keep Claude Code as the host, DeepSeek as the host-selected
  model, and provider credentials outside QA Master's installer. No API token,
  provider endpoint, or credential-input option is introduced by `053c287`.
- The tester correctly keeps `TC-HOST-002` as `NOT_EXECUTED`. Filesystem copy,
  helper output, and command exit status do not prove discovery or invocation in
  the supplied VS Code session.
- The installed CLI used by the tester is not cryptographically bound to the
  subject commit. The evidence discloses this limitation, and the frozen change
  has no `qa_master/` delta from its parent, so this does not create an
  additional finding for this documentation-only increment.

## Decision

`TC-HOST-003` is `FAIL`. The documented Claude paths and credential boundary are
sound, but the unresolved P1 containment gap prevents approval. `TC-HOST-001`
remains only the tester's bounded ordinary-directory result, and `TC-HOST-002`
remains `NOT_EXECUTED`. This review is not a Gate, release, acceptance, host
discovery, model-capability, or test-execution conclusion.

## Attempt 2 — repaired-subject re-review

- Subject: `7d6929bf9b45992e266f20193d40ea7be3b5529d`
- Evidence reviewed: attempt 2 in
  `EVID-CLAUDE-CODE-HOST-INSTALLATION-2026-10-20`
- Result: `PASS`
- Severity count: P0 0, P1 0, P2 0, P3 0

The attempt-1 `FAIL` above is retained as the result for `053c287`. The following
checks apply only to the repaired subject.

### Prior P1 — RESOLVED

`install_skill` now converts the requested path to a lexical absolute path and
uses `lstat` to reject a symlink or Windows reparse point anywhere in the
existing ancestor chain. It repeats this check before parent creation, staging,
update/recovery movement and final publication. This closes the prior gap where
only the final target was checked.

The independent tester exercised the source CLI through a real Windows
ancestor junction. It returned `SKILL_TARGET_CONFLICT` before bundle content was
written, while an ordinary `.claude/skills/qa-master` target still installed a
complete 5,882-file manifest and ran its installed helper. The repository unit
test for the Windows junction also passed. The ordinary directory-symlink test
was skipped on this Windows account because it lacks symlink privilege; the
same `lstat` branch covers both `stat.S_ISLNK` and Windows reparse attributes.

### Prior P3 — RESOLVED

`REQ-027` now explicitly permits installer-owned staging, backup and recovery
locations beneath validated non-linked parents. This matches the existing
update design instead of asserting that every write stays inside the final
`qa-master` directory.

The reviewer independently ran:

```powershell
D:\codex-rd-platform\.venv\Scripts\python.exe -m unittest tests.test_codex_skill.CodexSkillTests.test_managed_upgrade_keeps_restorable_archive -v
```

It passed in 95.983 seconds. The test performs a real managed bundle change,
requires `UPDATED`, verifies that the backup is beside the target, verifies that
the recovery tree is under `.qa-master-recovery`, reads the previous `SKILL.md`
from the archive, and confirms publication of the changed bundle. The updated
requirement and observed behavior therefore agree.

### Attempt-2 decision

`TC-HOST-003` is `PASS` for the repaired installer containment, controlled
update locations, documentation accuracy and host/model/credential boundary.
There are no unresolved P0–P3 findings in this bounded re-review.
`TC-HOST-002` remains `NOT_EXECUTED`: neither this code review nor the installer
tests prove VS Code Claude Code discovery, `/qa-master` visibility, selected
model behavior or a conversation result. This is not a Gate, release,
acceptance or host-integration execution conclusion.
