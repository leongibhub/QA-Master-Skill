# CR-020 oracle-consistency audit: CR-017/CR-019 public-development oracle versus its own visible facts

- Run IDs audited: `CR017-EXPANDED-PUBLIC-DEV-001`, `CR019-VERIFICATION-RERUN-001`
- Classification: `PUBLIC_DEVELOPMENT` / `DRAFT_UNAPPROVED`
- Auditor: comparison researcher (same agent family as the scenario author and the
  run executor — disclosed, not independent)
- Date: 2026-10-16
- Method: no model calls; byte-level read of every oracle row, the matching
  check question and the scenario's visible facts.

## Purpose

CR-019's residual-failure analysis repeatedly found checks where both arms'
answers look methodologically reasonable yet fail the exact oracle. Before a
second instruction round, the oracle itself must be audited against its own
facts so that the remaining gap is attributed to the correct side.

## Finding OA-1 (P1): `Q-STT-001` oracle contradicts its own facts

The facts define DRAFT/SUBMITTED/CANCELLED with submit (guarded), cancel
DRAFT→CANCELLED, and state that **SUBMITTED is terminal**: cancel from
SUBMITTED is invalid, archive is not a defined event, and submit with
owner=false is invalid. The oracle expects five rows:

- `REJECT SUBMITTED→DRAFT` — no REJECT event exists in any fact;
- `CANCEL SUBMITTED→CANCELLED` — F-STT-004 states the opposite;
- `PERSIST SUBMITTED→SUBMITTED` — a side effect treated as a transition.

No behaviour of either arm can satisfy this oracle while respecting the
facts. Both arms fail it in every run; the failure is an oracle defect, not a
skill defect. The exact/semantic tallies that include it undercount both arms
equally, so between-arm comparisons stay valid, but the check must not be
counted against either product.

## Finding OA-2 (P3): `Q-DTT-002`/`Q-STT-002` oracle provenance answers are one defensible reading among several

"Fact IDs that make the outcome unresolved / supporting the invalid
candidates": the oracle answers `["F-DTT-001"]` / `["F-STT-001"]` (the
state/universe-defining fact). Both arms answered with the specific
conflict/invalidity facts (`F-DTT-003`+`F-DTT-006`; `F-STT-004`+`F-STT-005`+
`F-STT-006`) — arguably the more precise reading of the question. Both
readings are defensible; the oracle picked one. Representation freedom, not
skill deficiency.

## Finding OA-3 (P3): `Q-DTT-031` oracle value for access grants (`GRANTED`) synthesizes a token absent from the facts

The facts say `access is allowed`/`is denied` (prose). The oracle expects
`GRANTED`/`DENIED`. Arm A answered `ALLOWED`/`DENIED`; arm B
`ALLOWED`/`DENIED`. No source token exists, so this is legitimate synthesis
territory — the oracle's choice of `GRANTED` over `ALLOWED` is arbitrary
relative to the phrasing. Any convention that fixes a non-source token here
would be oracle-fitting, so arm instructions must not be tuned to it; the
semantic layer already passes both arms' answers under row-set normalization
… wait, it does not (it fails because `ALLOWED` ≠ `GRANTED` after
normalization). Both arms fail exact and semantic. An oracle-side defect
class, retained.

## Finding OA-4 (P3): `Q-BND-021` rejected list contains a numeric duplicate

Carried over from CR-017 (already disclosed in CR-019 via rule S3): expected
`"100.00"` and `"100"` in the same rejected list. The pre-declared semantic
rule S3 handles it; the exact layer stays VIOLATED for convention-following
answers.

## What the audit does NOT change

- The two CR-018 targeted checks (`Q-BND-021`, `Q-DTT-011`) are correctly
  authored; CR-019 verified their fixes at value level.
- Between-arm comparisons remain valid: every oracle defect listed affects
  both arms equally (both fail, both unscorable, or both semantically
  failed), so no relative advantage was manufactured or removed.
- No scenario byte, oracle value or assertion changes now: the runs are
  recorded evidence. Corrections belong to a future fresh scenario set
  (CR-021+), pre-registered before any further run.

## Residual arm-A failure taxonomy after oracle-side defects are set aside

| Check | A failure form | Defect side |
|---|---|---|
| Q-DTT-001 | answers only legal combinations; no `excluded_combinations` member; `CONFLICTING` vs engine vocabulary `CONFLICT` | skill (shape) + skill (vocabulary consistency) |
| Q-DTT-002 | cites specific conflict facts, oracle wants universe fact | oracle (OA-2) |
| Q-DTT-021 | extra correct-but-undefined `FINAL_SALE` rows | skill (universe completeness discipline) |
| Q-STT-001 | answers invalid transitions where valid+invalid asked; shape mismatch | skill (multi-part) + oracle (OA-1) |
| Q-STT-002 | as Q-DTT-002 | oracle (OA-2) |
| Q-STT-011 | over-qualified event labels (`WRONG_PASSWORD_BEFORE_…`) | skill (label minimality) |
| Q-STT-021 | over-qualified event label (`CONFIRMED_PAYMENT`), guard-qualified rows | skill (label minimality) |
| Q-DTT-031 | `ALLOWED` vs oracle `GRANTED` (no source token) | oracle (OA-3) |

Skill-side targets for the second instruction round: (1) multi-part answer
completeness, (2) label minimality (shortest source-faithful form), (3) row
universe completeness discipline, (4) vocabulary alignment with the
deterministic engine (`CONFLICT`, not `CONFLICTING`).

Oracle-side defects (OA-1..OA-4) are recorded for future scenario-set
authoring: they must not be fixed in place (recorded runs bind these bytes),
and arm instructions must not be tuned to OA-3's arbitrary token.
