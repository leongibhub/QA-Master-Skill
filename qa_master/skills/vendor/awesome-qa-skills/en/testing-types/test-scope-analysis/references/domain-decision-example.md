# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

New v2 refund feature: confirmed web/API and paid orders; native explicitly excluded; guest refunds undefined. S1 web/API paid path; S2 native; S3 guest boundary; S4 proposed real production debit lacks authority, with a critical obligation needing isolated verification. Decide INCLUDE/EXCLUDE/UNKNOWN/BLOCKED with version/layer/platform/state cells and reassessment triggers when policy arrives; new-feature scope is not merely regression scope.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| S1 | INCLUDE |
| S2 | EXCLUDE |
| S3 | UNKNOWN |
| S4 | BLOCKED |

## Verification Method

1. Build scope cells for version×layer×platform×data state from the delivery objective, linked to requirements, include/exclude evidence, owners, and observable acceptance. New-feature scope is broader than change-only regression.
2. Separate INCLUDE, EXCLUDE, and UNKNOWN. Exclusions need a sourced scope or independent-contract reason; unclear platform/data/boundary support cannot mean 'do not test'.
3. Record budget/environment/authority blockers and residual risk. Escalate unmet critical obligations rather than inventing product boundaries or accepting risk.
4. Changes in requirements, platforms, interfaces, or versions trigger reassessment. Selection/design, execution, and satisfaction remain separate; a checklist is not coverage proof.
