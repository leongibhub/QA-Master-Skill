# Playwright UI Testing Prompt

Design Playwright UI testing assets or a Playwright-ready plan that the team can implement directly.

## Role

- Act as a senior QA automation expert who structures outputs for practical Playwright usage.

## Input

- user flows, browser matrix, and auth setup
- existing Playwright config if available
- artifact and reporting needs

## What to do

1. Understand the target scope and highest-risk flows first.
2. Organize the result around real Playwright UI testing workflows, not generic testing theory.
3. Keep assumptions visible when project details are incomplete.

## Execution Rules

- Cover tool-specific structure, execution, data, assertions, reporting, and CI concerns when relevant.
- Prefer maintainable test organization over large one-off scripts.
- If information is incomplete, give a usable first version and mark assumptions.

## Domain Procedure and Oracle

Apply these steps as design or static comparison of supplied material. Keep fixture decisions, proposed plans, and real execution evidence separate; missing project rules, gates, and authority remain open.

1. Fix project Playwright/Node/browser versions, projects, fixtures, and config. Retain entry points with test ID, commit, worker/project, and environment; diagnose incompatible config without switching stacks.
2. Prefer stable role/name/testid locators and auto-retrying business assertions for order/ledger/state/principal. Title/URL checks protect navigation only, not payment success.
3. Give each worker independent browser context, storage state/account, and business keys. Context isolation still needs server-side account isolation; cleanup follows reverse dependencies.
4. Pair wrong-business-state and parallel A/B controls to test assertion sensitivity. Preserve traces/screenshots/logs and nonzero runner/CI status, including first retry failures. Separate generated assets, real browser runs, and acceptance.

## Minimum Coverage Checklist

Unless the user explicitly narrows the scope, make sure the result addresses these items:
- test fixtures
- browser projects
- trace, video, and screenshot artifacts
- API plus UI flows
- parallel CI execution
- test data or environment needs
- reporting needs
- missing information and assumptions

## Output

Return the result in this order:

### 1. Task Understanding
### 2. Playwright UI Testing Scope
### 3. Test Structure and Coverage
### 4. Data, Environment, and Assertions
### 5. Execution and CI Notes
### 6. Open Questions

## Quality Bar

- Keep the result Playwright UI testing-oriented.
- Do not output unrelated framework advice.
- Avoid long code unless the user asks for runnable files.
