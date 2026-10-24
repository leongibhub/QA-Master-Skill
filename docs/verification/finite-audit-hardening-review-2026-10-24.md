# Finite-audit hardening independent review

- Review task: `TASK-143`
- Prospective change: `CR-035`
- Governing designs: `DES-062`, `DES-063`
- Merged product subject: `8fcaba97c14a12f447d2898d1902fff05576e996`
- Reviewed runtime subject: `c2e795716b9b37644476978402ecf50b32d281d4`
- Initial checkout subject: `16a73f765d3b8b86f69cd0b3f75ecc83e2416e71`
  (no `qa_master/` difference from the merged product)
- Frozen repaired subject: `8fc8533d4ec533bc5ba1ea66e6f24ef51a92f0f6`
- Document State: DRAFT
- Evidence Status: OBSERVED for the bounded public-API/CLI reproductions below
- Initial verdict: **CHANGES_REQUESTED**
- Initial unresolved findings: **P0 0 / P1 0 / P2 5 / P3 1**
- Frozen-source re-review: **PASS**
- Current unresolved findings: **P0 0 / P1 0 / P2 0 / P3 0**
- Installed-delivery evidence: **PASS** for the exact frozen source
- Bounded independent-review verdict: **PASS**
- Current CI status: **PASS** — four-job frozen-runtime workflow

## Scope and claim boundary

This review re-examines the existing finite case-conformance and change-impact
flows after their earlier bounded PASS reviews. It covers stable malformed-input
and output errors, preflight correctness, and the public audit renderer's report
precision. It also inspected candidate/context matching, baseline findings,
explicit gaps, unresolved obligations, row actions, typed values, canonical
identities and no-impact limits; no additional material defect was reproduced in
those paths on the initial subject.

The review does not assess a new subsystem, execute authored product tests,
rebuild a package, run the full suite, or make an acceptance, release, or Gate
decision. All project Gates remain controlled by the central Gate Register and
remain `BLOCKED`.

## Initial findings

### P2-001 / BUG-021 proposed — malformed gap reason escapes the audit domain

With an otherwise valid bundle/library and current digest, setting one gap to
`{"candidate_id":"<known>","reason_code":{}}` makes
`audit_method_cases` raise raw `TypeError: unhashable type: 'dict'`. A list has
the same result. `_validate_library` tests membership in `_GAP_REASONS` before
checking that `reason_code` is a string.

This violates DES-062/NFR-013's stable, value-free malformed-input contract.
The impact wrapper converts the raw exception to generic `INVALID_SCHEMA`, while
the audit CLI falls through to `COMMAND_REJECTED`; neither preserves the
specific `INVALID_GAP` diagnosis expected for that field. The independently
authored TC-FAH-004 reproduced the same failure.

### P2-002 / BUG-022 proposed — malformed model method escapes preflight

Changing a model's JSON-valid `method` value to `{}` makes
`audit_method_cases` raise raw `TypeError: unhashable type: 'dict'` before the
design engine can return its stable malformed-schema result. `_preflight` uses
the unvalidated value in set membership. `analyze_method_impact` happens to
adapt the same exception to `INVALID_SCHEMA`, so the two public Python
boundaries disagree.

This is a second validation root cause and should be fixed at preflight rather
than relying on the impact wrapper. TC-FAH-005 independently reproduced it.

### P2-003 / BUG-023 proposed — blocked output parent leaks traceback and path

For valid inputs, create a regular file `blocker` with sentinel bytes and choose
`blocker/audit.json` as output. Both `write_case_audit` and
`write_method_impact` raise raw `FileExistsError` from the parent-directory
`mkdir`. Both CLIs exit `1`, emit a traceback containing the supplied path, and
produce no JSON rejection. The sentinel remains intact and no output is
created, so no clobber occurred.

