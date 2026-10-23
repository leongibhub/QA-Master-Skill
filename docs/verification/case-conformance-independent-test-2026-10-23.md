# TASK-135 independent test plan and evidence record

- Change: `CR-033`
- Requirements: `REQ-029`, `REQ-030`, `REQ-031`, `NFR-013`
- Tester-owned source: `tests/test_case_conformance_independent.py`
- Evaluation State: `IN_REVIEW`
- Evidence Status: `OBSERVED`
- Execution status: independently executed against final frozen revision `e9e141fa1319c37d2166b1bebc69cee6f77ab1c8`; earlier `7bd6b9c` observations are retained as historical evidence only.

## Independent scope

The tests use a tester-authored corpus containing one or more ready candidates
from each engine method: boundary, decision table, state transition, pairwise,
and combinatorial. It does not import the developer test helpers or use their
fixtures. Exact row bindings are assembled from the published design-engine
candidate interface, then independently altered to exercise the public audit
contract.

| Test case | Requirement | Objective and observable expected result | Status / evidence |
| --- | --- | --- | --- |
| TC-CC-001 | REQ-029, NFR-013 | Each of five methods has a candidate row; exact bindings are `EXACTLY_BOUND`; model and total state counts equal the candidate denominator; report remains `DRAFT_UNAPPROVED` / `NOT_EXECUTED`. | PASS — frozen `7bd6b9c`, focused run evidence below. |
| TC-CC-002 | REQ-029 | Omit one candidate while retaining its requirement trace. The exact candidate is `MISSING`, proving requirement linkage alone is insufficient. | PASS — frozen `7bd6b9c`, focused run evidence below. |
| TC-CC-003 | REQ-029, NFR-013 | Substitute integer `1` for Boolean `true`, and alter a decimal string. Each produces `MISMATCH` / `DATA_MISMATCH`; no coercion may count either row. | PASS — frozen `7bd6b9c`, focused run evidence below. |
| TC-CC-004 | REQ-029 | Independently change state data, oracle IDs, source IDs, and requirement IDs. The corresponding data/oracle/source/trace mismatch code is observable. | PASS — frozen `7bd6b9c`, focused run evidence below. |
| TC-CC-005 | REQ-029, REQ-030 | Duplicate a row, combine an exact row with a declared gap, and supply an unknown candidate ID. These are duplicate, gap/case conflict, and orphan diagnostics, never coverage. | PASS — frozen `7bd6b9c`, focused run evidence below. |
| TC-CC-005a | REQ-029, NFR-013 | Duplicate state precedence does not suppress `CASE_DOCUMENTATION_INCOMPLETE` when the owning case has `expected: ""`. | PASS — final `e9e141f`, scoped evidence below. |
| TC-CC-005b | REQ-030, REQ-031 | Repeated identical recorded gaps are an ambiguous `DUPLICATE` / `GAP_DUPLICATE`, retain one rendered reason, and must not cause the public renderer to reject its own valid audit report. | PASS — final `e9e141f`, scoped evidence below. |
| TC-CC-006 | REQ-030, NFR-013 | Reject stale input digest; retain documentation incompleteness; an empty model set is `UNASSESSED` and never a completion claim. | PASS — frozen `7bd6b9c`, focused run evidence below. |
| TC-CC-006a | REQ-030, NFR-013 | Permuting declared reference ID sets and case order does not change the semantic case-library identity; pure API and file API agree. Step ordering remains significant. | PASS — frozen `7bd6b9c`, focused run evidence below. |
| TC-CC-006b | REQ-029 | A documented case with zero scenario rows is diagnosed as an orphan and contributes no exact binding. | PASS — frozen `7bd6b9c`, focused run evidence below. |
| TC-CC-007 | REQ-031, NFR-013 | Markdown is deterministic, includes candidate IDs and `NOT_EXECUTED`, excludes a secret-shaped case title, and preserves its formal-only limitation. | PASS — frozen `7bd6b9c`, focused run evidence below. |
| TC-CC-007a | REQ-030, REQ-031 | Markdown exposes a recorded gap reason and orphan finding with identifiers/codes, without source prose. | PASS — frozen `7bd6b9c`, focused run evidence below. |
| TC-CC-007b | REQ-031, NFR-013 | The public renderer rejects malformed/injected report shapes with `CaseConformanceError`, never a raw `KeyError` or interpolated markup. | PASS — final `e9e141f`, scoped evidence below. |
| TC-CC-007ba | REQ-031, NFR-013 | The public renderer rejects forged `PASS` diagnostics, Boolean schema/count fields, and nonzero extra model counts. | PASS — final `e9e141f`, scoped evidence below. |
| TC-CC-007c | REQ-031 | Markdown renders the owning case ID and both report identities: design-input and normalized case-library SHA-256. | PASS — final `e9e141f`, scoped evidence below. |
| TC-CC-007d | REQ-029, NFR-013 | Requirement IDs with Chinese/spaces and source/oracle IDs beginning with permitted punctuation remain typed data and bind exactly. | PASS — final `e9e141f`, scoped evidence below. |
| TC-CC-008 | REQ-030, NFR-013 | Duplicate JSON keys, `NaN`, depth 33, and more than 5 MiB (5,242,880-byte binary boundary) input reject with stable value-free error codes and preserve a pre-existing output; exactly 5,242,880 bytes remains accepted. | PASS — final `e9e141f`, scoped evidence below. |
| TC-CC-008a | REQ-030, NFR-013 | A malformed model that reaches aggregate preflight is a value-free `CaseConformanceError`, never a raw `TypeError` or partial report. | PASS — frozen `7bd6b9c`, focused run evidence below. |
| TC-CC-009 | REQ-030, REQ-031, NFR-013 | More than 10,000 cases, output equal to input, and a symbolic-linked output reject without changing the protected target. A link privilege skip is reported as a platform skip, never PASS. Windows junction coverage remains a frozen-build run item. | PARTIAL — final core checks passed; symbolic link skipped because account privilege is unavailable. |
| TC-CC-009a | REQ-030, REQ-031, NFR-013 | On Windows, `mklink /J` creates a native junction within a temporary directory. Both input and output junction ancestors reject and a protected target remains unchanged. | PASS — final `e9e141f`, scoped evidence below. |
| TC-CC-010 | REQ-031 | From a separate consumer directory invoke `audit-method-cases` with Markdown output; verify report creation, exit 0 only as report creation, and no raw secret echo. Fresh-wheel isolation is executed as a separate frozen-build command. | PASS — final clean-wheel and installed-Skill evidence below. |

