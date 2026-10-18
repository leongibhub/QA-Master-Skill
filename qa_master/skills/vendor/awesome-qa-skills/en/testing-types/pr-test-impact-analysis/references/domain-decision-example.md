# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

PR base=b1/head=h2 changes shared Money units from cents to decimal. E1 maps Money→refund→O-refund→T-refund. E2 maps Money→invoice→O-invoice→T-invoice. E3 removes the only T-tax protection for O-tax. E4 has unmapped dynamic plugin consumers. E5 is an independent avatar contract with no money dependency. Decide INCLUDE/COVERAGE_GAP/UNKNOWN/EXCLUDE for E1–E5 with base/head, test IDs and transitive evidence; diff size alone cannot justify unit-only scope.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| E1 | INCLUDE |
| E2 | INCLUDE |
| E3 | COVERAGE_GAP |
| E4 | UNKNOWN |
| E5 | EXCLUDE |

## Verification Method

1. Fix repository/base/head SHAs and diff scope. Source file/symbol/schema/config changes; names alone do not prove impact and results from different HEADs cannot be pooled.
2. Map changed symbol→direct/transitive consumer→obligation→test ID/layer/execution version. Label edges confirmed/candidate/unknown and stop only at evidenced isolation boundaries.
3. For removed/weakened tests check whether their obligations retain independent protection; selection from the remaining inventory alone can hide disappeared coverage.
4. Unknown dynamic dependencies/mappings trigger conservative contract/integration candidates with explicit gaps. Separate scope candidates, executed tests, and satisfied obligations; list expansion/escalation triggers.
