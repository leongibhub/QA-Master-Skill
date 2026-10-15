# Paired evaluation typed-value encoding clarification

- Artifact ID: `DOC-PAIRED-VALUE-ENCODING-CLARIFICATION-001`
- Document state: `DRAFT`
- Change: `CR-011`
- Requirements: `REQ-020`, `REQ-023`
- Design baseline affected: `DES-040` v1 sections 5, 10 and 11
- Decision record context: `ADR-005` v1
- Scope: pre-pilot normative correction of response/assertion value encoding; no implementation, test result, approval, pilot result, or Gate decision is represented

## 1. Problem and requirement intent

`REQ-020` requires a neutral common envelope, and `REQ-023` requires exact
typed assertions that cannot become fuzzy scores or human judgments. The
requirements leave the wire encoding to architecture.

`DES-040` selected a string for every observation and assertion value. The
current runtime and public-development oracle fixtures instead use native JSON
booleans, integers, arrays, and objects, with strings retained for decimal and
ordinary text. The independent `TC-PE-221` failure is a genuine conformance
failure against `DES-040` v1 and remains historical evidence. This document
resolves the design before any model pilot; it does not reinterpret that failed
test as a pass.

## 2. Options and decision

**String-encoded values** give the prompt-side schema one primitive, but require
double encoding for sets and structured JSON. They increase model formatting
errors, make evidence harder to inspect, and require two JSON parsing layers.
Their main advantage would matter if the provider enforced the supplied schema.

**Native JSON values with a discriminator** use boolean, integer, string,
array, and object values directly while `value_type` selects a strict local
validator. Decimal remains a string because JSON has no exact decimal primitive.
This avoids double encoding and preserves the public oracle's natural form. Its
risk is that JSON Schema alone cannot express every recursive/depth rule.

Adopt **native JSON values** for the corrected pre-pilot schema-v1 contract.
This follows the actual boundary: `ADR-005` and `DES-040` do not pass
`--output-schema` because provider compatibility is unproven. The fixed schema
is common prompt material and a structural aid; the local parser is the
authoritative acceptance boundary.

This is a controlled design correction, not an exception for current code. The
implementation is conformant only after sections 3–5 are implemented, all
dependent hashes are regenerated, and independent tests pass. No dual-format
compatibility or coercion is permitted.

## 3. Normative native encoding

| `value_type` | Required outer JSON value | Validation and canonical form |
|---|---|---|
| `BOOLEAN` | JSON boolean | Only `true` or `false`; integer `0`/`1` and strings are rejected. |
| `INTEGER` | JSON integer | Boolean, negative zero, and float/exponent forms are rejected. Normalize as the mathematical integer serialized in canonical base-10 JSON. |
| `DECIMAL` | JSON string | Match `-?(0|[1-9][0-9]*)(\.[0-9]*[1-9])?`, rejecting `-0`, exponent, plus sign, leading integer zero, and redundant fractional trailing zero. `"1"` remains distinct from integer `1`. |
| `STRING` | JSON string | Literal nonempty string under the existing 20,000-character bound; never reparsed. |
| `STRING_SET` | JSON array of strings | Zero to 256 unique nonempty strings, each within the string bound, sorted in ascending Unicode scalar-value sequence. |
| `JSON` | Any JSON value | Reject floats/non-finite numbers, duplicate keys, prohibited controlled keys, unpaired surrogates, depth over 16, or more than 4,096 nodes. Object keys canonicalize in sorted order; array order is significant. |

Examples:

```json
{"value_type":"BOOLEAN","value":true}
{"value_type":"INTEGER","value":1}
{"value_type":"DECIMAL","value":"1"}
{"value_type":"STRING","value":"1"}
{"value_type":"STRING_SET","value":["F-1","F-2"]}
{"value_type":"JSON","value":{"accepted":[1,2],"rejected":[0,3]}}
```

Boolean `true`, integer `1`, decimal `"1"`, string `"1"`, and JSON values
`true`, `1`, or `"1"` remain distinct because comparison includes
`value_type`.

Canonical JSON uses UTF-8, sorted object keys, compact separators, and
unescaped Unicode scalar values. It rejects duplicate keys, floats,
`NaN`/infinity, and unpaired surrogates. Node count includes the root and every
array element, object key, and object value. Depth is one at the root and rises
by one for every nested array or object. Observation and assertion values use
identical rules.

