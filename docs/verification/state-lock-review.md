# BUG-013 state-lock repair review

- Artifact ID: `DOC-STATE-LOCK-REVIEW-001`
- Evidence ID: `EVD-STATE-LOCK-REVIEW-001`
- Task: `TASK-052`
- Reviewer: independent reviewer `/root/pr2_review`
- Requirement / defect: `REQ-002` / `BUG-013`
- Document State: `DRAFT`
- Evaluation State: `DECIDED`
- Review conclusion: `PASS` for the bounded repair
- Change base: `1e77810`
- Repair commit: `ba7c49f`
- Reviewed source: `qa_master/state_store.py`, SHA-256
  `94660A7F7171442E19DC40C2E67E5892BB5D7C37B17EAD00BAB1B1446998C911`

## Scope and conclusion

This review covers only the BUG-013 change that moves zero-byte lock-sentinel
initialization inside the existing exclusive file-lock region, plus its developer
and independent concurrency evidence. It does not review the paired-evaluation
changes sharing the checkout, close BUG-013, decide a Gate, recommend a release,
or make a full-product acceptance claim.

No P0, P1, P2 or P3 finding remains in this bounded diff. Moving the sentinel
write after lock acquisition removes the reproduced write-before-lock race without
changing revision CAS, state schema, atomic replacement, legacy backup, or conflict
semantics. The reviewed result is supported by real Windows thread and independent
process contention, including reuse of the settled lock.

## Failure and repair analysis

The retained historical log
`docs/verification/evidence/cr011-independent/repaired-full.txt` records the actual
pre-repair failure: one `TC-SM-005` initializer raised `PermissionError` at
`lock.flush()` before entering the lock, leaving only the winning `created` outcome
instead of `created` plus `conflict`. The run ended with one failure and is not
relabelled as passing evidence.

At the base revision, every opener of a new or empty lock file could observe size
zero and write the sentinel before `msvcrt.locking`. Another contender could acquire
the byte-zero lock between that size check and write, causing the observed Windows
permission failure. The repair seeks to byte zero, acquires the platform lock, and
only the lock owner checks and initializes the sentinel. A later contender cannot
enter the initialization block until the first owner releases the lock.

The developer's direct Windows probe demonstrated that `msvcrt` can lock byte zero
of a zero-length file and that a second process receives the expected contention
error while the byte is held. This supports the ordering change; the sentinel remains
one byte after the first successful owner flushes it. Process exit or an exception
still releases the OS lock through the existing context-manager path.

## Evidence reviewed

| Evidence | Subject and result | Review assessment |
| --- | --- | --- |
| Developer source and record | `tests/test_state_lock_race.py` SHA-256 `FF2D7647FAD849CF817CA180E39ABA9F0B8A7751EEB007B99CF42F28096CB883`; `docs/verification/state-lock-race-repair.md` SHA-256 `6AC8A0EB3AE54E63E16A27B94611A0E4EFF42886344689D6A60C992CF271BEB5`; 5 focused tests passed and the dedicated race test passed 10 repeated runs. | Relevant developer evidence; not used alone as independent acceptance. |
| Independent concurrency tests | `tests/test_state_lock_independent.py` SHA-256 `42F9C07BF1A447DA953539DAF53933BB6E6084F1276D54A8EBD352242D03FE0F`. Three two-thread rounds and three two-process rounds each produced one save and one `StateConflictError`. | Directly exercises the original empty-file initialization boundary with both in-process and OS-process contenders. |
| Independent persisted-state checks | Every round retained complete revision-1 JSON, lock bytes `b"0"`, and no `.qa-master-state-*.json`; every process round then saved revision 2 through the settled lock. | Supports data integrity, cleanup and post-race reuse, rather than merely absence of the original exception. |
| Independent selected regression | Five relevant tests passed in 3.101 seconds with `ResourceWarning` treated as error. Report `docs/verification/state-lock-independent.md` SHA-256 `05F1B5D0958ED88058D442D1DEBBA9614EEB8236F17E126077ADDFF7EABEC1A9`. | Supports compatibility with existing CAS, migration and application initialization behavior. |
| Reviewer execution | The same five focused tests passed in 3.095 seconds; `git diff --check` passed. | Confirms the reviewed checkout reproduces the focused evidence. |

## Requirement, concurrency and failure-handling assessment

- **REQ-002 concurrency:** exactly one initializer publishes revision 1 and the
  loser receives `StateConflictError`; no silent overwrite or partial state was
  observed.
- **Data integrity:** the repair does not alter the destination read, revision and
  optional SHA checks, unique temporary-file write, `fsync`, or atomic replacement.
- **Failure handling:** sentinel initialization remains under `try/finally` protected
  lock ownership. The prior pre-lock write and flush have been removed.
- **Backward compatibility:** existing non-empty one-byte lock files skip the write;
  new and deliberately empty lock files converge to the same `b"0"` representation.
- **Security and secrets:** the change writes only the existing fixed sentinel and
  introduces no user payload, credential, network operation or external side effect.

## Limits retained

The independent execution environment was Windows with Python 3.13.5. The POSIX
`flock` path is structurally unchanged and was not independently fault-injected by
TASK-051. The state-lock tester intentionally ran a bounded selected regression,
not the whole suite; any later full-suite result belongs to its separately identified
executor and source revision. The existing blocking behavior and timeout semantics
of `msvcrt.LK_LOCK` and `fcntl.flock` were not changed or performance-qualified by
this repair. These limits do not reproduce a defect in the changed ordering, but
they prohibit broader cross-platform durability, performance, Gate, release or
acceptance claims.

BUG-013 remains open for governance to disposition after this evidence is registered;
this review does not close it.
