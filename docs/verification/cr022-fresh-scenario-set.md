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

## Scenario roster (8 scenarios, 16 checks)

| ID | Method | Domain | Upgrade class targeted | Checks |
|---|---|---|---|---|
| FS-01 | boundary | Gym membership duration tiers (whole-number months) | interior neighbours both sides + multi-part (accepted+rejected) | Q-FS-011, Q-FS-012 |
| FS-02 | boundary | Invoice line-quantity decimal cap (thousandths rule) | declared precision + scale-violation candidate + both classes | Q-FS-021, Q-FS-022 |
| FS-03 | decision_table | Shipping-speed rules with one excluded combination and one rule conflict | multi-part (legal + excluded members) + engine vocabulary (CONFLICT/EXCLUDED) + provenance (specific facts) | Q-FS-031, Q-FS-032, Q-FS-033 |
| FS-04 | decision_table | Support-ticket priority matrix (3 conditions) | row-universe discipline (fact-defined rows only) + exact row keys | Q-FS-041, Q-FS-042 |
| FS-05 | state_transition | Library-loan lifecycle (renew/damage/return) | label minimality + family consistency (renew family) + multi-part valid/invalid | Q-FS-051, Q-FS-052 |
| FS-06 | state_transition | Elevator control (idle/moving/fault) | family consistency (door-open/door-closed family) + label minimality | Q-FS-061, Q-FS-062 |
| FS-07 | state_transition | Batch job lifecycle (queued/running/failed/done) with retry counter | label minimality (retry counter separate from event names) + universe discipline | Q-FS-071, Q-FS-072 |
| FS-08 | decision_table | Discount-eligibility with promo overlap conflict | engine vocabulary (CONFLICT classification) + provenance specific facts | Q-FS-081, Q-FS-082, Q-FS-083 |

Embedded-ambiguity scenarios (gap behavior, no guessing): FS-04 (one cell
undefined), FS-07 (retry-count limit unstated). Two ambiguity scenarios
(matching the CR-017 density) rather than four, to keep the set focused on
the upgrade classes.

## Oracle validity script commitment

Before any run, a script asserts for every check: (a) every expected row and
value is string-derivable from that scenario's `known_facts` (OA-1);
(b) provenance answers name the specific conflict/invalidity fact IDs
(OA-2); (c) synthesized tokens appear only where the check question itself
fixes the token (OA-3); (d) expected lists contain no numeric duplicates
(OA-4). The script and its output hash are registered as evidence before the
run manifest is built.

## Non-goals

This set verifies the four upgrade classes behaviourally on fresh material.
It is not a holdout (the author is not independent of the instruction
author), not a superiority claim, and not a substitute for the Phase 3 human
protocol. Tallies will be reported per upgrade class, per arm, with the
CR-019 baseline classes for context only.
