# DES-055 — Installed deterministic method design path

- Artifact ID: `DES-055`
- Document State: `DRAFT`
- Evaluation State: `IN_REVIEW`
- Evidence Status: `PENDING`
- Change: `CR-013`
- Work: `TASK-055` / `work-17207978d5da4cb3b951cdd42ab3f757`
- Date: 2026-10-15
- Requirements: `REQ-025` Phase 1, `NFR-009`; preserves `REQ-013`–`REQ-018`

## 1. Decision and scope

The installed QA Master Skill shall expose one offline command:

```text
python -I <skill-root>/scripts/qa.py design --input <bundle.json> --output <report.json>
```

The command uses the existing strict campaign bundle, `campaign_cli` loader,
campaign preparation and deterministic `design_methods` engine. It adds one
installed-workflow metadata projection to the otherwise existing campaign
report. It does not introduce a second method schema, an application-state
transition, a model call, a runner, an adapter or an enterprise integration.

This slice produces deterministic draft method candidates, obligations and
their declared source/guide mapping. A candidate is not by itself proof of a
usable or executable test case. A Codex task using the Skill must still read
the selected guide and supplied source, then deliver a reviewable case or a
typed gap. Independent acceptance proves the helper and that task-level use as
separate facts.

Phase 2 semantic scoring and Phase 3 comparison/human judgement in `REQ-025`
remain outside this design. No output is a rating, aggregate, winner,
superiority statement, human approval, Gate result or executed-test result.

## 2. Existing components and compatibility boundary

`codex_skill.skill_bundle()` already copies all top-level `qa_master/*.py`, the
professional guides and `scripts/qa.py` into a self-contained install. Thus
`campaign_cli.py` and `design_methods.py` are present, but `qa_master.__main__`
does not route to them and the installed reference does not document them.

The change is additive:

- `qa_master.__main__` adds the `design` parser and dispatches it before any
  `CampaignApplicationService` load or mutation;
- `campaign_cli.write_campaign` gains an optional installed projection mode;
  omission preserves the current direct `python -m qa_master.campaign_cli`
  report and summary exactly;
- `codex_skill.skill_bundle()` keeps its current recursive resource packaging;
  the implementation adds the reference and example below under the canonical
  Skill resource tree, so they are included and hashed by the existing install
  manifest;
- the canonical Campaign application and schema, legacy approval assertions,
  CR-011 paired-run evidence and grader remain unchanged.

The global `--state` parser option may remain accepted for CLI compatibility,
but `design` never resolves, reads, creates or writes that path. Its report
records `state_access: NONE`.

## 3. Command and API contracts

### 3.1 CLI grammar and dispatch

`design` has exactly two required options, each occurring once:

```text
design --input FILE --output FILE
```

Unknown options, missing values or duplicate options are parser errors and
must not create or replace the output. Dispatch is in-process; it does not
launch `python -m`, change `PYTHONPATH`, or depend on the repository checkout.

The installed dispatch calls:

```python
write_campaign(input_path, output_path, installed_projection=True)
```

The new keyword is optional and defaults to `False`. No public callback or
guide-root injection is added. `True` is used only by the installed `design`
command. All file parsing, size limits, method validation, report preparation,
temporary-file handling and atomic replacement remain owned by
`campaign_cli.write_campaign`.

Successful stdout remains a secret-safe JSON summary. In installed mode it
contains only `project`, counts, `status: DRAFT_UNAPPROVED`,
`execution: NOT_EXECUTED`, and the requested output path. It never prints a
source locator, guide body, input value or exception representation.

### 3.2 Input

The input is the existing campaign JSON bundle from DES-033. The canonical
file loader remains `design_methods.load_bundle_json`; its duplicate-key,
UTF-8, non-finite-number, sensitive-shaped-key and method-model rules are not
redefined here. Maximum input size remains 5,000,000 bytes.

For a method-enabled result, `design_models` supplies exact source/oracle refs
and finite models. Requirement records remain unapproved unless the caller
explicitly supplied their existing legacy `approved` field. The packaged
example must use `approved: false`; neither the wrapper nor the engine changes
that value. A caller never has to claim approval to obtain method candidates.

