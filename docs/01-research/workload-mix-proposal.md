# Representative workload mix and minimum sample size proposal

- Artifact ID: `DOC-WORKLOAD-MIX-PROPOSAL-001`
- Proposed evidence ID: `EVD-WORKLOAD-MIX-PROPOSAL-001`
- Change: `CR-016`
- Work: `TASK-087` / `work-f71cecb4b722443bb72a4afeb94cc595`, attempt 1
- Related requirements: `REQ-011`; DRAFT `REQ-025`/`NFR-009` (readiness only;
  completes none of them)
- Resolves the `PENDING` Phase 3 item of
  `DOC-QA-QUALITY-EVALUATION-REQ-001` §"Ambiguities and decisions still
  required": _Representative workload mix and minimum sample size_.
- Document State: `DRAFT`
- Evaluation State: `IN_REVIEW`
- Date: 2026-10-16
- Classification: `PUBLIC_DEVELOPMENT` decision-support proposal. It selects
  nothing, executes nothing, and decides nothing. Every choice below is an
  **option with rationale** for a human pre-registration that remains
  `NOT_AVAILABLE` until real humans make it.

## Purpose and boundary

The quality-contract Phase 3 and `REQ-011` require that any future paired
comparison use a representative workload mix and a minimum sample size chosen
before the run, derived from the product's actual supported request classes —
not from three public fixtures. This document assembles those facts, derives
option sets with stated rationale, and states the statistical bounds as
formulas (no fabricated pilot data is used, because the retained six-call
pilot is exploratory-only and cannot be promoted to sizing evidence).

It defines **no** acceptance threshold, **no** winner rule, **no** aggregate
interpretation, and **no** automatic scoring. It authorizes no model call,
pair run, holdout release, rating, comparison, Gate, acceptance or release
decision. Those remain human `NOT_AVAILABLE` decisions under
`DOC-HOLDOUT-REGISTER-PROCEDURE-001` and `REQ-011`.

## FACT and EVIDENCE: the product's actual supported request classes

| FACT | EVIDENCE | Source / date |
| --- | --- | --- |
| QA Master's installed entry point recognizes five intake situations: no materials; repository only; deployed system only; development incomplete (WAITING_FOR_BUILD handoff); one-stage request. | `qa_master/skills/codex/SKILL.md` "Start with the requested outcome" bullet list. | Local frozen source, read 2026-10-16. |
| Method selection supports six professional guide families: requirements-review, functional-api, structural-integration, nonfunctional-compatibility, security-recovery, regression-evidence. | `SKILL.md` method table; `qa_master.skill_registry` enumerates the six required guides. | Local source, read 2026-10-16. |
| Three domain profiles are documented: Web/API, Linux and system software, AI computing software and hardware interfaces. | `qa_master/skills/codex/references/domains.md`. | Local source, read 2026-10-16. |
| Three deterministic offline design methods exist with strict finite contracts: boundary (integer/decimal), decision_table (≤4096-cell Cartesian), state_transition (≤128 states). | `qa_master/skills/codex/references/design-methods.md`; `qa_master.design_methods` implementation. | Local source, read 2026-10-16. |
| The paired plan fixes two comparison tracks: deterministic product verification (script-oracle) and paired agent behaviour, the latter with two lanes (specialist = method labels visible; router = labels withheld). | `DOC-PAIRED-EVALUATION-PLAN-001` §"INFERENCE: comparison structure". | Local repository, read 2026-10-16. |
| The upstream comparator has matching pinned specialists (boundary, decision-table, state-transition), a discovery router distinguishing installed from unavailable skills, plus 150 other testing types; QA Master has no installed-tool routing beyond the bundled guides. | `DOC-COMPARISON-RESEARCH-001` comparator snapshot (upstream `1a8c57c`). | Local repository, read 2026-10-16. |
| The existing benchmark manifest has twelve narrative/safety scenarios, all `NOT_EXECUTED`; they are the visible development set, not a holdout and not a sizing basis. | `benchmarks/manifest.json`, `benchmarks/scenarios.json`. | Local repository, read 2026-10-16. |
| The retained six-call exploratory run is `EXPLORATORY_CONFIGURED_SAME_MODEL` with unknown provider revision/system baseline; it cannot size or weight any future strict run. | `docs/verification/` retained pilot evidence; `qa_master.paired_evaluation` evidence classes. | Local repository, read 2026-10-16. |

## INFERENCE: request-class inventory (the denominator)

