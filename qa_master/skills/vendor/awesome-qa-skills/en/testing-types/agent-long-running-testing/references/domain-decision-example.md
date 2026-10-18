# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Protocol L-v1: checkpoint v2 records committed steps; expired leases cannot commit; one execution per task_id; cancellation after commit returns completed. L-1: A commits before crash; v2 recovery runs only B; active resources=0. L-2: recovery repeats A with a second write. L-3: expired lease=4 still commits. L-4: cancellation follows commit; state completed, active resources=0. Decide PASS/FAIL for each, checking versions, writes, and release evidence.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| L-1 | PASS |
| L-2 | FAIL |
| L-3 | FAIL |
| L-4 | PASS |

## Verification Method

1. Derive queued→running→checkpointed→interrupted→resuming→completed and running→cancelling→cancelled from the actual protocol; undefined transitions remain open.
2. Capture task_id, checkpoint schema/state version, committed step IDs, provenance, and integrity. Validate versions and committed effects before resuming; incompatible checkpoints cannot be blindly replayed.
3. Record owner, lease/fencing token, and expiry policy. A worker that loses its lease must not commit. Merge/reject duplicate task IDs according to project idempotency rules; do not assume exactly-once delivery.
4. Reconstruct cancellation versus commit races using the specified commit point. Preserve committed results and verify terminal state, released resources, and cancellation acknowledgment; missing race rules require Human decisions.
