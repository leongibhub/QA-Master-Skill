# Offline deterministic method design

Use this installed, local-only command for a finite design bundle:

```text
python -I "<skill-root>/scripts/qa.py" design --input bundle.json --output report.json
```

`design` accepts exactly one `--input` and one `--output`; abbreviations and
unknown options are rejected. The command reads only the input and atomically
replaces only the requested output. It never reads or changes Campaign state,
approves a requirement, opens source/oracle locators, runs tests, calls a
model, starts a process, uses a network, or writes an external system.

## Strict bundle contract

The top-level object has a non-empty string `project`, a `requirements` array,
and optional `design_models`. A requirement used by a model needs a unique
`id` and non-secret data; its dimension may be absent. If no requirement
supplies a non-empty dimension, the installed projection reports
`GUIDE_DIMENSION_NOT_SUPPLIED`. `approved: false`
is valid and remains unapproved. When present, `design_models` has exactly:

```json
{"schema_version":1,"source_refs":[],"oracle_refs":[],"models":[]}
```

There are at most 100 models. IDs are unique ASCII strings of 1–128 characters
matching `[A-Za-z0-9_.:-]+`. A source/oracle reference has exactly `id`,
`kind`, `locator`, and optional lowercase 64-hex `sha256`. A locator is a
non-secret relative opaque path-like identifier of at most 512 characters; no
URL, leading slash, backslash, `.`/`..`, whitespace, query, fragment, or drive
prefix is valid. Source kinds are `requirement`, `risk`, `contract`, `model`,
`guard`, `effect`, `change`, `defect`, `other`; oracle kinds are `valid`,
`invalid`, `outcome`, `transition`, `denial`, `effect`.

Each model has exactly `id`, `method`, `title`, `dimension`,
`requirement_ids`, `source_refs`, and `spec`. `method` is `boundary`,
`decision_table`, or `state_transition`; `dimension` is exactly one of
`functional`, `api`, `whitebox`, `integration`, `performance`, `load`,
`stress`, `stability`, `compatibility`, `negative`, `security`, `recovery`, or
`regression`; referenced requirements and source IDs must exist. Unknown fields, duplicate IDs/keys, JSON float/non-finite
values, and case-insensitive `password`, `token`, `cookie`, `private_key`,
`private-key`, or `privatekey` fields are rejected. Arrays treated as sets must
be unique. Top-level `source_refs`, `oracle_refs`, and `models` may be empty;
model `requirement_ids` and `source_refs` are non-empty. Other valid empty
arrays are stated by the method that owns them.

## Legacy requirement semantics and generic draft cases

The finite-method projection is separate from the existing generic campaign
draft projection. Each method model has its own `title`, but that title does
not supply a requirement description. To receive a meaningful generic draft
case and avoid the requirement-review findings `EMPTY_REQUIREMENT`,
`NO_PROVENANCE`, and `NO_ACCEPTANCE`, every requirement intended for generic
case design must provide all four non-empty fields:

```json
{
  "id": "REQ-X",
  "text": "The source-grounded behavior to review",
  "source": "declared/requirements.md",
  "acceptance": "The observable source-grounded outcome"
}
```

`id` is the trace identifier and must be unique. `text` is the behavior used
in the generic case title and steps. `source` is declared provenance only; the
helper does not open or verify it. `acceptance` is the generic expected
outcome, not a test result. A method candidate, model `title`, model source
reference, or method oracle does not fill any of these fields automatically.

Optional requirement fields accepted by the generic campaign route are:

- `approved`: only literal `true` removes the generic
  `REQUIREMENT_NOT_APPROVED` coverage gap. The helper never creates or promotes
  it; `false` may still produce a draft case when an oracle exists.
- `priority`: `P0`, `P1`, `P2`, or `P3`; an absent/invalid value becomes draft
  priority `P2`.
