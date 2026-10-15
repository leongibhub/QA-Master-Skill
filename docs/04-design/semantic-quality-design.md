# DES-060 — Process-free semantic quality evaluator

- Artifact ID: `DES-060`
- Document State: `DRAFT`
- Evaluation State: `IN_REVIEW`
- Evidence Status: `PENDING`
- Change: `CR-013`
- Work: `TASK-060` / `work-0448b9e2e7f841fa98840a0b355278e6`
- Date: 2026-10-15
- Requirements: `REQ-025` v1, `NFR-009` v1
- Inputs: `DOC-SEMANTIC-QUALITY-CONTRACT-001`, `DES-055`, and `TASK-053` /
  `DOC-PAIRED-PILOT-SEMANTIC-AUDIT-001`

## 1. Decision and limits

Add one dependency-free module, `qa_master.semantic_quality`, with three local,
process-free operations: `validate`, `evaluate`, and `inspect`. It evaluates a
retained QA response against an evaluator-owned, published bundle of visible
facts, semantic obligations, category applicability and a fixed case/gap
projection. It writes a new content-addressed result directory; it never edits
the response, bundle, source material or any earlier evaluation.

This design implements the deterministic portion of Phase 2 only. It reports
four independent dimensions for every obligation: `SHAPE`, `SEMANTIC`,
`USABILITY`, and `PROVENANCE`. It emits no aggregate, ratio, score, rating,
winner, fairness, superiority, approval, acceptance, release or Gate decision.
It neither calls a model nor executes a test. `DESIGN_READY` remains draft
reviewability and cannot become an executable-case or business-result claim.

`qa_master.paired_evaluation.grade_run`, its schemas, CR-011 raw responses,
public oracle, retained grade and assertion statuses remain byte-for-byte
historical evidence. The new evaluator does not import a legacy grade as a
semantic result or write beneath a legacy run root.

## 2. Component boundary and public API

The module owns strict loading, registered projection parsing, normalization,
evaluation, atomic publication and result reconciliation. Its public Python API
is:

```python
validate_bundle(bundle_path: str | Path) -> dict
evaluate_bundle(bundle_path: str | Path, output_root: str | Path) -> dict
inspect_result(result_root: str | Path) -> dict
```

The matching CLI is:

```text
python -m qa_master.semantic_quality validate --bundle BUNDLE
python -m qa_master.semantic_quality evaluate --bundle BUNDLE --output-root DIR
python -m qa_master.semantic_quality inspect --result-root RESULT_DIR
```

`validate` and `inspect` never create or modify a file. `evaluate` creates one
new child directory under `output-root`. No command accepts a Python callback,
custom normalizer, model launcher, network adapter, state path, enterprise
credential, human rating, threshold, weight or winner rule.

Successful `validate` returns `VALIDATED_NOT_EVALUATED`. Successful `evaluate`
returns the result ID, profile path and `EVALUATED_DRAFT_ONLY`. Successful
`inspect` returns `INTACT`, `MISSING`, `MISMATCH`, `UNDECLARED`, or
`INCOMPLETE`. These operation statuses are evidence-processing facts, never
quality outcomes.

## 3. Strict data rules and bounds

All controlled JSON is UTF-8, rejects duplicate keys, floats, `NaN`/infinity,
unpaired surrogates and integers over 34 magnitude digits, and canonicalizes
with sorted object keys, compact separators and unescaped Unicode scalar
values. Boolean is distinct from integer. Decimal remains canonical plain
decimal text. Identifiers use `[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}`. Relative
locators use the existing controlled path grammar and reject absolute, drive,
UNC, traversal, symlink and reparse paths.

The bundle, supplied response and each referenced source/projection artifact
are at most 2 MiB. Schema v1 has these further limits:

| Item | Limit |
|---|---:|
| source descriptors and visible facts | 256 each |
| obligations and normalized observations | 256 each |
| cases and gaps | 256 each |
| IDs or references in one row | 64 |
| claims in one case section | 64 |
| text member | 20,000 Unicode code points |
| typed JSON value | depth 16 and 4,096 nodes |
| profile rows | exactly `4 × obligation_count`, at most 1,024 |
| all available referenced source bytes combined | 4 MiB |
| complete staged result | 16 MiB |

Counts are checked before quadratic joins. Implementations build ID indexes and
evaluate in `O(facts + obligations + observations + cases + gaps + references)`
time and bounded memory. Limits are safety/capacity contracts, not performance
or availability claims.

Controlled objects recursively reject secret-shaped keys and the claim keys
`rating`, `score`, `winner`, `quality_grade`, `approval`, `execution_result`,
and `superiority`. String values are not rejected by keyword substring. The
byte-level secret scanner used by the local evidence runtime runs before raw
bytes are retained; a match rejects evaluation without publishing a result.

## 4. Evaluator bundle schema

The bundle has exactly:

```json
{
  "schema_version": 1,
  "evaluation_id": "SQE-DEV-001",
  "fixture_class": "PUBLIC_DEVELOPMENT",
  "created_at_utc": "2026-10-15T00:00:00Z",
  "contract": {
    "contract_id": "semantic-quality-v1",
    "contract_sha256": "<sha256>",
    "projection_id": "qa-quality-case-gap-v1",
    "projection_sha256": "<sha256>",
    "normalizer_id": "qa-quality-normalizer-v1",
    "normalizer_sha256": "<sha256>",
    "result_schema_id": "semantic-quality-result-v1",
    "result_schema_sha256": "<sha256>",
    "secret_scanner_id": "qa-quality-secret-scanner-v1",
    "secret_scanner_sha256": "<sha256>"
  },
  "response": {
    "state": "PRESENT",
    "source_path": "inputs/response.json",
    "byte_count": 123,
    "sha256": "<sha256>",
    "declared_projection_id": "qa-quality-case-gap-v1"
  },
  "sources": [],
  "facts": [],
  "category_applicability": [],
  "obligations": []
}
```

`fixture_class` is `PUBLIC_DEVELOPMENT`, `INDEPENDENT_HOLDOUT`, or
`PRODUCT_TEST`. The evaluator reports this declared class and never promotes
development data to a holdout. Holdout creation, location and release are
outside this module.

