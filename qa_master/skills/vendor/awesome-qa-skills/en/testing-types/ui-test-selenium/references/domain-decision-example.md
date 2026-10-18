# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Fixture Selenium4/Python with confirmed compatible driver. S1 retains a stale element after rerender and repeats payment click3times. S2 re-finds by data-testid, waits for paid, acts once with one ledger entry. S3 exception exits without quit, Grid session active. S4 preserves screenshot/original error and quits in finally, sessions0. S5 parallel sessions share account/order. Decide REPAIR/VALID/RESOURCE_LEAK/EXPECTED_FAILURE/ISOLATION_FAIL; larger sleeps are no universal repair.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| S1 | REPAIR |
| S2 | VALID |
| S3 | RESOURCE_LEAK |
| S4 | EXPECTED_FAILURE |
| S5 | ISOLATION_FAIL |

## Verification Method

1. Fix Selenium/binding/browser/driver/Grid versions, capabilities, and runner. Produce compatible config/POM; do not invent Grid topology and diagnose version conflicts first.
2. Explicitly wait on observable interactability, business state, window, or URL conditions. Presence/visibility is not business readiness; avoid mixed implicit/explicit waits and universal fixed sleeps.
3. After rerender/stale references re-find by stable locator and wait for fresh state. Bounded retries follow supplied policy; blind payment replay can duplicate effects.
4. Isolate accounts/business keys per parallel session. Use try/finally driver.quit with screenshots/logs/session/original failures. Rerender, business-failure, and exception controls verify cleanup and nonzero propagation.
