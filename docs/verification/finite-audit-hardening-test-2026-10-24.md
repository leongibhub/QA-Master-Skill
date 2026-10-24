# TASK-142 finite-audit hardening independent test record

- Change: `CR-035` (prospective hardening)
- Tester: independent tester `/root/case_audit_tester`
- Initial RED subject: `16a73f765d3b8b86f69cd0b3f75ecc83e2416e71`; `qa_master/` then had no diff from `origin/main` at `8fcaba97c14a12f447d2898d1902fff05576e996`.
- Final repair subject: `8fc8533d4ec533bc5ba1ea66e6f24ef51a92f0f6`; installed-consumer evidence uses a clean `git archive` of this exact SHA.
- Environment: Windows, Python shown by the retained scoped commands; local source checkout and a fresh offline virtual environment for installed-consumer checks.
- Evaluation State: `IN_REVIEW`
- Evidence Status: `OBSERVED`
- Scope: bounded local API/CLI contract testing plus one clean archive/wheel/offline-install/installed-helper consumer check. No full local regression, remote execution, Jira operation, model invocation, approval, or release decision was performed.

## Requirements and test design

The prospective regression cases derive from the CR-033/CR-034 public APIs,
DES-062/063 bounded-input and stable-error contracts, and the user-facing CLI
promise that rejected input/I/O returns JSON with exit `2`. Fixtures are owned
by `tests/test_finite_audit_hardening_independent.py`; they do not import a
developer test fixture.

| Test case | Contract / risk | Observable expected result | Initial RED result | Final result |
| --- | --- | --- | --- |
| TC-FAH-001 | DES-063 context completeness; prevent false `NO_DECLARED_IMPACT` | Exact rows spanning boundary, decision table, state transition, pairwise, and combinatorial remain no-impact for identical inputs; changed declared requirement context selects `REVIEW_BINDING`. | PASS | PASS |
| TC-FAH-002 | DES-063 baseline and explicit-gap separation | A missing candidate gets `BASELINE_NONCONFORMANT`; a separately recorded gap remains a `REVIEW_GAP` followup and does not become an invented covered scenario. | PASS | PASS |
| TC-FAH-003 | REQ-029 / NFR-013 typed equality | Replacing a declared Boolean scenario value with its integer form produces `DATA_MISMATCH` and `REVIEW_BASELINE`, never `NO_DECLARED_IMPACT`. | PASS | PASS |
| TC-FAH-004 | DES-062 bounded malformed case-library input | JSON-valid object/list `reason_code` values reject through `CaseConformanceError.code`, `MethodImpactError.code`, and CLI JSON exit `2`; no report is created. | FAIL — BUG-021 proposed | PASS |
| TC-FAH-005 | DES-062 malformed model preflight | JSON-valid object `method` rejects through the public domain error, without an uncaught `TypeError`. | FAIL — BUG-022 proposed | PASS |
| TC-FAH-006 | DES-062/063 output safety and CLI I/O contract | An output below an existing regular-file parent preserves its sentinel and rejects through public domain errors / CLI JSON exit `2`, without a traceback. | FAIL — BUG-023 proposed | PASS |
| TC-FAH-007 | Public API format contract | JSON-valid unhashable `format` argument rejects with `INVALID_FORMAT`, without an uncaught `TypeError`. | FAIL — BUG-024 proposed | PASS |
| TC-FAH-008 | DES-062 bounded preflight | A valid sparse open-world state model with 128 states and 100 declared triggers retains its one explicit candidate instead of reserving an unused closed-world grid. | FAIL — BUG-025 | PASS |
| TC-FAH-009 | DES-062 public Markdown renderer | Forged impossible candidate-state/code and finding-shape variants reject as `INVALID_REPORT`; a genuine repeated-identical-gap report remains renderable. | FAIL — BUG-026 | PASS |
| TC-FAH-010 | DES-062/063 output setup recovery | Injected `mkdir` and `mkstemp` failures in each writer return `OUTPUT_IO_ERROR`; the sentinel remains and no output is created. | NOT EXECUTED | PASS |
| TC-FAH-011 | DES-062 aggregate preflight, closed world | A 128-state, 100-trigger closed-world model rejects before design replay with `CANDIDATE_LIMIT_EXCEEDED`. | NOT EXECUTED | PASS |
| TC-FAH-012 | DES-062/063 publication cleanup recovery | A temporary cleanup failure after publication returns `OUTPUT_IO_ERROR` while the published report is valid; a link-race primary error remains `OUTPUT_EXISTS` and creates no output. | NOT EXECUTED | PASS |
| TC-FAH-013 | DES-062 aggregate preflight | Four valid decision-table models have 2,501 typed assignments each (10,004 total) and reject before replay, although each individual model is within the 4,096-row engine bound. | NOT EXECUTED | PASS |

