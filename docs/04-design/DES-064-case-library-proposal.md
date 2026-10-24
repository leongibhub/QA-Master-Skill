# DES-064 / ADR-007: non-applied case-library proposal overlay

Document State:DRAFT; CR-036; REQ-037–040 / NFR-015.

## Decision and alternatives

Add a pure overlay beside audit/impact. Reject in-place rewriting because it
would lose old evidence and hold/review work. Reject plain patched-library-only
output because it cannot preserve held cases and reasons. Choose one JSON
envelope with a strict after library, originals, review decisions and followups.
No new arbitrary-report renderer, apply/export command or mutable state machine.

Unique context-changed vectors may be proposed, always with mandatory review;
holding every context change would fail the selected source-version use case.
Unresolved model obligations hold affected cases conservatively. All old gaps
are held: the generator cannot decide whether an old gap reason still applies.
This deliberately differs from the alternative of automatically rebinding gaps.

## Public boundary

New module qa_master/case_library_proposal.py exports:

```python
class CaseLibraryProposalError(ValueError):  # stable value-free .code
    ...
def propose_method_case_library(before_bundle: dict, after_bundle: dict,
                                case_library: dict) -> dict: ...
def write_method_case_library_proposal(before_path, after_path, cases_path,
                                      output_path) -> dict: ...
```

CLI: propose-method-case-library --before old.json --after new.json
--cases old-cases.json --output proposal.json. JSON only; each flag exactly once.
No --apply/--format; no campaign state required/read/written. Exit0 means only
proposal created; rejection returns exit2 and {status:REJECTED,error:<code>}.
CLI stdout carries fixed status/execution/application_state, proposed/held case
and missing-vector counts, and output path; never case prose.

Existing case_conformance.py, method_impact.py and design_methods.py MUST remain
byte-identical. Reuse internal strict JSON/canonical identity/I/O helpers through
an error adapter: pass through own error first, then known domain .code; map
unknown structural exceptions to INVALID_SCHEMA. File-wrapper OSError/RuntimeError
reject stable OUTPUT_IO_ERROR. Preserve CR-035 post-publication cleanup behavior.

## Fixed result schemas

Root exact keys:
schema_version, status, execution, application_state,
before_design_input_sha256, after_design_input_sha256,
baseline_case_library_sha256, proposed_case_library_sha256,
proposed_case_library, candidate_deltas, case_decisions, row_decisions, held_gaps,
missing_vector_followups, baseline_audit_summary, baseline_findings,
obligation_deltas, unknowns, post_proposal_audit, summary, limitations.

Fixed schema_version1; status DRAFT_UNAPPROVED; execution NOT_EXECUTED;
application_state NOT_APPLIED. Nested proposed_case_library has ONLY existing
v1 keys schema_version, design_input_sha256(after), cases, gaps. Its gaps is
always empty in this slice. Never add approved/executed/status fields there.

Case decision exact keys: case_id, source_case_sha256, decision, review_required,
reason_codes, original_case, proposed_case_sha256. Original is a detached deep
copy of the parsed whole case. Source/proposed case hashes use the same normalized
case projection as existing normalized-library identity; proposed hash is null
when held. review_required is always true. Decisions:
CARRY_PROPOSED, REBIND_PROPOSED_REVIEW_REQUIRED, HELD_BASELINE, HELD_AMBIGUOUS,
HELD_REMOVAL, HELD_OBLIGATION. Priority baseline > ambiguity > removal > obligation.

Row decision exact keys: case_id, scenario_sha256, occurrence,
before_candidate_id, after_candidate_id, possible_after_candidate_ids, decision,
review_required, reason_codes, proposed_scenario. Row decisions use the same
normalized scenario hash/one-based occurrence as CR-034. Proposed row decision
is CARRY_PROPOSED or REBIND_PROPOSED_REVIEW_REQUIRED; ineligible row has its
HELD_BASELINE/AMBIGUOUS/REMOVAL/OBLIGATION reason; otherwise-eligible rows inside a
held case become HELD_CASE_ATOMICITY. All held rows have null after_candidate_id
AND null proposed_scenario. Possible IDs remain a sorted list, never a chosen
ambiguous mapping. review_required is always true.

Eligible proposed_scenario has EXACT existing five fields: candidate_id,
method_data, requirement_ids, source_ref_ids, oracle_ref_ids. Use after candidate
values, typed data and sorted unique reference-ID sets. Preserve case id/title/
preconditions/steps/expected exactly; retain original scenario order. Cases in
the nested library and case decisions sort by case ID; row decisions sort by
case ID/hash/occurrence. A case is CARRY_PROPOSED only if every formal projection
is unchanged and its only impact reason is FORMAL_VECTOR_UNCHANGED; otherwise
eligible cases/rows use REBIND_PROPOSED_REVIEW_REQUIRED.

