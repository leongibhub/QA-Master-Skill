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
    "result_schema_sha256": "<sha256>"
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
equal the module's fixed shipped artifacts. Callers cannot substitute a schema
or executable normalizer. A syntactically valid but unregistered projection ID
can be evaluated only as unsupported under section 8; a known ID with the wrong
digest is `PROJECTION_BINDING_MISMATCH` and rejects the bundle.

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

Each row has `category`, `state`, `reason`, and `fact_ids`. `state` is
`APPLICABLE`, `NOT_APPLICABLE`, `ORACLE_MISSING`, or `UNSCORABLE`.
`NOT_APPLICABLE` requires a nonempty source-linked reason; `APPLICABLE`
requires at least one obligation. `ORACLE_MISSING` requires at least one
matching missing-oracle obligation. No category is silently omitted. The array
is an applicability register, not a score or coverage percentage.

### 4.4 Obligations and source-bound comparison

Every obligation has exactly:

```json
{
  "id": "OB-1",
  "category": "FUNCTIONAL_API_INTEGRATION",
  "interpretation": "Published rule stated for reviewers",
  "source_fact_ids": ["F-1"],
  "oracle_state": "DETERMINATE",
  "check_id": "CHECK-1",
  "operator": "EQUALS",
  "expected_fact_ids": ["F-1"],
  "allowed_readiness": ["DESIGN_READY"],
  "case_required": true
}
```

`oracle_state` is `DETERMINATE`, `ORACLE_MISSING`, `CONFLICT`, or
`UNSCORABLE`. A determinate obligation requires a unique `check_id`, an
operator and available expected facts. Other states use null `check_id` and
operator; `expected_fact_ids` is empty for missing/unsupported and contains all
conflicting facts for `CONFLICT`.

Schema v1 permits only two operators:

- `EQUALS`: one expected fact; observed type and canonical native value must be
  identical;
- `ONE_OF`: one to 16 expected facts of the same type; the observation must
  equal exactly one canonical value.

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

The published projection deliberately separates **envelope structure** from
**assessable content**. The outer object and its eight members are required;
`observations`, `cases`, and `gaps` must be bounded arrays and each element must
be an object. Item schemas allow only their published member names, but content
members may be absent, null, wrong-enum strings or unknown references so the
normalizer can retain a deterministic diagnostic instead of hiding a
SEMANTIC/USABILITY/PROVENANCE defect behind global parse failure. It never
inserts a default or repairs a value.

An observation's published members are `check_id`, `value_type`, `value`, and
`source_fact_ids`. A well-formed observation supplies all four. Missing or
duplicate check identity makes that check absent/ambiguous for semantic
evaluation. Unknown `check_id`, mismatched `value_type`, invalid typed value or
insufficient/unknown fact refs is an assessable semantic/provenance defect, not
a fatal envelope error.

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
creates a case, but an exact gap can satisfy provenance honesty.

## 6. Validation and normalization

`validate_bundle` performs no evaluation. It validates bundle structure,
limits, unique IDs, references, category completeness, source/fact/oracle
states, operator compatibility, response descriptor integrity, registered
contract hashes, containment and absence of prohibited input patterns. It
returns only IDs, safe counts, hashes and limitations.

The normalizer is code-owned and selected by the fixed projection registry.
It does not execute bundle-supplied code. For the supported v1 projection it
validates the response and returns ID-indexed typed observations, cases and
gaps plus sorted `shape_diagnostics` and `item_diagnostics`. It preserves
source bytes and records normalized canonical bytes/hash separately.

Diagnostics are classified before evaluation:

| Class | Exact conditions | Downstream effect |
|---|---|---|
| `FATAL_STRUCTURE` | invalid UTF-8/JSON, duplicate key, over-limit bytes/nodes/depth, top level not an object, missing/wrong-type outer member, wrong schema/artifact/execution state, or `observations`/`cases`/`gaps` not an array | all SHAPE rows `VIOLATED`; other dimensions `UNSCORABLE` |
| `RECOVERABLE_SHAPE` | an array item is not an object, or a published item has an unknown member outside `extensions` | SHAPE rows `VIOLATED`; valid known portions remain assessable |
| `SEMANTIC_DEFECT` | unknown/missing/duplicate check, value-type mismatch, invalid typed value, unequal source-bound value | SHAPE unaffected; relevant SEMANTIC row is `VIOLATED` |
| `USABILITY_DEFECT` | missing/invalid case identity, obligation mapping, readiness, section, action, expected oracle, cleanup, or matching gap | SHAPE unaffected; relevant USABILITY row is `VIOLATED` or its declared missing-oracle outcome |
| `PROVENANCE_DEFECT` | unknown/insufficient source, fact, oracle or gap reference, or an invented expected fact | SHAPE unaffected; relevant PROVENANCE row is `VIOLATED` |

