# CR-033 case conformance independent review

- Review task: `TASK-136`
- Requirements: `REQ-029`, `REQ-030`, `REQ-031`, `NFR-013`
- Design: `DES-062`
- Initial reviewed subject: `7bd6b9c4024ed3135937b765a887bf64f03259bc`
- Intermediate repaired subject: `195fb30774603a74eedc919479572ea5c7abb009`
- Final reviewed product subject: `e9e141fa1319c37d2166b1bebc69cee6f77ab1c8`
- Document State: DRAFT
- Evidence Status: VERIFIED for the bounded source review and commands below
- Verdict: **PASS**
- Final unresolved findings: **P0 0 / P1 0 / P2 0 / P3 0**

## Scope and conclusion

The final product subject conforms to the fixed finite-model audit contract in
the reviewed scope. It recomputes the authoritative design candidates, compares
typed method data and exact requirement/source/oracle sets, retains missing,
duplicate, gap, mismatch, orphan and engine-obligation states, and keeps JSON and
Markdown results at `DRAFT_UNAPPROVED` / `NOT_EXECUTED`. Exact binding remains a
formal representation result only; it does not establish model completeness,
case-prose semantics, executability, approval, test execution, product acceptance,
release readiness or superiority over another Skill.

This review covers `qa_master/case_conformance.py`, the additive CLI route,
packaged/source instructions and example, relevant requirements/design/plan, and
the developer and independent conformance fixtures. It does not make a G0-G11
decision. All project Gates remain governed by the central Gate Register.

## Finding history and recheck

### P2-001 — exact output and bounded-input contract drift — resolved

The initial subject added an undeclared `summary.state` key although the plan
fixed the summary's exact keys. Its pure dictionary API also lacked the file
API's input-size boundary, and the implementation used 5,000,000 bytes while the
governing design specified 5 MiB (5,242,880 bytes). Exact-schema consumers could
therefore reject a nominal report, and inputs inside the declared binary boundary
could be rejected.

The repaired subjects remove the extra key, bound canonical pure-API inputs, use
`5 * 1024 * 1024`, accept an exactly 5,242,880-byte valid JSON input, and reject
the next byte. Final recheck passed the developer boundary regression and
independent `TC-CC-008`.

### P2-002 / CASE-R1 — duplicate precedence hid incomplete case documentation — resolved

On `7bd6b9c`, one case with `expected: ""` and two rows for one candidate returned
`DUPLICATE`, empty diagnostic codes and no `CASE_DOCUMENTATION_INCOMPLETE`
finding. This violated the requirement that incomplete cases receive a finding
even when their rows cannot be exactly represented.

The final code emits a case-level documentation finding independently of
candidate-state precedence. Developer and independent `TC-CC-005a` regressions
passed on the final subject.

### P2-003 / CASE-R2 — public Markdown rendering accepted untrusted report claims — resolved

The initial public renderer checked only `schema_version`. A crafted candidate ID
containing a pipe and newline injected a Markdown table row; a malformed report
raised raw `KeyError`. The first repair also accepted forged `PASS` diagnostic
codes, Boolean schema/count fields and nonzero counts for a model absent from the
candidate set. It could additionally reject a structurally possible finding set
because it reused the scenario-row limit as the finding limit.

The final renderer validates the exact report variants, typed counters,
candidate state/code coherence, known candidate/finding codes, bounded engine
obligation-code families, per-model arithmetic and a finding bound derived from
the input limits. Invalid reports fail with the value-free `INVALID_REPORT` code.
Developer checks and independent `TC-CC-007b` / `TC-CC-007ba` passed; a forged
`PASS` report is no longer renderable.

### P2-004 / CASE-R3 — audit IDs were incompatible with valid design-engine outputs — resolved

The initial audit required every reference ID to start with an alphanumeric
character. The authoritative engine permits leading `._:-` for model/source/
oracle IDs and permits unique nonempty requirement strings, including spaces and
Chinese text. Valid engine candidates such as requirement `_REQ` therefore could
not be exactly bound and failed with `INVALID_REFERENCE_SET`.

The final implementation follows each producer's contract: engine-alphabet IDs
retain the engine alphabet, while requirement IDs remain unique nonempty strings
and are not interpolated into Markdown. Developer coverage and independent
`TC-CC-007d` passed on the final subject.

### P3-001 / CASE-R4 — Markdown orphan findings omitted the owning case — resolved

An orphan scenario finding carried both candidate and case IDs in JSON, but the
initial Markdown chose only the candidate ID. Multiple cases referring to the
same unknown candidate were indistinguishable. The final renderer prints every
available candidate/case identity; the developer regression and independent
`TC-CC-007c` passed.

### P2-005 / CASE-R5 — Markdown omitted both audited-input identities — resolved

The initial Markdown did not include `design_input_sha256` or the normalized
`case_library_sha256`, so a standalone readable report could not identify the
two inputs it reconciled. The final summary renders both validated digests.
Developer coverage and independent `TC-CC-007c` passed.

### P2-006 — identical duplicate gaps made the renderer reject its own report — resolved

On intermediate subject `195fb307`, two identical gaps correctly produced
`DUPLICATE` / `GAP_DUPLICATE` with one normalized `gap_reasons` value. The public
renderer incorrectly required more than one unique reason and rejected the audit's
own report with `INVALID_REPORT`.

Final subject `e9e141f` accepts one or more normalized reasons when the state/code
pair is `DUPLICATE` / `GAP_DUPLICATE`, without relabelling the ambiguity as
coverage. Developer and independent `TC-CC-005b` passed.

## Independent observations

1. Typed canonical comparison distinguishes Boolean `true` from integer `1` and
   preserves decimal strings exactly. Independent `TC-CC-003` passed.