## 4. Schema and parser responsibilities

The fixed common response-schema artifact retains closed outer members and
expresses discriminator-dependent JSON primitive/container types where JSON
Schema can do so. It remains module-owned and content-addressed; callers cannot
substitute it.

The local parser is authoritative for strict boolean-versus-integer identity,
canonical decimal, set ordering/uniqueness, duplicate keys, prohibited keys at
arbitrary depth, depth/node limits, evidence references, and claim fields. It
recursively rejects `rating`, `score`, `winner`, `quality_grade`, `approval`,
`execution_result`, and `superiority` as object keys inside a `JSON` value, plus
existing secret-shaped controlled keys. The same text used as an ordinary
string value is not rejected by substring.

Validation precedes comparison. The parser never converts string `"1"` to
integer `1`, converts native JSON to encoded text, sorts a supplied set, or
otherwise repairs a nonconforming result.

## 5. Exact grading contract

Assertion `expected.value` uses the same native representation and validator as
observation `value`. The grader compares exact scenario/check binding, exact
`value_type`, canonical JSON bytes of the valid native value, and the required
evidence-reference subset.

An unequal valid typed value or missing required evidence reference is
`VIOLATED`. Missing/ambiguous participant output is `UNSCORABLE`. Invalid
observation output remains `OUTPUT_INVALID`; an invalid assertion bundle fails
atomically. No path uses substring, fuzzy matching, model judging, numeric
aggregate, or implicit conversion.

## 6. Compatibility and artifact lifecycle

This is a pre-pilot correction to DRAFT design. Schema version remains 1 only
because no conforming schema-v1 model pilot or accepted comparison result
exists; response-schema, prompt, manifest, and fixture digests remain the
byte-level binding. If a conforming baseline run existed, this incompatible
wire change would require schema v2.

Before a pilot, update and bind as one unit: the fixed schema and prompt;
observation/assertion validators; depth/node and recursive-key enforcement;
public oracle and affected visible fixtures; protocol inventory and all
schema/prompt/manifest/evaluator commitments; and developer/independent tests.

Superseded artifacts remain historical evidence and are never rewritten. The
old `TC-PE-221` result remains a failure against the old DES contract; new
native-value cases receive new IDs after this clarification is registered.

The apparent public visible-input hash mismatch was traced to CRLF conversion
in the checkout; the registered raw Git blob hashes match protocol v1. Pilot
preparation must continue to materialize and verify the registered raw bytes,
not silently substitute newline-normalized working-tree bytes. This finding is
validation-only and does not establish a completed pilot.

## 7. Quality attributes and required conformance

The existing 2 MiB envelope bound applies before parsing. Depth/node checks must
not permit stack exhaustion. Stable errors and logs expose IDs, types, outcomes,
and safe locators rather than oracle values. Native `JSON` does not relax
secret-key, claim-key, leakage, evidence-reference, DRAFT, NOT_EXECUTED,
rating, winner, approval, or superiority controls.

Rollback installs code, prompt, schema, fixtures, and hashes from one matching
contract. Mixed revisions fail binding.

Independent tests must cover:

1. valid native boolean, integer, string set, structured JSON, decimal string,
   and ordinary string on both observation and assertion sides;
2. every cross-type representation, including boolean-as-integer, plus integer
   negative-zero and exponent forms;
3. decimal exponent/zero/non-finite negatives;
4. string-set ordering, uniqueness, length, and item types;
5. JSON duplicate-key, float, prohibited-key, surrogate, depth 16/17, and node
   4,096/4,097 boundaries;
6. exact type-plus-canonical-value comparison with lookalikes;
7. no repair or coercion of invalid values;
8. fixed-schema substitution rejection and equal bytes across arms;
9. regenerated prompt/schema/oracle/manifest/protocol hashes before spawn; and
10. preservation of old `TC-PE-221` evidence with new test IDs for this contract.

Until the design revision, bindings, and independent conformance evidence are
registered, the pilot remains `NOT_EXECUTED`. This document makes no comparison,
rating, superiority, acceptance, release, or Gate claim.
