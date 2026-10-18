# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Fixture TestCafe3 with existing CLI/runner. T1 awaits all t actions, isolated Role/account, paid20 assertions and cleanup. T2 checks titleCheckout only and stays green on pending. T3 runner.run() returns failedCount1 but entry ignores it and exits0. T4 pending fails business assertion, CLI nonzero, screenshot tied to testID. T5 two Roles share account/business key and contaminate data. Decide VALID/REPAIR/FAILURE_HIDDEN/EXPECTED_FAILURE/ISOLATION_FAIL; artifacts alone are not run evidence.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| T1 | VALID |
| T2 | REPAIR |
| T3 | FAILURE_HIDDEN |
| T4 | EXPECTED_FAILURE |
| T5 | ISOLATION_FAIL |

## Verification Method

1. Confirm TestCafe/Node/browser, native automation mode, CI, and reporter versions. Produce fixtures/tests/config compatible with the existing runner; missing config is open, not an implicit upgrade.
2. Initialize isolated sessions with Roles or independent identities and isolate accounts/business keys too. Await asynchronous t actions and use supported Selector/assertion waits rather than fixed sleeps.
3. Verify paid state, amount, and principal. Boundary stubs must not bypass the real UI; a normal title is no success. Negative controls must fail business assertions.
4. CLI nonzero or programmatic failedCount>0 must fail CI. Reporters cannot swallow failures; retain screenshots/console/test IDs and cleanup. Parseable config is distinct from actual execution.