## Executed initial evidence

Command, complete stdout/stderr, and exit codes are retained under
[`evidence/cr035/task-142-initial`](evidence/cr035/task-142-initial/). The
expanded run retains the additional TC-FAH-007 reproduction:

```text
python -W error::ResourceWarning -m unittest tests.test_finite_audit_hardening_independent -v
```

The final initial command exited `1`: 9 tests ran in 0.168 seconds;
TC-FAH-001 through TC-FAH-003 passed, TC-FAH-004 through TC-FAH-008 errored,
and TC-FAH-009 recorded two failed forged-report subcases. This is an
intentional RED regression result on the pre-repair subject, not a product
acceptance result.

### BUG-021 proposed — unhashable gap reason escapes the audit boundary

Reproduction data has an otherwise valid current design digest and a known
candidate ID, with this gap:

```json
{"candidate_id":"<known candidate>","reason_code":{}}
```

`audit_method_cases` raised raw `TypeError: unhashable type: 'dict'` at
`case_conformance._validate_library` when it evaluated membership in
`_GAP_REASONS`; an array value fails in the same way. The CLI outer fallback
returned generic `COMMAND_REJECTED` rather than the audit rejection contract.
Expected repair behavior is `INVALID_GAP` via `CaseConformanceError.code`,
propagated unchanged by `MethodImpactError` and emitted by the CLI as
`{"status":"REJECTED","error":"INVALID_GAP"}` with exit `2`.

### BUG-022 proposed — unhashable model method escapes preflight

Changing one model's `method` to JSON object `{}` caused
`case_conformance._preflight` to evaluate membership in a method set and raise
raw `TypeError: unhashable type: 'dict'`. This occurs before the existing design
engine's stable malformed-schema adapter. The CLI again fell back to generic
`COMMAND_REJECTED`. Expected repair behavior is a stable `INVALID_SCHEMA`
domain rejection for the pure audit and `MethodImpactError` adapter.

### BUG-023 proposed — ordinary blocked output parent leaks traceback

The reproduction writes valid bundle and library files, then creates a regular
file named `blocker` containing `must-remain` and supplies
`blocker/audit.json` as output. Both `write_case_audit` and
`write_method_impact` raised raw `FileExistsError` at
`_write_exclusive`'s parent `mkdir`; both CLIs exited `1` with traceback and
no JSON response. The sentinel bytes remained unchanged and no output was
created, so no clobber was observed. Expected repair behavior is
`OUTPUT_IO_ERROR`, CLI exit `2`, and the existing no-clobber observation.

### BUG-024 proposed — unhashable public format escapes both writers

Both public file APIs accept a keyword-only `format` argument. Passing the
JSON-valid Python value `{}` to either `write_case_audit` or
`write_method_impact` raised raw `TypeError: unhashable type: 'dict'` during
set membership before a type check. The CLI parser limits its string flag, but
the direct public APIs still violate their stable value-free error boundary.
Expected repair behavior is `INVALID_FORMAT` through the respective domain
error class, before any file write.

The four BUG IDs are proposed for root registration. They remain open until a
separately frozen repair subject has independent retest evidence.

### BUG-025 — open-world state preflight reserves a nonexistent grid

A valid standalone state-transition model has 128 nonterminal states, 100
triggers, one explicit valid `S0` to `S1` transition, and `closed_world:false`.
`design_methods` returns one candidate and zero obligations, but
`audit_method_cases` rejects it before enumeration with
`CANDIDATE_LIMIT_EXCEEDED` by multiplying states by triggers as if the
closed-world undeclared-pair candidates existed. Expected behavior is a normal
audit report with denominator one and state `MISSING` for the empty library.

### BUG-026 — public renderer accepts reports no audit can produce

Starting from a genuine report with a `MISSING` candidate, changing that row to
`MISMATCH` with code `GAP_DUPLICATE` and reconciling summary counts rendered
successfully despite there being no cases or gaps. A second forged variant
appended `{"code":"ORPHAN_CASE","candidate_id":"<real candidate>"}` and
reconciled `finding_count`; it also rendered successfully. Those combinations
are impossible from `audit_method_cases` and permit a public renderer to show
forged diagnostics. Expected behavior is `INVALID_REPORT`. The regression also
keeps a genuine two-identical-gap report renderable as `DUPLICATE` with
`GAP_DUPLICATE` and one deduplicated reason.

At the time of this initial RED record, BUG-025 and BUG-026 were root-assigned
open findings and all six BUG IDs required a separately frozen repair subject
and independent retest evidence. That subsequent retest is recorded below;
formal defect lifecycle state remains in the registered defect records.

## Final independent retest evidence