The command does not open source/oracle locators. They are declared bindings,
not verified file contents. A malformed, unknown or incompatible non-null
reference remains the existing strict `DesignMethodError` rejection. Missing
optional semantic facts remain method obligations or installed-workflow gaps;
invalid structure is not downgraded to a gap.

### 3.3 Guide selection

Installed-mode guide selection is deterministic and uses the packaged guide
registry:

1. collect the sorted unique nonempty `dimension` strings from requirements;
2. if none exist, select no guide and add `GUIDE_DIMENSION_NOT_SUPPLIED`;
3. otherwise call `select_skills(intent="design", dimensions=dimensions,
   risk=None)`;
4. retain only registry-returned guide metadata and gaps; never load a guide
   from the input bundle;
5. replace each environment-specific absolute `path` with the stable installed
   locator `scripts/qa_master/skills/professional/<file>` and SHA-256 of the
   exact packaged guide bytes.

Each guide row is sorted by `id` and records the requirement IDs and method
model IDs whose dimensions intersect that guide's declared dimensions. Guide
selection means "applicable instruction was identified". It does not prove a
model read or followed the guide; that is a separate task-level acceptance
fact.

## 4. Installed-workflow output projection

When `installed_projection=True`, add exactly one top-level member to the
existing campaign report:

```json
{
  "installed_design": {
    "schema_version": 1,
    "entry_point": "scripts/qa.py design",
    "status": "DRAFT_UNAPPROVED",
    "execution": "NOT_EXECUTED",
    "state_access": "NONE",
    "external_writes": "REQUESTED_OUTPUT_ONLY",
    "guides": [
      {
        "id": "functional-api-design",
        "file": "functional-api.md",
        "locator": "scripts/qa_master/skills/professional/functional-api.md",
        "sha256": "<lowercase-64-hex>",
        "requirement_ids": ["REQ-X"],
        "model_ids": ["DM-X"]
      }
    ],
    "source_mapping": [],
    "gaps": [],
    "method_output": {
      "present": true,
      "candidate_ids": [],
      "obligation_ids": [],
      "usable_case_claim": false,
      "executable_case_claim": false
    }
  }
}
```

All arrays use stable ID ordering. `method_output` contains IDs already present
under `method_design`; it does not duplicate candidate or obligation bodies.
When `design_models` is absent, `present` is false and both ID arrays are empty.

`source_mapping` is one sorted row per declared source, with this exact shape:

```json
{
  "origin": "REQUIREMENT_SOURCE",
  "source_id": "REQ-X",
  "kind": "requirement",
  "locator": "requirements/spec.md",
  "sha256": null,
  "binding_state": "DECLARED",
  "requirement_ids": ["REQ-X"],
  "model_ids": [],
  "candidate_ids": [],
  "obligation_ids": []
}
```

`origin` is `REQUIREMENT_SOURCE` for a nonempty requirement `source` string or
`DESIGN_MODEL_SOURCE` for a resolved `design_models.source_refs` object.
Method-source rows preserve its `kind`, `locator` and optional declared digest.
`binding_state` is `DECLARED_DIGEST` when a digest is present and `DECLARED`
otherwise; neither means observed or verified. `source_id` is the requirement
ID for requirement-source rows and the ref ID for method-source rows.

The four ID arrays are derived only by following explicit requirement/model,
candidate and obligation links already in the report. No text matching or
semantic inference is allowed. Duplicate logical rows are rejected during
projection rather than silently merged. Locators are retained only in the
requested local report and are subject to the existing non-secret input rule.

### 4.1 Typed gaps

The projection may add only these wrapper-level gap codes:

| Code | Condition |
|---|---|
| `METHOD_MODELS_NOT_SUPPLIED` | top-level `design_models` is absent |
| `METHOD_MODELS_EMPTY` | valid `design_models.models` is empty |
| `SOURCE_NOT_SUPPLIED` | a requirement lacks a nonempty `source` and no resolved method source maps to it |
| `GUIDE_DIMENSION_NOT_SUPPLIED` | no nonempty requirement dimension exists |
| `METHOD_OUTPUT_REQUIRES_CASE_COMPLETION` | method candidates or obligations exist; task-level usable-case/gap completion has not been assessed |

