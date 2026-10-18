# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Project fixture locks Playwright1.48; Checkout title is constant. P1 payment remains pending but title-only assertion stays green. P2 toHaveText('paid') fails on pending, preserves trace, and CI exits nonzero. P3 two contexts share account/order and alter each other's data. P4 independent A/B principals/order_ids read own paid20 and clean without residuals. P5 only a generated file, no run. Decide REPAIR/EXPECTED_FAILURE/ISOLATION_FAIL/VALID/NOT_RUN; neither trace existence nor a normal title proves acceptance.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| P1 | REPAIR |
| P2 | EXPECTED_FAILURE |
| P3 | ISOLATION_FAIL |
| P4 | VALID |
| P5 | NOT_RUN |

## Verification Method

1. Fix project Playwright/Node/browser versions, projects, fixtures, and config. Retain entry points with test ID, commit, worker/project, and environment; diagnose incompatible config without switching stacks.
2. Prefer stable role/name/testid locators and auto-retrying business assertions for order/ledger/state/principal. Title/URL checks protect navigation only, not payment success.
3. Give each worker independent browser context, storage state/account, and business keys. Context isolation still needs server-side account isolation; cleanup follows reverse dependencies.
4. Pair wrong-business-state and parallel A/B controls to test assertion sensitivity. Preserve traces/screenshots/logs and nonzero runner/CI status, including first retry failures. Separate generated assets, real browser runs, and acceptance.
