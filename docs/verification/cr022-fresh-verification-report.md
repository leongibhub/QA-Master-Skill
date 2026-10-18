# CR-022 fresh-set paired verification — report (data-filled)

- Classification: `PUBLIC_DEVELOPMENT` / `DRAFT_UNAPPROVED`
- Run id: `CR022-FRESH-VERIFICATION-001`
- Executed by: comparison researcher (same agent family as the scenario and
  instruction author — disclosed; not an independent holdout)
- Date: 2026-10-18 (executed after upstream model quota recovery and a second
  codex.exe bin rotation; see "Execution notes")
- Status: complete for this report's bounded scope; no superiority, quality,
  acceptance, Gate or release claim is made (see R-03a)
- Skeleton: this document fills the pre-registered
  `cr022-report-skeleton.md` (frozen at `2c5abb6`, bindings re-derived
  2026-10-18 after the second bin rotation). Skeleton structure, columns,
  check-to-class mapping and status vocabularies were fixed before any CR-022
  model call and are reproduced here unchanged.

## Purpose

CR-022 measures whether the CR-018 + CR-021 arm-A instruction upgrades
transfer to **fresh material never graded before** — eight new scenarios
across new domains, authored after those upgrades, targeting the same upgrade
classes plus CR-018 persistence. This is the transfer check the prior CR-019
re-run (same material, unchanged oracle) could not perform. Both arms ran the
same model, same input, same schema, same no-tool policy, AB/BA schedule.

## Pre-registered bindings (re-derived 2026-10-18 after second bin rotation)

| Artifact | Value |
|---|---|
| Run manifest canonical digest (bound into assertion bundle) | `c04969f85af81484b5a9f5cb1834841cb46d7b3674dd57335e1aef7ef292ca7f` |
| Assertion bundle sha256 (live) | `ca6e95e1277bc7ac134f8f2117c5661941eee603d5d969bcf208642b6fd39af7` |
| Semantic rules sha256 (live) | `89ea6b6242c57d21267350cf26087c97e5be1126187cf5a1cbcabe1cb77ada77` |
| Arm A commit | `fa84f489abe62cbf7cfe9185729fc480466a80d3` (post CR-018 + CR-021) |
| Arm B commit (pinned) | `1a8c57c` byte-identical to CR-017/CR-019 upstream arm |
| codex.exe sha256 (re-bound 2026-10-18; version string unchanged at `0.163.0-alpha.10.2`) | `f6dbf48cb70f62649c645f26c87dc9bf84cc36986202dfad8e12fb5b8ca70312` |

## T1 — Per-check exact and semantic outcomes per arm (18 checks)

Exact vocabulary: `SATISFIED` / `VIOLATED` / `UNSCORABLE`. Semantic
vocabulary: `SEMANTIC_SATISFIED` / `SEMANTIC_VIOLATED` / `SEMANTIC_ABSENT`
(rules S1–S5 applied identically; S6 explicitly not adopted).

