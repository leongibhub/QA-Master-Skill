# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Existing framework: Playwright. C-1:stable login, isolated account, session principal matches account page, daily runs, logout cleanup. C-2:daily-changing prototype without state oracle. C-3:high-return payment only reaches real production debits without authorized sandbox/cleanup. C-4:existing checkout asserts title only; failed payment retains normal title. Decide ADOPT/DEFER/REPAIR without switching stacks or authorizing production effects; explain entry gates/business assertions.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| C-1 | ADOPT |
| C-2 | DEFER |
| C-3 | DEFER |
| C-4 | REPAIR |

## Verification Method

1. Select using candidate flow | protection obligation | repeat-frequency evidence | oracle/observability | isolation/cleanup | stability | maintenance constraint | adopt/defer rationale. Keep ROI cost scenarios separate; returns cannot remedy missing oracles or authority.
2. Reuse the existing framework. First require observable postconditions, independent data, and a CI entry that propagates failure. Defer unmet candidates with unblock conditions.
3. Specify unique identities/business keys, setup, actions, business postconditions, failure signal, and teardown. Failed assertions must fail runner/CI, not merely log.
4. Separate candidate selection, generated assets, real runs, and business acceptance. Rapidly changing prototypes or non-isolatable real payments may need Human/controlled verification, with evidence-based tradeoffs.
