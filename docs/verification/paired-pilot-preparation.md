# Exploratory paired-pilot preparation record

- Change context: `CR-011`
- Planned runtime task: `TASK-044` (not claimed or run)
- Prepared: 2026-10-15
- Document State: `DRAFT`
- Evidence Status: `OBSERVED`
- Pilot status: `PREPARED_NOT_RUN`

## Scope

This record covers a local, ignored input snapshot for the three public-development
fixtures described in `DOC-PAIRED-PILOT-PROTOCOL-001 v1`. It does not materialize
participant prompts, call a model, execute tests, grade output, record a human
rating, compare participants, or make a product-quality claim.

The preparation utility is [prepare_pilot.py](../../.qa-master/paired-pilot/prepare_pilot.py).
It is ignored by Git together with all generated inputs under `.qa-master/`; no
product source, benchmark fixture, or upstream source was changed.

## FACT and EVIDENCE: generated snapshot

The utility copied the current PR2 public visible inputs and bound the exact current
participant contexts below. It downloaded six public comparator files from the fixed
Awesome QA Skills commit `1a8c57c0e1c31b80aea5cb85dd830387dee09c9f`, checking each
against the SHA-256 values recorded in the task protocol (external source read on
2026-10-15). The snapshot is at:

`D:\QA-Master-PR2\.qa-master\paired-pilot\cr011-public-development-preparation-v4-final-freeze`

| Artifact | SHA-256 |
| --- | --- |
| `run-manifest.json` | `1c05657cf897f8e599cea1893accb642e4e245e9c298e81b238c729f076f4a44` |
| `PREPARATION.json` | `3977e5a482628b99402cf66164eb1543975fab6a7b53f2d83c6064cd7429464b` |
| `evaluator-v4-final-freeze/cr011-public-development-exclusions-v1.json` | `d1324210d708e2038538b0e7660bd2696bf45f33c8d593bb3f48192b943ad68b` |
| `evaluator-v4-final-freeze/cr011-public-development-assertions-v1.json` | `2242945e3ef634d9510771b1616e8a3af83175095c236af0f2efd9427827a05a` |
| `prepare_pilot.py` | `af08df29d1a3d777e2b5ff1cbbbee47864b15217e2d9f6b3c732400414189bb4` |

The evaluator exclusions registry is outside the snapshot/manifest directory. It
contains only forbidden oracle file identifiers, oracle byte hashes, and a fixture
marker; no oracle bytes are part of either participant's context, visible input,
prompt template, or response schema.

### Bound participant contexts

| Arm | Source identity | Entry asset | Assets |
| --- | --- | --- | --- |
| A | `QA-Master-PR2` commit `96926a282739865f90bcedf9eab2ec6c5ada6176`, tree `803e1385ee6b06d4fd348472f164e574f1c6d108` | `qa_master/skills/codex/SKILL.md` | Current packaged entry, `domains.md`, `work-protocol.md`, and the original `functional-api.md`, `requirements-review.md`, and `structural-integration.md` guides. |
| B | `awesome-qa-skills` commit `1a8c57c0e1c31b80aea5cb85dd830387dee09c9f`, tree `1671168ec44e760e4a191468722f35e2ae5fe164` | `skills/en/testing-types/boundary-value-testing/SKILL.md` | The pinned boundary, decision-table, and state-transition `SKILL.md` files and their declared method prompts. |

This replaces the earlier proposal's high-level QA Master context reference with the
current canonical packaged entry asset and its directly needed original references
and professional guides. It makes the treatment reproducible; it does not establish
that the two contexts are equally comprehensive or fair in every respect.

### Runtime readback recorded without a model call

The preparation utility invoked only `codex.exe --version`. It bound:

- executable: `C:\Users\leon.wang\AppData\Local\OpenAI\Codex\bin\9614f1d9b40d9c4f\codex.exe`
- version: `codex-cli 0.162.0-alpha.17.2`
- executable SHA-256: `e98c516f1c8935789aabe9122ee7e05ec4c3efd1ba6acf179242e031c495b99e`
- planned model configuration: `gpt-6-astra`, reasoning effort `medium`
- provider revision: `NOT_AVAILABLE`; system baseline: `UNVERIFIED`
- planned isolation label: `WRITE_RESTRICTED_READ_SCOPE_UNVERIFIED`

The manifest schedules exactly three public scenarios with one AB/BA pair each, or
six calls if a separately authorized future run reaches all attempts. It retains the
`EXPLORATORY_CONFIGURED_SAME_MODEL` profile and has no retries.

### Native-value contract and bound assertion bundle