`created_at_utc` is whole-second RFC 3339 UTC with literal `Z`; it is retained
metadata and never read from the host clock for identity. Contract digests must
equal the module's fixed shipped artifacts. Callers cannot substitute a schema,
scanner or executable normalizer. The schema-v1 registry contains exactly two
projection IDs: supported `qa-quality-case-gap-v1` and known legacy
`paired-neutral-envelope-v1`. Any other ID rejects the bundle with
`UNKNOWN_PROJECTION`; it cannot publish a profile without registered bytes.
Either registered ID with the wrong digest is `PROJECTION_BINDING_MISMATCH` and
rejects the bundle.

### 4.1 Response descriptor

For `PRESENT`, all descriptor members shown above are required and the local
file bytes must match length and digest. For `ABSENT`, `source_path`,
`byte_count`, and `sha256` are null while `declared_projection_id` remains a
nonempty ID. Other combinations are invalid bundle structure. A missing or
changed file for a `PRESENT` descriptor is an input-integrity failure, not an
`ABSENT` response and does not publish a profile.

The response descriptor is relative to the bundle directory. Inputs and the
output directory cannot contain one another. The evaluator never resolves a
network or enterprise locator.

### 4.2 Sources and visible facts

A source descriptor has exactly:

```json
{
  "id": "SRC-1",
  "kind": "requirement",
  "state": "AVAILABLE",
  "locator": "source/requirements.json",
  "sha256": "<sha256>"
}
```

`kind` is `requirement`, `risk`, `contract`, `model`, `guard`, `effect`,
`change`, `defect`, `evidence`, or `other`. `state` is `AVAILABLE` or
`NOT_AVAILABLE`. `AVAILABLE` requires a controlled relative locator and
SHA-256. The bundle binds the descriptor and digest but the evaluator does not
interpret the referenced source document. `NOT_AVAILABLE` requires null
locator/digest and cannot be referenced by a visible fact. Conflict is not a
source-descriptor state: an obligation declares `oracle_state: CONFLICT` and
references at least two unequal facts from at least two `AVAILABLE` sources.

A visible fact has exactly `id`, `source_ids`, `category`, `value_type`,
`value`, and `scope`. It may reference only `AVAILABLE` sources. `value_type`
and native value follow the current strict typed-value contract: `BOOLEAN`,
`INTEGER`, `DECIMAL`, `STRING`, `STRING_SET`, or `JSON`. `scope` is a nonempty
published explanation; it is evidence, not an executable expression.

Facts never use `NOT_AVAILABLE` as a value. There is a critical distinction:

- the visible source was inspected and explicitly lacks a required oracle:
  obligation `oracle_state: ORACLE_MISSING`, yielding `ORACLE_MISSING`;
- the source or response cannot be obtained/interpreted: obligation
  `oracle_state: UNSCORABLE`, yielding `UNSCORABLE`;
- source facts conflict: `oracle_state: CONFLICT`, yielding `UNSCORABLE` for
  semantic truth while an honest conflict gap may satisfy provenance.

### 4.3 Category applicability

The array contains exactly one row for each category, sorted in this order:

1. `REQUIREMENTS_CONFLICTS`
2. `METHOD_SELECTION`
3. `FUNCTIONAL_API_INTEGRATION`
4. `SECURITY_SCOPE_AUTHORITY`
5. `RECOVERY_REGRESSION`
6. `NON_FUNCTIONAL`
7. `DELIVERABLE_USABILITY`

Each row has `category`, `state`, `reason`, `source_ids`, and `fact_ids`.
`state` is
`APPLICABLE`, `NOT_APPLICABLE`, `ORACLE_MISSING`, or `UNSCORABLE`. The bundle
validator enforces this complete partition:

| State | Exact obligation invariant | Reason |
|---|---|---|
| `APPLICABLE` | at least one obligation in the category and at least one has `oracle_state=DETERMINATE` | null |
| `ORACLE_MISSING` | at least one obligation and every obligation has `oracle_state=ORACLE_MISSING` | nonempty and source-linked |
| `UNSCORABLE` | at least one obligation, none is `DETERMINATE`, and at least one is `CONFLICT` or `UNSCORABLE`; other obligations may be `ORACLE_MISSING` | nonempty and source-linked |
| `NOT_APPLICABLE` | no obligation in the category | nonempty and source-linked |

Every obligation names one registered category and every registered category
appears exactly once. For a category with obligations, `source_ids` and
`fact_ids` are the sorted unique unions of the corresponding obligation
bindings. For `NOT_APPLICABLE`, `source_ids` is nonempty and `fact_ids` is a
possibly empty list of same-category facts supporting the reason. Every listed
fact belongs to a listed source. Any other category/state/obligation or linkage
combination rejects the bundle with `CATEGORY_OBLIGATION_MISMATCH`. No category
is silently omitted.
The array is an applicability register, not a score or coverage percentage.

### 4.4 Obligations and source-bound comparison

Every obligation has exactly:

```json
{
  "id": "OB-1",
  "category": "FUNCTIONAL_API_INTEGRATION",
  "interpretation": "Published rule stated for reviewers",
  "source_ids": ["SRC-1"],
  "source_fact_ids": ["F-1"],
  "oracle_state": "DETERMINATE",
  "required_gap_reason": null,
  "check_id": "CHECK-1",
  "operator": "EQUALS",
  "expected_fact_ids": ["F-1"],
  "allowed_readiness": ["DESIGN_READY"],
  "case_required": true
}
```

`oracle_state` is `DETERMINATE`, `ORACLE_MISSING`, `CONFLICT`, or
`UNSCORABLE`. Its members obey this exact partition:

| Oracle state | `source_ids` | `check_id` / `operator` | `expected_fact_ids` | `required_gap_reason` |
|---|---|---|---|---|
| `DETERMINATE` | nonempty, all `AVAILABLE`; includes every source behind bound facts | unique non-null check plus `EQUALS` or `ONE_OF` | one or more available facts as required by the operator | null |
| `ORACLE_MISSING` | nonempty, all `AVAILABLE`, identifying inspected scope | both null | empty; `source_fact_ids` identifies the inspected scope that lacks the oracle | `ORACLE_MISSING` |
| `CONFLICT` | at least two `AVAILABLE` sources | both null | at least two same-typed, canonically unequal facts from at least two available sources | `CONFLICT` |
| `UNSCORABLE` + `SOURCE_MISSING` | at least one `NOT_AVAILABLE` source; no output can promote it | both null | empty; `source_fact_ids` may identify only available contextual scope | `SOURCE_MISSING` |
| `UNSCORABLE` + `UNSUPPORTED_CATEGORY` | nonempty registered sources identifying the unsupported scope | both null | empty; `source_fact_ids` may identify available context | `UNSUPPORTED_CATEGORY` |

Every expected/source fact used by an obligation has the same category as the
obligation. Violations reject the bundle with `INVALID_ORACLE_STATE` rather
than becoming response-quality rows.

Schema v1 permits only two operators:

- `EQUALS`: one expected fact; observed type and canonical native value must be
  identical;
- `ONE_OF`: one to 16 expected facts of the same type; their
  `(value_type, canonical value)` pairs must be pairwise distinct, and the
  observation must equal exactly one pair. Two different fact IDs with the
  same typed canonical value reject the evaluator bundle with
  `DUPLICATE_EXPECTED_VALUE`; values are never silently deduplicated. When
  multiple sources corroborate one value, use `EQUALS` with one expected fact
  and retain every corroborating fact in `source_fact_ids` for provenance.

Complex rules are normalized by the published projection to a typed JSON or
string-set fact and then compared with these operators. There is no expression,
substring, regex, fuzzy match, ordering guess, model judge or evaluator literal
expected value. Every expectation therefore originates from visible fact IDs.

`allowed_readiness` is a nonempty subset of `DESIGN_READY`, `STATIC_REVIEW`,
and `BLOCKED_ORACLE_MISSING`. `case_required` is true only when a usable case is
expected; conflict/review obligations may permit `STATIC_REVIEW`. A missing
oracle permits only `BLOCKED_ORACLE_MISSING` or an explicit typed gap.

## 5. Published response projection

`qa-quality-case-gap-v1` is a fixed JSON projection shipped with the module and
included verbatim in the contract digest. Its response has exactly:

```json
{
  "schema_version": 1,
  "artifact_id": "ART-1",
  "artifact_state": "DRAFT_UNAPPROVED",
  "execution_state": "NOT_EXECUTED",
  "summary": "Draft QA result",
  "observations": [],
  "cases": [],
  "gaps": [],
  "extensions": {}
}
```

`extensions` is the only permitted extension location. It accepts bounded,
secret-safe JSON and is retained but ignored by semantic comparison. Correct
extra detail there cannot create a semantic violation. Unknown members outside
published extension locations are a shape violation.

The published projection deliberately separates **envelope identity**,
**independent content channels**, and **assessable item content**. The published
response has nine members, but only parseable JSON object, `schema_version`,
and `artifact_id` are required to identify a response globally. Missing or
wrong-type `summary`, `artifact_state`, `execution_state`, `extensions`, or one
content channel produces a bounded diagnostic rather than erasing intact
channels. Item schemas allow only their published member names, but content
members may be absent, null, wrong-enum strings or unknown references so the
normalizer can retain a deterministic diagnostic instead of hiding a
SEMANTIC/USABILITY/PROVENANCE defect behind global parse failure. It never
inserts a default or repairs a value.

`observations`, `cases`, and `gaps` are independent channels. A valid channel
is a bounded array; a wrong-type or missing channel is marked unavailable.
Valid sibling channels remain assessable. An item that is not an object is a
recoverable shape diagnostic within only that channel and is otherwise ignored.
`artifact_state` or `execution_state` different from `DRAFT_UNAPPROVED` /
`NOT_EXECUTED` is an assessable claim-policy defect. It violates recoverable
SHAPE and is never trusted as an execution fact. It does not select an
obligation or change SEMANTIC/USABILITY/PROVENANCE unless a separate published
obligation and observation independently establish such a row.

An observation's published members are `check_id`, `value_type`, `value`, and
`source_fact_ids`. A well-formed observation supplies all four. Missing or
duplicate check identity makes that check absent/ambiguous for semantic
evaluation. Unknown `check_id`, mismatched `value_type`, invalid typed value or
insufficient/unknown fact refs is an assessable semantic/provenance defect, not
a fatal envelope error.

An observation whose valid `check_id` is not declared by any obligation is an
`UNBOUND_OBSERVATION` item diagnostic. It cannot satisfy any obligation and
does not alter any unrelated obligation's four rows. If the response therefore
lacks the observation required by a declared obligation, that obligation alone
receives the normal missing-observation `SEMANTIC=VIOLATED` result. Unknown
fact refs on an unbound observation remain attached to that diagnostic; they
do not create a global provenance violation.

### 5.1 Case projection

A case's published members are `case_id`, `obligation_ids`, `category`, `readiness`,
`setup`, `preconditions`, `data`, `actions`, `expected_oracle`, `cleanup`,
`source_fact_ids`, `gap_ids`, `missing_fields`, and `extensions`.

The item parser retains the row index plus every valid member independently.
A missing/invalid/duplicate `case_id`, absent content member, invalid readiness,
unknown obligation/fact/gap ref, or incomplete section becomes a typed item
diagnostic. It does not make the whole response uninterpretable. A row with no
valid obligation binding cannot satisfy any obligation; applicable obligations
then receive the ordinary usability result for no complete mapped case.

`setup`, `data`, and `cleanup` have `state`, `items`, and `reason`. State is
`DEFINED`, `NOT_APPLICABLE`, or `SOURCE_MISSING`. Each item is exactly
`{"text": "...", "source_fact_ids": [...]}`. `DEFINED` requires at least
one item and null reason; the other states require an empty item array and a
nonempty reason bound to a source fact or gap.

`preconditions` and `actions` are arrays of the same source-linked item; a
case requires at least one action. `expected_oracle` has `state`, `items`,
`oracle_fact_ids`, and `reason`. State is `DEFINED`, `ORACLE_MISSING`, or
`CONFLICT`; only `DEFINED` may contain items and requires available oracle
facts. Narrative text is not independently judged; its obligation semantics
come from normalized observations and typed facts.

