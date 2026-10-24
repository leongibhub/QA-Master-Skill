# CR-036: reviewable after-change case-library proposal

- Artifact: DOC-CASE-LIBRARY-PROPOSAL-REQ-001; Document State: DRAFT.
- Evaluation State:IN_REVIEW; Evidence Status:OBSERVED for scoped design only.
- Authorization: user explicitly selected option2, the offered next-version case
  library draft preserving the old library and human review. Detailed schema is
  orchestrator-authored engineering design, not formal baseline/Gate acceptance.
- Baseline: main ce9da58605dfbdaa27ef8749ee5d20070175b54d.
- Read-only requirement and architecture investigations informed the decisions;
  the fixed DES-064 below wins over their alternative suggestions.

| ID | Behavior / measurable acceptance |
| --- | --- |
| REQ-037 | Generate one non-applied proposal from before/after finite bundles and the before-bound strict v1 case library. The nested proposed_case_library binds the after digest and passes the existing after audit. Preserve inputs and original case values; no campaign, original library or external system is updated. |
| REQ-038 | A case enters the nested library only if every row has a conformant baseline, unique RETAINED_VECTOR pair and no unresolved model obligation. Ambiguous/removed/baseline-defective/obligation rows hold the entire case. Every old case/row remains identifiable, including empty cases and duplicate normalized occurrences. No partial case migration. |
| REQ-039 | Proposed scenarios exactly project after candidate_id, typed method_data, requirement/source/oracle ID sets. Case title, preconditions, steps and expected prose retain their values/order. Context/binding changes retain all impact/baseline reasons and require human review; formal pairing never establishes prose correctness or semantic equivalence. |
| REQ-040 | Every old explicit gap remains held verbatim for reason review; no gap is silently discarded or carried as newly confirmed. Every after-audit MISSING vector has one exact after-candidate binding/descriptor followup, including new points and points excluded by whole-case holds. Full requirement/model context is reviewed in the after bundle. Preserve baseline findings, obligation deltas and unmodeled changes. |
| NFR-015 | Stdlib-only, offline, bounded and deterministic, no input mutation/overwrite. Reuse strict CR-033–035 input/I/O contracts. Fixed draft/nonexecution/nonapplication fields; no apply/execution/history-copy path. Source and installed helper work from a consumer directory without campaign state. |

Limits:5MiB per input; input JSON depth32; existing per-design aggregate replay
budget10000; cases10000; rows+gaps50000. Output compact UTF-8 JSON including its
newline is <=5MiB, otherwise OUTPUT_TOO_LARGE before publication. Generated
envelope adds fixed nesting to already validated input; input-depth validation
must not be mistakenly reapplied to that wrapper. Nested library remains within
the existing audit input limits.

Test models: TC-PROP-001 unchanged;002 source-descriptor churn;003 requirement/
oracle/source context;004 whole-case removal/ambiguity;005 bad baseline/empty
case;006 obligations;007 all gap occurrences;008 exact missing-vector contexts;
009 row identity/order/type/no mutation;010 strict parse/size/I/O;011 installed
consumer delivery. No result authorizes actual test execution or regression skip.
