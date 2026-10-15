# TASK-050 state-lock initialization race repair

- Defect: `BUG-013` / `DOC-DEFECT-STATE-LOCK-INIT-RACE-001`
- Requirement: `REQ-002` local state concurrency
- Source subject: `qa_master/state_store.py`
- Document State: `DRAFT`
- Evaluation State: `IN_REVIEW`
- Evidence Status: `OBSERVED`

## Observed failure and minimal repair

The independently retained strict regression output at
`docs/verification/evidence/cr011-independent/repaired-full.txt` recorded a
parallel `TC-SM-005` initialization where the losing worker raised
`PermissionError: [Errno 13] Permission denied` from `_file_lock()` at
`lock.flush()`. The original code initialized the one-byte lock-file sentinel
before acquiring the file lock, so the expected loser outcome
(`StateConflictError`) was absent.

On the Windows test host, a direct `msvcrt.LK_NBLCK` probe acquired byte zero
of a newly created zero-byte lock file, and a second process received errno 13
while that lock was held. This establishes that the sentinel need not be
written before the lock is acquired.

The repair moves only the existing empty-file sentinel write and flush inside
the existing exclusive-lock region. It retains the one-byte sentinel, the
platform-specific lock mechanism, the subsequent CAS checks, and the atomic
temporary-file publication path. It does not change state schema, revisions,
or conflict semantics.

`tests/test_state_lock_race.py` starts two initializers against a deliberately
pre-created empty lock file. It requires exactly one creation, one
`StateConflictError`, a finalized one-byte sentinel, no unexpected I/O failure,
and no temporary state file. This test is developer regression coverage only;
the historical full-suite failure remains retained and no independent retest,
defect closure, Gate decision, or acceptance is claimed here.

## Developer verification

On the Windows host with
`D:\\codex-rd-platform\\.venv\\Scripts\\python.exe -X utf8`, the focused command

```text
python -m unittest tests.test_state_lock_race \
  tests.test_application_independent.CanonicalWorkflowIndependentTests.test_tc_sm_005_parallel_init_has_one_winner_without_partial_state \
  tests.test_state_store -v
```

passed 5 tests in 3.088 seconds. The dedicated test was then repeated 10 times:
all 10 executions passed, each in 1.012–1.029 seconds. `git diff --check` also
passed. These are developer observations only. Independent testing and review
are separate work, and the original full-suite failure remains historical
evidence rather than a rewritten result.