2. Missing candidates remain in the denominator even when other rows retain the
   same requirement trace. Duplicate rows, explicit gaps, gap/case conflicts and
   orphan rows do not become exact bindings.
3. Candidate lookup is indexed. A reviewer-constructed three-model Cartesian
   input estimated 12,288 replay rows and returned
   `CANDIDATE_LIMIT_EXCEEDED` in 0.000148 seconds before design enumeration.
4. Canonical library identity sorts case/scenario/gap order and reference-ID sets
   while preserving step order and typed method/text values. Pure and file APIs
   return the same normalized digest.
5. File output is exclusive and does not overwrite inputs or existing paths.
   The final independent Windows junction test rejected linked input and output
   ancestors and preserved the protected target. The ordinary symlink fixture is
   unavailable to this Windows account and is not reported as passed.
6. Diagnostics expose bounded IDs, codes and hashes rather than authored source
   prose. The installed instructions repeatedly state the formal-only and
   unexecuted limits; no source or document claims general semantic quality.

## Reviewer verification

Commands were run from `D:\QA-Master-Compare` against final product subject
`e9e141fa1319c37d2166b1bebc69cee6f77ab1c8`:

```powershell
python -W error::ResourceWarning -m unittest tests.test_case_conformance -v
python -W error::ResourceWarning -m unittest -v `
  tests.test_case_conformance_independent.CaseConformanceIndependentTests.test_tc_cc_003_typed_bool_integer_and_decimal_strings_do_not_coerce `
  tests.test_case_conformance_independent.CaseConformanceIndependentTests.test_tc_cc_005a_duplicate_precedence_retains_empty_expected_documentation_finding `
  tests.test_case_conformance_independent.CaseConformanceIndependentTests.test_tc_cc_005b_repeated_identical_gap_is_renderable_as_one_reason `
  tests.test_case_conformance_independent.CaseConformanceIndependentTests.test_tc_cc_007b_renderer_rejects_malformed_public_reports_without_keyerror `
  tests.test_case_conformance_independent.CaseConformanceIndependentTests.test_tc_cc_007ba_renderer_rejects_forged_pass_and_inconsistent_summary `
  tests.test_case_conformance_independent.CaseConformanceIndependentTests.test_tc_cc_007c_markdown_identifies_owning_case_and_both_input_identities `
  tests.test_case_conformance_independent.CaseConformanceIndependentTests.test_tc_cc_007d_requirement_and_reference_identifiers_are_data_not_markup `
  tests.test_case_conformance_independent.CaseConformanceIndependentTests.test_tc_cc_008_file_loader_rejects_malformed_json_and_keeps_existing_output `
  tests.test_case_conformance_independent.CaseConformanceIndependentTests.test_tc_cc_009a_windows_junction_ancestor_is_rejected_without_touching_target
git diff --check 195fb30774603a74eedc919479572ea5c7abb009..e9e141fa1319c37d2166b1bebc69cee6f77ab1c8
```

Observed results: 13/13 developer conformance tests passed in 0.490 seconds;
the nine reviewer-selected independent adversarial checks passed in 0.211
seconds; the final repair diff check passed. These are bounded local source
observations.

The tester-owned final scoped run then completed with exit 0 on the same
`e9e141f` product subject: 21 tests ran in 194.349 seconds, with 20 passed and
the ordinary Windows symbolic-link fixture skipped for unavailable privilege.
The native Windows junction fixture passed. `TC-CC-010` built from a clean Git
archive, created a fresh virtual environment, installed its wheel offline and
ran the consumer CLI outside the checkout. The retained evidence is under
`docs/verification/evidence/cr033/task-135-e9e141f/scoped-*`. An earlier full
repository discovery attempt was intentionally terminated as outside TASK-135
scope and is explicitly not counted as a product result.

The separate installed-Skill helper evidence preserves its unsuccessful setup
history rather than rewriting it as a product pass. The first wrapper ended
after successfully building the clean-archive wheel and left its exit file
empty; it did not reach an installed helper result and is not counted. The
resumed harness then installed that same 6,389,424-byte wheel, SHA-256
`0f8f203b5f080b1947ee7e1faea0a110c9b5a6eb5af66c4e79ce43fad808ac73`,
offline into a fresh virtual environment, confirmed the isolated import from
its `site-packages`, and installed the Codex Skill with 5,885 files and
`NOT_EXECUTED`. Its first helper call returned exit 2 / `INPUT_IO_ERROR`
because the tester copied inputs from a non-packaged source path. After
correcting only that fixture path to the installed Skill examples, without a
product patch, wheel rebuild or reinstall, the same installed helper exited 0
and generated a 1,663-byte Markdown report, SHA-256
`B29B086731B73C702CB1F887B1C54F4AE0628F1D7F32E801137EDFB25F72922C`,
with `DRAFT_UNAPPROVED`, `NOT_EXECUTED` and candidate denominator 10. The
machine-readable result and raw attempt logs are retained under
`docs/verification/evidence/cr033/task-135-e9e141f/`.

[GitHub Actions run `39953357673`](https://github.com/leongibhub/QA-Master-Skill/actions/runs/39953357673)
for the same final commit completed all four
configured Ubuntu/Windows and Python 3.10/3.12 jobs successfully. Each job ran
848 tests with zero failures and zero errors; each Ubuntu job reported 11
skips and each Windows job reported 3 skips. The retained decoded Ubuntu 3.12
record identifies job `120413033369`, 159.864 seconds. This CI observation is
cross-platform regression evidence only and does not expand the formal audit's
claim boundary.

No unresolved P0-P3 finding remains in the reviewed scope. This permits the
bounded CR-033 code-review verdict above; it is not human acceptance, release
approval, or a project Gate `PASS`.
