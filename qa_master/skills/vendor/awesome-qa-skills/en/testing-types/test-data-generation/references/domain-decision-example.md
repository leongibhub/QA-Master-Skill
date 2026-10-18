# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Schema:unique Order.id; Refund.order_id must exist; amount>0 and cumulative refunds<=Order.total; only paid orders may refund. D1 O1 total20 paid with F1 amount5, labeled valid. D2 two orders with idO1, labeled valid. D3 F2 references absent O9, labeled invalid with expected foreign-key rejection. D4 O2 pending with refund5, labeled valid. Decide VALID/INVALID/MATCHED_NEGATIVE per group, deliver a reproducible seed7 valid sample, and cleanup Refund before Order.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| D1 | VALID |
| D2 | INVALID |
| D3 | MATCHED_NEGATIVE |
| D4 | INVALID |

## Verification Method

1. Derive groups from supplied schema, foreign keys, uniqueness, state relationships, and scenario oracles. Fix seed/generator version; missing rules remain UNKNOWN without invented fields or real identities.
2. Separate valid happy/boundary data from deliberate invalid groups. Name the violated constraint and expected allow/reject outcome while preserving other relationships; invalid rows cannot silently enter valid groups.
3. Deliver actual sanitized samples with uniqueness, foreign-key, type/range, state, and reproducibility checks. Equal seeds must reproduce data identities, not merely a strategy statement.
4. Use isolated IDs/namespaces with provenance, privacy restrictions, and reverse dependency cleanup. Missing authority prevents real personal-data collection; synthetic rows do not establish population representativeness.
