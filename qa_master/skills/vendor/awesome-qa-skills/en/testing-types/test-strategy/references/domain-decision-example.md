# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Project gate requires independent executed assertions for refund idempotency and tenant isolation,20min each, with isolated environment and existing Playwright/API assets. C1 QA-A has45min and can run both sequentially. C2 QA-A has25min with no risk waiver. C3 only a case plan is called passed. C4 applies95% though no other pass-rate gate is supplied. Decide FEASIBLE/ESCALATE/NOT_RUN/UNKNOWN with obligation/owner/depth/evidence table, retaining capacity tradeoffs.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| C1 | FEASIBLE |
| C2 | ESCALATE |
| C3 | NOT_RUN |
| C4 | UNKNOWN |

## Verification Method

1. Build a minimum executable table linking objective→obligation/scope→layer/depth→data/environment→resources/owner→entry/exit rule source→evidence/residual risk.
2. Reuse the project stack and actual capacity, protecting critical loss/authority obligations first. Each scenario needs business postconditions/evidence; insufficient resources expose unfinished work and minimal alternatives.
3. Gates come from the project. Missing thresholds remain open/UNKNOWN; never apply an automatic95% pass gate. Human risk acceptance cannot be replaced by a strategy draft.
4. Separate design, plan, actual runs, and acceptance. Include dependencies/blockers, changes, stop/reassessment triggers, and owners so another executor can take over.
