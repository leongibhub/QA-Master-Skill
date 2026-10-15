# Independent state-lock repair verification

**Evidence ID:** `EVD-STATE-LOCK-INDEPENDENT-001` v1  
**Scope:** `TASK-051`, `BUG-013`, `REQ-002` local revisioned-state concurrency  
**Tester:** independent tester `/root/pr2_test`  
**Subject:** `qa_master/state_store.py`, SHA-256 `94660A7F7171442E19DC40C2E67E5892BB5D7C37B17EAD00BAB1B1446998C911` on the local candidate.  
**Environment:** Windows, Python 3.13.5 at `D:\codex-rd-platform\.venv\Scripts\python.exe`.

## Historical defect evidence

`docs/verification/evidence/cr011-independent/repaired-full.txt` retains the
pre-repair strict-suite observation: a parallel `TC-SM-005` initializer raised
`PermissionError: [Errno 13] Permission denied` at `_file_lock`'s `lock.flush`,
and the expected conflict outcome was absent. That historical run also finished
with one `TC-SM-005` failure. It is not rewritten as a pass.

## Executed independent tests

| ID | Objective and procedure | Observable result | Status | Evidence |
| --- | --- | --- | --- | --- |
| TC-SL-001 | For three fresh zero-byte lock files, release two real Python threads together to create the same state. Require one created document, one `StateConflictError`, a complete JSON winner at revision 1, byte `0` sentinel, and no state temporary file. | All three rounds produced exactly one save and one conflict; every persisted document parsed completely and each lock contained `0`. | PASS | `tests/test_state_lock_independent.py`; `evidence/state-lock-independent/focused.txt` |
| TC-SL-002 | For three fresh zero-byte lock files, synchronize two independent Python processes at a file start gate. Require one save and one conflict; then save revision 2 through the settled lock. | All three process rounds produced exactly one save and one conflict, no child process error, no partial JSON or temporary state file, and the settled reuse saved revision 2. | PASS | `tests/test_state_lock_independent.py`; `evidence/state-lock-independent/focused.txt` |
| TC-SL-003 | Run the relevant existing state-lock, parallel application initialization, and state-store regressions with `ResourceWarning` treated as error. | Five tests completed in 3.101 seconds with `OK`. | PASS | `evidence/state-lock-independent/selected-regression.txt` |

No product defect was reproduced against the stated repair subject. This bounded
evidence does not close `BUG-013`, replace independent review, validate every
platform/filesystem combination, or make a Gate or acceptance decision. A paired
tester owns the single later full-suite result; no full suite was repeated here.