`_write_exclusive` performs `path.parent.mkdir(...)` and `tempfile.mkstemp(...)`
outside its `OSError` adapter. DES-062/063 require stable value-free I/O failure
and CLI exit `2`; this ordinary invalid output shape must become
`OUTPUT_IO_ERROR`. TC-FAH-006 independently reproduced the failure for both
writers and CLIs.

The same boundary must include temporary-file cleanup. Fault-injecting
`os.unlink` to raise `PermissionError` after the exclusive link succeeds makes
the public writer leak that raw exception while the requested output already
exists. Cleanup failure must not expose exception text or mask an in-flight
domain error; its observable failure remains the stable `OUTPUT_IO_ERROR`.

### P2-004 / BUG-025 — open-world state preflight rejects a valid one-candidate design

A valid open-world state model with 128 states, 100 declared triggers and one
explicit valid transition succeeds through `design_methods`: one candidate,
zero obligations and one logical row. `audit_method_cases` rejects that same
bundle with `CANDIDATE_LIMIT_EXCEEDED`; method impact inherits the rejection.

For every state model, `_preflight` estimates
`len(states) * len(triggers) + len(transitions)`. The state engine enumerates
the Cartesian state/trigger grid only for `closed_world: true`; for open-world
models its logical keys are the explicit grouped transitions. The preflight
therefore counts 12,801 units for work that produces one row. This is a material
false rejection of an engine-valid, low-work design, rather than a bound on its
actual finite replay allocation.

### P2-005 / BUG-026 — public renderer accepts impossible diagnostic variants

Starting from a genuine audit report, change one candidate from `MISSING` to
`MISMATCH`, leave `case_ids` and `gap_reasons` empty, set
`codes:["GAP_DUPLICATE"]`, and reconcile the total/per-model state counters.
`render_audit_markdown` accepts and prints the impossible combination. It also
accepts `{"code":"ORPHAN_CASE","candidate_id":"<known>"}` after incrementing
`finding_count`, although the fixed ORPHAN_CASE variant is
`{code, case_id}`.

`_validate_report` currently accepts any nonempty known candidate code for a
`MISMATCH` and validates finding key shapes independently of each finding code.
This reopens the report-precision class addressed during TASK-136: a public
arbitrary-report renderer can present internally impossible known-code claims
as a valid audit. Unhashable renderer fields do correctly become
`INVALID_REPORT`; the defect is semantic variant coherence, not markup
injection.

### P3-001 / BUG-024 proposed — unhashable public format escapes both writers

Both public writers accept a keyword-only `format` argument. Passing the
JSON-valid Python value `{}` to either `write_case_audit` or
`write_method_impact` raises raw `TypeError: unhashable type: 'dict'` during
set membership before either domain can issue `INVALID_FORMAT`. The CLI parser
constrains its flag to strings, so this is limited to direct Python callers and
is classified P3. The reviewer reproduced the behavior independently after
TC-FAH-007 identified it.

## Initial verification evidence

Reviewer probes ran from `D:\QA-Master-Compare` without product edits. They
used the public Python APIs and subprocess CLI entry points. Observed results:

- malformed model method: audit raw `TypeError`; impact `INVALID_SCHEMA`;
- malformed gap reason: audit raw `TypeError`; impact `INVALID_SCHEMA`;
- blocked regular-file output parent: both writers raw `FileExistsError`; both
  CLIs exit `1` with traceback/path disclosure;
- fault-injected temporary cleanup: raw `PermissionError` after output link;
- valid open-world state model: design engine one candidate/one logical row,
  audit `CANDIDATE_LIMIT_EXCEEDED`;
- two impossible but arithmetically reconciled public report variants rendered
  successfully;
- both writers raised raw `TypeError` for `format={}`.

The separate tester's final initial scoped command ran nine tests: TC-FAH-001
through TC-FAH-003 passed; TC-FAH-004 through TC-FAH-008 errored; and
TC-FAH-009 recorded two failed forged-report subcases. Exit was `1`. That
independent RED evidence is retained under
`docs/verification/evidence/cr035/task-142-initial/`. It corroborates all six
findings but is not substituted for this review's source inspection and
public-boundary probes.

