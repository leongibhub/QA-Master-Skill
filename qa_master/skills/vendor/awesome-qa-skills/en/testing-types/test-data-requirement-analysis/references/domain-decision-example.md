# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

S1 has3 parallel workers, each with independent paid Order and related Refund, sharing forbidden. S2 is a refund scenario without schema/fields. S3 requests real customer emails without collection/sanitization authority. S4 retries the same order twice and must reuse refund_id rather than creating two business keys. Decide SPECIFIED/UNKNOWN/BLOCKED/SPECIFIED with relationships and quantity basis; do not generate or acquire real data.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| S1 | SPECIFIED |
| S2 | UNKNOWN |
| S3 | BLOCKED |
| S4 | SPECIFIED |

## Verification Method

1. Map scenario/risk→entities/states/relationships→values/boundaries→quantity basis→source/authority→setup/cleanup. This Skill analyzes needs, not implicit generation or collection.
2. Quantity derives from concurrency/isolation/repetitions/consumption. Missing counts yield formulas/gaps, not an invented100 rows; session counts are not entity counts.
3. Without schema separate known business relationships from undefined fields/keys and ask minimal questions. Trace cross-entity states/foreign keys rather than merely naming CSV files.
4. Prefer synthetic or permitted sanitized personal data with source constraints, retention/cleanup, and acceptance oracle. Unknown authority is BLOCKED; recommendations are no prepared-data evidence.
