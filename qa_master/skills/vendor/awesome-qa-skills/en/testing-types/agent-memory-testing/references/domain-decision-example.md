# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

M-v3 policy: strict tenant isolation; highest valid preference version wins; no retrieval immediately after deletion acknowledgment. M-1: A's preference query retrieves B/m9. M-2: A/m1 v1=SMS, v2=email, both valid; response still uses v1. M-3: A/m2 deletion acknowledged but index returns m2. M-4: A retrieves its own valid m3 v2 with no B records. M-5: assess backup expiry without a backup retention policy. Decide FAIL/PASS/UNKNOWN per ID.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| M-1 | FAIL |
| M-2 | FAIL |
| M-3 | FAIL |
| M-4 | PASS |
| M-5 | UNKNOWN |

## Verification Method

1. Capture tenant/user IDs, memory ID, content version, source, write time, expiry, and withdrawal/deletion status. Retain retrieved provenance/version, not only the final answer.
2. Resolve old/new preferences using supplied precedence rules. Undefined conflicts remain open; never assume last-write-wins or invent retention periods.
3. Compare visibility for the same query in two tenants. Assess stale versions, expired returns, and post-deletion retrieval using the project's consistency window.
4. Check deletion across the actual index/cache/backup scope. Missing propagation/backup policies limit the conclusion. Include permitted retrieval as the isolation control.
