# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Authorization permits read-only checks on isolated fixture tenants A/B. S1 automated scan has zero findings, business authorization untested. S2 A reads own O1 as allowed with no foreign data. S3 A reads B/O2 and receives200 plus B's amount; logs/response supplied. S4 is a deletion-permission plan with no run or deletion authority. Decide NOT_RUN for S1's business authorization, CONTROL_PASS for S2, CONFIRMED for S3, and DESIGNED for S4 with threat/control/evidence mapping; no whole-system safety claim from S1.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| S1 | NOT_RUN |
| S2 | CONTROL_PASS |
| S3 | CONFIRMED |
| S4 | DESIGNED |

## Verification Method

1. Within actual authorization map asset/principal→threat→control→steps→oracle→evidence/state. Record environment, permitted actions, stop conditions, and authority provenance.
2. Pair authorized access with unauthorized-denial controls. Denial requires no data disclosure or tool/write effects; error responses and scans alone are insufficient.
3. Separate DESIGNED plans, EXECUTED evidence, and CONFIRMED control failures supported by supplied observations. Unchecked business authorization stays NOT_RUN/UNKNOWN; static indications are candidates.
4. A clean scan covers its scanned surface only. Missing authority permits design/static review; real exploitation/production actions require explicit scope. Do not generate dangerous content or extend testing without authorization.