`missing_fields` is a sorted unique subset of `SOURCE`, `SETUP`, `DATA`,
`EXPECTED_ORACLE`, `TARGET_INTERFACE`, `OBSERVABLE_LOCATOR`,
`CLEANUP_INVENTORY`, and `NON_FUNCTIONAL_THRESHOLD`. It makes the draft's
readiness limits machine-readable. Schema v1 contains no target endpoint or
credential and no `EXECUTABLE` readiness.

Readiness is validated, never repaired:

- `DESIGN_READY`: core design source, action and expected oracle are defined;
  target/observable may remain missing because this is not executable;
- `STATIC_REVIEW`: the obligation explicitly permits static review and the
  case describes a source-linked review action;
- `BLOCKED_ORACLE_MISSING`: expected oracle or another required design fact is
  missing and a matching typed gap is present.

### 5.2 Gap projection

A gap's published members are `gap_id`, `obligation_ids`, `reason`, `fact_ids`,
`source_ids`, `needed_evidence`, and `evidence_pointer`. `reason` is
`SOURCE_MISSING`, `ORACLE_MISSING`, `CONFLICT`, or `UNSUPPORTED_CATEGORY`.
A conforming gap maps at least one obligation. Missing identity/content,
invalid reason or unknown refs is retained as an item diagnostic and cannot
satisfy the affected obligation. A gap never satisfies semantic truth or
creates a case, but an exact gap can satisfy provenance honesty. An exact gap's
`reason` equals every mapped obligation's `required_gap_reason`, its `fact_ids`
include every required available contextual/conflicting fact, and its
`source_ids` include every obligation `source_id`. A gap may name a
`NOT_AVAILABLE` source only for `SOURCE_MISSING`; this binds absence declared by
the bundle and never lets response text promote that source to available.

## 6. Validation and normalization

`validate_bundle` performs no evaluation. It validates bundle structure,
limits, unique IDs, references, category completeness, source/fact/oracle
states, operator compatibility, response descriptor integrity, registered
contract hashes, containment and absence of prohibited input patterns. It
returns only IDs, safe counts, hashes and limitations.

Every `AVAILABLE` source is opened as opaque bytes: the evaluator applies
length, containment, link/reparse, digest and scanner checks but never parses it
as JSON or assigns meaning beyond the frozen visible fact. Exact source bytes
are retained in the result. A source read failure or digest change rejects the
command before any result reservation.

The normalizer is code-owned and selected by the fixed projection registry. It
does not execute bundle-supplied code. For the supported projection it returns
three independent channel objects (`AVAILABLE` with normalized rows, or
`UNAVAILABLE` with a diagnostic), plus sorted diagnostics. It never inserts a
default, coerces a type or discards a valid sibling channel.

Typed equality is `(value_type, canonical-native-value)` equality from
`DOC-PAIRED-VALUE-ENCODING-CLARIFICATION-001`: booleans are distinct from
integers; integer tokens are canonical and at most 34 magnitude digits;
decimals are canonical decimal strings; strings compare exact Unicode scalar
sequences; string sets are sorted unique strings; JSON compares canonical JSON
bytes with array order significant. Python `==` is not the comparison oracle.

### 6.1 Frozen installed assets

The wheel contains these exact package resources under
`qa_master/semantic_quality_assets/`:

| Resource | Registered identity and purpose |
|---|---|
| `contract.json` | `semantic-quality-v1`; exact bundle and item contract |
| `projection.json` | `qa-quality-case-gap-v1`; supported response projection |
| `legacy-paired-projection.json` | `paired-neutral-envelope-v1`; known unsupported compatibility descriptor |
| `result-schema.json` | exact profile, diagnostic and manifest member contract |
| `normalizer.json` | `qa-quality-normalizer-v1`; declarative canonicalization and reason-map revision |
| `secret-scanner.json` | `qa-quality-secret-scanner-v1`; scanner rule IDs, key classes and byte-pattern classes |

Each resource is canonical compact JSON: UTF-8, sorted object keys, unescaped
Unicode, compact separators and exactly one terminal LF. Its SHA-256 is over
those installed bytes, not a reconstructed object. Assets are loaded only with
`importlib.resources.files("qa_master").joinpath("semantic_quality_assets",
name)`. Packaging explicitly includes `semantic_quality_assets/*.json`.
Missing resources reject with `CONTRACT_ASSET_MISSING`; a byte mismatch rejects
with `CONTRACT_BINDING_MISMATCH` or `PROJECTION_BINDING_MISMATCH`.

`normalizer_sha256` binds `normalizer.json`, never a Python string constant.
`secret_scanner_sha256` binds `secret-scanner.json`; scanner executable logic
is also covered by the evaluator implementation hash. The evaluator
implementation hash is SHA-256 over exact installed
`qa_master/semantic_quality.py` bytes. Fresh-wheel verification must read all
six resources through `importlib.resources` and reproduce these hashes.

### 6.2 Diagnostic compartments

Security-policy failures (`PROHIBITED_FIELD` or `PROHIBITED_INPUT_PATTERN`) are
command preflight rejections with no profile. They are outside the following
response-quality diagnostics.