The snapshot is based on the final combined source freeze `96926a2`, which adds the
explicit 34-digit native-integer bound to the native-value repair. Current
`qa_master/_paired_contract.py` SHA-256 is
`4d8ada7cd03e62ce1bebca5865e878ef895c9fcf33847bb41e1495d92f3bd235`.
The exact manifest-bound prompt template is 1,048 bytes with SHA-256
`6fed7e3981b21fd9547c6838ff9c2150f6f862ad404bf7b229c2b9debd4fa4d2`;
the discriminator response schema is 4,596 bytes with SHA-256
`3d7af8672381d897b9096985db3a78204957e8d9cb01d52ecb18ef7188d09f57`.

The final assertion bundle is outside the snapshot and arm roots. It binds exactly
six public assertion rows to manifest-canonical SHA-256
`2126d4aa4ec433dc0fd3b9603edb6d55986e88f34f40feb73f091636cb46762b`
and the response-schema SHA-256 above. A direct structural check confirmed each
public assertion's ID, scenario/check relation, expected native typed value, required
evidence references, and oracle reference were preserved; this is
`ASSERTIONS_BOUND_NOT_GRADED`, not a grading result.

## FACT and EVIDENCE: non-executing validation

The utility called `validate_run_manifest` directly, then the public command:

```text
python -m qa_master.paired_evaluation validate .qa-master/paired-pilot/cr011-public-development-preparation-v4-final-freeze/run-manifest.json
```

Both produced `VALIDATED_NOT_EXECUTED` with manifest-canonical SHA-256
`2126d4aa4ec433dc0fd3b9603edb6d55986e88f34f40feb73f091636cb46762b`,
`claim_status: NOT_ASSERTED`, and `human_rating_status: NOT_EXECUTED`.
The `validate` path is documented in `qa_master.paired_evaluation` as process-free;
neither validation invoked its `run_pair` model-call path.

## FACT and EVIDENCE: Git-byte fixture provenance

The snapshot uses `git show HEAD:<path>` to extract raw committed blobs, avoiding
Windows checkout line-ending conversion. All six raw Git blobs at source commit
`96926a282739865f90bcedf9eab2ec6c5ada6176` match the inventory registered in
`DOC-PAIRED-PILOT-PROTOCOL-001 v1`.

| File | Git blob ID | Raw-blob SHA-256 |
| --- | --- | --- |
| `PE-BND-001.json` | `ce590c552358e6197aa26edf98f8f7ad3d89d9f2` | `e160e7212335d17aac0feecdff6201cbe3c5e4cea45c0e2c9f2748ee7258160c` |
| `PE-DTT-001.json` | `8e0e4b5a0e189e2cdd2e95b71828672dd4ad9d0d` | `8ef491bf4ded08583cd6831dc83df856b5d5304610b310a16a121744bc1bd543` |
| `PE-STT-001.json` | `e9c4dfc06dc6a14a7891c5037d3b38a82b41da69` | `b09f9e3772d608b825611569979d8841b310d9bf5f537216b4261e7e8a885689` |
| `PE-BND-001.public-oracle.json` | `3453bb7bd09599e58e543a596083db3ea1d28fd5` | `8f66bbe77e68e3163c871b265403771180546d359ef62a17d8752c3712e82ee8` |
| `PE-DTT-001.public-oracle.json` | `d6b85fb55ec0adcadc6347e2ba24ced9c4819984` | `913d8d7ea2743738628f4b264b8c1206fe1da3c966510e0ab0d6b3ec9bd1f0b6` |
| `PE-STT-001.public-oracle.json` | `9b661f1decf720b7bb4a295aad33df5ba1f19e7a` | `4857508b014d972aee8cd36d863682a199960e0efe84dcf27f8b4f24b5105dd5` |

Plain working-tree reads on this Windows host returned CRLF checkout bytes and thus
different SHA-256 values. That is a representation difference, not a new fixture
version. The preparation therefore binds the raw Git blobs and records their commit
and blob IDs in `PREPARATION.json`. The frozen public-oracle v1 was not modified.

## INFERENCE

The generated snapshot is structurally runnable by the current manifest validator
and binds the registered fixture bytes. It is still `PREPARED_NOT_RUN`: runtime
dependencies and a separate claimed execution task control any model launch.

## RISK

- `--sandbox read-only`, feature-disable requests, and an empty external current
  directory do not demonstrate filesystem-read or network isolation.
- Unknown provider revision and unverified system baseline prohibit a strict or
  superiority interpretation even after an exploratory run.
- The snapshot's public fixtures are development material, not a holdout.

## FACT: separate concurrent-state repair

The previously observed concurrent-state initialization failure is a separate
`TASK-050`/`BUG-013` repair, committed as `ba7c49f`. Its independent verification
record reports bounded focused and selected-regression tests passing. It is not a
paired-pilot result and is not used as a comparison, grade, or release conclusion.

## RECOMMENDATION

Before claiming or running `TASK-044`, rehash the ignored snapshot and native
executable, then confirm the existing independent-test and formal-review
dependencies (`TASK-042`, then `TASK-043`). They remain prerequisites for any model
call.