Combining the facts, the product's supported request space factors into three
orthogonal axes. Every future workload-mix choice must be expressed as weights
over **these** cells, because both arms must face the same cells.

### Axis 1 — intake situation (5 classes)

`I1` no materials · `I2` repository only · `I3` deployed system only ·
`I4` development incomplete / waiting-for-build · `I5` one-stage bounded
request.

### Axis 2 — method demand (6 guide families + router)

`M1` requirements review · `M2` functional/API · `M3`
structural/integration · `M4` non-functional/compatibility · `M5`
security/recovery · `M6` regression/evidence · `M7` method selection /
routing (the router lane, where the plan withholds method labels).

### Axis 3 — domain (3 profiles)

`D1` Web/API · `D2` Linux/system · `D3` AI computing.

Not every (I, M, D) cell is meaningful (e.g. a boundary-value design against
"no materials" is not a valid request; performance thresholds without a
system are `THRESHOLD_UNCONFIRMED` by contract). The proposal below restricts
mixes to valid cells only, and the validity table is part of the proposal.

### Deterministic-product track (separate mix)

The deterministic track is judged by script oracle, not human rating. Its mix
is over the three design methods (boundary, decision_table, state_transition)
× integer/decimal and constraint shapes. It needs its own sample sizing (see
options) and must be reported separately from behaviour, per the plan.

## Proposal: workload-mix options

Three coherent options are offered. They are alternatives; a human
pre-registration must pick one (or direct a bounded revision) before any
holdout is drawn or any run is authorized. Weights are proportions of paired
behaviour-track pairs, valid cells only, and sum to 1.

### Option W-A — "specialist-anchored mix" (lowest cost)

Mirrors the three deterministic specialists where both arms have pinned
capabilities, plus the minimal router and narrative coverage:

| Stratum | Weight | Rationale |
| --- | --- | --- |
| Specialist lane, boundary (M2×D1/D2) | 0.20 | Both arms have pinned boundary specialists; highest method parity. |
| Specialist lane, decision-table (M2/M3) | 0.20 | Same parity reasoning; upstream demands sourced domains/exceptions. |
| Specialist lane, state-transition (M2/M3) | 0.20 | Same parity reasoning. |
| Router lane (M7, mixed domains) | 0.15 | Evaluates selection explanation and availability boundaries — the sharpest documented capability difference (165 upstream skills vs 6 bundled guides). |
| Narrative/safety (M1/M6, from the 12-scenario grammar) | 0.25 | Covers requirements review and regression/evidence restraint the deterministic track cannot see. |

Cost estimate: the smallest pair count of the three options.

### Option W-B — "intake-representative mix" (recommended)

Adds the five intake situations as first-class strata, because intake
behavior is documented product surface (asking vs. assuming, scope
preservation, WAITING_FOR_BUILD) and both arms face it:

| Stratum | Weight | Rationale |
| --- | --- | --- |
| Specialist lane, three methods equally (as W-A) | 0.45 | Method parity core. |
| Router lane (M7) | 0.15 | As W-A. |
| Intake: repository-only (I2, M1/M2) | 0.10 | "Read code, cite revision/path/symbols; behaviour is candidate requirement." |
| Intake: deployed-system-only (I3, M1/M4) | 0.10 | Observation boundary agreement before formal testing. |
| Intake: waiting-for-build (I4, M6) | 0.05 | Design-now/handoff restraint — a distinctive documented behavior. |
| Intake: one-stage bounded (I5, M2/M3) | 0.05 | Scope restraint against unrequested expansion. |
| Narrative/safety (M1/M6) | 0.10 | Reduced from W-A; deterministic-track separation limits its need. |

Cost estimate: ~1.6–1.8× W-A.

### Option W-C — "full-factorial probe" (highest cost)

Every valid (I, M, D) cell with nonzero weight (the validity table yields 24
valid cells), minimum 2 pairs per cell. Cost estimate: ~4–5× W-A. Offered for
completeness; not recommended for a first controlled comparison because
per-cell depth is too thin for any stable per-cell statement.

**Deterministic-track mix (all options):** boundary:decision_table:
state_transition = 1:1:1 with ≥50% of boundary models decimal-typed and ≥1
closed-world state model, matching the design-methods contract's stress
points (`precision`/`scale`, constraint AST, closed-world denial).

## Proposal: minimum sample size derivations

Stated as bounds and formulas only — no fabricated data. Two independent
sizing questions exist; they must not be conflated.