| Class | Exact conditions | Downstream effect |
|---|---|---|
| `GLOBAL_UNINTERPRETABLE` | invalid UTF-8/JSON, duplicate key, response byte/node/depth limit, top level not an object, or missing/invalid `schema_version` or `artifact_id` | every SHAPE row `VIOLATED/MALFORMED_KNOWN_RESPONSE_FATAL`; other dimensions `UNSCORABLE/RESPONSE_SHAPE_DEPENDENCY` |
| `RECOVERABLE_SHAPE` | missing/wrong-type `summary`, `artifact_state`, `execution_state`, or `extensions`; missing/wrong-type channel; non-object channel item; unknown member outside an item `extensions` | every SHAPE row `VIOLATED/MALFORMED_KNOWN_RESPONSE_RECOVERABLE`; safely normalized sibling content remains assessable |
| `CLAIM_POLICY_DEFECT` | `artifact_state` is not `DRAFT_UNAPPROVED` or `execution_state` is not `NOT_EXECUTED` | SHAPE is recoverably violated with `MALFORMED_KNOWN_RESPONSE_RECOVERABLE`; no execution claim is trusted and no obligation-local row changes solely from this outer field |
| `SEMANTIC_DEFECT` | missing/duplicate declared check, value-type mismatch, invalid typed value, or unequal source-bound value | only the mapped SEMANTIC row is violated |
| `USABILITY_DEFECT` | missing/invalid case identity, obligation/category mapping, readiness, section, action, expected oracle, cleanup, or required gap | only mapped USABILITY rows change |
| `PROVENANCE_DEFECT` | unknown/insufficient source, fact, oracle or gap reference, invented expected fact, or missing required honest gap | only mapped PROVENANCE rows change |

The three channel states are independent. `observations` unavailable affects
only determinate semantic rows and provenance that requires an observation;
`cases` unavailable affects only case-required usability and case provenance;
`gaps` unavailable affects only obligations whose source state requires a gap.
A definite mapped defect in an available channel is retained even if another
channel is unavailable. Unknown-only items remain diagnostics and cannot change
an unrelated obligation. Extra **known** source/fact references are retained
and permitted; the required references must be a subset. Any unknown reference
is a provenance defect.

For valid channel arrays, an observation is content-valid only with a unique
registered `check_id`, a registered `value_type`, a valid native `value`, and a
bounded unique `source_fact_ids` array. A case is content-valid only with a
unique `case_id`, nonempty known `obligation_ids`, one matching `category`, a
registered readiness, all section objects/arrays from section 5.1, and bounded
unique reference arrays. A gap is content-valid only with a unique `gap_id`,
nonempty known `obligation_ids`, registered reason, bounded known fact/source
IDs, nonempty `needed_evidence`, and a controlled relative or opaque
`evidence_pointer`. Invalid content is retained as an item diagnostic; it is
never repaired into a valid item.

`paired-neutral-envelope-v1` is the only registered legacy projection. Its
registered asset is retained in `contracts/projection.json`; all Phase 2 rows
are `UNSCORABLE/LEGACY_PROJECTION_UNSUPPORTED`. It is never coerced into the
new case schema and no new interpretation is attached to the old grade.

## 7. Four-dimensional evaluation

`profile.json` has exactly `schema_version`, `result_id`, `evaluation_id`,
`fixture_class`, `evaluation_state`, `execution_state`, `claim_status`,
`human_rating_status`, `legacy_grade_changed`, `response_mode`,
`category_applicability`, `shape_diagnostics`, `item_diagnostics`, `rows`, and
`limitations`. `response_mode` is `SUPPORTED`, `ABSENT`, or
`LEGACY_UNSUPPORTED`. A diagnostic has exactly `code`, `channel`, `index`,
`item_id`, and `member`; nullable fields stay explicit. Diagnostics are sorted
by `(code, channel, index-or--1, item_id-or-empty, member-or-empty)` and contain
no source text or typed value.

The profile contains exactly four rows per obligation, sorted by obligation ID
then `SHAPE`, `SEMANTIC`, `USABILITY`, `PROVENANCE`. Each row has
`obligation_id`, `category`, `dimension`, `outcome`, `reason_code`,
`source_fact_ids`, and `evidence_pointers`. Outcome is exactly `SATISFIED`,
`VIOLATED`, `ORACLE_MISSING`, or `UNSCORABLE`.

Each dimension uses the first matching row in its ordered table. This prevents
an implementation from replacing a definite defect with a dependency outcome.

### 7.1 SHAPE

| Order | Condition | Outcome / reason |
|---:|---|---|
| 1 | response descriptor is `ABSENT` | `UNSCORABLE / RESPONSE_ABSENT` |
| 2 | registered legacy projection | `UNSCORABLE / LEGACY_PROJECTION_UNSUPPORTED` |
| 3 | any `GLOBAL_UNINTERPRETABLE` diagnostic | `VIOLATED / MALFORMED_KNOWN_RESPONSE_FATAL` |
| 4 | any `RECOVERABLE_SHAPE` or `CLAIM_POLICY_DEFECT` diagnostic | `VIOLATED / MALFORMED_KNOWN_RESPONSE_RECOVERABLE` |
| 5 | supported projection with no shape diagnostic | `SATISFIED / PROJECTED_SHAPE_VALID` |

Malformed known response does not reject an otherwise valid evaluator bundle.
Only `GLOBAL_UNINTERPRETABLE` makes all other dimensions dependency-
`UNSCORABLE`; missing summary, a bad state enum, an unavailable channel or an
invalid item never suppresses intact sibling content. Bundle corruption, hash
drift, mixed contract digests or prohibited data rejects evaluation atomically
and publishes no profile.

### 7.2 SEMANTIC

| Order | Obligation-local condition | Outcome / reason |
|---:|---|---|
| 1 | `oracle_state=ORACLE_MISSING` | `ORACLE_MISSING / SOURCE_ORACLE_MISSING` |
| 2 | `oracle_state=CONFLICT` | `UNSCORABLE / SOURCE_FACT_CONFLICT` |
| 3 | `oracle_state=UNSCORABLE` | `UNSCORABLE / SEMANTIC_RULE_UNAVAILABLE` |
| 4 | observations channel unavailable for a determinate obligation | `UNSCORABLE / OBSERVATIONS_CHANNEL_UNAVAILABLE` |
| 5 | more than one row has the declared `check_id` | `VIOLATED / OBSERVATION_AMBIGUOUS` |
| 6 | no row has the declared `check_id` | `VIOLATED / OBSERVATION_MISSING` |
| 7 | matched row has invalid/mismatched `value_type` or invalid native value | `VIOLATED / OBSERVED_VALUE_INVALID` |
| 8 | valid typed value does not satisfy `EQUALS`/`ONE_OF` | `VIOLATED / OBSERVED_VALUE_MISMATCH` |
| 9 | valid typed value satisfies the operator | `SATISFIED / SOURCE_BOUND_VALUE_MATCH` |

