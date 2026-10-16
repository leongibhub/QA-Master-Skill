# TASK088 independent review of the workload mix and sample size proposal

- Artifact ID: `DOC-WORKLOAD-MIX-PROPOSAL-REVIEW-001`
- Proposed evidence ID: `EVD-WORKLOAD-MIX-PROPOSAL-REVIEW-001`
- Runtime: `work-6ae9a1ba61f44b4c9df26ee00ad4e104`, attempt 1 / version 1
- Subject: `DOC-WORKLOAD-MIX-PROPOSAL-001` v2 at commit `ca50007`
- Reviewer: independent (`/root/workflow_review`); not the proposal author
- Date: 2026-10-16
- Classification: `AGENT_REVIEW_ONLY`. Bounded document review with
  independent re-derivation. No model call, pair run, holdout release,
  rating, comparison, Gate, acceptance or release decision is made or
  implied.

## Method

1. Verified every FACT/EVIDENCE row against its cited source file
   (`SKILL.md`, `domains.md`, `design-methods.md`, the paired plan, the
   comparator research, `benchmarks/manifest.json`).
2. Re-derived all four Clopper-Pearson intervals by independent bisection
   on the binomial CDF.
3. Recomputed the option weights and pair-count arithmetic.
4. Checked the deterministic-track floors against the design-methods
   contract's oracle classes and obligation types.
5. Checked boundary semantics (threshold/winner-rule/run-authorization).

## Findings

| ID | Severity | Observation | Verification |
|---|---|---|---|
| AR-1 | P2 | W-B minimum is stated as "10 strata × 8 = 80 pairs minimum", but the W-B table defines **9** strata (3 specialist + router + 4 intake + 1 narrative). The correct arithmetic is 9 × 8 = **72** pairs minimum. Either the total must be corrected to 72 or the table must be revised to 10 explicit strata. The error is material because the total feeds a human pre-registration's cost decision. | Recomputed: W-B weights sum to 1.00 across 7 table rows = 9 strata; 9 × 8 = 72 ≠ 80 |
| AR-2 | P2 | The W-C option claims "the validity table yields 24 valid cells" and the inventory section states "the validity table is part of the proposal", but **no validity table is present in the document**. The 24-cell count (and therefore W-C's 48-pair minimum) is unverifiable from the document as written. | Full-text read: no (I, M, D) validity table exists |

Confirmed correct (no action needed):

- All four Clopper-Pearson figures in v2 match independent re-derivation to
  3 decimals (n=6: [0.118, 0.882] hw 0.382; n=8: [0.157, 0.843] hw 0.343;
  n=10: [0.187, 0.813] hw 0.313; n=12: [0.211, 0.789] hw 0.289), and the
  n=8 floor is now correctly tied to an explicit precision criterion
  (< 0.35) that n=6 fails. The author's self-check correction was sound.
- W-A: 5 strata × 8 = 40 ✓; weights sum to 1.00 ✓.
- Inventory facts match the cited sources (5 intake situations, 6 guide
  families, 3 domains, 3 deterministic methods, 12 `NOT_EXECUTED` scenarios,
  exploratory-only pilot).
- Deterministic-track floors cover the contract's four `oracle_by_class`
  classes, the decision-table obligation types (empty-match, overlap,
  conflict, exclusion, default) and the state-transition coverage points
  (valid/invalid, terminal, closed/open world).
- No threshold, winner rule, aggregate interpretation or run authorization
  leaked into the document; every option is framed as unselected and the
  human `NOT_AVAILABLE` boundary is stated consistently.

## Verdict

`REVIEW_REQUIRED` — two narrow repairs before this proposal is handed to a
human pre-registration:

1. AR-1: correct the W-B minimum to 9 × 8 = 72 pairs (or revise the table to
   10 explicit strata and restate the total).
2. AR-2: add the promised (I, M, D) validity table, or replace the "24 valid
   cells" claim with the table's actual count.

This review authorizes no run, holdout release, model call, rating,
comparison, Gate, acceptance or release decision, and no selection among
W-A/W-B/W-C.
