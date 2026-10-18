# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Current O1/O2/O3 are v2. O1 maps to T1/T2; T1 v2 has an effective assertion and passed run R1, T2 is unexecuted. O2 has only a stale v1 mapping. O3 maps to v2 T3 without a run. Two sources reuse O9 for 'free shipping' and 'refund time limit'. Decide SATISFIED/STALE/MAPPED/IDENTITY_CONFLICT for O1/O2/O3/O9. Report current three-obligation mapped/satisfied numerators and denominators; two O1 tests do not inflate coverage.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| O1 | SATISFIED |
| O2 | STALE |
| O3 | MAPPED |
| O9 | IDENTITY_CONFLICT |

| METRIC | VALUE |
| --- | --- |
| mapped_obligations | 2 |
| satisfied_obligations | 1 |
| current_obligation_denominator | 3 |

## Verification Method

RT/TC relationship types remain direct/derived/indirect/contradictory/missing and coverage statuses complete/partial/unverified/stale/unexecuted/unassessed. MAPPED/EXECUTED/SATISFIED and IDENTITY_CONFLICT are additional decision columns, not replacement enums; mapped-but-unrun stays unexecuted and unresolved identity conflicts never count as satisfied.

1. Fix IDs/versions for requirements, obligations, implementation, tests, and runs. Keep relationship types direct/derived/indirect/contradictory/missing; record implements/validates/executed-by/satisfies as a separate edge-purpose column with sources; file existence or name similarity is no evidence edge.
2. Deduplicate obligation denominators when multiple tests protect one obligation, preserving layers/assertions. Same ID with conflicting content is IDENTITY_CONFLICT, not a mergeable duplicate.
3. Separate MAPPED, EXECUTED, and SATISFIED. Mapping is no run; a passed run without an effective obligation assertion is no satisfaction. Old-version edges cannot satisfy new versions.
4. Check both directions for unlinked obligations, orphan tests, and stale edges. Coverage reports use current unique obligations with explicit exclusions/UNKNOWN; gaps cannot become PASS.
