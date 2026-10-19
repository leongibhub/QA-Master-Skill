# CR-019 verification re-run report: CR-018 instruction upgrades under the unchanged CR-017 oracle

- Run ID: `CR019-VERIFICATION-RERUN-001`
- Classification: `PUBLIC_DEVELOPMENT` / `DRAFT_UNAPPROVED`
- Executor: comparison researcher (same agent family as the CR-018 author and the
  CR-017 executor — disclosed, not independent)
- Date: 2026-10-16
- Status: complete for this report's bounded scope; see Execution notes

## Purpose

CR-018 (commit `c193774`) upgraded five arm-A instruction rules mapped to
observed CR-017 failure modes. TASK-092 verified the content and packaging and
TASK-093 reviewed it PASS, but behavioural effect was unproven. This re-run
measures whether the codified instructions changed arm-A behaviour under the
**unchanged** CR-017 scenario bytes, oracle values and pre-bound assertion
semantics.

## Design

- Same 12 public-development scenarios, same prompt template, same neutral
  response schema, same model (`gpt-6-astra`, medium, all 15 features
  disabled, read-only sandbox), same AB/BA schedule as CR-017.
- Arm A: packaged assets at `62f22f6` (8 files: the 7 CR-017 files plus the
  new `references/typed-observations.md`; SKILL.md / functional-api.md /
  work-protocol.md upgraded per CR-018).
- Arm B: pinned upstream skill library `1a8c57c` — all 6 file bytes
  re-verified identical to CR-017.
- Assertion bundle re-bound to the new manifest hash; the 24 assertion values
  are byte-identical to CR-017.
- Supplementary semantic rules S1–S5 (including S3 numeric set-dedupe)
  declared in `cr019-semantic-rules-v1.md` BEFORE execution, per the TASK-093
  R-03 requirement.

### Required disclosure (R-03a)

Arm-A instructions at `62f22f6` were derived in CR-018 from the CR-017
grading failure modes of **this same oracle**. The re-run therefore measures
whether codified instructions close the observed failure modes on development
material, and must not be presented as independent of that linkage. The
holdout protocol for any unbiased claim remains the CR-014/CR-016 human
protocol, unchanged.

## Execution notes

- 22/24 calls COMPLETE (804.6 s total model time across completed calls).
- `PE-STT-004` both arms `NOT_EXECUTED`: the upstream model reported a usage
  limit for both calls within seconds of each other. Identical condition for
  both arms; per protocol no retry, no synthesis. `Q-STT-031`/`Q-STT-032`
  are therefore `UNSCORABLE` and excluded from all tallies below.
- Run integrity: `INTACT` / `RECORDED` via `inspect_run`; all captured assets
  `RETAINED`; run tree local-only (gitignored) as before.

## Results — same-22 comparable set

Pre-registered exact typed-assertion grading:

| | CR-017 (same 22) | CR-019 | Δ |
|---|---|---|---|
| A — QA Master post-CR018 | 8 | 8 | 0 |
| B — the upstream skill library (pinned) | 6 | 7 | +1 |

Pre-declared supplementary semantic layer (S1–S5):

| | CR-017 (same 22) | CR-019 | Δ |
|---|---|---|---|
| A — QA Master post-CR018 | 12 | **14** | +2 |
| B — the upstream skill library (pinned) | 10 | 11 | +1 |

### Mechanism verification (byte-level)

The two checks that flipped from fail to semantic-pass for arm A are exactly
the two the CR-018 upgrades targeted:

- `Q-BND-021` (decimal precision). CR-017 arm A observed `0.5`, no
  scale-violation candidate. CR-019 arm A observed
  `accepted: ["0.50","0.51","99.98","99.99"], rejected: ["0.49","0.505","100.00"]`
  — declared precision preserved (`0.50`) and the one-beyond-scale candidate
  (`0.505`) present. Arm B (unchanged bytes) still emits `0.5` and
  `0.501`/`99.989` free-form precision-violating values. The exact layer
  stays VIOLATED for A only because the oracle's rejected list contains the
  numeric duplicate `"100.00"`/`"100"` (an oracle authoring artifact, handled
  by declared rule S3).
- `Q-DTT-011` (synthesized band labels). CR-019 arm A synthesizes
  `BELOW_1000` / `AT_OR_ABOVE_1000` as the conventions require; arm B still
  answers `below 1000` / `1000 or above` in free prose form.

The gap taxonomy is also now structural rather than spontaneous: arm-A gap
records on the ambiguity scenarios carry `ENDPOINT_AMBIGUITY`,
`EXECUTION_OBSERVABLE_MISSING` and `SETUP_CLEANUP_MISSING` as stable gap IDs
mirroring the codified work-protocol rule.

### Noise disclosure

Arm B's bytes did not change, yet its exact score moved 6→7 (`Q-BND-031`,
interior neighbour 998 now present). This bounds single-run, no-seed
variation at roughly ±1 check in this setup. Arm A's exact-pass set is
byte-for-byte the same 8 checks in both runs. Arm A's +2 semantic gain
therefore stands just above the observed noise floor and is supported by the
byte-level mechanism above, but a single run cannot exclude that part of the
movement is noise.

### Residual arm-A failure taxonomy (unchanged or incompletely fixed)

- Multi-part checks answered partially: `Q-DTT-001` answers only the legal
  combinations (no `excluded_combinations` member); `Q-STT-001` answers
  invalid transitions where valid transition rows were asked for. Both arms
  fail both checks; the conventions' "every check answers every part" rule
  did not fully transfer to these shapes.
- Label over-qualification: `Q-STT-011` emits
  `WRONG_PASSWORD_BEFORE_THIRD_CONSECUTIVE_WRONG_PASSWORD` where the source
  phrase collapses to `WRONG_PASSWORD`; `Q-STT-021` emits `CONFIRMED_PAYMENT`
  where the source phrase order gives `PAYMENT_CONFIRMED`. The
  uppercase-underscore form is followed; minimal source-derived phrasing is
  not.
- Extra rows: `Q-DTT-021` adds a correct-but-extra `FINAL_SALE` row beyond
  the defined combinations.

These are candidate targets for a further iteration, to be assessed against
fresh scenarios before any broader statement.

## Bounded conclusion

On the same 22 comparable public-development checks under the unchanged
oracle: arm A (QA Master post-CR018) scores 8 vs 7 (exact) and 14 vs 11
(semantic) against the pinned upstream skill library, versus 8 vs 6 and 12 vs 10 in
CR-017. The two newly-passing arm-A checks are precisely the CR-018 targets,
verified at value level. This is exploratory evidence that the codified
instructions closed the targeted failure modes on development material. It is
not a superiority, quality or acceptance claim; single-run no-seed variation
and the disclosed instruction-oracle linkage both apply, and the formal claim
path (strict profile, human ratings, holdout) remains unchanged and
`NOT_AVAILABLE`.
