# PR2 independent installer verification

**Evidence ID:** `EVD-PR2-INDEPENDENT-001` v2  
**Task:** `TASK-047`, independent tester `/root/pr2_test`  
**Final tested subject:** base commit `0ae0ec0287a62d1b91e0c108c5d9def377cd70a2` with the uncommitted repair `qa_master/codex_skill.py` SHA-256 `E008FBD1263BD32CBE9E7C62C688F3D4CDAD3B15D2CAEB4BC21DDC24C1B3F93F`.  
**Environment:** Windows and `D:\codex-rd-platform\.venv\Scripts\python.exe` (Python 3.13.5). No model, enterprise system, user-wide installation, or external write was invoked.

## Final executed cases

| ID | Requirement / risk | Observable result | Status | Evidence |
| --- | --- | --- | --- | --- |
| TC-PR2-001 | Self-contained local skill and no-execution boundary | Disposable-project install returned `INSTALLED` and `NOT_EXECUTED`; installed helper ran with `-I` from a different directory, found six guides and no gaps. | PASS | `wheel-final-skill-install.txt`, `wheel-final-isolated-smoke.txt` |
| TC-PR2-002 | Managed update, full backup and discovery containment | Explicit update retained the original complete ZIP, returned a recovery path below `.agents/.qa-master-recovery`, and left exactly one `SKILL.md` below `.agents/skills`. | PASS | `tests/test_codex_skill_independent.py`; `post-repair-focused-final.txt` |
| TC-PR2-003 | Verify-to-detach, archive-time and rollback races (`BUG-009`, `BUG-011`) | A user edit injected after last verification and a late edit injected while archiving were both rejected; the late edit was restored. A synthetic double publication/rollback failure returned `SKILL_INSTALL_RECOVERY_REQUIRED` with the complete old tree retained outside discovery. | PASS | `tests/test_codex_skill_independent.py`; `post-repair-focused-final.txt` |
| TC-PR2-004 | User data and link/reparse defenses (`BUG-010`, `BUG-012`) | A non-`.pyc` file under `__pycache__` caused update refusal and was retained. A Windows junction target was refused without changing the external marker. Manifest hashes matched every managed file. | PASS | `tests/test_codex_skill_independent.py`; `post-repair-focused-final.txt` |
| TC-PR2-005 | Strict regression and warning hygiene | `Ran 562 tests in 59.722s`, `OK (skipped=2)` with `ResourceWarning` promoted to error. | PASS | `full-strict-final-task047.txt` |
| TC-PR2-006 | Repaired wheel packaging and isolated use | Fresh wheel `qa_master_skill-0.1.0-py3-none-any.whl`, SHA-256 `0CED0B3412375FBCF6765611064BDE7AF34BA637577A0EC4BF3240C7C7D8CCAF`, built, installed with `--no-index --no-deps` into a new virtual environment, and passed the isolated helper smoke. | PASS | `wheel-final-build.txt`, `wheel-final-install.txt`, `wheel-final-skill-install.txt`, `wheel-final-isolated-smoke.txt`, `wheel-final-summary.json` |

The two skipped cases require ordinary filesystem symbolic-link creation. This
Windows session returned `WinError 1314`; these branches are **NOT EXECUTED**.
The junction case was executed separately and passed.

## Repair history and limits

`BUG-009` through `BUG-012` are reviewer-reported defects. Their original-source
reproductions are reviewer evidence; this tester did not capture the original
source hash before concurrent repair changed the working tree. Accordingly,
`pre-repair-regressions.txt` is retained only as an intermediate repair snapshot
(10 tests, 2 skips), not as proof of original failure. The earlier 557-test result
is a pre-repair baseline and is not final verification.

The current repaired subject passed the bounded independent cases above. This does
not close the BUG records, constitute human acceptance, validate a fresh Codex
session or model behavior, prove real system integration, or establish superiority
over another skill.
