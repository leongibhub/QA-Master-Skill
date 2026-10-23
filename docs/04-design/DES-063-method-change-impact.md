# DES-063: finite-model change impact

- Change: CR-034; requirements REQ-032–036 / NFR-014.
- Document State: DRAFT. Implementation/test/review initially NOT_EXECUTED.
- Approach selected by orchestrator within the user's continuation authorization;
  not a formal human architecture/Gate approval.

## Architecture decision ADR-006

Use an additive overlay beside CR-033. Reject raw candidate-ID diff because IDs
include whole-model source/requirement context and cause false wholesale churn.
Reject NLP, fuzzy matching and guessed rename maps because they lack an exact
contract. Defer permanent-UUID/schema migration. Reuse existing typed design,
baseline audit, canonicalization and safe I/O helpers without altering them.

Candidate grouping key is canonical typed JSON of `{model_id, method, dimension,
method_data}`. The display fingerprint is SHA-256 of that key; matching uses exact
canonical bytes, not only its hash. Requirement/oracle/source identities are
compared separately, so a retained vector may still require all bindings and
expectations to be reviewed. This explicitly chooses formal-input continuity
over calling it semantic equivalence. Requirement/model renames are not inferred.

Each group yields one candidate_delta with exact keys `model_id`,
`formal_fingerprint`, `pair_state`, `before_candidate_ids`, `after_candidate_ids`,
`reason_codes`. States are RETAINED_VECTOR, ADDED, REMOVED, AMBIGUOUS. Unique
retained pairs carry one old/new ID. Groups with multiplicity are AMBIGUOUS; never
select an arbitrary pairing. Sum old/new ID cardinalities to the corresponding
engine candidate totals.

Review amendment after frozen `ebfc947`: candidate groups carrying a before
candidate in baseline MISSING, DUPLICATE or MISMATCH also carry controlled reason
BASELINE_NONCONFORMANT. This preserves the candidate identity needing baseline
repair without inventing an authored gap. GAP_RECORDED remains a separate gap
followup. In an ambiguous group the marker applies conservatively to the group.
Action precedence selects the action only; retain the union of applicable
baseline, formal/context and unresolved-obligation reasons. Preserve each old
explicit gap occurrence, including duplicates and orphan references.

## Public boundary

New module `qa_master/method_impact.py` exports:

```python
analyze_method_impact(before_bundle: dict, after_bundle: dict, case_library: dict) -> dict
write_method_impact(before_path, after_path, cases_path, output_path, *, format="json") -> dict
class MethodImpactError(ValueError):  # stable value-free .code
    ...
```

CLI: `impact-method-cases --before old.json --after new.json --cases old-cases.json
--output impact.json [--format json|markdown]`. Duplicate flags reject. Exit 0
means report creation only; exit 2 means rejected input/I/O. No state file needed.
The Markdown renderer is private and consumes generated internal reports only;
all displayed IDs/text are escaped for Markdown/HTML/newlines. No new public
arbitrary-report rendering or trust contract is introduced.

## Fixed report and actions

Root exact keys: `schema_version`, `status`, `execution`,
`before_design_input_sha256`, `after_design_input_sha256`, `case_library_sha256`,
`library_rebinding_required`, `baseline_audit_summary`, `baseline_findings`,
`candidate_deltas`, `case_row_actions`, `review_case_ids`, `new_candidate_ids`,
`obligation_deltas`, `gap_followups`, `unknowns`, `summary`, `limitations`.

Row action exact keys: `case_id`, `scenario_sha256`, `occurrence`,
`before_candidate_id`, `after_candidate_id`, `action`, `reason_codes`. Normalize
reference-ID sets before hashing rows; within a case sort canonical row bytes
and number identical occurrences from 1. Actions: NO_DECLARED_IMPACT,
REVIEW_BINDING, REVIEW_REMOVAL, REVIEW_BASELINE, REVIEW_AMBIGUOUS. Baseline issues
take precedence, followed by ambiguity, removal, changed binding/context, no
declared impact. Case-level audit findings select orphan/undocumented cases even
when they have no rows. Explicit gaps remain separate followups and are never
counted as existing case coverage.

Controlled reasons: FORMAL_VECTOR_UNCHANGED, FINITE_VECTOR_ADDED,
FINITE_VECTOR_REMOVED, AMBIGUOUS_FORMAL_MATCH, CANDIDATE_REBIND_REQUIRED,
REQUIREMENT_BINDINGS_CHANGED, REQUIREMENT_CONTEXT_CHANGED,
SOURCE_BINDINGS_CHANGED, SOURCE_DESCRIPTORS_CHANGED, ORACLE_BINDINGS_CHANGED,
ORACLE_DESCRIPTORS_CHANGED, MODEL_CONTEXT_CHANGED, BASELINE_NONCONFORMANT,
UNRESOLVED_MODEL_OBLIGATION. Full linked records/descriptors are compared with
typed canonical equality. Requirements are unique nonempty strings, including
Chinese/spaces, as allowed by the existing engine.

Obligation grouping key is `{model_id, method, code, subject}` with exact typed
data. Delta keys: `model_id`, `formal_fingerprint`, `state`,
`before_obligation_ids`, `after_obligation_ids`, `code`. States PRESENT_BOTH,
AFTER_ONLY, BEFORE_ONLY, AMBIGUOUS. Retain old/new identities; never call an old
obligation resolved. Cases touching a model with unresolved before/after
obligations require review even if their own vector is unchanged.

Gap followup exact keys: `before_candidate_id`, `reason_code`,
`after_candidate_ids`, `action` (always REVIEW_GAP). Unknown exact keys: `code`,
`requirement_ids`; use UNMODELED_REQUIREMENT_CHANGE for changed/added/removed
requirements not represented by before/after models. Always disclose that code
changes and unrefreshed external source bytes were not analyzed.

Summary exact keys: `before_candidate_count`, `after_candidate_count`,
`candidate_group_states`, `before_obligation_count`, `after_obligation_count`,
`case_count`, `row_count`, `review_case_count`, `new_candidate_count`,
`baseline_finding_count`, `unknown_count`, `assessment`. Assessment UNASSESSED if
both designs have zero candidates, otherwise ASSESSED; neither is a quality pass.
Case-library hash uses CR-033 normalized identity. Library-rebinding flag compares
the two engine input digests, even when all formal points match.

## Safety, compatibility and evidence

Reuse package-internal CR-033 validation/read/write helpers behind a small
MethodImpactError adapter. Three bounded engine passes (before audit plus two
designs) are allowed, each capped before enumeration; comparison/indexing is
linear in candidates/obligations/rows. Enforce input bytes/depth/rows before work.
Do not mutate input dictionaries, files, campaign state, approvals or adapters.

The feature writes only one new report atomically. JSON/Markdown derive from the
same result object and carry all three input identities. Existing audit behavior
and schemas remain unchanged. Source interpretation and regression execution
remain separate user/Agent decisions. Independent tests and review must verify
stale baseline, metadata-only ID churn, types, context changes, obligations,
multi-row cases, ambiguity, count reconciliation and installed delivery.
