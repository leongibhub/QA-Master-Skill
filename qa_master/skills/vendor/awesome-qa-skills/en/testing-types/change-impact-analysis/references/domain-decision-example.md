# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Config v8 changes money units cents→decimal. E1:config→checkout reader→refund obligation O1→T-refund. E2:checkout→invoice shared amount→O2→T-invoice. E3:dynamic plugin-registry consumers unknown. E4:image service has a confirmed independent contract and never reads money config. Decide INCLUDE/EXCLUDE/UNKNOWN for O1,O2,E3,E4 with edge sources and conservative validation for unknown dependencies.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| O1 | INCLUDE |
| O2 | INCLUDE |
| E3 | UNKNOWN |
| E4 | EXCLUDE |

## Verification Method

1. Fix change version/scope and build typed changed file/symbol/config→dependent→business obligation→test ID evidence edges with source/version and confirmed/candidate/unknown states.
2. Traverse direct/transitive consumers with cycle deduplication. Stop only at evidenced contract isolation/no-consumer boundaries and record why; directories alone are no boundary.
3. Dynamic registration/runtime configuration/untraced dependencies remain unknown. Propose risk-based consumer contract/integration checks; absent mapping does not mean no impact.
4. Explain inclusion/exclusion, minimum validation, residual risk, and expansion triggers. This Skill covers code/data/config changes broadly; the PR-specific counterpart owns base/head/diff identity.