- `dimension`: one of the 13 dimensions listed above; absent defaults to
  `functional` for generic design. Installed guide selection uses only non-empty
  singular `dimension` values, so if none is supplied it reports
  `GUIDE_DIMENSION_NOT_SUPPLIED`; `dimensions` does not select a guide.
- `dimensions`: an optional explicit list of applicable dimensions. For each
  listed dimension, provide `oracles[dimension]`; the singular/primary
  `dimension` may use `acceptance` as its fallback.
- `oracles`: an optional object mapping dimensions to non-empty expected
  outcomes. It does not create an external assertion or execution evidence.
- `thresholds`: an optional object. A non-functional generic dimension needs
  `thresholds[dimension]`, otherwise it remains the
  `THRESHOLD_UNCONFIRMED` gap.
- `preconditions` and `test_data`: optional draft inputs. If omitted, the
  generic case records a pending environment/initial-state or test-data
  placeholder rather than inventing one.
- `origin`: when set to `code`, requires literal `approved: true` or the
  requirement review records `CODE_UNCONFIRMED`; it is not a way to infer a
  business requirement from implementation behavior.

The report keeps `test_cases` (generic draft cases and generic coverage gaps)
separate from `method_design` (finite candidates/obligations). Generic cases
carry `approval: DRAFT`; `workflow.execution` is `NOT_AUTHORIZED`.
`method_design`, `installed_design`, and the installed CLI summary carry
`DRAFT_UNAPPROVED` and `NOT_EXECUTED`. `case_review.pass` only means the
generated generic collection has no blocker-level structural finding; with
zero generic cases it is not a requirement-quality, case-completeness,
approval, execution, or overall product PASS. Read `requirement_review`,
`unresolved.design_gaps`, `coverage`, and `method_design.obligations` before
making a task-level draft deliverable.

## Boundary model

The `boundary` `spec` has exactly `numeric_type`, `origin`, `step`, `lower`,
`upper`, and `oracle_by_class`; decimal also requires `precision` and `scale`.
For `integer`, origin, step and bound values are JSON integers (not booleans),
have at most 34 significant digits, and `precision`/`scale` are forbidden. For
`decimal`, values are canonical plain decimal strings (no exponent, `+`,
redundant zero, or `-0`), `precision` is 1–34, and `scale` is 0–18. `step` is
positive; bounds are ordered and lie on the declared grid. Bounds are objects
with exactly `value` and boolean `inclusive`. `oracle_by_class` may contain
the keys `IN_DOMAIN`, `LOWER_INVALID`, `UPPER_INVALID`, `BOTH_INVALID`: the
first uses a `valid` oracle; the others use `invalid` or `denial`. An absent
needed class is the typed `BOUNDARY_ORACLE_MISSING` obligation.

## Decision-table model

The `decision_table` `spec` has exactly `conditions`, `constraints`, and
`rules`. `conditions` is non-empty; `constraints` and `rules` may be empty. A condition is `{"id": ID, "values": [SCALAR, ...]}`; scalar values
are unique string, boolean, or integer values, where `true`, `1`, and `"1"`
are distinct. The Cartesian product is at most 4,096.

Constraints are an implicit top-level `all`. A leaf is exactly
`{"op":"eq"|"ne","condition":ID,"value":SCALAR}` or
`{"op":"in"|"not_in","condition":ID,"values":[SCALAR,...]}`. A composite
is exactly `{"op":"all"|"any","items":[NODE,...]}`. Values must occur in
the named condition; nesting is at most 8 and there are at most 128 AST nodes.
A rule is exactly `{"id":ID,"when":{},"outcome_id":STRING,
"source_refs":[ID,...],"oracle_ref":ID|null}`. `when` is a partial condition
map (including an explicit empty default); a non-null rule oracle has kind
`outcome` or `effect`. Zero match, missing oracle, overlap, and conflict become
draft obligations rather than guessed candidates.

## State-transition model

