# Case Conformance Implementation Plan

> For agentic workers: execute through subagent-driven-development; implementation,
> independent test and review have distinct owners. User approved the recommended
> scope on 2026-10-23; ordinary execution choices are delegated to the orchestrator.

**Goal:** audit authored finite-model case scenarios before Agent delivery.

**Architecture:** recompute the existing design engine; compare typed scenario
rows with its candidates, preserve all obligations and render readable findings.
An additive command leaves existing campaign/evaluator contracts unchanged.

**Tech Stack:** Python 3.10+, standard library, unittest, Windows/Linux.

**Spec:** [DES-062](../04-design/DES-062-case-conformance-proposal.md),
[REQ-029–031 / NFR-013](../03-requirements/case-conformance-2026-10-23.md).

## Global constraints

- No new mandatory dependencies, model credentials, network or test execution.
- No campaign authority/state mutation or external writes.
- Results: DRAFT_UNAPPROVED / NOT_EXECUTED; exact binding is not semantic quality.
- Inputs <=5 MiB each; <=10,000 cases/candidates, <=50,000 total scenario/gap
  rows; JSON depth <=32. Bound total finite-model replay work before enumeration.
- Preserve unknown/conflicting/unreachable design obligations without relabelling.
- New reports never overwrite input or existing output, including linked paths.

## Fixed public contract

Library: `audit_method_cases(campaign_bundle: dict, case_library: dict) -> dict`;
`render_audit_markdown(report: dict) -> str`;
`write_case_audit(input_path, cases_path, output_path, *, format='json') -> dict`;
`CaseConformanceError.code` is a stable value-free diagnostic.

Case library exact root keys:

```json
{"schema_version":1,"design_input_sha256":"<design_methods input_sha256>",
 "cases":[],"gaps":[]}
```

Each case has exactly `id`, `title`, `preconditions`, `steps`, `expected`,
`scenarios`. Nonempty textual fields/steps document the case but do not prove
business correctness. Cases with missing/empty documentation receive findings
and cannot have their rows counted as exactly represented. `scenarios` is a list
of rows with exactly `candidate_id`, `method_data`, `requirement_ids`,
`source_ref_ids`, `oracle_ref_ids`. The rows are the authoritative typed scenario
inputs; the Agent's human-facing case table must carry these same values.
Sets use unique IDs; all other data uses type-sensitive canonical JSON equality.

Each gap has exactly `candidate_id`, `reason_code`; reason is one of
`SOURCE_MISSING`, `ORACLE_MISSING`, `SETUP_MISSING`, `OBSERVABLE_MISSING`,
`CLEANUP_MISSING`, `OTHER`. A gap does not count as a represented scenario.
Both gap and case rows for one candidate are a conflict, not a success.

Audit root includes `schema_version`, `status`, `execution`,
`design_input_sha256`, `case_library_sha256`, `candidates`, `obligations`,
`findings`, `summary`, `limitations`. Candidate rows contain IDs/model/method,
`state`, `case_ids` and diagnostic `codes`. States: `EXACTLY_BOUND`,
`GAP_RECORDED`, `MISSING`, `DUPLICATE`, `MISMATCH`. Codes distinguish
`DATA_MISMATCH`, `ORACLE_MISMATCH`, `SOURCE_MISMATCH`, `TRACE_MISMATCH`,
`CASE_DOCUMENTATION_INCOMPLETE`, `ORPHAN_CANDIDATE`, and `GAP_CASE_CONFLICT`.
Per-model and total counts reconcile to the candidate denominator. Empty
candidate sets are `UNASSESSED`, never implied complete. `obligations` preserve
engine IDs/codes/model IDs, without copying source prose into diagnostics.

CLI: `audit-method-cases --input bundle.json --cases cases.json --output audit.json
[--format json|markdown]`. Duplicate flags are rejected. Exit 0 means report
creation, never a quality pass. Exit 2 is a validation/I/O rejection; stderr/stdout
must not reveal raw input or secrets. The installed helper inherits this command.

## TASK-132: requirements/design and governance (orchestrator)

- [x] Inspect latest GitHub source, code, existing gaps and lifecycle state.
- [x] Obtain requirement-analyst and architect investigations.
- [x] Present reviewable proposal and record actual user `ok`.
- [ ] Record CR-033, RTM and the versioned design/plan before implementation.

## TASK-133: implementation and developer tests (developer)

Owned files: `qa_master/case_conformance.py`, `qa_master/__main__.py`,
`tests/test_case_conformance.py`. No other file writes.

- [ ] Add a failing missing-candidate test through the public API:

```python
result = audit_method_cases(bundle, empty_library_for(bundle))
assert result['summary']['states']['MISSING'] == len(result['candidates'])
```

- [ ] Implement strict validation and bounded engine replay, exact typed matching,
  deterministic diagnostic arithmetic, hashes, Markdown and exclusive atomic I/O.
- [ ] Add the CLI before campaign-state loading; preserve existing commands.
- [ ] Run `python -m unittest tests.test_case_conformance -v` and relevant CLI
  regressions; retain commands/counts and report any failures without erasing them.
- [ ] Self-review code; hand off exact Git revision for independent tests/review.

## TASK-134: docs/example delivery (documentation worker)

Owned files: README addition only near design usage, both source/bundled SKILL.md
entries, `qa_master/skills/codex/references/case-audit.md`, and
`qa_master/skills/codex/examples/method-cases.json`. Root owns lifecycle docs.

- [ ] Explain the ordinary chat trigger, source model limits and repair loop.
- [ ] Build a valid example for the packaged `examples/design-methods.json`.
  Include one intentional missing scenario so the visible example demonstrates
  the gap; do not teach a copy-binding trick as proof of prose correctness.
- [ ] Document JSON/Markdown invocations, no-overwrite and exact flags/schema.
- [ ] After implementation exists, run both example commands and validate README
  catalogue/install regressions without broad unrelated README reformatting.

## TASK-135: independent test (tester)

Owned files: `tests/test_case_conformance_independent.py`,
`docs/verification/case-conformance-independent-test-2026-10-23.md`.

- [ ] Prepare tests from the spec, independently of developer fixtures.
- [ ] At frozen revision, exercise all five design methods and each mutation,
  missing/duplicate/gap/orphan/stale/empty case and documentation limitation.
- [ ] Validate input/size/depth/type limits and report no-clobber/link safety.
- [ ] Run fresh wheel plus standalone invocation outside the repository.
- [ ] Run required regression once; retain failures and separate platform skips.

## TASK-136: independent review (reviewer)

Owned file: `docs/verification/case-conformance-independent-review-2026-10-23.md`.

- [ ] Inspect frozen code/spec/installed evidence and catalogue integrity.
- [ ] Classify findings P0–P3, require correction of material issues and re-review.
- [ ] Verify no exact-binding, directory-count or CI result is sold as general
  semantic quality or overall superiority.

## Completion and delivery

- [ ] Orchestrator records task-to-commit/test trace and all limits in the RTM.
- [ ] Commit reviewed code/docs; push the authorized repository branch, create a
  PR, inspect CI, merge the accepted increment and verify remote main readback.
- [ ] Report the concrete new capability and current evidence; do not claim
  real host discovery, model benchmark quality, acceptance or release.