If one item has defects in several classes, each applicable dimension receives
its own deterministic row; a lower-level content defect never erases a
higher-value assessable finding. Duplicate item identities are ambiguous only
for that identity: the corresponding semantic/usability/provenance rows are
evaluated as absent/ambiguous, while unrelated obligations remain assessable.
Prohibited claim/secret keys or byte patterns are security-policy preflight
rejections under precedence rule 1, before shape normalization; they publish no
profile and never appear as `FATAL_STRUCTURE` quality observations.

`paired-neutral-envelope-v1` and all CR-011 artifacts are legacy inputs for
this evaluator. They are never coerced into the new case schema. A bundle may
bind their hash and projection ID to demonstrate the compatibility boundary;
all Phase 2 dimensions are `UNSCORABLE` with `LEGACY_PROJECTION_UNSUPPORTED`,
and no new interpretation is attached to the old grade.

## 7. Four-dimensional evaluation

The profile contains exactly four rows per obligation, sorted by obligation ID
then `SHAPE`, `SEMANTIC`, `USABILITY`, `PROVENANCE`. Each row has
`obligation_id`, `category`, `dimension`, `outcome`, `reason_code`,
`source_fact_ids`, and `evidence_pointers`. Outcome is exactly `SATISFIED`,
`VIOLATED`, `ORACLE_MISSING`, or `UNSCORABLE`.

### 7.1 SHAPE

- supported projection, present response and valid published form:
  `SATISFIED`;
- present response declared as the supported projection with any
  `FATAL_STRUCTURE` diagnostic:
  `VIOLATED / MALFORMED_KNOWN_RESPONSE_FATAL`;
- present response with only `RECOVERABLE_SHAPE` diagnostics:
  `VIOLATED / MALFORMED_KNOWN_RESPONSE_RECOVERABLE`; other dimensions still
  evaluate normalized known content;
- response descriptor state `ABSENT`: `UNSCORABLE / RESPONSE_ABSENT`;
- syntactically valid unregistered or legacy projection:
  `UNSCORABLE / PROJECTION_UNSUPPORTED`.

Malformed known response does not reject an otherwise valid evaluator bundle.
Fatal structure makes `SEMANTIC`, `USABILITY`, and `PROVENANCE`
`UNSCORABLE / RESPONSE_SHAPE_DEPENDENCY`. Recoverable item shape does not: the
evaluator assesses every safely normalized known member and records an
obligation-specific defect where identity/binding is unavailable. By contrast,
bundle corruption, input hash drift, mixed contract digests or prohibited data
rejects evaluation atomically and publishes no profile.

### 7.2 SEMANTIC

For a valid supported response:

- `DETERMINATE`: exactly one matching typed observation that satisfies the
  source-bound operator and required fact refs is `SATISFIED`; absent,
  contradictory or insufficiently bound observation is `VIOLATED`;
- `ORACLE_MISSING`: `ORACLE_MISSING` regardless of participant wording;
- `CONFLICT` or `UNSCORABLE`: `UNSCORABLE`.

The evaluator never derives a missing expected value from a case sentence,
nearby fact, code behavior, historic grade or another participant.

### 7.3 USABILITY

- determinate case-required obligation with at least one structurally complete,
  source-linked case at an allowed readiness is `SATISFIED`;
- determinate case-required obligation with no case, `cases: []`, analysis
  only, invalid readiness, missing required member or only an unrelated gap is
  `VIOLATED`;
- explicit missing oracle/source with a matching case/gap is
  `ORACLE_MISSING`, never `SATISFIED`;
- conflict/unsupported category with an honest matching gap is `UNSCORABLE`;
- a non-case obligation with a valid permitted static review artifact is
  `SATISFIED`.

Completeness does not imply executable readiness. No schema-v1 outcome says a
test can run.

### 7.4 PROVENANCE

- every observation/case claim uses known facts required by the obligation and
  no unsupported expected fact: `SATISFIED`;
- missing, unknown, mismatched or fabricated source/oracle refs, or a source
  gap presented as a determinate expectation: `VIOLATED`;
- missing oracle with an exact `ORACLE_MISSING`/`SOURCE_MISSING` gap, or conflict
  with a gap citing all conflicting facts: `SATISFIED` for honesty while the
  semantic/usability rows retain their own non-success outcomes;
- response/projection unavailable: `UNSCORABLE`.

This dimension assesses binding and gap honesty, not the truth of natural
language prose.

## 8. Precedence and total result derivation

Evaluation applies this exact precedence:

1. invalid bundle, input integrity, contract binding, security or output-path
   precondition → reject; no result directory;
2. response `ABSENT` or projection unsupported/legacy → all four rows
   `UNSCORABLE` with the corresponding reason;
3. response present for known projection with `FATAL_STRUCTURE` →
   `SHAPE=VIOLATED`, other three rows `UNSCORABLE`;
4. response with `RECOVERABLE_SHAPE` → `SHAPE=VIOLATED`, then assess valid
   known members independently; unbindable item content cannot satisfy an
   obligation but does not suppress unrelated results;
