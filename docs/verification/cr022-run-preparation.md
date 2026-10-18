# CR-022 run preparation record (v1, rehearsed, not executed)

- Classification: `PUBLIC_DEVELOPMENT` / `DRAFT_UNAPPROVED`
- Prepared by: comparison researcher (same agent family as the scenario and
  instruction author — disclosed)
- Date: 2026-10-16
- Status: **READY_TO_EXECUTE**, blocked only on the upstream model quota
  (recovery 2026-10-22). No model call has been made against these bytes.

## Materialization

- Preparation dir: `.qa-master/paired-pilot/cr022-run-preparation-v1/`
  (local-only, gitignored, as with all run material)
- Evaluator dir: `.qa-master/paired-pilot/cr022-evaluator/`
- Run id: `CR022-FRESH-VERIFICATION-001`
- Manifest validation: `VALIDATED_NOT_EXECUTED`

## Arms

- **Arm A** `QA-Master-post-CR021` — repository `QA-Master-PR2` at commit
  `fa84f489abe62cbf7cfe9185729fc480466a80d3` (post CR-018 + CR-021, including
  the R-01 family-consistency repair), 8 packaged instruction assets,
  entry asset `qa_master/skills/codex/SKILL.md`.
- **Arm B** `Awesome-QA-Skills-pinned-1a8c57c` — byte-identical to the
  CR-017/CR-019 pinned upstream arm (6 assets), copied from the CR-019
  preparation bytes and re-hashed.

## Contract bindings

| Artifact | Value |
|---|---|
| Manifest canonical digest (bound into the assertion bundle) | `c04969f85af81484b5a9f5cb1834841cb46d7b3674dd57335e1aef7ef292ca7f` (re-bound 2026-10-18 after a second bin rotation; was `d102763f…`) |
| Manifest file sha256 | `18c5fd76976178d2fc98a478a166e54c88ededbbb3992b4046ddeb0e0b89a070` (was `f94ef94c…`) |
| Evaluator commitment (`cr022-exclusions-v1.json`, canonical digest) | `9fe6b813b0b7698d9f56d6d60a08b5578a44f3b25d295b7fe35e72610dcc9b22` |
| Assertion bundle `cr022-assertions-v1.json` sha256 | `ca6e95e1277bc7ac134f8f2117c5661941eee603d5d969bcf208642b6fd39af7` (was `466b71ef…`; changed only because its bound `run_manifest_sha256` field re-pointed to the new manifest digest) |
| Pre-declared semantic rules `cr022-semantic-rules-v1.md` sha256 | `89ea6b6242c57d21267350cf26087c97e5be1126187cf5a1cbcabe1cb77ada77` |
| Oracle validity script output (`ALL PASS` 131/131) sha256 | `82164292cf6f24188582a98c1a5ad5f00bb84ae795f7a41bea2b89ff1830eab2` |

Runtime: codex-cli `0.163.0-alpha.10.2` (executable re-pinned after the
previous bin directory rotated; the CR-019 manifest's old path no longer
exists, so the CR-022 manifest pins the currently installed binary — same
model alias and reasoning effort, read-only sandbox, 16 features disabled as
before). The runtime block difference vs CR-019 is limited to the executable
identity; model, policy and timeout settings are unchanged.

Second bin rotation, 2026-10-18 (immediately before execution, quota
recovered): the `e78bad9887fa50cf` directory re-pinned in TASK-100 no longer
exists; the currently installed binary lives at
`896a0166b774037a\codex.exe` with sha256
`f6dbf48cb70f62649c645f26c87dc9bf84cc36986202dfad8e12fb5b8ca70312`. The
version string is **unchanged** (`codex-cli 0.163.0-alpha.10.2`); only the
binary identity (path + hash) differs. Model alias, reasoning effort,
read-only sandbox and all 16 disabled features are byte-identical to the
TASK-100 manifest. The manifest runtime block, its canonical digest and the
assertion bundle's bound `run_manifest_sha256` were re-derived and
re-validated (`VALIDATED_NOT_EXECUTED`). No scenario, oracle, arm asset,
semantic-rule or exclusion byte changed.

## TEST_DOUBLE full-pipeline rehearsal (zero model calls)

Executed through the private deterministic port
(`_run_pair_with_ports`, evidence class `TEST_DOUBLE`) with a shape-complete
fake launcher that answers every check with the oracle's expected value:

- 16/16 attempts `COMPLETED_PROCESS`; arm order A,B,B,A,A,B,B,A,A,B,B,A,A,B,B,A
  (AB/BA alternation preserved);
- envelope parsing, trace/final match, ledger and integrity checks all pass
  (`inspect_run` → `INTACT`);
- grading with the bound bundle: **36/36 `SATISFIED`** (18 assertions × 2 arms).

Interpretation: the manifest, schedule, materialization, response-contract
and assertion-binding plumbing is verified end-to-end. The rehearsal proves
nothing about model behaviour; it only proves the instrument works. The
rehearsal output tree lives under
`.qa-master/paired-pilot/cr022-dryrun/CR022-FRESH-VERIFICATION-001/` and its
grade report (`cr022-dryrun-grade-v1.json`, sha256
`8194223ae2a4a5b108c9d69e588062c0a0c9c85c8d23747b8bc3f1ebc6b00ce9`) is
retained as evidence.

The real run must target a fresh output root
(`observed-cr022/CR022-FRESH-VERIFICATION-001`), not the rehearsal root.

## Execution checklist (when quota recovers)

1. Re-verify the codex executable still matches the manifest hash (bin
   directories rotate; if rotated, update the runtime block and re-bind the
   assertion bundle, then re-validate). — **DONE 2026-10-18**: second rotation
   handled (see "Second bin rotation" note above).
2. `run_pair(PREP/'run-manifest.json', EVAL/'cr022-exclusions-v1.json',
   observed-cr022)` — do NOT reuse the dry-run root.
3. Grade with `EVAL/'cr022-assertions-v1.json'`; apply the pre-declared
   semantic rules S1–S5 (S6 explicitly not adopted) from
   `cr022-semantic-rules-v1.md`.
4. Report per upgrade class per arm per the pre-declared reporting plan;
   descriptive handling of FS-04/FS-07 gap behaviour; R-03a linkage
   disclosure carried in every report.