Held gap exact keys: gap_sha256, occurrence, original_gap,
possible_after_candidate_ids, decision, reason_codes. Preserve each occurrence
including identical duplicates/orphan references. decision is always
HELD_GAP_REVIEW_REQUIRED. No proposed gap is inserted in the nested library.

Missing-vector followup exact keys: candidate_id, model_id, method, dimension,
method_data, requirement_ids, source_ref_ids, oracle_ref_ids, source_refs,
oracle_refs, action, reason_codes. Full refs are exact sorted after descriptors;
action is AUTHOR_CASE_OR_RECORD_GAP. Context identifies formal data only and does
not invent expected prose or business reasons.

Reason codes preserve all applicable CR-033 diagnostic and CR-034 controlled
codes, plus CASE_PARTIAL_REBIND_FORBIDDEN, CASE_HELD, GAP_HELD,
GAP_REASON_REVIEW_REQUIRED. Mix of eligible/ineligible rows adds the partial-case
code to the case and every row; do not lose context/obligation/baseline reasons.
Missing followups union matching impact reasons with held-case/gap reasons.

Summary exact keys: source_case_count, source_row_count, source_gap_count,
proposed_case_count, proposed_row_count, proposed_gap_count, held_case_count,
held_row_count, held_gap_count, after_candidate_count, exact_after_candidate_count,
missing_after_candidate_count, case_decision_counts, row_decision_counts,
assessment. Count maps include all corresponding decision values with zeroes.
assessment copies post-audit ASSESSED/UNASSESSED; never a quality PASS.

## Algorithm and invariants

1. Fresh analyze_method_impact(before,after,library); do not accept a caller report.
2. Fresh design_methods(after), compare its digest to the impact after digest.
3. Build O(n) indexes for old/new deltas, after candidates, case findings, impact
   row locators, raw row/gap candidate counts and normalized source cases.
4. A row is eligible only when CR-034's fresh audited action is NO_DECLARED_IMPACT
   or REVIEW_BINDING, no UNRESOLVED_MODEL_OBLIGATION, a unique RETAINED_VECTOR has
   exactly1 old/after ID, and action/delta/after candidate identity agree.
5. Determine whole-case eligibility before copying any row. Keep all originals
   and decisions even when the case has zero scenarios. Refresh only eligible
   whole cases; no generated prose, case deletion, guessed rename or partial case.
6. Hold every old gap, build possible mappings without choosing ambiguity.
7. audit_method_cases(after, proposed_library). Require no findings, no DUPLICATE,
   MISMATCH or GAP_RECORDED. Only EXACTLY_BOUND/MISSING are possible here.
8. Emit one full followup per MISSING after candidate. Include new/unrepresented
   retained points, held-case/gap reasons, unresolved model obligations as relevant.
9. Reconcile every source case/row/gap exactly once; proposed+held counts match;
   exact+missing equals after candidate count; followups count equals MISSING;
   library hash equals post-audit case_library_sha256. Impossible internal
   mapping/count/post-audit outcomes reject PROPOSAL_INVARIANT_FAILED.

Impact performs3 bounded replays; after design and post-audit add2, maximum5.
Do not call the before audit redundantly. Compare/index by exact keys, not an
O(rows*candidates) search. Preserve all input dictionaries/files and detach
returned original/proposed values from caller-owned input objects.

## Serialization and determinism

Same parsed input produces byte-stable compact sorted-key UTF-8 JSON plus one
newline. API validates the exact same encoded output size as writer:5MiB maximum,
otherwise OUTPUT_TOO_LARGE before writing. Use a private serializer for generated
objects, with allow_nan=False; do not reapply the input-depth32 walker to the
envelope, which adds fixed wrapper nesting to validated original cases.

Case/reference/scenario set permutations preserve normalized library identity,
row locators/decisions and normalized proposed-library content. Verbatim parsed
original-case copies and preserved scenario order may change raw envelope bytes;
do not promise byte equality across such representation permutations. Steps
remain ordered. Input errors retain existing5MiB/depth32/10000 replay-budget/
10000-case/50000-row+gap limits. Output-size rejection is a declared first-slice
limit, not a promise to stream or shard arbitrarily large proposals.

No source locator is dereferenced, model/provider called, subprocess executed,
state mutated or external object written by this feature. Existing safe file
helpers reject linked/reparse ancestors, collisions and existing outputs.
