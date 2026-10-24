# CR-036 case-library proposal independent review

- Artifact: DOC-CR036-INDEPENDENT-REVIEW-001
- Owner: reviewer `/root/rebind_reviewer`
- Review role: independent read-only product review; this file is the reviewer's only write scope.
- Baseline: `ce9da58605dfbdaa27ef8749ee5d20070175b54d`
- Branch: `codex/qa-case-library-proposal`
- Current reviewed product freeze: `ddb2fc2665b2b6f044eba9bf56a70de69211db7e`
- Current reviewed test/evidence head: `83afa5837bac375d291ae9d4742a1b6dd4f8540e`
- Review state: `DECIDED`
- Evidence status: independent review `VERIFIED`; underlying source, package,
  installed-consumer and CI executions are retained as `OBSERVED` evidence.
- Final bounded verdict: `PASS`; unresolved P0/P1/P2/P3 findings: `0/0/0/0`.
- Gate/release/acceptance effect: none.

## Attempt 1 — preimplementation contract preflight

The initial design commit `1d2442b` was reviewed before TASK-148 implementation.
No P0/P1 was found. The reviewer requested changes for the following P2 contract
and governance issues, plus P3 metadata/determinism clarification:

1. Mixed-row case CARRY/REBIND semantics and `possible_after_candidate_ids` were
   ambiguous.
2. Gap digest/occurrence identity and gap reason propagation were not fixed.
3. Case, row, gap and missing-followup reason unions were not independently
   reproducible.
4. `exact after-context` exceeded the fixed followup schema.
5. Source/oracle descriptor ordering was unspecified.
6. Count equations were implicit.
7. The proposal repeats original prose/descriptors but NFR-003 input sensitivity,
   stdout/error privacy and non-secret caller boundary were not traced.
8. The inherited-NFR RTM row, actual independent owners and change-impact record
   were incomplete.

Disposition: `CHANGES_REQUESTED` for specification freeze only. This was not a
source-code verdict because production implementation did not yet exist.

## Attempt 2 — preimplementation resolution readback

Resolution evidence:

- `1210f6a` fixed mixed-row decisions, possible-ID semantics, gap identity,
  missing-followup attribution, exact candidate-context scope, descriptor order,
  count equations, output-size boundary, sensitivity and lifecycle metadata.
- `84711da` fixed exact case/row reason formulas, made `CASE_HELD` uniform on all
  held rows, limited partial-case reasons to mixed eligibility, kept the old gap
  business reason only in `original_gap`, and moved inherited NFR-003 inside the
  CR-036 RTM table.
- `fb5e4be` recorded the developer, documentation manager, independent tester and
  independent reviewer owners before the implementation GO, without inventing a
  Runtime lease, Gate result or human approval.

Preimplementation result at `fb5e4be`: `PASS` with zero open P0/P1/P2/P3 contract
findings. This result only means the implementation contract is sufficiently
decidable for TASK-148. It does not approve code, tests, packaging, release,
acceptance, execution, a Gate, or any superiority claim.

## Final source and evidence review

### Attempt 3 — provisional source prefreeze

The uncommitted production/source-test worktree based on `fb5e4be` was reviewed
against the fixed `84711da`/`fb5e4be` contract before the one archive/wheel
attempt. Initial source review found these P2 issues:

1. missing-vector followups used held-row reasons but omitted that row's held-case
   reason union, losing a different row's removal/root cause;
2. baseline-finding and followup attribution performed quadratic scans despite
   the indexed-work contract;
3. eligible rows did not verify fresh action/delta/after-candidate identity;
4. post-audit/hash/count/source reconciliation was incomplete;
5. raw file-wrapper `OSError`/`RuntimeError` could escape instead of the stable,
   value-free `OUTPUT_IO_ERROR`;
6. held gaps were re-sorted by digest rather than canonical gap projection.

Each issue was repaired before freeze. The reviewer reproduced the former causal
loss with a mixed retained/removed case and read back `FINITE_VECTOR_REMOVED` in
the affected retained after-vector followups after repair. A forced sensitive
`RuntimeError` now returns only `OUTPUT_IO_ERROR`. The implementation now indexes
findings and held reasons, validates action/formal/post-audit identities and
counts, preserves canonical gap ordering, and keeps every held row/case reason.

