# CR-022 fresh verification scenario set — pre-registration

- Classification: `PUBLIC_DEVELOPMENT` / `DRAFT_UNAPPROVED`
- Author: comparison researcher (same agent family as the CR-018/CR-021
  instruction author — disclosed; the set is pre-registered before any run)
- Date: 2026-10-16
- Execution: blocked until upstream model quota recovers (2026-10-22); no run
  has occurred against these bytes

## Purpose

Behavioural verification of the CR-018 + CR-021 instruction upgrades on
material that was never a grading target of any prior run. The recorded
CR-017/CR-019 fixtures must not be reused (TASK-097 boundary): second-round
instructions were shaped by those residuals, so verification on the same
bytes would reward tuning rather than measure generality.

## Design rules

1. **Fresh content domains** (none reuse plan/destination, refund, login,
   order-shipment, discount-rate, ticket-count or delivery-fee semantics).
2. **Targets the four upgrade classes** with at least two scenarios each:
   multi-part answers, label minimality/family consistency, row-universe
   discipline, engine vocabulary alignment; plus two decimal-precision and
   two interior-neighbour checks to confirm CR-018 behaviors persist.
3. **Oracle authoring corrections** from the CR-020 audit:
   - OA-1: every oracle row must be derivable from the visible facts alone
     (a validity script is part of this pre-registration);
   - OA-2: provenance checks ask for the specific conflict/invalidity facts,
     not the universe fact, and the question wording names that reading;
   - OA-3: no synthesized token where the facts supply one; where a value
     must be synthesized, the check question itself fixes the token
     (e.g. "use GRANTED/DENIED"), so both arms receive identical
     instructions and no oracle-side arbitrariness remains;
   - OA-4: no numeric duplicates within one expected list.
4. **Same harness conditions** as CR-017/CR-019: one manifest, neutral
   response schema, same model and no-tool policy, AB/BA alternation, B arm
   pinned `1a8c57c` byte-identical, A arm at the post-CR-021 HEAD.

## Scenario roster (8 scenarios, 18 checks)

| ID | Method | Domain | Upgrade class targeted | Checks |
|---|---|---|---|---|
| FS-01 | boundary | Gym membership duration tiers (whole-number months) | interior neighbours both sides + multi-part (accepted+rejected) | Q-FS-011, Q-FS-012 |
| FS-02 | boundary | Invoice line-quantity decimal cap (thousandths rule) | declared precision + scale-violation candidates + both classes | Q-FS-021, Q-FS-022 |
| FS-03 | decision_table | Shipping-speed rules with one excluded combination and one rule conflict | multi-part (legal + excluded members) + engine vocabulary (CONFLICT/DEFINED) + provenance (specific facts) | Q-FS-031, Q-FS-032, Q-FS-033 |
| FS-04 | decision_table | Support-ticket priority matrix (2x2) | row-universe discipline (fact-defined rows only) + exact row keys; embedded ambiguity (escalation continuation undefined) | Q-FS-041, Q-FS-042 |
| FS-05 | state_transition | Library-loan lifecycle (renew/return/loss) | label minimality + family consistency (renewal family) + multi-part valid/invalid | Q-FS-051, Q-FS-052 |
| FS-06 | state_transition | Elevator control (idle/moving/doors/fault) | family consistency (fault family across three states) + universe discipline | Q-FS-061, Q-FS-062 |
| FS-07 | state_transition | Batch job lifecycle with retry counter | label minimality (retry counter separate from event names) + universe discipline; embedded ambiguity (retry limit unstated) | Q-FS-071, Q-FS-072 |
| FS-08 | decision_table | Discount-eligibility with promo overlap conflict | engine vocabulary (CONFLICT classification) + provenance specific facts | Q-FS-081, Q-FS-082, Q-FS-083 |

Embedded-ambiguity scenarios (gap behavior, no guessing): FS-04 (escalation
continuation undefined), FS-07 (retry-count limit unstated). Two ambiguity
scenarios (matching the CR-017 density) rather than four, to keep the set
focused on the upgrade classes.

## Frozen bytes and validity-script commitment (executed)

The scenario/oracle bytes are frozen under
`.qa-master/paired-pilot/cr022-fresh-preparation-v1/` (local-only,
gitignored, as with all run material). The pre-registered validity script
`cr022-oracle-validity-v1.py` was executed against those bytes and passed
**123/123 checks** covering OA-1 (evidence refs exist; checks exist;
value_type match; oracle bytes match hand-derived tables; every value token
derivable from facts text), OA-2 (provenance questions name the
specific-facts reading and expected answers are the specific fact IDs), OA-3
(synthesized token forms — classification, discount, event names, precision
— fixed in the question text itself, identical information for both arms),
OA-4 (no numeric duplicates).

- `cr022-oracle-validity-v1.py` sha256:
  `88f6caaaff954448391d24bc232c274034b909a2cfd572dda67533af8e9ab67f`
- `cr022-oracle-validity-v1.output.txt` sha256 (`ALL PASS`, 123/123):
  `c6c737276882757a8829ba321bce5235118257a9d169f8970b1d980572ebb547`

During validity checking, three scenario/question wording weaknesses were
found and corrected BEFORE any run (event-name form fixed in questions;
scale-violation derivation phrasing sharpened; hyphenated-phrase
derivation), and the final bytes re-validated 123/123. No model has seen
these bytes.

## Non-goals

This set verifies the four upgrade classes behaviourally on fresh material.
It is not a holdout (the author is not independent of the instruction
author), not a superiority claim, and not a substitute for the Phase 3 human
protocol. Tallies will be reported per upgrade class, per arm, with the
CR-019 baseline classes for context only.