## Frozen repair and source re-review

The repaired source is frozen at
`8fc8533d4ec533bc5ba1ea66e6f24ef51a92f0f6`. Working copies of
`qa_master/case_conformance.py` and `qa_master/method_impact.py` matched their
frozen Git blobs exactly during re-review.

| Finding | Frozen-source disposition |
| --- | --- |
| P2-001 / BUG-021 | `reason_code` is type-checked before membership; audit returns `INVALID_GAP` and impact preserves it. |
| P2-002 / BUG-022 | preflight rejects non-string methods as stable `INVALID_SCHEMA` before set membership. |
| P2-003 / BUG-023 | parent preparation/temporary creation are inside the I/O adapter; cleanup failure is stable `OUTPUT_IO_ERROR` and cannot mask an in-flight `OUTPUT_EXISTS`. Documentation states that a post-link cleanup error may leave the atomically published target present. |
| P2-004 / BUG-025 | open-world state preflight charges explicit transition records rather than the unused closed-world state/trigger grid. |
| P2-005 / BUG-026 | candidate state/code combinations, finding code/key variants and candidate-local case-ID cardinalities now match the actual audit emitter. Genuine exact, documentation, mismatch, gap/case conflict, duplicate case, duplicate gap, orphan scenario/gap and zero-scenario case reports remain renderable. |
| P3-001 / BUG-024 | both public writers type-check `format` and return their domain `INVALID_FORMAT` error. |

The reviewer executed the developer hardening tests, independent hardening
tests, and the pre-existing case-conformance and method-impact suites against
the exact frozen checkout:

```text
python -W error::ResourceWarning -m unittest \
  tests.test_finite_audit_hardening \
  tests.test_finite_audit_hardening_independent \
  tests.test_case_conformance \
  tests.test_method_impact -q
```

Result: **41 tests ran in 1.950 seconds, all passed**. `git diff --check` passed
for the frozen product/test paths. This supports a bounded frozen-source PASS
with no unresolved P0-P3 finding. Clean installed delivery and current CI are
kept pending above until their separately retained evidence is available; no
package, full-suite, release, acceptance or Gate result is inferred here.

The independent tester then reran its final frozen-source fixture from a
separate test file:

```text
python -W error::ResourceWarning -m unittest \
  tests.test_finite_audit_hardening_independent -v
```

Result: **12 tests ran in 0.913 seconds, all passed; exit 0**. The run covers
the original six findings plus injected setup/cleanup failures, retained
closed-world preflight rejection, and the final finding-cardinality variants.
Its command, binary stdout/stderr and exit record are retained under
`docs/verification/evidence/cr035/task-142-final/`. This is independent source
retest evidence; installed-delivery and CI evidence are assessed separately.

The tester then added one test-only post-freeze regression for the aggregate
budget and reran the independent file. The final valid result was **13 tests in
0.966 seconds, all passed; exit 0**. TC-FAH-013 constructs four decision-table
models with 2,501 typed assignments each, first proves each model is individually
valid, then observes aggregate `CANDIDATE_LIMIT_EXCEEDED` before replay at
10,004 rows. An earlier strengthening attempt using 3,500 state transitions per
model exited `1` with `STATE_LIMIT_EXCEEDED`, because the proposed fixture
exceeded the design engine's 512-transition per-model limit; that retained result
is a fixture error, not a product finding. The final test-only addition does not
change the frozen product commit or the CI frozen-corpus count.

## Installed-delivery evidence recheck

The tester produced one internally coherent archive, wheel, fresh virtual
environment, offline install and installed-consumer ledger from the exact
frozen commit. The final command ledger contains 19 records under the single
temporary root `t142-0vtu5dyc`. All build/install and normal module/helper
commands exited `0`; the six malformed CLI probes exited the required `2`; the
direct public format probe exited `0` after observing `INVALID_FORMAT` from
both writers.

