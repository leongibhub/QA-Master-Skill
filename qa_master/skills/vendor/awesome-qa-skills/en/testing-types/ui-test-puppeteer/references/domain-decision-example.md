# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Fixture baseline Puppeteer23 with its installed browser bundle. U1 popup belongs to the original page, receipt shows paid20, finally closes both pages/browser. U2 load error is swallowed, returns0, browser remains active. U3 titleCheckout but statepending. U4 timeout captures screenshot/currentURL, propagates original error, finally leaves active resources0. U5 supplied launch log confirms incompatible browser. Decide VALID/FAIL/REPAIR/EXPECTED_FAILURE/CONFIG_ERROR with popup/load/timeout lifecycle evidence.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| U1 | VALID |
| U2 | FAIL |
| U3 | REPAIR |
| U4 | EXPECTED_FAILURE |
| U5 | CONFIG_ERROR |

## Verification Method

1. Read actual Puppeteer/Node/browser and launch config/support scope. Incompatibility is CONFIG_ERROR; successful launch does not prove every feature is compatible.
2. Identify new windows through target creation/opener association and wait for a usable page, verifying URI/authority. Navigation readiness and business readiness are separate; real state is the oracle, not a fixed sleep.
3. Close owned pages/browser in try/finally and preserve timeout/load errors. Report primary and cleanup failures separately; never swallow exceptions and return success.
4. Minimum fixtures include good payment, wrong state, popup, load failure, and timeout. Verify business state/principal plus screenshot/URL/log/version evidence; generated files and successful loads are no business pass.
