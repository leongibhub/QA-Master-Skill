# TASK093 review report: CR-018 skill-instruction upgrades

- Artifact ID: `DOC-SKILL-INSTRUCTION-OPTIMIZATION-REVIEW-001`
- Proposed evidence ID: `EVD-SKILL-INSTRUCTION-OPTIMIZATION-REVIEW-001`
- Runtime: `work-ed270a49ed5a494dbfbeb4d962fd1381`, attempt 1 / version 1
- Subject: `CODE-SKILL-INSTRUCTION-OPTIMIZATION-001` v1 at commit `c193774` (+ test report at `445e7cd`)
- Reviewer: independent (`/root/workflow_review`); not the implementer or tester
- Date: 2026-10-16
- Classification: `AGENT_REVIEW_ONLY`. Bounded instruction-content review.
  No execution, rating or claim decision.

## Method

Read all four changed assets at `c193774` in full; checked the technical
correctness of each new clause; checked consistency against the unchanged
instruction set (SKILL.md, work-protocol.md, domains.md, design-methods.md,
the six professional guides); checked for overreach (any new execution,
approval or claim authority); and assessed suitability of the CR-019
verification re-run design.

## Findings

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| R-01 | P3 | `work-protocol.md`: the general "Every deliverable that reports gaps…" bullet is placed between artifact-specific bullets (Requirement review / Test strategy) in the deliverables list. Functional, but a general rule reads better as its own paragraph. | Accept as-is; cosmetic only |
| R-02 | P3 | `functional-api.md`: the example phrase "includes both `2`, `3` and `8`, `9` as accepted neighbours" is awkward to parse; parenthesized pairs would be clearer. | Accept as-is; cosmetic only |
| R-03 | P2 (forward-looking; not a defect in this change) | The typed-observation conventions were derived from CR-017 grading failure modes, and CR-019 plans to reuse the same oracle and assertions. Two consequences the CR-019 protocol MUST handle: (a) the linkage "instructions informed by this oracle's failure modes" must be disclosed in the CR-019 report, otherwise the re-run invites a taught-to-the-test objection; (b) the CR-017 `PE-BND-002` oracle's rejected list contains a numeric duplicate (`"100.00"` and `"100"`), which a convention-following answer will legitimately not reproduce — the CR-019 supplementary semantic layer must therefore use numeric set-dedupe equality, declared before the run. | Required input to the CR-019 protocol; does not block CR-018 |

## Verified correct

- **Technical content.** The both-side interior-step rule is correct
  (endpoints + adjacent interior step point per end; `2..9` → `2,3,8,9`).
  The decimal clause correctly separates the two failure modes CR-017
  observed: declared-precision text (`0.50` not `0.5`) and scale-violation
  rejection candidates (`0.505` when scale is two).
- **Token conventions.** Literal source tokens + uppercase-underscore
  synthesized labels + minimal values + both-classes answers are internally
  consistent and mirror how a typed grader must compare values. The
  extra-member examples (`source_refs`, `step`, `expectation_scope`) match
  the actual CR-017 observation failures.
- **Gap taxonomy.** The three mandatory categories (execution observable,
  setup/cleanup preconditions, oracle source) codify what arm A did
  spontaneously in CR-017 — turning an unrepeatable behaviour into a
  contract.
- **No overreach.** No new execution, approval, import, enterprise-write or
  claim authority was introduced. The SKILL.md wiring places the conventions
  beside work-protocol/domains without altering the method table, the
  design-methods path or the preserve-decisions section. The final
  no-superiority-claim sentence in SKILL.md is untouched.
- **No contradictions** with the unchanged instruction set; design-methods
  CLI guidance and the paired-evaluation neutral envelope are referenced
  generically and consistently.
- **Packaging** (`_files` `.md` recursion) ships the new reference without
  code change, as TASK-092 verified.

## Verdict

`PASS` with two P3 cosmetic notes accepted as-is and one P2 forward-looking
requirement (R-03) that binds the CR-019 protocol, not this change. The
instruction upgrades are technically correct, mapped, consistent, packaged
and free of authority overreach. Behavioural effect remains unproven until
the CR-019 re-run.