The final local scoped command is retained as byte-preserved stdout/stderr and
an exit code under
[`evidence/cr035/task-142-final`](evidence/cr035/task-142-final/):
`scoped-13-valid-exit.txt` records exit `0`; its paired byte-preserved stderr
records all 13 independent cases `OK` in 0.966 seconds. The
first 12 cases are the frozen fixture set; TC-FAH-013 is a test-only
post-freeze aggregate-budget regression. Thus the local count is not the CI
frozen-corpus count.

An earlier TC-FAH-013 strengthening attempt is retained as
`scoped-13-final-*`: it exited `1` because its proposed 3,500-record
state-transition fixture exceeds the design engine's own 512-transition state
limit (`STATE_LIMIT_EXCEEDED`). That was a fixture error, not a product finding.
The final decision-table fixture above explicitly proves each 2,501-row model
is independently valid before it tests the aggregate preflight rejection.

The repaired behavior above is independently observed at the stated final
subject. This test record does not make a defect-closure or release decision;
the registered BUG records remain the system of record for their lifecycle
state.

### Clean installed-consumer evidence

One coherent retained command chain used `git archive` of
`8fc8533d4ec533bc5ba1ea66e6f24ef51a92f0f6`, built the wheel with
`--no-deps --no-build-isolation`, installed it offline into a fresh virtual
environment, installed the Codex Skill into a fresh consumer directory, and
then used both `python -I -m qa_master` and the installed
`skill/scripts/qa.py` helper. Its durable command log has 19 commands: 13
normal commands exited `0`, and the six deliberate CLI rejection checks exited
`2` with only their prescribed JSON result. The foreground wrapper's own final
exit record is `NOT_AVAILABLE`, because that process started before durable
wrapper exit recording was added; therefore this is command-level observed
evidence, not an inferred end-to-end wrapper PASS. The complete command arguments,
captured stdout/stderr and exit codes are in
[`delivery-commands.json`](evidence/cr035/task-142-final/delivery-commands.json);
the source/archive/wheel/output hashes and report values are in
[`delivery-manifest.json`](evidence/cr035/task-142-final/delivery-manifest.json).

The installed module and Skill helper both produced the same audit JSON hash
`218efedd75d3f1935c2d567e1bfe18e181efba3e5646344fb2e8cebbc73c9cbd` and
the same Markdown hash
`b29b086731b73c702cb1f887b1c54f4ae0628f1d7f32e801137edfb25f72922c`.
The normal audit reports `DRAFT_UNAPPROVED`, `NOT_EXECUTED`, denominator 10;
the impact report reports `DRAFT_UNAPPROVED`, `NOT_EXECUTED`, and nine review
cases. Packaged malformed gap and method inputs yielded `INVALID_GAP` and
`INVALID_SCHEMA`; blocked output parents yielded `OUTPUT_IO_ERROR` for both
CLI commands; the direct Python public APIs yielded `INVALID_FORMAT` for
`format={}`. Those rejection outputs had exit `2` (where CLI), empty stderr,
and no private temporary-root path or traceback.

The installer reported 5,888 payload files. A filesystem count after helper
execution was 5,900; both values are retained without inferring a packaging
discrepancy or attributing the difference to a specific file type. The structured chain
reconciliation, including the manifest hash, is
[`delivery-result.json`](evidence/cr035/task-142-final/delivery-result.json).

The two-command `delivery-commands-interrupted-foreground.json` file is an
`EARLY_PARTIAL_SNAPSHOT_OF_COMPLETED_0VTU_CHAIN`, not a separate attempt: it
shares the completed chain's `t142-0vtu5dyc` temporary root. The separately
started `t142-xaxef1hn` detached retry was interrupted after concurrent-run
discovery and is retained as historical non-PASS evidence.

### Completed isolated confirmation

To close the missing foreground-wrapper exit record without overwriting the
historical chain, one final isolated confirmation used the same wrapper in
[`evidence/cr035/task-142-confirmed`](evidence/cr035/task-142-confirmed/).
It ran directly in tool session `36511`, whose returned exit code and the
wrapper's durable `delivery-script-exit.txt` are both `0`. The isolated command
log is coherent: 19 commands, 13 normal exit-`0` commands and six prescribed
exit-`2` rejection commands. It again used an archive of the exact final SHA,
an offline wheel install, and an installed-Skill helper. The confirmation's
structured result, including the archive hash, wheel hash, manifest hash,
installer-reported 5,888 files and post-helper count of 5,900, is
[`delivery-result.json`](evidence/cr035/task-142-confirmed/delivery-result.json).
This completed confirmation supplies the installed-consumer completion evidence;
the older `t142-0vtu5dyc` command chain remains useful observed history.

No full local regression was run. Cross-platform regression evidence, Gate
status, defect closure, and release decisions are outside this independent
tester's scope.
