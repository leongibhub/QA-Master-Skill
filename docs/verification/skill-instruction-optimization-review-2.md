# TASK098 review report: CR-021 second-round instruction upgrades

- Artifact ID: `DOC-SKILL-INSTRUCTION-OPTIMIZATION-REVIEW-002`
- Proposed evidence ID: `EVD-SKILL-INSTRUCTION-OPTIMIZATION-REVIEW-002`
- Runtime: `work-6666b2cba328442692410c22b4bc32d9`, attempt 1 / version 1
- Subject: `CODE-SKILL-INSTRUCTION-OPTIMIZATION-002` v1 at commit `a68bffa`
- Reviewer: independent (`/root/workflow_review`); not the implementer or tester
- Date: 2026-10-16
- Classification: `AGENT_REVIEW_ONLY`

## Method

Read both changed assets at `a68bffa` in full; checked technical correctness
of each clause against the CR-020 residual taxonomy, the CR-018 conventions
and the deterministic engine vocabulary; checked for overreach and for
oracle-coupling; assessed the verification plan.

## Findings

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| R-01 | P2 | The label-minimality clause's "do not reorder source phrasing" example is self-contradictory: `CONFIRMED_PAYMENT` (arm A's CR-019 answer) is the direct source-order collapse of "a confirmed payment" and equally short, so the stated condition ("acceptable only when no shorter source-faithful form exists") never selects `PAYMENT_CONFIRMED`. The rule as written will not change the behavior it targets. The defensible underlying principle is **family consistency**: paired/negated events around one concept must be derived from one canonical (most structurally explicit) phrasing so the family stays parallel — the actual CR-019 defect was `CONFIRMED_PAYMENT` beside `PAYMENT_NOT_CONFIRMED` (mixed stems), not ordering per se. | Repair required before closure |
| R-02 | P3 | Grammar: "missing a asked-for member" should be "missing an asked-for member" (typed-observations.md, multi-part section). | Fix with R-01 |
| R-03 | P3 | The new behavioral rule in SKILL.md sits at the end of the deterministic-engine paragraph; it reads acceptably there (engine-vs-reading contrast) but could equally live in the conventions reference. | Accept as-is |

## Verified correct

- **Multi-part completeness**: one member per asked kind, exact row keys,
  no renames — correct and matches the Q-DTT-001/Q-STT-001 failure shapes.
- **Universe discipline**: consistent between typed-observations.md and
  SKILL.md; extra rows routed to the case table.
- **Engine vocabulary alignment**: `CONFLICT`/`EXCLUDED`/`GAP` definitions
  match the engine's actual emissions (verified against
  `design_methods.py` analysis rows); the anti-pattern examples
  (`CONFLICTING`, `UNSUPPORTED_EXCLUDED`, `UNRESOLVED`) are exactly the
  variants observed in CR-019 arm answers.
- **No oracle coupling**: `GRANTED`/`ALLOWED` appear nowhere (OA-3
  respected); no clause references any specific scenario, fact ID or
  oracle value.
- **No overreach**: no new execution, approval or claim authority; the
  SKILL.md wiring paragraph is additive within the existing structure.
- **Verification plan**: correctly requires a fresh pre-registered scenario
  set rather than reusing CR-019 fixtures; quota recovery date noted.

## Verdict

`REVIEW_REQUIRED` for the increment pending repair of R-01 (P2) and R-02
(P3). The remaining content is technically correct, mapped and free of
oracle coupling. After repair and byte-level re-verification of the changed
clauses only, the chain can close.
