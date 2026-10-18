# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Existing fixture baseline Cypress13/E2E, not a latest-version recommendation. Title always Checkout. C1 real payment yields paid/amount20/principalA; spec asserts these values. C2 bug mode keeps title but statepending; spec checks title only. C3 intercept stubs only external payment; real UI remains pending, so business assertion should fail. C4 CI appends ||true after failed spec. C5 isolated A/B accounts and cleanup are evidenced. Decide VALID forC1/C5, REPAIR forC2, EXPECTED_FAILURE forC3, INVALID forC4, explaining retries, boundaries, and failure propagation.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| C1 | VALID |
| C2 | REPAIR |
| C3 | EXPECTED_FAILURE |
| C4 | INVALID |
| C5 | VALID |

## Verification Method

1. Read Cypress, Node, browser, config, and component/E2E scope from project artifacts. Generate compatible config, custom commands, specs, and CI commands without implicit upgrades or mixed legacy formats.
2. Exercise real page/component logic; cy.intercept replaces only confirmed external boundaries. Stub responses alone cannot prove business postconditions. Define isolated fixture data/session cleanup.
3. Separate retryable queries/assertions, one-time actions, and whole-test retries. Wait on aliased requests/observable states, not sleeps. Preserve first failures and prevent repeated effects.
4. Use minimum-app positive/negative controls for paid state, amount, and principal. Correct titles with wrong business state must fail assertions and CI. Preserve screenshots/video/failures, teardown, and actual run evidence; files alone prove nothing.
