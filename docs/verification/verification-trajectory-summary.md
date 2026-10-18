# Verification trajectory summary — three instruction rounds and two fresh sets

- Classification: `PUBLIC_DEVELOPMENT` / `DRAFT_UNAPPROVED`
- Author: comparison researcher (same agent family as the instruction author —
  disclosed, R-03a)
- Date: 2026-10-18
- Scope: retrospective consolidation of CR-018 → CR-027; no new run, no new
  change, no superiority claim

## Purpose

Collate the full evidence chain of the paired-evaluation work into one
document: three evidence-driven instruction-optimization rounds, two
pre-registered fresh scenario sets, two measurement corrections, and the
resulting transfer signal — as the input bridge to the (still `NOT_AVAILABLE`)
Phase 3 strict-profile + human-rating + independent-holdout protocol.

## Trajectory

| Stage | What | Material | Result |
|---|---|---|---|
| CR-018 | Round 1: five instruction-layer upgrades (both-side interior step points, declared-precision + one-beyond-scale, typed-observation reference convention, gap taxonomy, SKILL.md wiring) | — | delivered + verified + reviewed; behavioural effect deferred |
| CR-021 | Round 2: four upgrades (multi-part completeness, label minimality/family consistency, row-universe discipline, `CONFLICT`/`EXCLUDED`/`GAP` vocabulary) | — | delivered + verified + reviewed; behavioural effect deferred |
| CR-022 | First fresh set (8 scenarios, 18 checks) | never-graded domains | **null transfer**: exact A 13:5 vs B 12:6; semantic **14:14 tied** |
| CR-023 | Convention regression guard (delivery guard only) | — | suite 763 OK, no behavioural claim |
| CR-024 | Token-form instrument correction (OA-5) + re-run | CR-022 set re-run | **null transfer confirmed**: exact A 12:6 vs B 13:5; semantic **A 14:4 vs B 15:3** (B +1) |
| CR-025 | Round 3: explicit-scope discipline + exhaustive-universe provenance | — | delivered + verified 7/7 + reviewed PASS |
| CR-026 | Second fresh set (8 scenarios, 16 checks) | never-graded domains | run 16/16 `INTACT` |
| CR-027 | FS-02 oracle token-form correction + re-grade (no re-run) | CR-026 envelopes | **transfer**: corrected semantic **A 16:16 vs B 13:16** |

Arm A advances across rounds (`fa84f48` → `b379c941`); arm B is pinned
byte-identical (`1a8c57c`, the Awesome QA Skills upstream). Same model
`gpt-6-astra`, same schema, same `NO_TOOL_USE`, AB/BA alternation throughout.

## Failure-class transfer (the core)

Three residual classes emerged from the first fresh set. Their resolution
across rounds is:

| Class | CR-022 / CR-024 | CR-026 (second fresh set) | Verdict |
|---|---|---|---|
| Event-name token form | symmetric noise, both arms (`RETURN_EVENT` vs `RETURN`) | n/a (corrected instrument; oracle-side defect caught separately) | **instrument-side** (CR-024), not an arm weakness |
| Over-generation (explicit-scope) | both arms 7 candidates vs oracle 1 | **A 4/4 vs B 3/4** (B over-generates on FS-04) | **arm-A fix transfers** |
| "Only states" provenance | A 0/3 vs B 2/3 (CR-022); A 0/3 vs B 1/3 (CR-024) | **A 4/4 vs B 2/4** (B omits on FS-03/FS-04) | **arm-A fix transfers; reverses the directional weakness** |

Two measurement defects were themselves discovered and corrected along the
way, both symmetric to the grading target and neither an arm-side weakness:

- **CR-024 (instrument-side OA-5):** the transition-list question did not pin
  whether the generic noun `event` is part of the event name; the oracle
  dropped it (`return event` → `RETURN`) while the arms were inconsistent.
  Fixed by pinning the convention in the question text; re-run confirmed both
  arms then reproduce the oracle exactly.
- **CR-027 (oracle-side OA-5):** the CR-026 FS-02 oracle used `SUBMIT`/`RESUBMIT`
  while the facts state "a submit action"/"a resubmit action"; both arms
  correctly produced `SUBMIT_ACTION`/`RESUBMIT_ACTION`, so the grading target
  was wrong. Fixed by correcting the oracle and re-grading the frozen
  envelopes (no re-run — the oracle is not in the prompt).

## Key result

The CR-022/CR-024 conclusion was that rounds 1–2 (CR-018/CR-021) **did not
transfer** a generalizable advantage to fresh material — on a clean instrument
arm A was statistically tied with (and on provenance marginally worse than)
arm B. That conclusion was the evidence base for round 3.

Round 3 (CR-025) targeted exactly the two classes the clean instrument exposed.
The second fresh set (CR-026/CR-027) then showed a **reversed, directional
transfer**:

- **exhaustive-universe provenance**: A **4/4** vs B **2/4** (was A 0/6 vs B
  3/6 across CR-022+CR-024);
- **explicit-scope discipline**: A **4/4** vs B **3/4** (was symmetric 7-vs-1);
- **controls**: 8/8 both arms — the new clauses did not leak into boundary or
  decision-table checks;
- **overall**: corrected semantic **A 16/16 vs B 13/16** (corrected exact A
  15/16 vs B 12/16).

This is the first fresh-set result in the series in which the post-upgrade arm
A is measurably ahead of the pinned arm B, and it holds on the two pre-declared
failure classes rather than on noise.

## Boundaries and what remains blocked

- **Bounded observation, not a holdout.** Both fresh sets were authored by the
  same agent family as the instruction author (R-03a disclosed), so transfer
  is measured against the author's own oracle, not an independent one.
- **No formal "stronger than Awesome QA Skills" claim is made.** Per REQ-011
  that claim requires the strict profile, independent human rating, and an
  independent holdout — all `NOT_AVAILABLE` in this environment.
- **Single-model, single-family evidence.** All runs use `gpt-6-astra`; the
  ±1 single-run noise floor documented since CR-019 applies. The CR-026
  advantage (A 16 vs B 13) is larger than one check, but remains a single
  paired run on a single fresh set.

The natural next step, when the missing resources become available, is the
Phase 3 protocol: freeze an independent holdout set (author-independent),
define the strict profile, and obtain human ratings — using this trajectory as
the input specification for which classes to instrument and how to score them.