Independent reviewer verification in this worktree:

- `python -m unittest tests.test_case_library_proposal tests.test_case_library_proposal_independent`
  ran 20 tests in 1.061 seconds and returned `OK`.
- `git diff --check` reported no whitespace error (only the existing Windows
  line-ending warning for the edited design document).
- `git diff --exit-code ce9da58 -- qa_master/case_conformance.py
  qa_master/method_impact.py qa_master/design_methods.py` returned zero; the
  three protected core modules have no diff from the baseline.
- The packaged teaching inputs produced 9 proposed cases, 9 proposed rows, zero
  held cases/rows/gaps and one missing-vector followup, matching the documented
  example without implying case correctness.

Provisional source-freeze result: `PASS`, zero open P0/P1/P2/P3 findings. This is
not yet the final delivery verdict. Frozen commit identity, independent archive/
wheel installation, isolated module/helper byte comparison, retained raw evidence,
full CI and final documentation/traceability readback remain `NOT_EXECUTED` by
this reviewer at this point.

### Attempt 4 — frozen source and installed-consumer readback

Product source froze at `ddb2fc2665b2b6f044eba9bf56a70de69211db7e` and was
pushed on the feature branch. The reviewer repeated the 20 scoped proposal tests
on that source (`OK`, 1.435 seconds), confirmed the three protected core modules
still have an empty diff from `ce9da58`, and found zero open P0/P1/P2/P3 source
findings.

TASK-150 then completed its single SHA-gated archive/wheel attempt in one test
session. The retained post-cleanup marker and nine command records show:

- 11/11 independent tests passed in 298.459 seconds with process exit zero;
- archive SHA-256 `94176e96a048a0b7532575fa1f8707d548fd3f14c948b654bd54a30ace7ba9f2`;
- wheel SHA-256 `9ed0d4e3fd02e6a31cf19deff5e3a39d5c4b813ab88dab50fa017d640458cc36`;
- the isolated runtime loaded from the temporary venv and contained the same
  1,077 Python-file count as the archived source;
- installed module and installed Skill-helper proposals were byte-identical:
  31,744 bytes, SHA-256
  `49dee810a4c56027f2000d5d5180d17e519ce1b2cfd8319535db8c916fd1ddb0`;
- the nested library readback audited 17 `EXACTLY_BOUND` and zero `MISSING`,
  `DUPLICATE`, `MISMATCH`, or `GAP_RECORDED` candidates;
- the proposal remained `DRAFT_UNAPPROVED`, `NOT_EXECUTED`, `NOT_APPLIED`.

The first CI run `40079455590` is retained as failed because its new Linux
fixture expected `LINK_PATH_REJECTED` for an already-existing output symlink,
while the established safe-output precedence correctly returned
`OUTPUT_EXISTS` without touching the protected target. The test-only commit
`83afa5837bac375d291ae9d4742a1b6dd4f8540e` corrected that expectation and added
a separate linked-input assertion for `LINK_PATH_REJECTED`; it did not change
product or protected-core source. Corrected CI run `40080022358` completed on
`83afa58` with all four jobs successful. Each job reported 910 tests, zero
failures and zero errors; Ubuntu Python 3.10/3.12 each retained 12 skips and
Windows Python 3.10/3.12 each retained 3 skips. The job IDs, conclusions and
counts are persisted in `evidence/cr036/corrected-ci.json`.

Final delivery review result: `PASS`, with zero open P0/P1/P2/P3 findings. The
frozen source, bounded installed-consumer result, corrected four-platform CI,
requirements/design/task/test traceability, retained failed attempts and
publication boundaries are mutually consistent. The successful installed
attempt was not rerun because `83afa58` changed only the independent fixture;
the reviewed product remains `ddb2fc2` and the protected core remains unchanged.

This verdict is limited to REQ-037–040, NFR-015 and the inherited NFR-003
boundary in CR-036. It is not a human acceptance, release recommendation,
project Gate decision, business-correctness proof, test execution result, or
overall comparison/superiority conclusion. The delivery record is intentionally
a pre-merge snapshot; merge/main identity remains subject to later Git/PR
readback rather than inference in this review.
