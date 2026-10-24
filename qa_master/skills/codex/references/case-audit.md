# Finite-model case audit

Use this audit after an Agent has created draft test cases from a strict finite
design model. The QA user stays in normal chat: ask the Agent to design cases,
audit their declared finite-model scenarios, repair findings, and return the
draft. The Agent prepares the campaign bundle and case-library JSON; the user
does not hand-fill them.

The audit recomputes `design_methods(bundle)` and compares each declared
scenario to its current candidate. It is useful for visible boundary points,
decision combinations, state transitions, pairwise rows and combinatorial rows.
It preserves unresolved engine obligations and reports missing, duplicate,
mismatched, stale and unknown bindings.

## Agent workflow

1. Read the sources and create the strict design bundle from explicit facts. Do
   not infer a missing source, oracle, setup, observable or cleanup fact.
2. Author ordinary draft cases with concrete preconditions, steps and expected
   results. Alongside every finite-model scenario, record the exact candidate
   ID, typed method data, requirement IDs, source-reference IDs and
   oracle-reference IDs.
3. Put those records in a case library and run the audit before delivering the
   cases. Review each finding against the source and case prose, repair only
   justified omissions or mismatches, then use a new output path for the next
   audit.
4. Return the cases and any genuine unresolved gaps. An audit report is not a
   requirement baseline, approval, test execution result or quality pass.

From a source checkout:

```text
python -m qa_master audit-method-cases --input bundle.json --cases cases.json --output audit.json
python -m qa_master audit-method-cases --input bundle.json --cases cases.json --output audit.md --format markdown
```

From an installed Skill, resolve the Skill directory and use its bundled helper:

```text
python -I "<skill>/scripts/qa.py" audit-method-cases --input bundle.json --cases cases.json --output audit.json
python -I "<skill>/scripts/qa.py" audit-method-cases --input bundle.json --cases cases.json --output audit.md --format markdown
```

`--input`, `--cases` and `--output` are each required exactly once. JSON is the
default report; `--format markdown` renders the same findings for reading. The
command refuses an existing output and never overwrites an input, so choose a
new report path on every run. Exit code 0 only means that a report was created;
validation or I/O rejection returns exit code 2 and is not a quality result.

## Rejection and retry

Malformed artifact fields are rejected with a stable error code; correct the
declared JSON rather than expecting a fallback report. `OUTPUT_IO_ERROR` means
report writing, its preparation, or cleanup failed. If cleanup fails after
atomic publication, the target report may already exist: inspect that target
before retrying. Do not assume silent success or automatic rollback. The command
never overwrites an input or an existing output path.

## Case-library contract

The root has exactly these keys:

```json
{
  "schema_version": 1,
  "design_input_sha256": "<design_methods input_sha256>",
  "cases": [],
  "gaps": []
}
```

Each case has exactly `id`, `title`, `preconditions`, `steps`, `expected` and
`scenarios`. Each scenario has exactly `candidate_id`, `method_data`,
`requirement_ids`, `source_ref_ids` and `oracle_ref_ids`. The ID sets must be
unique. `method_data` uses type-sensitive JSON equality: `true` differs from
`1`, and declared decimal strings remain strings.

Use a `gaps` row only for a genuine unresolved obligation. Each has exactly
`candidate_id` and one `reason_code`: `SOURCE_MISSING`, `ORACLE_MISSING`,
`SETUP_MISSING`, `OBSERVABLE_MISSING`, `CLEANUP_MISSING` or `OTHER`. A gap is
not a represented scenario, and a gap plus a case scenario for the same
candidate is a conflict.

The report binds a library to the current `design_input_sha256`. The digest
detects changes to the declared model and its recorded source descriptors. It
does not open arbitrary external files or URLs named by source locators: if
their bytes change without refreshed declared metadata, this audit cannot
detect the change. Refresh the source facts and model before review when that
is possible; do not reuse a stale digest. Requirement IDs alone do not
represent a finite candidate.

`case_library_sha256` is a canonical digest, not a raw input-file hash. It
normalizes case, scenario and gap ordering and sorts ID sets; the order of case
steps remains significant. The summary reports `assessment: UNASSESSED` when
there are no candidates, otherwise `ASSESSED`; neither state is a coverage or
quality pass. Candidate rows retain sorted `gap_reasons`, and the report keeps
root findings for orphan rows and other non-candidate diagnostics.

## What an exact binding does not establish

The audit checks the formal representation of a finite model only. It does not
judge whether human-readable prose is semantically correct, whether steps can
run in a real environment, whether an expected result is sufficient, whether a
case is approved, or whether any test ran. Do not use copied metadata or a
generic phrase such as “satisfy the oracle” as a substitute for a concrete
expected result. The Agent must inspect the sources and review the prose before
delivery.

`examples/method-cases.json` binds the packaged
`examples/design-methods.json` model. It deliberately omits one declared amount
candidate and has no `gaps`, so the report visibly contains `MISSING`. This is a
teaching finding, not an executed defect or a claim that all other case prose is
business-correct.
