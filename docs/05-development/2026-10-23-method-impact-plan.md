# Method Change Impact Implementation Plan

> Execute through distinct implementation, independent testing and review owners.
> Continue the user's authorized roadmap; do not request routine execution choices.

**Goal:** show which old case rows need review after a declared finite-model change.
**Architecture:** additive comparison overlay; typed formal vector groups, separate
context reasons, baseline audit and existing safe I/O, private Markdown rendering.
**Tech Stack:** Python 3.10+, stdlib, unittest, Windows/Linux.
**Spec:** DES-063; DOC-METHOD-IMPACT-REQ-001; CR-034.

## Constraints

5 MiB per input, JSON depth32, each replay<=10,000 candidates, <=10,000 cases and
<=50,000 rows/gaps. No network/model/subprocess/state/external operations in the
feature. Retain DRAFT_UNAPPROVED/NOT_EXECUTED. No semantic equivalence, rename,
safe-to-skip, execution, approval, resolved-defect or overall-superiority claim.

## TASK-137 — requirements/design/governance (orchestrator)

- [x] Read latest main/status/history and CR-033 evidence; inspect existing code.
- [x] Obtain independent requirement/architecture investigations and fix DES-063.
- [ ] Register CR/RTM/actual assignments before implementation.

## TASK-138 — pure comparison and CLI (developer)

Own `qa_master/method_impact.py`, additive edits to `qa_master/__main__.py`,
`tests/test_method_impact.py`. Preserve `case_conformance.py`/design engine bytes.

- [ ] Write failing source-only-churn test: source digest changes candidate IDs,
  but all deltas RETAINED_VECTOR with review/rebind reasons and no ADDED/REMOVED.
- [ ] Implement fixed DES-063 schema and indexed exact grouping; typed context
  comparisons, baseline issues/row identities, obligation/gap/unknown handling.
- [ ] Add strict input/CLI/file handling through reviewed CR-033 helpers; escape
  private Markdown fields; carry all hashes/counts/limits; no raw exception echo.
- [ ] Run `python -m unittest tests.test_method_impact -v` plus existing audit
  regression; self-review and hand off source for independent verification.

## TASK-139 — chat instructions and example (documentation worker)

Own a concise README addition, both Skill entry files, bundled
`references/method-impact.md` and `examples/design-methods-after.json`.

- [ ] Explain before/after+old-case-library inputs are prepared by the Agent.
- [ ] Base after-example on packaged design-methods.json with only source SHA
  descriptor changed; command consumes existing method-cases.json. Document no
  false ID churn, but review/rebinding still required; original example has one
  intentional missing scenario, which stays explicit.
- [ ] Verify source and installed command examples after code freeze; keep
  catalogue/install tables intact. No new mandatory dependency/credential.

## TASK-140 — independent black-box QA (tester)

Own `tests/test_method_impact_independent.py` and
`docs/verification/method-impact-independent-test-2026-10-23.md` plus its evidence.

- [ ] Build fixtures independently covering all five methods and test-model IDs.
- [ ] On frozen source, test unchanged/source-only/context/value/type/rename/
  stale/duplicate/gap/obligation/unmodeled changes and row/count identity.
- [ ] Check strict parser/byte/depth/no-clobber/link/reparse behavior, no mutation,
  escaped Markdown, no campaign creation and deterministic results.
- [ ] Use one clean Git archive built wheel -> offline venv -> installed module
  -> installed Skill helper test in the same fixture (avoid duplicate builds).
  Use installed example paths, durable UTF-8 logs and explicit exit checks.
- [ ] Preserve failures/skips; root runs full cross-platform CI instead of
  parallel redundant local full-suite discovery.

## TASK-141 — independent review (reviewer)

Own `docs/verification/method-impact-independent-review-2026-10-23.md`.

- [ ] Review frozen contract/code, false-equivalence/skip claims, ambiguity,
  context changes, baseline/obligation/gap persistence and output safety.
- [ ] Send reproducible material findings as a batch; repair then recheck.
- [ ] Bind final verdict to actual code/tests/installed evidence; retain history.

## Delivery

- [ ] Persist source/test/review/CI evidence in RTM and change/work registers.
- [ ] Push reviewed branch to the existing repository, create PR, inspect current
  source CI, merge the authorized increment and read back main.
- [ ] Explain the new review/proposal capability and actual limits to the user.