Observation reference defects are assessed independently under PROVENANCE. A
typed value can therefore be semantically correct while its provenance is
violated, or semantically wrong while its known references are honest. The
evaluator never derives a missing expected value from prose, code, a historic
grade or another participant.

### 7.3 USABILITY

| Order | Obligation-local condition | Outcome / reason |
|---:|---|---|
| 1 | `oracle_state=ORACLE_MISSING` | `ORACLE_MISSING / USABLE_ORACLE_UNAVAILABLE` |
| 2 | `oracle_state=CONFLICT` | `UNSCORABLE / USABLE_OUTCOME_CONFLICTING` |
| 3 | `oracle_state=UNSCORABLE` | `UNSCORABLE / USABILITY_RULE_UNAVAILABLE` |
| 4 | determinate, `case_required=false`, no case mapped | `SATISFIED / CASE_NOT_REQUIRED` |
| 5 | required cases channel is unavailable | `UNSCORABLE / CASES_CHANNEL_UNAVAILABLE` |
| 6 | no case maps a case-required obligation | `VIOLATED / REQUIRED_CASE_MISSING` |
| 7 | `case_required=true` and any mapped case has ambiguous identity, wrong category/obligation mapping, invalid readiness, missing section/action/oracle/cleanup, or a concrete incomplete section | `VIOLATED / MAPPED_CASE_INVALID` |
| 8 | a mapped case exists when `case_required=false` and is invalid | `VIOLATED / OPTIONAL_CASE_INVALID` |
| 9 | at least one mapped case is complete and its readiness is allowed | `SATISFIED / USABLE_DRAFT_ARTIFACT_PRESENT` |

An unrelated gap never satisfies a case obligation. A source-level missing
oracle remains `ORACLE_MISSING`, and a conflict/unsupported rule remains
`UNSCORABLE`, whether or not the response supplies a gap; gap honesty is a
PROVENANCE concern. Completeness does not imply executable readiness.

### 7.4 PROVENANCE

For each obligation, relevant artifacts are its declared-check observation,
every case naming the obligation, and every gap naming the obligation. The
first matching condition applies:

| Order | Obligation-local condition | Outcome / reason |
|---:|---|---|
| 1 | any relevant artifact uses an unknown source/fact/gap/obligation ID, omits a required fact, maps the wrong category, fabricates an expected fact, or presents a gap as a determinate expectation | `VIOLATED / SOURCE_BINDING_INVALID` |
| 2 | `ORACLE_MISSING`, `CONFLICT`, or `UNSCORABLE` has an available gaps channel but no exact matching gap | `VIOLATED / REQUIRED_GAP_MISSING` |
| 3 | a channel required to assess the obligation's relevant artifacts is unavailable and no definite violation above exists | `UNSCORABLE / PROVENANCE_CHANNEL_UNAVAILABLE` |
| 4 | missing-oracle obligation has an exact `ORACLE_MISSING` gap citing its available source facts | `SATISFIED / MISSING_ORACLE_HONESTLY_REPORTED` |
| 5 | conflict obligation has an exact `CONFLICT` gap citing all conflicting facts and sources | `SATISFIED / CONFLICT_HONESTLY_REPORTED` |
| 6 | unscorable obligation has an exact gap matching its declared `SOURCE_MISSING` or `UNSUPPORTED_CATEGORY` reason | `SATISFIED / UNSCORABLE_GAP_HONESTLY_REPORTED` |
| 7 | determinate obligation's relevant artifacts contain all required known refs | `SATISFIED / SOURCE_BINDING_COMPLETE` |

Extra known references do not violate provenance. Unknown-only observations,
cases with no valid obligation binding, and unrelated gaps are retained as
diagnostics but do not change unrelated obligation rows. Invalid observed value
or readiness with otherwise valid references may therefore yield
`SEMANTIC=VIOLATED` or `USABILITY=VIOLATED` while `PROVENANCE=SATISFIED`.

### 7.5 Evidence pointers and totality

`evidence_pointers` is a sorted unique array of evaluator-created logical IDs,
never caller path text: `bundle:obligation/<id>`, `bundle:fact/<id>`,
`response:observation/<zero-based-index>`, `response:case/<index>`,
`response:gap/<index>`, or `diagnostic:<code>/<channel>/<index-or-root>`.
SHAPE rows point to every applicable shape diagnostic (or
`diagnostic:PROJECTED_SHAPE_VALID/root/root`). SEMANTIC rows point to the
obligation, expected facts and matched observation/absence diagnostic.
USABILITY rows point to the obligation and mapped cases/gaps or channel/missing
diagnostic. PROVENANCE rows point to the obligation and every reference-bearing
artifact used by its decision. Each row always has at least one pointer.

## 8. Precedence and total result derivation

Evaluation applies this exact global precedence:

1. invalid bundle, input integrity, contract/asset binding, security or
   output-path precondition → command rejection; no result directory;
2. response `ABSENT` → every row `UNSCORABLE/RESPONSE_ABSENT`;
3. registered legacy projection → every row
   `UNSCORABLE/LEGACY_PROJECTION_UNSUPPORTED`;
4. supported response with `GLOBAL_UNINTERPRETABLE` → SHAPE is
   `VIOLATED/MALFORMED_KNOWN_RESPONSE_FATAL`; other dimensions are
   `UNSCORABLE/RESPONSE_SHAPE_DEPENDENCY`;
5. identified supported response → derive SHAPE and every obligation-local
   dimension independently from section 7. A recoverable/channel/item defect
   never suppresses an intact sibling result.

An explicitly inspected visible source that lacks an expected oracle produces
`ORACLE_MISSING`. A source artifact that is unavailable or an unsupported
semantic rule produces `UNSCORABLE`. Conflict is never guessed into a winner;
it is semantically `UNSCORABLE` and may be provenance-honest.

The result has `evaluation_state: EVALUATED_DRAFT_ONLY`,
`execution_state: NOT_EXECUTED`, `claim_status: NOT_ASSERTED`,
`human_rating_status: NOT_EXECUTED`, and `legacy_grade_changed: false`.

## 9. Result identity, publication and inspection

