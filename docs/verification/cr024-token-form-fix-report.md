# CR-024 — Fresh-set event-name token-form correction + re-run (OA-5)

- Status: `DRAFT_UNAPPROVED` / `PUBLIC_DEVELOPMENT`
- Change register row: CR-024
- Runtime work item: TASK-106 (see Runtime registry)
- Predecessor: CR-022 (fresh-set verification, null transfer under a noisy instrument)

## 1. Purpose

CR-022 identified an oracle-side under-specification in the fresh set: the
transition-list checks instructed "uppercase-underscore form of the event
phrasing" but never pinned whether the generic noun `event` is part of the
event name. The oracle consistently dropped `event` (`return event` → `RETURN`,
`arrival event` → `ARRIVAL`), while the arms were inconsistent (arm A kept
`RETURN_EVENT` on FS-05 but dropped it on FS-06/07; arm B kept `_EVENT` on
FS-05/06 but dropped it on FS-07). This symmetric noise suppressed both arms'
scores on the token-form checks and could not be resolved by re-grading the old
outputs (the arms' recorded values are fixed and mutually inconsistent).

CR-024 corrects the instrument (OA-5) by pinning the convention in the question
text itself — the CR-020 OA-1..4 precedent of "write the token form into the
question" — then re-runs and re-grades to obtain the clean transfer signal.

## 2. Method & bindings

- Correction: the transition-list question text now reads
  `…Express event names as the uppercase-underscore form of the event phrasing
  in the facts, dropping the generic noun 'event' where it is part of the
  phrasing (for example 'return event' becomes RETURN, 'arrival event' becomes
  ARRIVAL, 'dispatch event' becomes DISPATCH).`
  Applied to 4 checks across 3 scenarios: FS-05 Q-FS-051/Q-FS-052, FS-06
  Q-FS-061, FS-07 Q-FS-071.
- Oracle expected values: **unchanged** (the oracle already used the `drop
  event` convention; the fix pins the question to that convention, not the
  reverse). The reverse fix (oracle → `RETURN_EVENT`) was rejected because it
  would break FS-06 arm A and FS-07 both arms, which already correctly dropped
  `event`.
- Arms frozen: A = `fa84f48` (post CR-018+CR-021), B = `1a8c57c` (pinned
  upstream, identical to CR-017/CR-019). Model `gpt-6-astra`, no-tool, both
  arms. Runtime `896a0166b774037a\codex.exe` (`f6dbf48c…`) unchanged.
- Exclusions regenerated with `cr024-evaluator` locators (oracle bytes
  identical, so `forbidden_sha256` unchanged; only `forbidden_locators` updated).

Binding hashes:

| artifact | sha256 |
|---|---|
| run manifest (canonical digest) | `342ba7f8fb342134e3d5eeff69b2141099199419b92fa7223e42b8f3bf79a042` |
| manifest file | `1bf79b8a0228bcd2b0ca2ad1c45866ea0bb53dea0625dbc55cfa69096c5ca7ba` |
| evaluator commitment | `bd6bb6798530bb5ce80dd5ab5da6f65d9286c6a232e5454c6bbd92e288b36293` |
| assertion bundle | `77bc1ad6a62cc58213871bc8e70f6a7bdeedd5fa16d2e4142e3863c52fccef53` |
| exclusions | `fe3cb0c3b1ec075569568af131137c219dcc3b24526258fa4d14f3f110dee0f8` |
| semantic rules | `89ea6b6242c57d21267350cf26087c97e5be1126187cf5a1cbcabe1cb77ada77` (unchanged) |

## 3. T1 — per-check results (exact → semantic)

`exact` = value order-sensitive + refs subset. `semantic` = S1/S3 set
equivalence + refs subset (S4 provenance rescue applies to fact-set only; S6
synonym equivalence not adopted).

| check | A exact | B exact | A sem | B sem | note |
|---|---|---|---|---|---|
| AS-FS-011 | SAT | SAT | SAT | SAT | |
| AS-FS-012 | SAT | SAT | SAT | SAT | |
| AS-FS-021 | VIOL | VIOL | SAT | SAT | S1 dict set (rejected order) |
| AS-FS-022 | SAT | SAT | SAT | SAT | |
| AS-FS-031 | SAT | SAT | SAT | SAT | |
| AS-FS-032 | SAT | SAT | SAT | SAT | |
| AS-FS-033 | SAT | SAT | SAT | SAT | |
| AS-FS-041 | SAT | SAT | SAT | SAT | |
| AS-FS-042 | SAT | SAT | SAT | SAT | |
| AS-FS-051 | VIOL | VIOL | VIOL | VIOL | value set-equal (order), **missing F-FS-051** |
| AS-FS-052 | VIOL | VIOL | VIOL | VIOL | over-generation 7 vs 1 |
| AS-FS-061 | VIOL | SAT | VIOL | SAT | **A missing F-FS-061**; B value+ref correct |
| AS-FS-062 | SAT | SAT | SAT | SAT | |
| AS-FS-071 | VIOL | VIOL | VIOL | VIOL | value correct, **missing F-FS-071** |
| AS-FS-072 | SAT | SAT | SAT | SAT | |
| AS-FS-081 | VIOL | VIOL | SAT | SAT | S1 rows set |
| AS-FS-082 | SAT | SAT | SAT | SAT | |
| AS-FS-083 | SAT | SAT | SAT | SAT | |

## 4. T2 — tallies

| layer | arm A | arm B | comparison |
|---|---|---|---|
| exact | 12 SAT / 6 VIOL | 13 SAT / 5 VIOL | B +1 |
| semantic | 14 SAT / 4 VIOL | 15 SAT / 3 VIOL | B +1 |

CR-022 → CR-024 comparison (same oracle, arms frozen; only question text and
manifest binding changed):

| layer | CR-022 | CR-024 |
|---|---|---|
| exact | A 13:5 vs B 12:6 | A 12:6 vs B 13:5 |
| semantic | A 14:4 vs B 14:4 (tied) | A 14:4 vs B 15:3 |

## 5. T3 — process

- 16/16 `COMPLETED_PROCESS`, run integrity `INTACT`.
- AB/BA alternation preserved: `A B B A A B B A A B B A A B B A`.
- `run_id` = `CR024-TOKEN-FORM-RERUN-001`; evidence class
  `EXPLORATORY_CONFIGURED_SAME_MODEL`; manifest validated
  `VALIDATED_NOT_EXECUTED` pre-run.

## 6. T4 — residual failure characterization (clean instrument)

After the token-form correction, the three residual categories are:

1. **Token-form — RESOLVED (instrument-side, OA-5).** Both arms now produce
   `RETURN`, `ARRIVAL`, `DOOR_CLOSE`, `FAULT_CLEAR`, `DISPATCH` correctly on all
   4 token-form checks. Confirms the CR-022 token-form failures were caused by
   the ambiguous instruction, not by an arm weakness.

2. **Over-generation (AS-FS-052) — symmetric, unchanged.** Both arms list 7
   invalid candidates where the oracle expects 1 explicitly-stated candidate.
   Neither arm disciplines "list only invalid candidates *explicitly stated*,
   do not derive more from the general rules".

3. **Provenance "only states" ref (F-FS-0x1) — asymmetric.** The transition-list
   checks require the `F-FS-0x1` "only states" fact as an evidence ref. Arm A
   omits it on **all 3** transition checks (0/3); arm B omits it on 2 (FS-05,
   FS-07) but retains `F-FS-061` on FS-06 (1/3). The value is correct in every
   case; the sole difference is the missing ref. This is the **only** semantic
   difference between the arms (AS-FS-061: A VIOL vs B SAT).

4. **List ordering (S1-rescued).** AS-FS-021 (rejected list), AS-FS-051 (row
   order), AS-FS-081 (row order) are exact-layer VIOLATED purely on ordering and
   are set-equal at the semantic layer.

## 7. R-03a — oracle-instruction association disclosure

The CR-024 correction edits the instruction text (question) in the scenario set,
not the oracle values. The corrected instruction is authored by the same agent
family as the scenario/oracle authors (CR-022 disclosure already noted the
author-vs-author overlap). The correction was made to close an instrument
ambiguity, not to favour either arm: it pins the oracle's *pre-existing*
convention (`drop event`), so it cannot change which arm is "correct" on the
token-form checks — it only removes the ambiguity that let the arms pick the
wrong convention. The same text was applied uniformly to both arms (both arms
receive the identical question).

## 8. Execution-time findings

1. **OA-5 confirmed instrument-side.** The token-form under-specification was a
   measurement defect: under the clarified instruction, both arms reproduce the
   oracle's event naming exactly. No arm-side token-form weakness exists.

2. **Null transfer is confirmed under a clean instrument.** The CR-022
   "null transfer" conclusion was *not* an artefact of the token-form noise in
   the direction of hiding an arm-A advantage — after cleaning, arm A and arm B
   remain statistically tied (semantic 15:14, a single-check difference well
   inside the ±1 single-run noise floor the CR-019 rerun already bounded).

3. **Candidate arm-A provenance weakness.** Across CR-022 and CR-024 combined,
   arm A cites the "only states" fact on 0/6 transition-list opportunities;
   arm B cites it on 3/6. This is a consistent directional pattern — plausibly
   a side effect of the CR-021 "label minimality" upgrade over-trimming evidence
   refs — but its score impact is small (one check) and requires a dedicated
   provenance-targeted comparison to establish as more than noise.

## 9. Conclusion

CR-024 corrected the token-form instrument defect and re-ran on the frozen arms.
Result: **semantic A 14:4 vs B 15:3 (exact A 12:6 vs B 13:5)**, the sole
semantic difference being arm A's omission of the `F-FS-061` "only states"
provenance ref. The token-form failures are confirmed instrument-side.

The overall conclusion for the paired comparison is unchanged and now rests on a
clean instrument: **the CR-018/CR-021 instruction upgrades do not transfer a
generalizable advantage to fresh material.** Arm A is not better than arm B
(Awesome QA Skills) on this set; on provenance it is marginally worse. Formal
"stronger than Awesome QA Skills" claims remain `NOT_AVAILABLE` pending the
REQ-011 strict profile + independent human rating + independent holdout.