| Scenario | Check | Classes (pre-declared) | A exact | B exact | A semantic | B semantic |
|---|---|---|---|---|---|---|
| FS-01 | Q-FS-011 | interior-neighbour persistence | SATISFIED | SATISFIED | SEMANTIC_SATISFIED | SEMANTIC_SATISFIED |
| FS-01 | Q-FS-012 | interior-neighbour persistence | SATISFIED | SATISFIED | SEMANTIC_SATISFIED | SEMANTIC_SATISFIED |
| FS-02 | Q-FS-021 | multi-part completeness; precision and scale-violation persistence | SATISFIED | VIOLATED | SEMANTIC_SATISFIED | SEMANTIC_SATISFIED (S1) |
| FS-02 | Q-FS-022 | precision and scale-violation persistence | SATISFIED | SATISFIED | SEMANTIC_SATISFIED | SEMANTIC_SATISFIED |
| FS-03 | Q-FS-031 | multi-part completeness; engine vocabulary alignment | SATISFIED | SATISFIED | SEMANTIC_SATISFIED | SEMANTIC_SATISFIED |
| FS-03 | Q-FS-032 | provenance specificity | SATISFIED | SATISFIED | SEMANTIC_SATISFIED | SEMANTIC_SATISFIED |
| FS-03 | Q-FS-033 | provenance specificity | SATISFIED | SATISFIED | SEMANTIC_SATISFIED | SEMANTIC_SATISFIED |
| FS-04 | Q-FS-041 | row-universe discipline | SATISFIED | SATISFIED | SEMANTIC_SATISFIED | SEMANTIC_SATISFIED |
| FS-04 | Q-FS-042 | provenance specificity | SATISFIED | SATISFIED | SEMANTIC_SATISFIED | SEMANTIC_SATISFIED |
| FS-05 | Q-FS-051 | multi-part completeness | VIOLATED | VIOLATED | SEMANTIC_VIOLATED (S6) | SEMANTIC_VIOLATED (S6) |
| FS-05 | Q-FS-052 | multi-part completeness | VIOLATED | VIOLATED | SEMANTIC_VIOLATED | SEMANTIC_VIOLATED |
| FS-06 | Q-FS-061 | label minimality and family consistency | VIOLATED | VIOLATED | SEMANTIC_VIOLATED (S4) | SEMANTIC_VIOLATED (S6) |
| FS-06 | Q-FS-062 | provenance specificity | SATISFIED | SATISFIED | SEMANTIC_SATISFIED | SEMANTIC_SATISFIED |
| FS-07 | Q-FS-071 | label minimality and family consistency; row-universe discipline | VIOLATED | VIOLATED | SEMANTIC_VIOLATED (S4) | SEMANTIC_VIOLATED (S4) |
| FS-07 | Q-FS-072 | provenance specificity | SATISFIED | SATISFIED | SEMANTIC_SATISFIED | SEMANTIC_SATISFIED |
| FS-08 | Q-FS-081 | row-universe discipline; engine vocabulary alignment | VIOLATED | VIOLATED | SEMANTIC_SATISFIED (S1) | SEMANTIC_SATISFIED (S1) |
| FS-08 | Q-FS-082 | provenance specificity | SATISFIED | SATISFIED | SEMANTIC_SATISFIED | SEMANTIC_SATISFIED |
| FS-08 | Q-FS-083 | provenance specificity | SATISFIED | SATISFIED | SEMANTIC_SATISFIED | SEMANTIC_SATISFIED |

**Exact totals:** A **13** SATISFIED / **5** VIOLATED / 0 UNSCORABLE; B
**12** SATISFIED / **6** VIOLATED / 0 UNSCORABLE.
**Semantic totals:** A **14** SEMANTIC_SATISFIED / **4** SEMANTIC_VIOLATED;
B **14** SEMANTIC_SATISFIED / **4** SEMANTIC_VIOLATED.

Semantic-rule applications (per check, identical to both arms):

- **S1 row/dict set semantics** rescued `Q-FS-021` (B) and `Q-FS-081` (A, B)
  — both were pure row/field ordering differences with identical sets after
  normalization. `Q-FS-021` B's `rejected` list is the same four strings in a
  different order; `Q-FS-081` both arms list the same four legal
  discount combinations in a different order.
- **S6 (synonym equivalence) is NOT adopted**, so the event-name token-form
  differences `RETURN_EVENT` vs `RETURN` (FS-05, both arms) and `ARRIVAL_EVENT`
  vs `ARRIVAL` (FS-06, arm B) are **not** rescued and remain
  SEMANTIC_VIOLATED. See "Execution-time oracle-side findings".
- **S4 (provenance subset) is fact-set-only** (STRING_SET observations). It
  does **not** rescue a JSON row-list observation whose value is correct but
  whose `evidence_refs` omit the required `F-FS-0x1` "only states" fact
  (`Q-FS-061` arm A missing `F-FS-061`; `Q-FS-071` both arms missing
  `F-FS-071`). Those remain SEMANTIC_VIOLATED.

## T2 — Per-class tallies per arm (computed from T1 only)

Plan-vs-oracle deviation disclosure carried forward from the skeleton: the
pre-declared plan names `Q-FS-053` under label minimality, but the frozen
18-check oracle contains no `Q-FS-053`; the class tally below counts the
checks that actually exist (`Q-FS-061`, `Q-FS-071`) and retains `Q-FS-053`
as a named-but-absent member that can never be counted.

| Class | Checks | A exact | B exact | A semantic | B semantic |
|---|---|---|---|---|---|
| multi-part completeness | Q-FS-021, Q-FS-031, Q-FS-051, Q-FS-052 | 2/4 | 1/4 | 2/4 | 2/4 |
| label minimality and family consistency | Q-FS-053 (absent), Q-FS-061, Q-FS-071 | 0/2 | 0/2 | 0/2 | 0/2 |
| row-universe discipline | Q-FS-041, Q-FS-071, Q-FS-081 | 1/3 | 1/3 | 2/3 | 2/3 |
| engine vocabulary alignment | Q-FS-031, Q-FS-081 | 1/2 | 1/2 | 2/2 | 2/2 |
| precision and scale-violation persistence | Q-FS-021, Q-FS-022 | 2/2 | 1/2 | 2/2 | 2/2 |
| interior-neighbour persistence | Q-FS-011, Q-FS-012 | 2/2 | 2/2 | 2/2 | 2/2 |
| provenance specificity | Q-FS-032, Q-FS-033, Q-FS-042, Q-FS-062, Q-FS-072, Q-FS-082, Q-FS-083 | 7/7 | 7/7 | 7/7 | 7/7 |

