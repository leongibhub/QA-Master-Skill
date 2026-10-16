# TASK098 closure re-review: CR-021 repairs at `726a4b8`

- Artifact ID: `DOC-SKILL-INSTRUCTION-OPTIMIZATION-REVIEW-002` (addendum)
- Proposed evidence ID: `EVD-SKILL-INSTRUCTION-OPTIMIZATION-REVIEW-002` (addendum)
- Runtime: `work-6666b2cba328442692410c22b4bc32d9` follow-up
- Subject: repair commit `726a4b8` for findings R-01 (P2) / R-02 (P3)
- Reviewer: independent (`/root/workflow_review`); byte-level re-verification of
  the changed clauses only
- Date: 2026-10-16
- Classification: `AGENT_REVIEW_ONLY`

## Re-verification

| Finding | Required repair | Result at `726a4b8` |
|---|---|---|
| R-01 (P2) self-contradictory "do not reorder" example | Replace with a rule that actually selects the family-consistent form | PASS — the reorder example is removed; the new family-consistency rule (paired/negated events share one canonical stem; `PAYMENT_CONFIRMED` beside `PAYMENT_NOT_CONFIRMED` as the canonical example, `CONFIRMED_PAYMENT` beside `PAYMENT_NOT_CONFIRMED` as the anti-example; stem selection by most-family-members, tie-break by grammatically complete phrase) is internally consistent and now selects the intended form through a defensible principle rather than an arbitrary ordering preference |
| R-02 (P3) grammar | "missing an asked-for member" | PASS |

Scope check: the repair commit touches only
`qa_master/skills/codex/references/typed-observations.md` (16 insertions, 9
deletions); all other CR-021/CR-018 clauses re-verified byte-identical; full
suite 752 OK after the repair (developer re-run, exit-status artifact of the
PowerShell pipeline noted by the tester previously).

## Verdict

`REVIEW_REQUIRED` **closed** for the CR-021 development increment. Both
findings resolved; no new findings. All CR-021 outputs remain
`DRAFT_UNAPPROVED`; behavioural verification awaits the fresh pre-registered
scenario set after quota recovery.