### S1 — Behaviour track: per-stratum pair minimum

Human ratings on the five dimensions are ordinal (1–5 with UNSCORABLE).
Without agreed rater reliability there is no defensible effect-size-based n.
The bounded floor is therefore precision-driven:

- **Per stratum, minimum n = 8 pairs.** Rationale: with binary per-dimension
  outcome coding (better/equal/worse per dimension per pair) and no prior,
  the floor is a precision criterion, not a power calculation. Exact
  Clopper-Pearson 95% intervals for the sign proportion p at the observed
  midpoint (k = n/2) are: n = 6 → [0.118, 0.882] (half-width 0.382);
  n = 8 → [0.157, 0.843] (half-width 0.343); n = 10 → [0.187, 0.813]
  (0.313); n = 12 → [0.211, 0.789] (0.289). Under a pre-declared precision
  criterion of midpoint half-width < 0.35, n = 8 is the smallest qualifying
  floor (n = 6 fails at 0.382). Humans pre-registering a different precision
  criterion should re-derive; at these widths no per-stratum statement is
  threshold-grade — direction-of-interest only.
- **Overall minimum (W-A):** 5 strata × 8 = **40 pairs minimum**, before
  repeat policy.
- **Overall minimum (W-B):** 10 strata × 8 = **80 pairs minimum**, before
  repeat policy.
- **Overall minimum (W-C):** 24 cells × 2 minimum (probe granularity;
  per-cell statements are explicitly not supported at this depth) = 48 pairs
  minimum.
- **Repeat policy (if provider seed unsupported):** same pre-registered
  repeat count r ≥ 2 for both arms on every pair; effective judged unit is
  the pair, repeats report variation, never reduce to a single silent sample.
  Pair minimums above are unaffected; total calls = 2 × pairs × r.

### S2 — Deterministic track: fixture minimum

Script-oracle outcomes are per-assertion `SATISFIED`/`VIOLATED`/`UNSCORABLE`.
Sizing is completeness-driven, not statistical:

- Boundary: ≥ 12 visible + ≥ 12 holdout models, covering all four
  `oracle_by_class` classes, integer and decimal, on/off-grid bounds.
- Decision-table: ≥ 8 visible + ≥ 8 holdout models, covering empty-match,
  overlap, conflict, exclusion and default rules.
- State-transition: ≥ 8 visible + ≥ 8 holdout models, covering valid/invalid
  transitions, terminal-state rule, closed and open world.
- UNSCORABLE must remain a reportable outcome everywhere; a parser failure is
  an observed outcome, never re-run silently.

### What these minimums do NOT license

- No acceptance threshold (how many SATISFIED is "good enough") — human
  pre-registration, deliberately absent.
- No winner rule, no aggregate score, no superiority inference from any n
  here. `REQ-011` and the benchmark contract keep `HUMAN_REVIEW_REQUIRED`.
- The holdout fixtures per CR-014 classes are drawn only after freeze by the
  evaluation owner; this document's numbers are planning floors for that
  future draw, and no holdout material exists.

## RISK

- **Strata too thin:** W-B intake strata at 0.05–0.10 with n = 8 yield noisy
  per-stratum statements; the pre-registration should declare which strata
  are exploratory (reported, not thresholded).
- **Router-lane asymmetry:** upstream's 150-type catalog vs QA Master's six
  guides is a real capability difference; the router lane measures it, but a
  mix dominated by rare-method requests would measure catalog breadth more
  than QA method quality — hence the 0.15 cap in W-A/W-B.
- **Sizing evidence gap:** no pilot data with known rater reliability exists;
  the n = 8 floor is a precision bound, not a power calculation. If humans
  pre-register an effect size and reliability, recompute.
- **Repeat-policy ambiguity:** if the provider exposes no seed, variation is
  confounded with arm; the repeat policy above bounds but does not eliminate
  this. A strict-profile run additionally requires the CR-015 verifier to
  pass with administrator attestations, which do not exist yet.

## Current conclusion

`NOT_EXECUTED`. This proposal turns a `PENDING` Phase 3 item into three
bounded, fact-grounded option sets (W-A/W-B/W-C mixes; S1/S2 sizing floors)
ready for human pre-registration. It selects nothing, runs nothing, and
supports no quality or superiority claim. The human decision — which mix,
which minimum, which thresholds (if any) — remains `NOT_AVAILABLE` until real
humans register it under the CR-014 procedure.
