# CR-036 reviewable case-library draft delivery

Artifact: `EVD-CR036-DELIVERY-001`; Document State: `DRAFT`.

- Baseline: `ce9da58605dfbdaa27ef8749ee5d20070175b54d`.
- Frozen product: `ddb2fc2665b2b6f044eba9bf56a70de69211db7e`.
- Test-only portability correction: `83afa5837bac375d291ae9d4742a1b6dd4f8540e`.
- PR: https://github.com/leongibhub/QA-Master-Skill/pull/11.
- Scope: REQ-037–040, NFR-015 and inherited NFR-003; DES-064/ADR-007;
  TASK-147–151; TC-PROP-001–011.

## Behavior

`propose-method-case-library` compares before/after finite models and an old
case library. Eligible exact and unambiguous rows receive an after-version
binding in a separate proposed library. It preserves human-authored case prose
and scenario order, holds an entire case if any row is unsafe, holds every old
gap for review, and reports every still-missing after vector. It does not write
the old library or apply the proposal. Every result remains `DRAFT_UNAPPROVED`,
`NOT_EXECUTED`, `NOT_APPLIED` and requires human review.

The five bounded methods are boundary values, decision tables, state transitions,
pairwise and combinatorial models. Formal exactness establishes consistency with
the supplied model; it does not establish business correctness or source truth.

## Observed verification

| Evidence | Result / identity |
| --- | --- |
| Root focused regression | 43 tests passed: 9 developer, 11 independent source, 23 existing audit/impact; package branch was gated at that point. |
| Independent frozen consumer | One session `66660`, exit 0; 11/11 tests in 298.459 seconds, including clean archive, wheel, isolated install, module CLI and installed Skill helper. |
| Archive / wheel | 8,847,851 / 6,407,909 bytes; full hashes in `evidence/cr036/task150-final/final-run.md` and per-command records. |
| Installed Skill | 5,890 reported files; 1,077 source and runtime Python files. |
| Installed output | Module/helper byte-identical, 31,744 bytes; nested audit 17 EXACTLY_BOUND, 0 missing/duplicate/mismatch/gap. |
| Teaching example | 9 proposed cases/rows, 0 held, 1 missing vector; original case prose preserved. Four existing README catalogue checks passed. |
| Protected core | `case_conformance.py`, `method_impact.py`, `design_methods.py` unchanged from baseline. |
| Test-only correction | Local independent 11/11 PASS, 1.248 seconds (retained tester record) after correcting output-symlink collision precedence. |
| Full matrix | CI run `40080022358` at `83afa58`: all four jobs PASS; each 910 tests, 0 failures/errors, Ubuntu 12 skips / Windows 3 skips. See EVD-CR036-CI-001. |
| Independent final review | Source and installed evidence reviewed; final verdict recorded in the independent review report. |

Independent records: `case-library-proposal-test-2026-10-24.md` and
`case-library-proposal-review-2026-10-24.md`. Prototype BUG-027–031 were fixed
before freeze; see `../08-project-management/cr036-defect-record.md`.

## Retained failed attempts and limits

Initial independent collection failed because the feature module did not yet
exist; it was not eleven executed tests. A later source-CLI fixture used isolated
mode before installation and failed import; its harness was corrected. Neither
is attributed as a final product failure. Initial CI `40079455590` failed all four jobs on
the same fixture assertion about an existing output symlink (`OUTPUT_EXISTS`, not
`LINK_PATH_REJECTED`); its target remained protected. The failure remains in
`evidence/cr036/initial-ci-fixture-failure.md`. A separate symlink-input assertion
now verifies link rejection. No runtime or protected-core change was necessary.

Automatic shell safety rejected cleanup of the teaching-only temporary JSON:
`C:\Users\leon.wang\AppData\Local\Temp\qa-master-doc-proposal-ddb2fc\case-library-proposal.json`.
It remains outside the repository; no alternate deletion was attempted. This is
separate from the successful installed-test fixture cleanup and its final marker.

No business test was executed, no Jira/GitLab record was changed, and no human
acceptance, release, Gate PASS or overall competitor-superiority result is
inferred. Existing central Gate statuses remain unchanged. Runtime registration
is NOT_AVAILABLE; actual host owners are recorded in the work register.

## Chat entry

Ask the Agent: “Use QA Master to compare the old and new requirements/models
against my old case library. Generate a proposed new library, held cases and
missing-test followups; preserve my original cases and wait for my review.”
The Agent prepares structured inputs using the bundled reference; QA users do
not need to hand-author JSON. A reviewed nested library may be extracted to a
new file and audited against the after model. The envelope itself is not a
case-library input, and there is no apply operation.

## Publication — pre-merge snapshot

PR publication observed; merge and main readback PENDING at this document freeze.
Subsequent merge/main identity is recorded by Git history and the PR #11 body,
with actual user-facing readback; it must not be invented in this snapshot.
Product source remains
the frozen identity above; subsequent evidence-only commits must not change its
runtime, Skill guidance or README.