Every between-arm difference is ±1 on a count and sits inside the CR-019
noise-floor disclosure (±1). The only exact-layer difference that favours arm
A (`Q-FS-021`) is a pure list-ordering artifact that S1 rescues; after the
semantic layer the two arms are **tied on every class**.

## T3 — Process layer (both arms)

All 16 calls `COMPLETED_PROCESS` with output `COMPLETE`; no `PARTIAL`,
`FAILED` or `NOT_EXECUTED` (no quota event like CR-019 `PE-STT-004`).

| Scenario | Arm A process | Arm B process | Notes |
|---|---|---|---|
| FS-01 | COMPLETE | COMPLETE | |
| FS-02 | COMPLETE | COMPLETE | |
| FS-03 | COMPLETE | COMPLETE | |
| FS-04 | COMPLETE | COMPLETE | |
| FS-05 | COMPLETE | COMPLETE | |
| FS-06 | COMPLETE | COMPLETE | |
| FS-07 | COMPLETE | COMPLETE | |
| FS-08 | COMPLETE | COMPLETE | |

Integrity `INTACT`; AB/BA order preserved (`A,B,B,A,A,B,B,A,A,B,B,A,A,B,B,A`).

## T4 — Embedded-ambiguity gap behaviour (descriptive, not pass/fail)

| Scenario | Arm | Rows produced | Gap handling | Ambiguity flagged? |
|---|---|---|---|---|
| FS-04 (ticket priority) | A | 4 legal rows (URGENT/HIGH/BASIC, URGENT/HIGH/PREMIUM, NORMAL/LOW/BASIC, HIGH/LOW/PREMIUM) | `ESCALATION_CONTINUATION_UNDEFINED` + `EXECUTION_OBSERVABLE_AND_FIXTURES_MISSING` + `HANDLING_SEMANTICS_UNSPECIFIED` | Yes |
| FS-04 (ticket priority) | B | same 4 legal rows | `GAP-01` (post-escalation priority undefined) | Yes |
| FS-07 (batch job retry) | A | 4 legal transitions (DISPATCH, SUCCESS_REPORT, FAILURE_REPORT, RETRY_REQUEST) | `RETRY_LIMIT_UNSPECIFIED` + `TRANSITION_ORACLES_MISSING` + `EXECUTION_OBSERVABLE_MISSING` + `SETUP_CLEANUP_MISSING` | Yes |
| FS-07 (batch job retry) | B | same 4 legal transitions | `G-01` (retry threshold) + `G-02` + `G-03` + `G-04` | Yes |

Both arms flagged the embedded ambiguity as a gap and did **not** invent the
undefined post-escalation priority (FS-04) or the undefined retry limit
(FS-07). Gap-labelling id/style differs (arm A uses descriptive
`X_Y` ids; arm B uses `GAP-0n`/`G-0n`), but behaviour is equivalent. This
gap-discipline behaviour is the CR-018 persistence target and it holds on
both arms — it is not an arm-A differentiator. Note: the skeleton's T4 header
labels FS-07 "elevator retry"; FS-07 is the batch-job scenario (retry-limit
ambiguity); FS-06 is the elevator. Filled table uses the correct domain.

## Execution-time oracle-side findings (disclosed, symmetric)

These were observed at execution, not pre-registered, and are disclosed here
per the report's linkage obligations. All three affect both arms and so do
not change any between-arm comparison; they do suppress both arms' scores on
the valid-transition checks of FS-05/FS-06/FS-07.

1. **Event-name token form under-specified (FS-05/FS-06, affects
   `Q-FS-051`/`Q-FS-061`).** The checks instruct "express event names as the
   uppercase-underscore form of the event phrasing in the facts". The facts
   phrase these as "a return event", "an arrival event", "a door-close event",
   "a fault-clear event", "a dispatch event". The oracle systematically drops
   the generic noun "event" (`RETURN`, `ARRIVAL`, `DOOR_CLOSE`, `FAULT_CLEAR`,
   `DISPATCH`), but that convention is not stated in the question text, and
   "the event phrasing" literally reads as including the word "event". Both
   arms are inconsistent: arm A emits `RETURN_EVENT` (FS-05) but `ARRIVAL`
   (FS-06); arm B emits `RETURN_EVENT` (FS-05), `ARRIVAL_EVENT`/`DOOR_CLOSE_EVENT`
   (FS-06) but `DISPATCH` (FS-07). Under S6-not-adopted, no rule equates
   `X_EVENT` with `X`, so these stay VIOLATED. This mirrors the CR-020 OA-3
   class (token form not pinned in the question), and belongs to future
   scenario-authoring correction, not arm tuning.
