# CR-027 report: CR-026 second fresh-set run, FS-02 oracle token-form correction, and re-grade

- Classification: `PUBLIC_DEVELOPMENT` / `DRAFT_UNAPPROVED`
- Author: comparison researcher (same agent family as the CR-025 instruction
  author — disclosed, R-03a: arm-A instructions derive from the CR-022/CR-024
  oracle failure modes)
- Date: 2026-10-18
- Run ID: `CR026-SECOND-FRESH-VERIFICATION-001`
- Model: `gpt-6-astra` · policy `NO_TOOL_USE` · arm A `b379c941` (post-CR-025)
  · arm B pinned `1a8c57c`

## Purpose

Behavioural verification of the two CR-025 instruction upgrades on the
pre-registered CR-026 second fresh set (8 never-graded scenarios, 16 checks,
16 calls), followed by a disclosed oracle correction (CR-027) and re-grade of
the frozen envelopes.

## Run

16/16 calls `COMPLETED_PROCESS`, AB/BA alternation preserved, integrity
`INTACT`, backend `NATIVE_CODEX`, evidence class
`EXPLORATORY_CONFIGURED_SAME_MODEL`.

## Mechanical grade (as-registered oracle)

| Arm | SATISFIED / 16 |
|---|---|
| A | 14 |
| B | 11 |

`VIOLATED` under the as-registered oracle: `AS-FS-021` (both arms),
`AS-FS-031` (B), `AS-FS-041` (B), `AS-FS-042` (B), `AS-FS-081` (both arms).

## Oracle defect identified (OA-5 class, oracle-side)

`AS-FS-021` was violated by **both** arms for the same reason: the FS-02
oracle used `SUBMIT` / `RESUBMIT`, but the facts state "a submit action" and
"a resubmit action". The question pins "uppercase-underscore form of the event
phrasing", so the correct token is `SUBMIT_ACTION` / `RESUBMIT_ACTION`. Both
arms produced the correct form; the oracle had dropped the generic noun
`action` without pinning that drop in the question. This is the same
token-form under-specification class CR-024 identified for the CR-022
instrument, but this time the defect was **oracle-side** (the arms were
correct, the grading target was wrong).

## CR-027 correction + re-grade (frozen envelopes, no re-run)

The oracle is not part of the prompt, so correcting it does not change the
arms' outputs; a re-run is unnecessary. The FS-02 oracle was corrected
(`SUBMIT` → `SUBMIT_ACTION`, `RESUBMIT` → `RESUBMIT_ACTION`), re-validated as
fact-derivable, and the frozen envelopes re-graded under the unchanged
semantic rules (S1 set semantics, S3 numeric dedupe; S6 not adopted).

| Grade | A | B |
|---|---|---|
| Exact (corrected) | 15 / 16 | 12 / 16 |
| Semantic (corrected) | 16 / 16 | 13 / 16 |

The one exact-but-not-semantic difference is `AS-FS-081` (request-routing
legal combinations): both arms listed the same four rows in a different order,
rescued by S1. The corrected assertion bundle is `cr026-assertions-v2.json`
(sha256 `0fed53dddb589e1c2b265d466ed816c6c9ee03251a2082dea6572fddd8ad8d28770`).

## Per-failure-class result (semantic, corrected)

| Class | A | B | Arm-B residual |
|---|---|---|---|
| Exhaustive-universe provenance (4 valid-transition checks) | 4 / 4 | 2 / 4 | omits the "only states" fact on FS-03 (`F-FS-031`) and FS-04 (`F-FS-041`) |
| Explicit-scope discipline (4 invalid-candidate checks) | 4 / 4 | 3 / 4 | over-generates on FS-04 (`AS-FS-042`): 4 candidates vs oracle 1 (derives `WORK_START`/`RESOLUTION`/`CLOSURE` from `CLOSED` from the "final: no event leaves it" rule) |
| Controls (8 boundary + decision-table checks) | 8 / 8 | 8 / 8 | none |

## Conclusion

On never-graded material, the two CR-025 upgrades transfer:

- **Exhaustive-universe provenance**: arm A now cites the "only states" fact
  in 4/4 valid-transition checks, versus arm B's 2/4. This reverses the CR-024
  residual (arm A 0/3 vs arm B 1/3 on the same class).
- **Explicit-scope discipline**: arm A lists only the explicitly-stated
  invalid candidate in 4/4 checks, versus arm B's 3/4. This reverses the
  CR-022 residual (both arms 7 candidates vs oracle 1 on Q-FS-052).
- The control scenarios (8/8 both arms) confirm the CR-018/CR-021 behaviours
  persist and the new clauses do not leak into boundary or decision-table
  checks.

The FS-02 oracle defect is a self-inflicted authoring error, disclosed and
corrected before any conclusion was drawn; it does not affect the arm-B
residuals, which are genuine and match the CR-022/CR-024 classes.

## Boundaries

This is a bounded observation on two fresh (non-holdout) scenario sets. The
set author is the same agent family as the instruction author (R-03a
disclosed). Per REQ-011, a formal "stronger than Awesome QA Skills" claim
requires the strict profile, human scoring and an independent holdout — all
`NOT_AVAILABLE`. No superiority, quality, acceptance, Gate or release claim is
made here.