The deterministic result ID is `SQ-` plus the first 32 lowercase hex characters
of SHA-256 over canonical JSON containing:

- exact source bundle SHA-256 and canonical bundle SHA-256;
- response state and exact response SHA-256 when present;
- the sorted `(source-id, source-byte-digest)` list;
- contract, selected projection, normalizer, result-schema and secret-scanner
  installed-byte digests;
- evaluator implementation SHA-256.

A one-byte change creates a different result ID. Re-evaluating identical bytes
derives the same ID; if that directory already exists, `RESULT_EXISTS` returns
without reading it as success or overwriting it.

`evaluate` fully parses/evaluates in memory, then stages a unique sibling
private directory containing:

```text
<result-id>/
  bundle.source.json
  response.source.json       # only when PRESENT
  sources/<source-sha256>.source # exact bytes for each AVAILABLE source
  contracts/contract.json
  contracts/projection.json
  contracts/result-schema.json
  contracts/normalizer.json
  contracts/secret-scanner.json
  contracts/evaluator.py
  bundle.canonical.json
  response.normalized.json   # only when globally interpretable and supported
  profile.json
  manifest.json
```

Available source bytes are copied exactly and are never JSON-decoded. Assets
and evaluator bytes are copied exactly after their length/hash and scanner
checks succeed. Controlled ledger locators derive from lowercase hashes or the
fixed names above, never caller paths. Identical source bytes are retained once
and may serve multiple source IDs.

Before publication the evaluator checks the 16 MiB total, closes/fsyncs files
where supported, re-reads every staged file and records length, SHA-256 and
role. Publication uses this cross-platform logical commit protocol:

1. Create the final `<output-root>/<result-id>` with exclusive `mkdir`. An
   existing file or directory makes the caller the loser: delete only its own
   staging directory and return `RESULT_EXISTS`; never inspect, repair or
   replace the existing result.
2. Create-exclusive `reservation.json` containing result ID and a random
   owner nonce. Copy each staged non-manifest file into the reserved directory
   with create-exclusive semantics and verify it again.
3. Only the process holding the exact nonce may clean up that incomplete final
   directory after an ordinary failure. A crash may leave it permanently
   `INCOMPLETE`; no later evaluation resumes or overwrites it.
4. Remove `reservation.json`, then atomically rename a fully written temporary
   manifest within the reserved directory to `manifest.json`. Manifest
   presence is the sole logical commit marker. After it appears, no file is
   mutated.

This protocol does not claim an atomic whole-directory rename. It guarantees a
single result-ID owner, no replacement of a concurrent winner, and no partial
directory being reported as committed.

`manifest.json` binds the result ID, input/canonical/normalized hashes,
contract identities, evaluator implementation, file ledger, fixture class,
category applicability, exact diagnostic set, row IDs/outcomes/reasons/pointers
and all limitations. It contains no aggregate. The ledger covers every retained
file except the manifest itself and forbids extras.

`inspect_result` is process-free and never repairs. It rejects any symlink or
reparse point before following it. It strict-parses the manifest, canonical
bundle and profile; re-hashes every retained byte; recomputes the result ID
from retained inputs/assets/evaluator bytes; checks the directory basename;
checks bundle/category/obligation identities; and verifies that the profile has
exactly the manifest-declared four rows per obligation with identical category,
outcome, reason and pointer values. It does not trust the ledger or re-run
semantic evaluation.

Inspection applies one deterministic boundary:

| Precedence | Condition | Result |
|---:|---|---|
| command | any path component is a link/reparse point, or traversal/absolute-path policy fails | reject `LINK_FORBIDDEN` or `PATH_ESCAPE`; no integrity status |
| command | an existing path cannot be opened/read because of local I/O | reject `LOCAL_IO_FAILURE`; no integrity status |
| 1 | result root does not exist or is not a directory | `MISSING` |
| 2 | `reservation.json` exists, manifest is absent/invalid, or manifest/result invariants cannot be established | `INCOMPLETE` |
| 3 | valid manifest declares a file that is absent | `MISSING` |
| 4 | declared size/hash/role, recomputed result ID, profile/category/row cross-check, asset or implementation binding differs | `MISMATCH` |
| 5 | an undeclared file or directory exists | `UNDECLARED` |
| 6 | all checks pass | `INTACT` |

For mixed retained defects the status precedence is
`INCOMPLETE > MISSING > MISMATCH > UNDECLARED > INTACT`. A missing input path
to `validate`/`evaluate` is instead a command rejection
`LOCAL_INPUT_MISSING`; an input/output link is `LINK_FORBIDDEN`; an existing
non-directory output root is `OUTPUT_PATH_CONFLICT`.

The output root must be outside every bundle/response/source path and outside
any CR-011 run/evidence root supplied as an input. The evaluator has no delete,
retention expiry, migration, import-to-old-grade, or in-place upgrade command.

## 10. Errors and observability

Stable command errors contain only `{"status":"REJECTED","error":CODE}` and
exit 2. They do not echo source text, typed values, locators or exception
representations. Required codes include:

- `INVALID_BUNDLE`, `DUPLICATE_JSON_KEY`, `SIZE_LIMIT`, `COUNT_LIMIT`;
- `UNKNOWN_REFERENCE`, `INVALID_OPERATOR`, `INVALID_ORACLE_STATE`,
  `DUPLICATE_EXPECTED_VALUE`, `CATEGORY_OBLIGATION_MISMATCH`;
- `SOURCE_INTEGRITY_FAILURE`, `RESPONSE_INTEGRITY_FAILURE`;
- `CONTRACT_ASSET_MISSING`, `CONTRACT_BINDING_MISMATCH`,
  `PROJECTION_BINDING_MISMATCH`, `UNKNOWN_PROJECTION`;
- `PROHIBITED_FIELD`, `PROHIBITED_INPUT_PATTERN`;
- `PATH_ESCAPE`, `LINK_FORBIDDEN`, `LOCAL_INPUT_MISSING`,
  `OUTPUT_PATH_CONFLICT`;
- `RESULT_EXISTS`, `RESULT_SIZE_LIMIT`, `LOCAL_IO_FAILURE`.

