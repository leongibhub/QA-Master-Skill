# CR-017 expanded paired comparison attempt and grade report

- Artifact ID: `DOC-CR017-PAIRED-COMPARISON-001`
- Proposed evidence ID: `EVD-CR017-PAIRED-COMPARISON-001`
- Change: `CR-017`
- Work: `TASK-090` / `work-e92f4ec4238d4276bb6953e2c18061df`, attempt 1
- Run ID: `CR017-EXPANDED-PUBLIC-DEV-001`
- Date: 2026-10-16
- Classification: `PUBLIC_DEVELOPMENT` executed exploratory comparison with
  typed-assertion grades. Evidence class `EXPLORATORY_CONFIGURED_SAME_MODEL`:
  the model alias is configured identically for both arms, but provider
  revision and system baseline remain `NOT_AVAILABLE`/`UNVERIFIED` and no seed
  exists. This is **not** a strict comparison under `REQ-024`, not a human
  rating, not a quality verdict, and not an acceptance, Gate, release or
  superiority decision.

## Purpose and boundary

The user directed an actual comparison with the upstream skill library now that
development and testing are complete. This run executes that comparison under
the retained paired-pilot machinery: one run manifest binds both arms to
identical visible inputs, neutral response schema, prompt template, model
configuration and tool policy; the evaluator assertion bundle was bound to the
run-manifest hash **before** execution; the graded oracle values were fixed
before the run and excluded from the run tree. No holdout material was created
or touched; the nine new scenarios are visible public-development fixtures of
the same class as the retained three.

## Setup

| Item | Value |
| --- | --- |
| Scenarios | 12 visible-input fixtures: `PE-BND-001..004`, `PE-DTT-001..004`, `PE-STT-001..004` (3 retained CR-011 fixtures reused byte-identically + 9 new; 4 embed deliberate ambiguities: `PE-BND-004`, `PE-DTT-002`, `PE-DTT-004`, `PE-STT-004`) |
| Arm A | `QA-Master-current-HEAD` — packaged skill assets at commit `2c6fb290108a58d09a4f20c0835bea04bda38912` (SKILL.md, domains, work-protocol, design-methods, functional-api, requirements-review, structural-integration; 7 files) |
| Arm B | `upstream-skill-library-pinned-1a8c57c` — upstream `1a8c57c0e1c31b80aea5cb85dd830387dee09c9f` specialist skills: boundary-value, decision-table, state-transition SKILL.md + prompts (6 files; all bytes re-verified against the pinned SHA-256 values before the run) |
| Model | `gpt-6-astra`, reasoning effort medium, both arms identical; provider revision `NOT_AVAILABLE`, system baseline `UNVERIFIED`, seed `NOT_AVAILABLE` |
| Policy | read-only sandbox, ephemeral, all 15 features disabled (no tools, no shell, no network), `--ignore-user-config`, `--skip-git-repo-check` |
| Schedule | 12 pairs, AB/BA orders alternated per method (6 AB, 6 BA); both orders represented |
| Assertions | 24 pre-bound typed assertions (12 value checks + 12 source-provenance checks), `run_manifest_sha256 = 24f2511a8a6b44b7…`, `response_schema_sha256 = 3d7af8672381d897…` |
| Run root | `.qa-master/paired-pilot/observed-cr017/CR017-EXPANDED-PUBLIC-DEV-001` (2.3 MB, 351 files; integrity `INTACT`, completion `RECORDED` per `inspect_run`) |

## FACT: execution and pre-registered grading

- All 24 native calls completed (`pilot_status: COMPLETE`); every attempt
  `terminal_status: COMPLETED_PROCESS`, `output_outcome: COMPLETE`,
  `policy_outcome: NO_VIOLATION_OBSERVED`, `stop_reason: none`. Total wall
  time 880 s; per-call durations 20–59 s.
- Pre-registered exact grading (`grade_run` with the pre-bound bundle):

| Metric (24 assertions) | Arm A (QA Master) | Arm B (the upstream skill library) |
| --- | --- | --- |
| `SATISFIED` | **8** | 6 |
| `VIOLATED` | 16 | 18 |
| `UNSCORABLE` | 0 | 0 |

Per-check exact-grade matrix (A/B): BND-001 `SAT/VIOL`, BND-002 `SAT/SAT`,
BND-021 `VIOL/VIOL`, BND-031 `SAT/VIOL`, BND-032 `SAT/SAT`, BND-041 `SAT/SAT`,
BND-042 `VIOL/VIOL`, DTT-001..032 all `VIOL/VIOL` except DTT-002-both `VIOL`,
STT-012 `SAT/SAT`, STT-022 `SAT/SAT`, STT-001/002/021/031/032 `VIOL/VIOL`
where STT-001 means `AS-STT-001` etc.

## FACT: supplementary declared-rule semantic grading

The exact grader requires canonical structural equality, so a free-text label
difference (for example `STANDARD` vs `standard`, `<1000` vs `below 1000`,
`SCAN_SUCCESS` vs `successful scan`) fails an otherwise correct answer. Because
the nine new scenarios were authored for this run, several expected values
over-specified label tokens that the check questions did not dictate; this
penalised both arms equally. A supplementary grading layer was therefore
computed under rules declared in this report — applied identically to both
arms — and is reported separately from the pre-registered exact grades:

- R1 row-set semantics: lists of rule/transition rows are compared as sets
  after per-field normalization (case-fold; non-alphanumeric runs to one
  underscore).
- R2 numeric-string semantics: strings that parse as decimals compare
  numerically (`0.50` = `0.5`; `100.00` = `100`).
- R3 provenance subset: a fact-set observation passes when it contains the
  required fact IDs (extra cited visible facts are acceptable).
- R4 per-row field values must all match after R1–R3.

| Metric (24 checks) | Arm A | Arm B |
| --- | --- | --- |
| Exact (pre-registered) | **8** | 6 |
| Semantic (declared rules) | **13** | 11 |
| Both-differ (genuine misses) | 8 | 10 |

Genuine misses (both arms, after semantic rules): `PE-BND-002` both arms
omitted the precision-boundary rejects `100.00`-vs-`100` and `0.505` (both
returned only `0.49` and `100`, missing the two-decimal-precision rejection
candidates); `PE-DTT-001` and `PE-STT-001` (retained fixtures) both use richer
structures than the compact oracle objects. Arm-only differences: `PE-BND-001`
and `PE-BND-003` exact-pass for A while B added extra structural members /
missed the `998` interior neighbour; `PE-DTT-004` both arms listed the
`FREE/ADVANCED_REPORTING` denied row (a correct extra) and A also used
`ALLOWED` vs the expected `GRANTED` token.

## FACT: deliberate-ambiguity handling (embedded traps)

Four scenarios embed unspecified or conflicting facts. Both arms recorded gaps
instead of guessing on all four (no invented requirements observed):

| Scenario | Arm A gaps | Arm B gaps |
| --- | --- | --- |
| `PE-BND-004` (ambiguous "up to 5") | 2 (endpoint ambiguity + case-completion observability) | 2 (endpoint ambiguity + input audit) |
| `PE-DTT-002` (unknown customer type) | 2 (oracle missing + target observable missing) | 1 (undefined combination scope) |
| `PE-DTT-004` (trial EXPORT overlap) | 2 (source conflict + observables/setup) | 1 (no unconditional FREE/EXPORT outcome) |
| `PE-STT-004` (undefined events) | 3 (undefined outcomes + model scope + execution details) | 3 (undefined outcomes + side effects + incomplete matrix) |

Both arms behaved honestly; arm A's gap descriptions additionally and
consistently identify execution observability and setup/cleanup preconditions,
which arm B does not mention.

## INFERENCE: bounded observations

1. Under identical inputs, model configuration and tool policy, QA Master's
   packaged skill produced more pre-registered typed-assertion passes than the
   the pinned upstream skill library specialists on this 12-scenario public-development
   set (8 vs 6 exact; 13 vs 11 semantic). The margin is small (2 assertions of
   24 in both layers) and the set is visible development material — this is an
   observed difference on these fixtures, not a general quality verdict.
2. Both arms fail the retained-fixture structural-oracle assertions
   (`PE-DTT-001`, `PE-STT-001`) for representation-freedom reasons; those
   failures measure oracle strictness, not method failure.
3. Both arms missed the decimal-precision rejection candidates on
   `PE-BND-002`, suggesting the check wording (not the skills) drove that
   miss; a future oracle should phrase precision-rejection candidates
   explicitly.
4. Neither arm invented requirements on the four ambiguity scenarios; both
   recorded gaps. QA Master's gap set additionally covers execution
   observability and setup/cleanup preconditions on every scenario where the
   facts omitted them.
5. Single run, no seed: with no provider seed, per-call variation is
   unquantified; the observed margins are within plausible repeat variation
   and this run alone cannot support any statistical claim.

## RISK

- `EXPLORATORY_CONFIGURED_SAME_MODEL` only: provider revision and system
  baseline remain unverified; a strict comparison additionally requires the
  CR-015 verifier path (administrator trust registry + provider
  attestations), which does not exist yet.
- The semantic grading layer is a post-hoc supplementary analysis with rules
  declared after seeing the runs; it is reported for transparency and must
  not be cited as a pre-registered grade.
- 12 visible public-development scenarios with 1 attempt per pair; no holdout
  was used. Results on developer-visible material cannot be generalized.
- The author of this report is the same agent family that executed the run;
  the run's integrity facts are machine-recorded, but any future claim-grade
  comparison requires independent human review under `REQ-011`.

## Current conclusion

`NOT_ASSERTED`. The expanded paired comparison was executed end-to-end under
one manifest, graded by pre-bound typed assertions, and independently
inspected (`INTACT`/`RECORDED`). On this bounded, visible 12-scenario set with
identical model and policy, QA Master's current packaged skill passed more
typed assertions than the pinned upstream skill library specialists (8 vs 6 exact;
13 vs 11 under declared semantic rules), and both arms handled the embedded
ambiguities honestly. No superiority, quality, acceptance, Gate or release
claim is made: the evidence class is exploratory, the margin is small, the
material is developer-visible, and any comparative claim requires the strict
profile and human rating that remain `NOT_AVAILABLE`.
