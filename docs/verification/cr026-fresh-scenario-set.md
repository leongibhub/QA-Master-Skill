# CR-026 second fresh verification scenario set — pre-registration

- Classification: `PUBLIC_DEVELOPMENT` / `DRAFT_UNAPPROVED`
- Author: comparison researcher (same agent family as the CR-018/CR-021/CR-025
  instruction author — disclosed; the set is pre-registered before any run)
- Date: 2026-10-18
- Execution: blocked; no run has occurred against these bytes at registration
  time

## Purpose

Behavioural verification of the two CR-025 instruction upgrades on material
that was never a grading target of any prior run. The recorded CR-022/CR-024
fixtures must not be reused (TASK-108 boundary): third-round instructions were
shaped by those residuals, so verification on the same bytes would reward
tuning rather than measure generality.

## Design rules

1. **Fresh content domains** — none reuse the CR-022 semantics (library-loan,
   elevator, batch-job, gym-membership, invoice-quantity, shipping-speed,
   ticket-priority, discount-eligibility). New domains: order-fulfilment,
   document-review, payment-processing, support-ticket, team-subscription,
   print-page-count, delivery-options, request-routing.
2. **Targets the two CR-025 failure classes**:
   - **Exhaustive-universe provenance** — four state-transition scenarios each
     carry an "only states are …" universe fact and a valid-transition check
     whose `required_evidence_refs` includes that fact (the CR-024 residual:
     arm A omitted the `F-FS-0x1` universe fact 0/3 vs arm B 1/3).
   - **Explicit-scope discipline** — four invalid-candidate checks each ask for
     the invalid transition candidates *explicitly stated* by the facts and
     expect exactly the single stated invalid (the CR-022 residual: Q-FS-052
     over-generation, both arms 7 vs oracle 1).
   - Four control scenarios (two boundary, two decision-table) confirm the
     CR-018/CR-021 behaviours persist and the new clauses do not leak into
     unrelated check types.
3. **Oracle authoring corrections** (CR-020 audit, re-applied):
   - OA-1: every oracle row derivable from the visible facts alone;
   - OA-2: provenance checks name the specific invalid/conflict facts;
   - OA-3: no synthesized token where the facts supply one (event names are
     uppercase-underscore of the fact phrasing; `DEFINED`/`CONFLICT` are fixed
     by the question text — identical information for both arms);
   - OA-4: no numeric duplicates within one expected list.
4. **Same harness conditions** as CR-022/CR-024: one manifest, neutral
   response schema, model `gpt-6-astra`, no-tool policy, AB/BA alternation,
   arm B pinned `1a8c57c` byte-identical, arm A at the post-CR-025 HEAD.

## Scenario roster (8 scenarios, 16 checks)

| ID | Method | Domain | Failure class targeted | Checks |
|---|---|---|---|---|
| FS-01 | state_transition | Order-fulfilment lifecycle (ORDERED/PAID/SHIPPED/DELIVERED/CANCELLED) | universe provenance + explicit-scope | Q-FS-011, Q-FS-012 |
| FS-02 | state_transition | Document-review workflow (CREATED/SUBMITTED/IN_REVIEW/APPROVED/REJECTED) | universe provenance + explicit-scope | Q-FS-021, Q-FS-022 |
| FS-03 | state_transition | Payment-processing lifecycle (PENDING/AUTHORIZED/SETTLED/DECLINED) | universe provenance + explicit-scope | Q-FS-031, Q-FS-032 |
| FS-04 | state_transition | Support-ticket lifecycle (OPEN/IN_PROGRESS/RESOLVED/CLOSED) | universe provenance + explicit-scope | Q-FS-041, Q-FS-042 |
| FS-05 | boundary | Team-subscription seat-count bounds (whole-number) | control (interior neighbours + provenance) | Q-FS-051, Q-FS-052 |
| FS-06 | boundary | Print-job page-count bounds (whole-number) | control (interior neighbours + provenance) | Q-FS-061, Q-FS-062 |
| FS-07 | decision_table | Delivery-option rules with one excluded combination and one conflict | control (row-universe + engine vocabulary + provenance) | Q-FS-071, Q-FS-072 |
| FS-08 | decision_table | Request-routing priority matrix with undefined maintenance behaviour | control (row-universe + gap discipline + provenance) | Q-FS-081, Q-FS-082 |

Each state-transition scenario embeds a "final: no event leaves it" statement
alongside one explicitly-stated invalid transition, so an over-generating arm
that derives candidates from the terminal-state rule or from universe
completeness can be distinguished from an arm that lists only the stated item.

## Frozen bytes and validity-script commitment (executed)

The scenario/oracle bytes are frozen under
`.qa-master/paired-pilot/cr026-fresh-preparation-v1/` (local-only, gitignored,
as with all run material). The validity script
`cr026-oracle-validity-v1.py` was executed against those bytes and passed
**96/96 checks** covering OA-1 (evidence refs exist; checks exist; value_type
match; every value token derivable from facts text), OA-4 (no numeric
duplicates), the CR-025 target checks (valid-transition refs cite the "only
states" fact; invalid-candidate oracle is a single explicitly-stated row), and
contract-shape checks (title/request/scope non-empty text).

- `cr026-oracle-validity-v1.py` sha256:
  `2cd409a8ddb0ad422018fc8725ac06562a9a1424a6f740815066b4594a984d4c`
- `cr026-oracle-validity-v1.output.txt` sha256 (`ALL PASS`, 96/96):
  `497d462bd9fa2fd583b282b5cd6c97adf0a319c0866c101b2b57aaa8f73a8115`

## Run-preparation commitment (executed)

Run preparation built the manifest + assertion bundle + exclusions and
rehearsed the full pipeline with a TEST_DOUBLE launcher (zero model calls).

- `run_id`: `CR026-SECOND-FRESH-VERIFICATION-001`
- `run_manifest_sha256`: `095e2757e1d3bc46d900534e3c0d5eec562db344bef9139277980e821257e10e`
- `evaluator_commitment_sha256`: `94d5f2e248ee7be0b2c0cc75af9a3fba4d800f3b2417dafcb2296b00e494ee66`
- assertion bundle `cr026-assertions-v1.json` sha256:
  `ce489822ecb365b32f89af28a727c3bea193ce4aae2b8513291390b1a5ab028b`
- exclusions `cr026-exclusions-v1.json` sha256:
  `f70e9186713cb01b2bb511ebf6a0fe09063e1ea7ebf5dcd643beab574ab80f89`
- semantic rules `cr026-semantic-rules-v1.md` sha256 (identical to CR-022/CR-024,
  S1–S5, S6 not adopted):
  `89ea6b6242c57d21267350cf26087c97e5be1126187cf5a1cbcabe1cb77ada77`
- arm A commit: `b379c9418ae09295894f37bb660b6dd8b9921139` (post-CR-025)
- arm B commit: `1a8c57c0e1c31b80aea5cb85dd830387dee09c9f` (pinned, unchanged)
- model: `gpt-6-astra`; policy `NO_TOOL_USE`; runtime
  `codex-cli 0.163.0-alpha.10.2` (executable `896a0166b774037a`)
- TEST_DOUBLE rehearsal: 16/16 calls `COMPLETED_PROCESS`, 32/32 rehearsal
  assertions `SATISFIED`, integrity `INTACT`

## Non-goals

This set verifies the two CR-025 upgrade classes behaviourally on fresh
material. It is not a holdout (the author is not independent of the
instruction author), not a superiority claim, and not a substitute for the
Phase 3 human protocol. Tallies will be reported per failure class, per arm,
with the CR-022/CR-024 baseline classes for context only.