## Deferred frozen-build checks

After the orchestrator supplies the frozen revision, the tester will add
withheld omission/mutation cases without exposing them during development,
then run the focused independent suite, one strict full regression, and these
fresh-package steps from an unrelated directory:

```powershell
python -m pip wheel . --no-deps --no-build-isolation -w <temporary-wheel-dir>
python -m venv <temporary-venv>
<temporary-venv>\Scripts\python.exe -m pip install --no-index --no-deps <wheel>
Push-Location <consumer-directory>
<temporary-venv>\Scripts\python.exe -I -m qa_master audit-method-cases --input bundle.json --cases cases.json --output audit.json
Pop-Location
python -W error::ResourceWarning -m unittest discover -s tests -v
```

The package check must prove imports come from the temporary environment, not
the checkout. No performance threshold, real test execution, semantic-quality
rating, approval, or release result is included in this scope. The audit has
no network or external-system integration; reliability/security coverage here
is bounded parsing, deterministic output, secret non-disclosure and path
safety.

## Executed evidence

### Final subject `e9e141f`

Final subject: `e9e141fa1319c37d2166b1bebc69cee6f77ab1c8`. The scoped
independent command and its durable exit/output are retained at
`docs/verification/evidence/cr033/task-135-e9e141f/scoped-*`:

```powershell
python -W error::ResourceWarning -m unittest discover -s tests -p test_case_conformance_independent.py -v
```

- Exit code: `0`. **21 tests ran: 20 passed and 1 skipped** in **194.349
  seconds**. The skip is only the account-restricted native symbolic-link
  creation in TC-CC-009. The independent native Windows junction test
  TC-CC-009a passed.
- This run covered all five design methods; omissions; typed Boolean/integer
  and decimal changes; state/oracle/source/trace changes; gaps, duplicates,
  stale/empty/orphan/documentation cases; parser/depth/5 MiB/count limits;
  output/link safety; renderer claim/injection/count validation; ID
  compatibility; and the fresh archived-wheel consumer CLI.