5. structurally usable response, including content-level semantic, usability
   or provenance defects → `SHAPE=SATISFIED`, then apply section 7 to produce
   the relevant `VIOLATED`, `ORACLE_MISSING`, or `UNSCORABLE` rows.

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
- every referenced source/projection artifact digest;
- contract, projection, normalizer and result-schema digests;
- evaluator implementation SHA-256.

A one-byte change creates a different result ID. Re-evaluating identical bytes
derives the same ID; if that directory already exists, `RESULT_EXISTS` returns
without reading it as success or overwriting it.

`evaluate` fully parses/evaluates in memory, then stages a sibling private
directory containing:

```text
<result-id>/
  bundle.source.json
  response.source.json       # only when PRESENT
  sources/<source-sha256>.source # exact bytes for each AVAILABLE source
  contracts/projection.json
  contracts/result-schema.json
  bundle.canonical.json
  response.normalized.json   # only when valid and supported
  profile.json
  manifest.json
```

Available source bytes and the module-owned schema bytes are copied only after
their length/hash and prohibited-pattern checks succeed. Their controlled
ledger locators derive from lowercase content hashes, never from caller paths.
Identical source bytes are retained once and may serve multiple source IDs.
This lets `inspect`
reconcile every retained source/schema hash without reopening the original
location. The normalizer is code, not a copied executable artifact; its module
hash and source revision remain explicit manifest dependencies.

Before publication it checks the 16 MiB total, closes/fsyncs files where the host
supports it, re-reads every file and records length, SHA-256 and role. It then
renames the complete staging directory to the non-existing result path. Any
failure deletes only its own staging directory and leaves inputs, previous
results and destination unchanged. Abrupt host loss may leave a named staging
directory; `inspect` reports it as `INCOMPLETE` and never promotes or repairs it.

`manifest.json` binds the result ID, input/canonical/normalized hashes,
contract identities, evaluator implementation, file ledger, fixture class,
category applicability, row IDs/outcomes and all limitations. It contains no
aggregate. `inspect_result` rejects links/reparse points, recomputes every file
and manifest identity, identifies missing/mismatched/undeclared files, and
never evaluates or rewrites a profile.

The output root must be outside every bundle/response/source path and outside
any CR-011 run/evidence root supplied as an input. The evaluator has no delete,
retention expiry, migration, import-to-old-grade, or in-place upgrade command.

## 10. Errors and observability

Stable command errors contain only `{"status":"REJECTED","error":CODE}` and
exit 2. They do not echo source text, typed values, locators or exception
representations. Required codes include:

- `INVALID_BUNDLE`, `DUPLICATE_JSON_KEY`, `SIZE_LIMIT`, `COUNT_LIMIT`;
- `UNKNOWN_REFERENCE`, `INVALID_OPERATOR`, `INVALID_ORACLE_STATE`;
- `SOURCE_INTEGRITY_FAILURE`, `RESPONSE_INTEGRITY_FAILURE`;
- `CONTRACT_BINDING_MISMATCH`, `PROJECTION_BINDING_MISMATCH`;
- `PROHIBITED_FIELD`, `PROHIBITED_INPUT_PATTERN`;
- `PATH_ESCAPE`, `LINK_FORBIDDEN`, `OUTPUT_PATH_CONFLICT`;
- `RESULT_EXISTS`, `RESULT_SIZE_LIMIT`, `LOCAL_IO_FAILURE`;
- `RESULT_INTEGRITY_FAILURE` for failed inspection parsing/invariants.

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
| shape/projection | valid v1, permitted extension detail, fatal duplicate/outer/container failure, recoverable unknown item member, absent response, unsupported and legacy projection |
| semantic | exact typed match, mismatch, `ONE_OF`, missing/duplicate observation, value-type mismatch, invalid typed value, missing oracle, conflicting facts, unsupported rule/side-effect invariant |
| usability | complete design-ready case, permitted static review, analysis-only/empty cases, missing case content, invalid readiness, missing/duplicate identity, matching and unrelated gaps |
| provenance | complete fact binding, missing/unknown/insufficient ref, invented expected fact, honest source/oracle gap, complete conflict citation |
| requirements/conflicts | compound/conflicting rules and missing acceptance fact |
| method selection | applicable finite method with candidate-to-case mapping and candidate-only violation |
| functional/API/integration | supplied observable versus missing endpoint/response contract |
| security/scope/authority | no-execution preserved; draft/process exit never becomes authorization or security proof |
| recovery/regression | supplied change/evidence mapping and absent failure/recovery semantics |
| non-functional | visible threshold and `NON_FUNCTIONAL_THRESHOLD` missing-oracle case |
| usability/category | every category present, reasoned N/A, invalid silent omission, no rating/aggregate/winner fields |
| provenance lifecycle | one-byte bundle/response/source/schema drift, mixed version, result collision, staging fault, ledger mismatch, input/output containment |
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