Readable retained-result defects are always represented by the fixed `inspect`
status table; they are not converted into a second, overlapping command error.

Malformed known response is deliberately a profile outcome, not a command
error. Safe stdout exposes only result/evaluation IDs, counts, operation status
and paths supplied by the caller. Profile reason codes make missing source,
unsupported projection, malformed response and semantic contradiction
distinguishable without revealing content.

## 11. Compatibility, deployment and rollback

This is an additive local module and command. It does not change installed
`design`, Campaign state, deterministic methods, paired runtime, benchmark,
legacy response parser or old evidence schema. `qa_master.quality.review_cases`
may remain a lightweight draft lint; its `pass` flag is not imported as a
Phase 2 outcome.

Schema/normalizer changes require a new ID and hashes. A known schema with a
changed digest fails closed. Rollback installs the previous package and leaves
ordinary JSON result roots readable by integrity tools; it never deletes
evidence. There is no service, database or migration.

## 12. Public development fixture matrix

The implementation fixtures are public development material and cannot be
reported as holdout evidence. At minimum, independent tests freeze cases for:

| Family | Required oracle |
|---|---|
| shape/projection | valid v1, permitted extension detail, global invalid JSON/identity, each unavailable channel with intact siblings, missing summary/extensions, wrong artifact/execution state, recoverable unknown/non-object item, absent response, registered legacy projection, unregistered projection rejection |
| semantic | exact canonical typed match including boolean/integer/JSON lookalikes, mismatch, `ONE_OF`, duplicate canonical expected value rejection, missing/duplicate declared observation, unbound-only observation isolation, value-type mismatch with valid provenance, invalid typed value, missing oracle, conflicting facts, unsupported rule/side-effect invariant |
| usability | complete design-ready case, permitted static review, `case_required=false` with no artifact, invalid optional artifact, analysis-only/empty cases, unavailable cases channel, missing case content, invalid readiness with valid provenance, missing/duplicate identity, matching and unrelated gaps |
| provenance | complete binding, extra known refs, missing/unknown/insufficient ref, invented expected fact, unknown-only item isolation, honest source/oracle gap, conflict/unsupported with and without the required gap, unavailable gaps channel |
| requirements/conflicts | compound/conflicting rules and missing acceptance fact |
| method selection | applicable finite method with candidate-to-case mapping and candidate-only violation |
| functional/API/integration | supplied observable versus missing endpoint/response contract |
| security/scope/authority | no-execution preserved; draft/process exit never becomes authorization or security proof |
| recovery/regression | supplied change/evidence mapping and absent failure/recovery semantics |
| non-functional | visible threshold and `NON_FUNCTIONAL_THRESHOLD` missing-oracle case |
| usability/category | every valid applicability state including mixed missing/conflict `UNSCORABLE`; each contradictory category/obligation combination; no rating/aggregate/winner fields |
| installed assets | exact six-resource bytes/hashes through a fresh wheel, missing asset, mixed version, scanner/normalizer/projection drift, evaluator-byte drift |
| provenance lifecycle | opaque non-JSON source bytes, one-byte bundle/response/source/schema drift, concurrent result-ID reservation with one winner, injected stage/reservation/manifest fault, no overwrite or auto-resume, input/output containment |
| inspection | each status alone and mixed precedence, invalid/absent manifest, missing/hash/identity/profile/category/row/asset/implementation mismatch, undeclared file, link/reparse and I/O error boundary |
| historical boundary | hashes for retained CR-011 raw/oracle/grade stay unchanged and no Phase 2 file is written under that root |

Capacity boundary tests cover every maximum and maximum-plus-one. Metamorphic
tests prove that adding ignored extension detail does not change semantic rows,
removing an oracle cannot increase semantic/usability success, and changing one
fact invalidates the identity rather than rewriting a profile.

## 13. Implementation and independent handoff

1. **Developer task:** own only the new semantic-quality module, fixed
   projection/result schemas, CLI and developer tests. Do not change paired
   evaluation, historical evidence, installed-design behavior or TASK-057's
   frozen subject.
2. **Independent tester:** own evaluator-authored public fixtures and negative,
   boundary, mutation, atomicity, side-effect-sentinel and historical-hash
   tests. Any holdout material stays in a separately governed location.
3. **Independent reviewer:** inspect source/operator binding, precedence,
   readiness derivation, lack of hidden scoring, result manifest and legacy
   immutability.
4. **Governance:** link REQ-025/NFR-009 → DES-060 → implementation/test/review
   artifacts. A complete local test is still not a Gate or product acceptance.

Suggested future evidence IDs are `EVD-SEMANTIC-QUALITY-EVALUATOR-001` for the
independent local evaluator result and `EVD-SEMANTIC-QUALITY-LEGACY-IMMUTABILITY-001`
for the CR-011 preservation check. They do not exist in this design.

## 14. Alternatives and deferred decisions

- Extending `grade_run` was rejected because it would mix an exact hidden-shape
  checker with the new published semantic/usability contract and risk changing
  historical interpretation.
- A model judge or fuzzy semantic matcher was rejected because it cannot supply
  deterministic source-bound truth and would introduce another model/runtime.
- A caller-supplied normalizer was rejected because it is executable evaluator
  code outside the content/trust boundary.
- An aggregate score was rejected because requirements mandate separate rows
  and no accepted threshold or weighting exists.
- Executable readiness was deferred because Phase 2 supplies no target,
  fixture, observable or cleanup authority contract.

No separate ADR is required for this slice: separation from the paired grader,
process-free operation, published projections and non-aggregation are direct
requirements of the frozen sub-contract. Human rubric, representative workload
mix/sample size, holdout ownership/release, category weights/thresholds,
adjudication, narrative preference and any comparison or superiority decision
remain `NOT_AVAILABLE` and cannot be local defaults.

## 15. Unverified items

Implementation, fixtures, evaluator execution, independent tests, independent
review, held-scenario evaluation, human assessment and any Gate decision are
`PENDING` or `NOT_EXECUTED`. This DRAFT design is not an evaluation result and
does not establish full REQ-025 acceptance, executable cases, product quality
or superiority.