The `state_transition` `spec` has exactly `states`, `initial_state`,
`triggers`, `transitions`, `closed_world`, and
`closed_world_deny_oracle_ref`. A state is exactly
`{"id":ID,"terminal":BOOLEAN,"source_refs":[ID,...]}`. There are at most 128
states, 512 explicit transitions, and 4,096 closed-world state/trigger pairs.

A transition is exactly `{"id":ID,"validity":"valid"|"invalid",
"from_state":ID,"to_state":ID|null,"trigger":ID,"guard_refs":[ID,...],
"effect_refs":[ID,...],"source_refs":[ID,...],"oracle_ref":ID|null}`.
Every trigger and state reference must exist. Guard refs have kind `guard` and
effect refs kind `effect`. A valid transition needs a non-null target, one or
more effects, and an oracle of kind `transition` or `effect`; an invalid one
has `to_state: null` and an oracle of kind `denial` when supplied. A terminal
state cannot have an outgoing valid transition. `guard_refs` may be empty;
`effect_refs` may be empty only for an invalid transition.

With `closed_world: true`, triggers are non-empty and
`closed_world_deny_oracle_ref` names a `denial` oracle; missing pairs become
guardless invalid draft checks. With `false`, that field is `null`; empty
triggers are allowed whenever there are no transition records. Guards
are structurally possible, never execution evidence. Duplicate logical
transitions, conflicts, unreachable states, and missing oracles are reported
as draft obligations where structurally valid.

## Output, gaps, and errors

Valid output is always `DRAFT_UNAPPROVED` and `NOT_EXECUTED`.
`method_design` contains deterministic `model_results`, `candidates`,
`obligations`, and counts. Candidates carry `approval: DRAFT`,
`evidence_state: PENDING`, and `validation_action: NOT_EXECUTED`.
`installed_design` has `schema_version`, `entry_point`, `status`, `execution`,
`state_access`, `external_writes`, `guides`, `source_mapping`, `gaps`, and
`method_output`. Each guide has `id`, `file`, stable installed `locator`, exact
packaged-byte `sha256`, `requirement_ids`, and `model_ids`. Each source mapping
has `origin` (`REQUIREMENT_SOURCE` or `DESIGN_MODEL_SOURCE`), `source_id`,
`kind`, `locator`, nullable `sha256`, `binding_state`, `requirement_ids`,
`model_ids`, `candidate_ids`, and `obligation_ids`. `DECLARED` means a locator
only and `DECLARED_DIGEST` means the caller supplied a digest; neither is
observed or verified. `method_output` has `present`, candidate/obligation ID
arrays, and both usable/executable-case claims set false.

Wrapper gaps are `METHOD_MODELS_NOT_SUPPLIED`, `METHOD_MODELS_EMPTY`,
`SOURCE_NOT_SUPPLIED`, `GUIDE_DIMENSION_NOT_SUPPLIED`, and
`METHOD_OUTPUT_REQUIRES_CASE_COMPLETION`. Existing strict method errors remain
stable `REJECTED` JSON with exit code 2; malformed bundle/input failures use
`INVALID_CAMPAIGN_INPUT`, filesystem failures use `CAMPAIGN_IO_ERROR`, and
parser failures emit no product JSON. A rejected call leaves an existing output
unchanged. Missing source, target, observable, setup, cleanup, or oracle facts
are typed gaps, not approval, execution, a rating, or a comparison conclusion.
Strict finite-model limit errors are `MODEL_LIMIT_EXCEEDED`,
`DECISION_LIMIT_EXCEEDED`, and `STATE_LIMIT_EXCEEDED`; structural reference,
schema, decimal, constraint, and state errors retain their stable existing
`DesignMethodError` code in the same `REJECTED` envelope.

The packaged `../examples/design-methods.json` constructs all three methods
using declared non-secret instructional bindings. It is not an approved
baseline and its locators need not exist in a fresh install.