Registry gap objects such as `GUIDE_FILE_MISSING`, `GUIDE_METADATA_INVALID`,
`UNKNOWN_DIMENSION` and `NO_MATCHING_BUNDLED_GUIDE` are retained with their
existing schema. A missing source/model is therefore visible without becoming
approval. A valid input with these gaps still produces a draft report. A
malformed supplied model/source/oracle remains a whole-call rejection.

## 5. Skill reference and example

The installed bundle adds:

- `references/design-methods.md`: command grammar, the strict DES-033 input
  contract, output fields, gap/error meanings and the draft/no-execution
  boundary;
- `examples/design-methods.json`: a non-secret finite example with
  `approved: false`, at least one valid `design_models` model, explicit source
  and oracle references, and no credentials, environment endpoint or approval
  receipt.

`SKILL.md` and `references/work-protocol.md` direct an applicable design task
to: inspect supplied source; choose the applicable packaged guide; create the
strict bundle without inventing missing facts; invoke the single command;
review `method_design` and `installed_design`; then produce a usable draft case
for each determinable obligation or a typed gap. The instruction must say that
method candidates are inputs to this task-level deliverable, not automatic
proof that usable or executable cases exist.

The example is instructional data only. Its `source` and ref locators need not
exist in a fresh install because the engine does not read them; the reference
labels them declared example bindings. Acceptance uses separate fixtures with
actual visible source bytes.

## 6. Errors, reliability and data lifecycle

The installed route preserves campaign CLI error contracts:

- `DesignMethodError.code` → `{"status":"REJECTED","error":CODE}`, exit 2;
- JSON/bundle/type/key failure → `INVALID_CAMPAIGN_INPUT`, exit 2;
- filesystem failure → `CAMPAIGN_IO_ERROR`, exit 2;
- argparse failure → exit 2 without product JSON.

Validation and complete report construction precede temporary-file creation.
Any failure leaves a pre-existing output byte-identical and removes only the
command's own temporary file. Input and output resolving to the same file is
rejected. Success atomically replaces only the requested local output. No
Campaign state, approval record, handoff, external system, network endpoint,
process runner or test result is read or written.

The existing method limits bound CPU and result growth. Guide selection scans
the fixed six packaged files and source mapping is linear in requirements,
models, candidates and obligations, all within existing campaign/method caps.
This is a local bounded-design claim, not latency or throughput evidence.

Input/output retention and deletion are caller-managed. Installer updates use
the existing content-addressed manifest and backup/recovery behavior. Rollback
uses the prior installed bundle; direct `campaign_cli` users retain the old
shape because installed projection defaults off.

## 7. Security, privacy and authority

The command runs under the invoking user's filesystem authority. It accepts
only local non-secret planning data, performs no network or subprocess call,
and has no credential provider. It does not validate that a locator is an
authorized enterprise source or that a declared digest is truthful. The
task-level user remains responsible for supplying permitted source material.

`approved: true` remains only legacy input data and is never created or
promoted here. No guide, method candidate, exit code, file hash or atomic write
is trusted human approval. `execution` remains `NOT_EXECUTED`; `test_cases`,
`method_design.candidates`, and wrapper metadata do not authorize testing or
external writes.

## 8. Acceptance and negative tests

Independent testing freezes a wheel/source revision and records actual hashes.
The helper tests and representative installed task are distinct evidence.

