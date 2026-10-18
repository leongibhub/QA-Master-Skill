# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Gate-v3 requires all critical obligations to PASS with version-matched evidence no older than 24h. UNKNOWN/BLOCKED stops advancement; exceptions need owner approval and unexpired validity. G-1 lacks a test record. G-2 cannot execute because the environment failed. G-3 has a fresh failed assertion with an expired signed exception. G-4 has all fresh required PASS evidence. G-5 has a 48-hour-old PASS. Decide UNKNOWN/BLOCKED/FAIL/PASS with STOP/GO advice; stale or missing evidence cannot become green.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| G-1 | UNKNOWN |
| G-2 | BLOCKED |
| G-3 | FAIL |
| G-4 | PASS |
| G-5 | UNKNOWN |

## Verification Method

1. Define each obligation, evidence version/freshness, operator and PASS/FAIL/BLOCKED/UNKNOWN table. Execution prevented is BLOCKED; missing or indeterminate evidence is UNKNOWN; absence never means PASS.
2. Apply project aggregation and fail-closed rules. Preserve unknown/blocked causes and recommend advancement only when all required gates have fresh valid evidence.
3. Record exceptions separately with scope, authorizer, reason, approval, expiry, compensating controls and revocation. Invalid exceptions do not override or rewrite failures.
4. State triggers, owners, revalidation and stop/rollback conditions. Separate design, evidence comparison and pipeline implementation; missing policy needs Human resolution.
