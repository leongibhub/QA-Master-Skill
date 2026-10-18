# TASK109 review report: CR-025 third-round instruction upgrades

- Artifact ID: `DOC-SKILL-INSTRUCTION-OPTIMIZATION-REVIEW-003`
- Proposed evidence ID: `EVD-SKILL-INSTRUCTION-OPTIMIZATION-REVIEW-003`
- Subject: `CODE-SKILL-INSTRUCTION-OPTIMIZATION-003` v1 at commit `fb4f2d3`
- Reviewer: independent (`/root/workflow_review`); not the implementer or tester
- Date: 2026-10-18
- Classification: `AGENT_REVIEW_ONLY`

## Method

Read the changed asset at `fb4f2d3` in full; checked technical correctness of
each clause against the CR-022/CR-024 residual taxonomy, the CR-018/CR-021
conventions and the deterministic-engine vocabulary; checked for overreach,
oracle coupling and CR-022-material coupling; assessed the verification plan.

## Findings

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| R-01 | P3 | Clause 1's "one member per stated item" is unambiguous for the observed FS-05 shape (a single stated source state per invalid item) but would need clarification if a future fact states one invalid item across two source states ("X from Y and Z is invalid"): is that one row or two? Not a blocker for the current failure class; note for future scenario authoring. | Accept as-is |
| R-02 | P3 | Clause 2 says "cite … as a source reference", which is the file's established term (line "source references … not inside the observation value"), while the envelope field is `evidence_refs`. The model resolves the mapping via the neutral-response schema; no change needed, but the wording could in future name the field explicitly. | Accept as-is |

## Verified correct

- **Explicit-scope discipline**: conditionally scoped to checks that name
  "explicitly stated" items; the three anti-patterns ("no event leaves a
  terminal state", "implied negation", "symmetric inference") are exactly the
  general rules the arms misapplied in Q-FS-052 to inflate 1 → 7 candidates.
- **Exhaustive-universe provenance**: conditional on the facts containing an
  exhaustive-universe statement; correctly generalises from the "only states"
  fact (state transitions) to dimension-enumeration facts (decision tables),
  which the oracle requires for both. Over-citing is harmless under the
  subset match (`required ⊆ evidence`).
- **No oracle coupling**: `GRANTED`/`ALLOWED` appear nowhere; no clause
  references a specific scenario, fact ID or oracle value. The example was
  neutralised to `DRAFT, ACTIVE, CLOSED` (no CR-022 state token).
- **No overreach**: instruction-layer only; no new execution, approval or
  claim authority; both clauses live in the typed-observations reference that
  SKILL.md already wires.
- **Verification plan**: correctly requires a second fresh pre-registered
  scenario set rather than reusing CR-022 material, exercising the same two
  failure classes on never-graded content.

## Verdict

`PASS` — no blocking findings. The two upgrades are technically correct,
mapped, free of oracle and CR-022-material coupling, and appropriately
scoped. Two P3 observations recorded (multi-state "one member" edge case;
field-name wording), neither requiring repair before behavioural
verification.
