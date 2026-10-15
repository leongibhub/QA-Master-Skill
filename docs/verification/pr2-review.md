# PR2 installer repair review

- Artifact ID: `DOC-CODEX-CORE-INDEPENDENT-REVIEW-001`
- Evidence ID: `EVD-CODEX-CORE-INDEPENDENT-REVIEW-001`
- Reviewer: independent reviewer `/root/pr2_review`
- Review conclusion: `PASS WITH P3 FOLLOW-UP`
- Evaluation state: `DECIDED`
- Base commit: `0ae0ec0287a62d1b91e0c108c5d9def377cd70a2`
- Repair source: working-tree `qa_master/codex_skill.py`, SHA-256
  `E008FBD1263BD32CBE9E7C62C688F3D4CDAD3B15D2CAEB4BC21DDC24C1B3F93F`
- Independent test source observed during review: SHA-256
  `0EB17370A2AC0B7033474C0841F59EDFF1BCFAFD4885A9D5434491DBC8F4AFE6`
- Independent test evidence: `EVD-PR2-INDEPENDENT-001` v2 at
  `docs/verification/pr2-independent.md`, SHA-256
  `E61EC2F47511CD204C353049B426311F4D1BED022A1D160D40528D6D10507C2B`

## Scope and disposition

This review covers the self-contained Codex Skill installer and the repair of the
data-preservation, failure-recovery and Windows reparse-point findings reproduced
against PR2. It does not review model behaviour, remote execution, enterprise
integration, comparative quality, acceptance, release, or the whole V1 product.

No P0, P1 or P2 finding remains in the bounded repair source identified above.
The repair has current independent focused, strict-regression and fresh-wheel
evidence and passes this bounded local review with the P3 follow-up below. This is
not a Gate decision, human approval, release recommendation or full-V1 conclusion.

## Finding disposition

| Original finding | Severity | Repair evidence | Disposition |
| --- | --- | --- | --- |
| A concurrent save between verification and publication could disappear from both the new install and ZIP backup. | P1 | The installer now atomically detaches the old tree into a persistent recovery location, verifies it before and after archive creation, and restores it on detected modification. Reviewer fault injection changed `SKILL.md` during ZIP creation; installation raised `SKILL_TARGET_MODIFIED` and the changed bytes were restored at the active target. | RESOLVED in reviewed source |
| Every file below a directory named `__pycache__` was ignored, so an unknown user file could be deleted without backup. | P2 | Only direct `__pycache__/*.pyc` files are excluded from the managed-state comparison. Reviewer reproduction placed `user-notes.txt` in that directory; update raised `SKILL_TARGET_MODIFIED` and retained the file. The archive traverses all files in the detached tree. | RESOLVED in reviewed source |
| If staged publication and rollback rename both failed, temporary-directory cleanup removed the old installation. | P2 | The detached tree is now outside the temporary staging directory. Reviewer double-failure injection produced `SKILL_INSTALL_RECOVERY_REQUIRED:<path>`; the active target was absent as expected, while the complete old tree remained at the reported recovery path. | RESOLVED in reviewed source |
| Windows junctions bypassed `is_symlink()` checks and were treated as managed directories. | P2 | `_linked` checks symbolic links and Windows reparse-point attributes at the target and inside the managed tree. A real `mklink /J` target was rejected with `SKILL_TARGET_CONFLICT`, and its external marker was unchanged. | RESOLVED in reviewed source |
| The first persistent-recovery repair retained the old `SKILL.md` as a sibling below `.agents/skills`, creating two discoverable entries named `qa-master`. | P1 | Standard project/user installs now retain old trees under `.agents/.qa-master-recovery`, outside the Skill discovery root. After a successful reviewer update, recursive enumeration below `.agents/skills` found exactly one `SKILL.md`; the recovery tree remained available at the returned path. | RESOLVED in reviewed source |

## Current checks

Reviewer-executed checks on the identified repair source:

- `python -X utf8 -m unittest tests.test_codex_skill -v`: 9 passed.
- `python -X utf8 -m unittest tests.test_codex_skill_independent -v`: 11 run,
  9 passed and 2 skipped. The skipped cases require Windows symbolic-link privilege;
  the real Windows junction case executed and passed.
- TASK-047 final strict regression: 562 tests in 59.722 seconds, 560 passed and
  2 skipped, with `ResourceWarning` promoted to error. Evidence:
  `evidence/pr2-independent/full-strict-final-task047.txt`.
- TASK-047 fresh wheel SHA-256
  `0CED0B3412375FBCF6765611064BDE7AF34BA637577A0EC4BF3240C7C7D8CCAF`
  installed with `--no-index --no-deps` into a new virtual environment; the
  installed helper ran with Python `-I` from another directory and found all six
  guides with no gaps.
- Separate reviewer fault injection covered archive-time concurrent modification,
  publication plus rollback failure, unknown data below `__pycache__`, duplicate
  discovery after a successful update, and a real Windows junction. All five
  produced the required preservation or refusal result.
- `git diff --check`: passed for the current working tree at review time.

The final tester evidence binds the same repair source SHA-256 recorded above.
Earlier pre-repair full-suite results remain historical and are not used for this
conclusion. A new remote CI result for the eventual committed repair is separate
evidence and is not required for this bounded local review.

## P3 follow-up and evidence limits

**P3 — retained recovery trees require manual lifecycle management.** Every successful
update intentionally keeps both a ZIP and a full recovery directory. README now tells
the user to inspect and remove the recovery directory manually, which preserves data
but can accumulate storage across repeated updates. A future bounded cleanup/listing
command should identify only installer-owned recovery directories and require an
explicit user choice before removal.

The Windows host could not create ordinary symbolic links (`WinError 1314`), so the
target-symlink and nested-symlink test branches are `NOT_EXECUTED` here. Source review
shows the existing `is_symlink()` rejection remains, and the independently executable
junction/reparse path passed. Current cross-platform CI is still required after the
repair is committed. Process or machine loss after detaching the old tree is also not
an automatic-recovery guarantee; the design preserves the old bytes in the hidden
recovery directory but may require manual restoration after an interrupted process.

