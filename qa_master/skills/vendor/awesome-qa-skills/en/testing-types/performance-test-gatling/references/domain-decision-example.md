# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

The synthetic build record establishes Java DSL/Gatling 3.13/JDK 17 and successful offline test-compile. G-1 has one request per user, no loops/retries, constantUsersPerSec(10).during(2), and 20 observed requests over 2 seconds. G-2 calls constantConcurrentUsers(10) a 10 RPS profile without completion counts. G-3 uses 5 queue feeder rows for 20 users feeding once and hides exhaustion at the sixth consumption. G-4 invents p95<500ms and calls it passed without an SLO. Decide VALID/UNSUPPORTED/FAIL/UNKNOWN, keeping compilation separate from runtime gates.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| G-1 | VALID |
| G-2 | UNSUPPORTED |
| G-3 | FAIL |
| G-4 | UNKNOWN |

## Verification Method

1. Read project Gatling/plugin/JDK and Java/Scala/Kotlin DSL versions, retaining its layout. Use compatible injection/assertion APIs in one DSL. Offline test-compile generated assets with the project build; uncached dependencies mean BLOCKED, not a passed compile.
2. Open models control user arrivals; arrivals equal request RPS only for one request per user without additional loops/retries. Closed models control concurrency; verify RPS from actual request counts/windows.
3. Calculate feeder consumption per user/loop. Queue exhaustion must visibly fail; circular reuse requires policy permission and non-conflicting identities/business keys.
4. Use project thresholds and version-supported assertions. Missing gates yield an unconfigured skeleton, not invented 500ms/1% values. Compile, achieved load, and SLO results are distinct evidence.