The retained manifest records:

- source freeze `8fc8533d4ec533bc5ba1ea66e6f24ef51a92f0f6`;
- wheel `qa_master_skill-1.0.0-py3-none-any.whl`, 6,399,339 bytes, SHA-256
  `dc2360f9d218640c17869c4d5870b81deeb0df73c69e22cb065a082bf7bdf49c`;
- installer response `files: 5888`, plus a later post-helper target count of
  5,900 files; the retained evidence does not attribute that difference to a
  specific file type;
- byte-identical module/helper audit JSON and Markdown outputs;
- audit status/execution `DRAFT_UNAPPROVED` / `NOT_EXECUTED`, denominator 10;
- impact status/execution `DRAFT_UNAPPROVED` / `NOT_EXECUTED`, review count 9;
- stable `INVALID_GAP`, `INVALID_SCHEMA`, `OUTPUT_IO_ERROR` and
  `INVALID_FORMAT` rejection observations.

The first foreground command outlived its tool wait, and a replacement detached
attempt was briefly started. The tester stopped the duplicate after discovery.
Its separate record identifies temp root `t142-xaxef1hn` as
`INTERRUPTED_NO_RECORDED_RESULT` after source-freeze/archive only. The successful
ledger and manifest above use only `t142-0vtu5dyc`; the interrupted attempt is
historical and is not counted as delivery evidence.

The coherent command ledger and manifest supported the bounded
installed-delivery contract, but that first retained directory did not contain
an explicit successful wrapper-exit record. Its completion therefore remained
pending at that point.

### Completed isolated installed confirmation

The tester subsequently ran the same wrapper in an isolated tool session and
retained both the tool-session completion and wrapper exit. Session `36511` and
`delivery-script-exit.txt` both record exit `0`. Its 19-command ledger uses only
temporary root `t142-h2bp1ota`: 13 normal commands exit `0`, and the six
prescribed malformed-CLI probes exit `2`. The exact source archive SHA-256 is
again `82b772eff5be48d93b50019ae26ec81360ab02c4ce782e677812b594bc893725`.

The completed confirmation records wheel SHA-256
`ee85671a0ea42f7136eb5491b1ad8619c2865639c5f4f6906c5e40810f762a7b`
(6,399,339 bytes), installer response `files: 5888`, and post-helper target
count 5,900. Module and installed-helper audit outputs are byte-identical; their
JSON SHA-256 is
`218efedd75d3f1935c2d567e1bfe18e181efba3e5646344fb2e8cebbc73c9cbd`
and Markdown SHA-256 is
`b29b086731b73c702cb1f887b1c54f4ae0628f1d7f32e801137edfb25f72922c`.
Audit and impact outputs retain `DRAFT_UNAPPROVED` / `NOT_EXECUTED`; the same
four stable rejection classes are observed. Evidence is retained under
`docs/verification/evidence/cr035/task-142-confirmed/`.

This closes the installed-delivery completion gap while retaining the earlier
wrapper-unknown chain and interrupted detached retry as historical evidence.
CI readback was still pending at that point; its final result is recorded below.
No release, acceptance or Gate result is inferred.

## Current CI readback

The exact frozen SHA completed PR workflow run
[`40074191090`](https://github.com/leongibhub/QA-Master-Skill/actions/runs/40074191090).
The retained `EVD-CR035-CI-001` readback at 2026-10-24 07:47:53 UTC records
workflow conclusion `success`. Ubuntu Python 3.10 and 3.12 jobs
`120813941849` and `120813941687` each ran 889 tests with zero failures/errors
and 12 skips. Windows Python 3.10 and 3.12 jobs `120813941798` and
`120813941832` each ran 889 tests with zero failures/errors and 3 skips. The
structured evidence is retained at
`docs/verification/evidence/cr035/final-ci-summary.json`.

This CI PASS adds frozen-runtime regression evidence; it does not alter the
formal claim boundary or establish a project Gate, acceptance or release
decision.