2. **Over-generation of invalid candidates (FS-05 `Q-FS-052`).** The facts
   explicitly state a single invalid candidate ("renewal from RENEWED is
   invalid", `F-FS-053`) and state that RETURNED/LOST "are final: no event
   leaves them" (`F-FS-055`). The oracle expects only the one explicit
   candidate; both arms additionally derive invalid candidates from the
   final-state rule and emit ~7 rows instead of 1. This is a symmetric
   "listing only what is explicitly stated" miss, not an arm-A-specific
   regression.
3. **Provenance omission of the "only states" fact.** The valid-transition
   checks require the `F-FS-0x1` "only states" fact as an evidence ref. Arm A
   omits it on all three transition checks (FS-05/06/07); arm B omits it only
   on FS-07. Descriptive observation only — S4 is fact-set-only and does not
   rescue it, so the checks stay VIOLATED; the between-arm score is unchanged
   (both arms fail `Q-FS-061`/`Q-FS-071`).

## Interpretation (bounded, exploratory)

On the CR-022 fresh material the two arms are **statistically
indistinguishable**: exact A 13 vs B 12 (the one difference is a list-ordering
artifact rescued by S1), semantic **tied 14:14**. This contrasts with the
CR-019 re-run (same material, A 14:11 semantic over B) and means the CR-018 +
CR-021 upgrades did **not** demonstrate transfer to never-seen material: on
every pre-declared class the arms tie after the semantic layer, and the
residual failures are symmetric oracle-side under-specifications (event token
form, over-generation reading, "only states" provenance) rather than
arm-A-targeted classes showing a differential effect.

This is a null/neutral transfer result. It does not support a claim that arm A
outperforms arm B on fresh material; it is consistent with the prior upgrades
being at least partly specific to the failure modes of the earlier oracle.
The gap-discipline persistence target (record-the-gap, do-not-invent) is the
one behaviour that visibly holds on both arms and is therefore not a
differentiator.

## R-03a linkage disclosure (fixed wording)

Arm-A instructions at commit `fa84f48` embed the CR-018 and CR-021 upgrades,
which were derived from the CR-017/CR-019 failure modes of the prior oracle.
The CR-022 set is fresh material authored AFTER those upgrades, targeting the
same upgrade classes with new domains; the scenario author is the same agent
family as the instruction author (not independent). Results are exploratory
public-development evidence. No superiority, quality, acceptance, Gate or
release claim is authorized by this run; the formal claim path (strict
profile, human ratings, independent holdout) remains `NOT_AVAILABLE`.

## Execution notes

- Executed 2026-10-18 after upstream model quota recovery and a second
  codex.exe bin directory rotation (`e78bad9887fa50cf` → `896a0166b774037a`).
  Version string unchanged (`0.163.0-alpha.10.2`); only the binary identity
  (path + sha256) changed. The manifest runtime block, its canonical digest and
  the assertion bundle's bound `run_manifest_sha256` were re-derived and
  re-validated (`VALIDATED_NOT_EXECUTED`). No scenario, oracle, arm asset,
  semantic-rule or exclusion byte changed. Model alias, reasoning effort,
  read-only sandbox and all 16 disabled features are byte-identical to the
  TASK-100 manifest.
- Output root `.qa-master/paired-pilot/observed-cr022/` (fresh, not the
  TEST_DOUBLE dry-run root); grade report `cr022-grade-v1.json` bound to
  manifest digest `c04969f8…` and assertion-bundle sha `025f25c0…`.

## Status legend

- Exact: `SATISFIED` = mechanical grader matched expected value and evidence
  refs; `VIOLATED` = mismatch; `UNSCORABLE` = no single retained observation.
- Semantic: `SEMANTIC_SATISFIED`/`SEMANTIC_VIOLATED` = equivalent after S1–S5
  normalization (rule cited per use); `SEMANTIC_ABSENT` = no retained
  observation to normalize.
- Process: `COMPLETE` / `PARTIAL` / `FAILED` / `NOT_EXECUTED`.
