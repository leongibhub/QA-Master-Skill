# CR-033: test-case conformance proposal

- Artifact: DOC-CASE-CONFORMANCE-REQ-001
- Document State: DRAFT
- Evaluation State: IN_REVIEW
- Evidence Status: PENDING for implementation and evaluation
- Source: user request to improve QA Master beyond the Awesome skill library.
- Design direction: user explicitly replied `ok` on 2026-10-23 to implementing
  concrete-test-point audit and readable gap reports. This authorizes scoped
  engineering, not a formal requirement baseline, product acceptance or release.

## User outcome

After an Agent turns supplied requirements into test cases, QA Master should show
which declared boundary points, decision combinations, state transitions and
combinatorial vectors those cases actually represent. It should identify missing,
duplicated, mismatched and stale case rows before delivery. Users continue to work
in their Agent chat; the Agent prepares the structured files and calls the helper.

The current design engine creates precise candidates, but the ordinary case
review checks fields and requirement-level trace links. Merely associating one
case with a requirement does not account for its individual finite test points.
See `qa_master/quality.py:review_cases`, `qa_master/design_methods.py:_candidate`
and `qa_master/campaign_cli.py:_installed_design`.

## Requirements and acceptance

| ID | Proposed behaviour | Measurable acceptance |
| --- | --- | --- |
| REQ-029 | Audit authored test-case scenario rows against freshly recomputed deterministic design candidates. | Every current candidate appears once in the audit denominator; an exact typed input/oracle/source/requirement match is distinguished from missing, duplicate or mismatched representations. Requirement IDs alone never count as a match. One parameterized case may represent multiple candidates through separate explicit scenario rows. |
| REQ-030 | Bind the case library to its design input and retain unresolved design obligations. | Reject a stale design digest; changed declared source metadata/digests or models require a new review. External source contents are not opened by the auditor, so an unrefreshed descriptor cannot reveal external-byte drift. Existing missing-oracle, conflict and unreachable obligations remain visible rather than becoming covered cases. Unknown candidate IDs are diagnosed. |
| REQ-031 | Deliver readable, reproducible audit results through the installed Agent workflow. | Provide an offline CLI and JSON/Markdown audit output. Include concrete candidate IDs and missing/mismatch reasons so the Agent can revise cases. Update bundled instructions and an example; a fresh installed package runs from an unrelated consumer directory. No extra model key or mandatory third-party Python dependency. |
| NFR-013 | Keep formal representation separate from semantic quality and execution. | Typed equality distinguishes booleans from integers and preserves declared decimal strings. All results remain DRAFT_UNAPPROVED / NOT_EXECUTED; no approval, executable-case, prose-correctness or overall-superiority claim. Schema/size/depth/identity failures are bounded and deterministic. |

An exact scenario binding establishes only formal representation of a declared
finite candidate. Copying binding metadata into a generic narrative must not be
presented as proof that its steps or expected-result prose are correct. A missing
expected-result description or required case field is a separate documentation
finding; nonempty prose is not proof of semantic correctness.

## Proposed test model

| Test group | Required independent observations |
| --- | --- |
| Five design methods | Boundary, decision table, state transition, pairwise and combinatorial exact representations; reconciliation by model. |
| Deliberate omissions | Remove a scenario while leaving its requirement trace: the missing finite candidate remains visible. |
| Deliberate mutations | Alter one value, bool/int type, decimal representation, state, oracle, source or requirement binding at a time: the appropriate mismatch is reported. |
| Staleness and ambiguity | Change the model digest; duplicate a case/scenario; invent a candidate: reject or diagnose as specified, never infer coverage. |
| Unresolved knowledge | Missing oracle/conflicting model/unreachable transition remains an obligation even when other candidates have exact representations. |
| Integrity and limits | Duplicate JSON keys, nonfinite values, excessive nesting/size/count and output overwrite fail safely. Equivalent ordered sets produce stable results. |
| Installed user flow | Fresh wheel and standalone Skill helper produce the same audit from outside the repository; no network or external-system writes. |

An independent tester should select additional withheld omission/mutation cases
after the implementation freezes. This measures audit reliability, not general
LLM generation quality. No model benchmark, execution result or human acceptance
exists for this proposed increment.

## Scope and later work

First increment: explicit finite-model case audit and readable findings, plus
installed instructions. Existing `design`, campaign state and evaluator contracts
remain compatible. No inference of arbitrary document semantics, requirement
approval, real-system execution or Jira import is added.

Later increments require their own requirements: source-grounded requirement
contract authoring, requirement-change regression selection, and case exports to
Excel-readable formats. A representative same-model, independently rated trial
would be needed to claim improved end-to-end generation quality.
