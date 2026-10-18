# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Version v3 originals: AC-7: orders >= 100 currency units have free shipping; an order of exactly 100 was charged 5. AC-8: retries with the same refund_id must not debit twice; retrying a successful 20-unit refund raised the cumulative refund to 40. AC-9: orders < 100 pay 5 shipping; an order of 99 was charged 5. AC-10 says "refund promptly" without a time limit or observable start/end.
Review each original AC ID and text. Keep proposed rewrites separate. Use FAIL/PASS/MISSING_RULE decisions and explain threshold equality and duplicate-request postconditions.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| AC-7 | FAIL |
| AC-8 | FAIL |
| AC-9 | PASS |
| AC-10 | MISSING_RULE |

## Verification Method

1. Select `review` (check existing criteria), `proposed-rewrite` (suggest a rewrite), or `missing-rule` (undefined policy). Retain each original AC ID, version, text, and source; a proposal never replaces the source rule.
2. Produce: AC ID | original criterion | mode | observable oracle | proposed wording | reason for change | product confirmation. Leave undefined rules open.
3. For each comparison, split below/equal/above inputs using the supplied operator. For repeated requests capture the business key, cumulative refund, refundable balance, and persisted state; a successful response does not prove correct accounting.
4. Proposed Given/When/Then wording includes observable data and error paths. Mark a sufficiently defined criterion testable instead of manufacturing ambiguity.
