# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Supplied support matrix: Android 14/D1 and iOS 17/D2. Raw coupon=A%2BB must decode once to A+B. B-1 drops coupon on D1 cold start. B-2 retains A+B, correct route and permission on D2 warm start. B-3 debits 20 for op7 before backgrounding, then debits another 20 on resume. B-4 queries op7 on resume and shows paid 20 with one ledger entry. B-5 calls Android 15 passed without execution. Decide FAIL/PASS/NOT_RUN with raw URI, persistent state and matrix gaps.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| B-1 | FAIL |
| B-2 | PASS |
| B-3 | FAIL |
| B-4 | PASS |
| B-5 | NOT_RUN |

## Verification Method

1. Select OS×device×install/upgrade×network×lifecycle combinations from distribution, changes, and incidents. Record samples and gaps; do not invent supported devices.
2. Preserve raw deeplink URI, decoding policy, route/parameters, and authorization. Compare cold/warm/resume paths; restoration must not drop parameters or double-decode.
3. For interrupted payments retain order/operation IDs and commit point. Read back ledger state and reconcile UI on resume; query lost responses before retrying to avoid duplicate payment.
4. Check upgrade data compatibility, permissions, process termination/restoration, and resources. Unexecuted devices are candidates; support claims require actual device evidence.
