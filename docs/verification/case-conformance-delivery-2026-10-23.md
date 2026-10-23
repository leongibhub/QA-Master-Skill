# CR-033 case conformance delivery record

- Requirements: REQ-029–031, NFR-013; design DES-062.
- Tasks: TASK-132–136.
- Document State: DRAFT; Evaluation State: IN_REVIEW.
- Current implementation evidence: OBSERVED; TASK-135 bounded tests/installed delivery and TASK-136 bounded review complete on e9e141f; full four-job CI success.
- Baseline: GitHub main e8e085e, after CR-032 provenance metadata correction.

## Actual scope authorization

The user requested a substantive improvement over Awesome, then explicitly
answered `ok` to the proposed concrete-test-point audit on 2026-10-23. The
orchestrator dispatched separate developer, documentation, tester and reviewer
identities. This record asserts scoped engineering authorization only; no formal
requirement baseline, authenticated acceptance or release is manufactured.

## Subjects and observations

| Subject | Observation |
| --- | --- |
| c0e01d1 / fc84e2c | DRAFT requirements/design/implementation plan; root clarified candidate precedence, canonical identity and declared-source staleness. |
| 7bd6b9c | Initial implementation, bundled docs/example and independent fixtures frozen. Author developer/doc check 16/16 OK. Independent preliminary suite reported 13 checks OK plus bounded size/no-clobber checks; one symbolic-link subcheck skipped for Windows privilege. |
| 7bd6b9c fresh installed delivery | Tester built a 6,387,872-byte wheel (~56 seconds), created an isolated environment (11.8 seconds), installed offline (19.1 seconds), verified imports from site-packages and generated consumer Markdown with 17 candidate rows. This is preliminary installed evidence, not automatically transferred to later repairs. |
| 195fb30 | Renderer/field compatibility/size-contract corrections frozen. Re-review found that two identical gaps produced a valid DUPLICATE audit row that the Markdown validator rejected. The finding and failed predicate are retained. |
| e9e141f | Identical-gap renderer predicate corrected; 13/13 developer tests passed. TASK-136 independently reviewed the final source: PASS, P0–P3 unresolved=0; 9 selected independent adversarial checks passed, including native Windows junction rejection. Full tester-owned suite/package result remains separately recorded. |

## Retained review findings and corrections

The independent reviewer is `/root/case_audit_reviewer`; implementation owner is
`/root/case_audit_developer`. Final source re-review is PASS on e9e141f; the exact retained findings and results are in the independent review report. The original subject/findings remain history.

| Finding | Actual issue | Repair state |
| --- | --- | --- |
| CASE-R1 | Duplicate scenario rows bypassed incomplete case documentation findings. | Developer added case-level documentation findings independent of candidate-state precedence; verified resolved by TASK-136 on e9e141f. |
| CASE-R2 | Public Markdown renderer trusted malformed reports and allowed an injected table row through crafted identity text. | Developer added strict report/value/count validation and stable INVALID_REPORT errors; verified resolved by TASK-136 on e9e141f. |
| CASE-R3 | Uniform ID validation rejected valid existing engine requirement IDs (spaces/Chinese) and leading punctuation in source/oracle IDs. | Root corrected the overly narrow rule; developer now follows each authoritative field contract. Final independent recheck PENDING. |
| CASE-R4 | Markdown orphan diagnostics omitted the owning case ID. | Developer renders all available identity fields; verified resolved by TASK-136 on e9e141f. |
| CASE-R5 | Markdown omitted design/library digests, so the exported report did not identify both audited inputs. | Developer added both validated digests; verified resolved by TASK-136 on e9e141f. |
| CASE-R6 | Renderer schema/count validation accepted Boolean counters, fake nonzero model counts or invented PASS diagnostics; finding capacity was inconsistent with possible audit output. | Known diagnostic/state/type/arithmetic rules and derived finding bounds implemented; TASK-136 verified the bounded source repair. |
| CASE-R7 | The implementation's decimal 5,000,000-byte bound differed from the specified binary 5 MiB. | Corrected to 5,242,880 bytes, with exact-limit acceptance and next-byte rejection checked by independent fixtures. |
| CASE-R8 | Identical repeated gaps deduplicated their reason list, but the Markdown DUPLICATE predicate required multiple unique reasons. | Fixed and independently rechecked on e9e141f; repeated gaps remain DUPLICATE/GAP_DUPLICATE, not covered. |

## Reproducible user-visible example

`evidence/cr033/run-example-comparison.py --subject e9e141fa1319c37d2166b1bebc69cee6f77ab1c8`
ran on the frozen product. The retained
[JSON observation](evidence/cr033/example-comparison-e9e141f.json) binds both
input identities. On the same public authored scenario rows:

| Check | Actual result |
| --- | --- |
| Preexisting requirement-link check | No UNCOVERED_REQUIREMENT finding, because the requirement still has linked cases. |
| New finite-scenario audit | Denominator 10; EXACTLY_BOUND 9; MISSING 1 (`TC-MD-0F09CDEA90500A24D043`). |

This is a controlled demonstration of the new audit behaviour versus QA Master's
old link-level check. It is not an Awesome model-output comparison or a general
quality benchmark. The older 195fb30 example observation is also retained.

The tester's initial Windows wheel harness hit an output-decoding error before
product assertions. The tester corrected decoding with replacement for diagnostic
logs and retained the original harness failure. It is not recorded as a product
defect or a passing wheel test.

## Current regression evidence

For frozen product e9e141f, GitHub run `39953357673` Ubuntu/Python 3.12 job
`120413033369` was read back as success: 848 tests, failures 0, errors 0, skipped
11, 159.864 seconds. At the later final readback, all four jobs succeeded:
Ubuntu/Windows with Python 3.10/3.12 each ran 848 tests with zero failures/errors.
Ubuntu jobs skipped 11 each; Windows jobs skipped 3 each. The initial Ubuntu-only
observation is retained separately; the [final matrix](evidence/cr033/ci-matrix-e9e141f.json)
contains the actual job identities and counts. This is regression evidence, not
product execution or removal of the retained skip boundaries.

The tester's final e9e141f scoped run exited 0: 21 tests in 194.349 seconds,
20 passed and one skipped because the Windows account lacks symbolic-link
privilege. The independent native Windows junction test passed. This run includes
a clean Git archive, newly built wheel, isolated environment, offline installation
and consumer CLI invocation. See the [tester record](case-conformance-independent-test-2026-10-23.md)
and its durable logs. The additional fresh-wheel installation delivered 5,885
standalone Skill files; its isolated helper produced a 1,663-byte Markdown audit
with exit 0, denominator 10 and DRAFT_UNAPPROVED / NOT_EXECUTED. The clean
[standalone result](evidence/cr033/task-135-e9e141f/standalone-result.json)
records wheel/output hashes. A first harness wrapper ended without an exit record;
a later helper call correctly rejected the tester's missing input path. Both
attempts remain history; the tester corrected the input to the installed examples
and reused the same wheel/environment/Skill for the successful call. No product
patch or failed result was hidden.

## Delivery limits

The audit checks formal representation of explicitly declared finite candidates.
It does not validate the completeness/business meaning of the model, prose
semantics, real-system coverage, executability or host discovery. It detects
declared source/model digest drift; it does not open arbitrary source locators.
No same-model Awesome output-quality comparison was executed in this increment.
Current project Gates and whole-product acceptance/release states remain unchanged.