| ID | Acceptance oracle |
|---|---|
| `TC-IMD-001` | From an unrelated working directory, a fresh installed Skill runs `python -I .../scripts/qa.py design` without repo, `PYTHONPATH` or external package and produces a parseable report. |
| `TC-IMD-002` | Valid model input reaches all three existing methods as applicable; engine candidate/obligation IDs equal direct campaign results and the installed projection maps them without changing their bodies. |
| `TC-IMD-003` | Absent and empty models produce the exact wrapper gaps; `approved: false` stays false and method candidates remain `DRAFT`/`PENDING`/`NOT_EXECUTED`. |
| `TC-IMD-004` | Missing source produces `SOURCE_NOT_SUPPLIED`; malformed, unknown or incompatible supplied refs produce the existing strict rejection and no output replacement. |
| `TC-IMD-005` | Guide IDs, relative locators and hashes match exact installed bytes; selected requirement/model IDs follow dimension intersection and no absolute install path appears. |
| `TC-IMD-006` | Duplicate JSON keys, non-finite values, over-limit input, same input/output, unknown CLI options and read/write failures exit 2; an existing sentinel output remains byte-identical and no owned temp file remains. |
| `TC-IMD-007` | Network, subprocess/runner, adapter, Campaign-state and approval-mutation sentinels observe zero calls; only the requested successful output changes. |
| `TC-IMD-008` | Same installed bytes and input bytes produce byte-identical report bytes; a changed input or packaged guide changes its bound digest/result while prior output is not rewritten in place by inspection. |
| `TC-IMD-009` | Direct `python -m qa_master.campaign_cli` with installed mode omitted retains existing report/summary compatibility for bundles both with and without `design_models`. |
| `TC-IMD-010` | An independent offline Codex task reads the packaged Skill/reference and applicable guide, cites supplied source IDs, invokes the command, and turns each in-scope method obligation into a usable draft case or explicit typed gap. Helper output alone cannot satisfy this test. |
| `TC-IMD-011` | Without target/observable/cleanup facts, the task labels cases draft/static or blocked by a typed gap and does not invent an API, UI, rejection signal, side effect or execution result. |
| `TC-IMD-012` | Output and evidence contain no rating, aggregate, fairness, winner, superiority, human approval, Gate decision or executed-test claim. |

`TC-IMD-010` requires an actual separately authorized installed-Skill task and
retained artifact/source hashes. A unit test that calls the helper, a mocked
model, or the CR-011 six-call pilot cannot substitute for it. Model narrative
quality and human preference remain `NOT_EXECUTED`.

## 9. Minimal implementation handoff

1. **TASK-056 — installed route and packaged assets:** own
   `qa_master/__main__.py`, the minimal optional projection in
   `qa_master/campaign_cli.py`, canonical Skill instructions/reference/example,
   and developer tests. Do not change Campaign state, method algorithms,
   paired runtime or evaluator.
2. **Independent test task:** own black-box fresh-wheel/`python -I` tests,
   evaluator-owned fixtures, sentinels and the separately authorized
   representative offline task evidence. It must not reuse developer assertions
   as its oracle.
3. **Independent review task:** check source-to-guide-to-method mapping,
   compatibility, authority boundaries, artifact hashes and unresolved findings.
4. **Governance update:** add the final DES/TASK/test/evidence links to the RTM.
   This DRAFT design and future agent review do not create a Gate decision.

Suggested future evidence IDs are
`EVD-INSTALLED-METHOD-HELPER-001` for the isolated deterministic helper and
`EVD-INSTALLED-METHOD-TASK-001` for the representative task-level artifact.
Suggested handoff document ID, if governance requires a separate record, is
`DOC-INSTALLED-METHOD-DESIGN-HANDOFF-001`.

## 10. Alternatives and rationale

- **Run `campaign_cli.py` directly from the installed tree:** rejected because
  package-relative imports are not a supported user entry and it creates a
  second undocumented command.
- **Add method actions to canonical Campaign state:** rejected because the
  operation is a stateless draft and must not acquire approval/execution
  authority or schema migration risk.
- **Generate cases with a model inside the helper:** rejected because Phase 1
  must work offline and deterministic method synthesis must remain separately
  assessable from task-level narrative quality.
- **Merge method candidates into legacy `test_cases`:** rejected by ADR-004;
  it changes established output semantics and hides the finite-model
  denominator.
- **Treat missing source/model as invalid input:** rejected for absent optional
  context because REQ-025 requires an honest typed gap. Structurally invalid
  supplied context still fails closed.

No new ADR is required: the material choices reuse ADR-004's separate,
deterministic method projection and ADR-001's canonical-state boundary. This
document resolves only the previously delegated installed wrapper, mapping and
acceptance details.

## 11. Unverified items

Implementation, fresh-wheel execution, side-effect sentinels, deterministic
readback, representative installed Codex task, independent test, independent
review, human assessment and any Gate decision are `PENDING` or
`NOT_EXECUTED`. The design does not establish actual product superiority.