- TC-CC-010 built from `git archive HEAD`, installed the fresh wheel offline
  in a new venv, imported only with `-I`, and invoked the consumer CLI. This
  is an offline report-creation result, not test execution, approval,
  acceptance, or release evidence.

The installed helper was separately verified from the same archived frozen
wheel. The durable `standalone-skill*.log` and exit files retain this sequence:

- The clean wheel built successfully at **6,389,424 bytes**, SHA-256
  `0f8f203b5f080b1947ee7e1faea0a110c9b5a6eb5af66c4e79ce43fad808ac73`.
- Offline install succeeded; isolated import resolved to the venv
  `site-packages`; `install-codex --target` returned `INSTALLED` with **5,885
  files** and `NOT_EXECUTED`.
- A first helper call returned `INPUT_IO_ERROR` because the tester fixture
  copied inputs from a non-packaged source path. This was a fixture error, not
  product behavior. Without rebuilding or reinstalling, the test reused the
  installed wheel/venv/Skill, copied `bundle.json` and `method-cases.json`
  from the installed Skill examples, and reran its `scripts/qa.py` helper.
- The corrected helper exit code was `0`; it generated a **1,663-byte**
  Markdown audit with SHA-256
  `B29B086731B73C702CB1F887B1C54F4AE0628F1D7F32E801137EDFB25F72922C`.
  Its summary reports `DRAFT_UNAPPROVED`, `NOT_EXECUTED`, and candidate
  denominator `10`.

### Historical subject `7bd6b9c`

Frozen subject: `7bd6b9c4024ed3135937b765a887bf64f03259bc` (`feat(CR-033):
audit finite test scenarios before case delivery`). Commands ran from
`D:\QA-Master-Compare` using local Python with `ResourceWarning` promoted to
an error:

```powershell
$env:PYTHONPATH='tests'
python -W error::ResourceWarning -m unittest -v <TC-CC-001 through TC-CC-009 selected tests>
```

- TC-CC-001–008a: **PASS**. Thirteen tester-owned checks completed in
  **1.296 seconds**. They exercised every required mutation/limit/output
  observation listed above and did not report a product defect.
- TC-CC-009: **PARTIAL**. Its no-clobber, input/output conflict, 10,001-case
  and 50,001-row bounds passed. The symbolic-link subcheck was **SKIPPED**
  because this Windows account cannot create symbolic links. Windows junction
  execution remains **NOT EXECUTED** in this run.
- TC-CC-010: **PASS** by the equivalent standalone frozen-package flow. A
  fresh 6,387,872-byte wheel built in about 56 seconds; a new venv was created
  in 11.8 seconds; offline `--no-index --no-deps` installation completed in
  19.1 seconds. From a separate consumer directory, the venv interpreter with
  `-I` imported `qa_master` from `venv\\Lib\\site-packages`, generated a
  1,840-byte Markdown audit, reported `DRAFT_UNAPPROVED` / `NOT_EXECUTED` and
  candidate denominator 17. A deliberate `case-secret-DO-NOT-ECHO` case title
  was absent from the generated Markdown.

The standalone result shows report creation only; exit 0 is not an approval,
semantic-quality, execution, acceptance, or release result. The root is
preparing a follow-up freeze that removes a redundant summary alias. These
results remain evidence for `7bd6b9c` only; final re-execution is recorded
above for `e9e141f`.

Before the measured `7bd6b9c` package result, pre-freeze harness preparation
failed while its
own `subprocess` diagnostic reader decoded Windows `pip` output as strict
UTF-8 (`UnicodeDecodeError` at byte `0xC1`). The process result was therefore
unavailable and no product behavior was evaluated. The tester harness now uses
replacement decoding for diagnostic text. This is a test-harness correction,
not a `BUG-xxx` or a product result. It is superseded for the 7bd subject by
the measured TC-CC-010 package result above. The final clean-wheel check is
recorded above for `e9e141f`.

## Defects

No separate `BUG-xxx` tracker object has been created by this tester. This does
not erase the concrete frozen-subject review findings `CASE-R1` through
`CASE-R5`, their repair state, or their required rechecks, retained in
[the delivery record](case-conformance-delivery-2026-10-23.md). A new observed
requirement violation will be assigned a `BUG-xxx` and linked to its affected
`TC-CC-*` case and requirement.
