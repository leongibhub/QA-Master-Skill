# TASK-150 final frozen attempt marker

Evidence status: `OBSERVED`. This marker was written after the single test
process completed and its `TemporaryDirectory` fixture had cleaned up.

- Frozen source: `ddb2fc2665b2b6f044eba9bf56a70de69211db7e`
- Direct test session: `66660`
- Command: `python -m unittest tests.test_case_library_proposal_independent -v`
- Environment: `QA_MASTER_PROPOSAL_FROZEN_SHA` set to the frozen source and
  `QA_MASTER_PROPOSAL_EVIDENCE_DIR` set to this directory's `task150-final`
  parent.
- Actual command exit: `0`
- Observable result: `Ran 11 tests in 298.459s` / `OK`.

The durable subcommand records are in
`installed-attempt-037938bc1f26439db306b48ea4580cdf/`. Its `artifacts.json`
records:

| Artifact | Observable value |
| --- | --- |
| Source archive | 8,847,851 bytes; SHA-256 `94176e96a048a0b7532575fa1f8707d548fd3f14c948b654bd54a30ace7ba9f2` |
| Wheel | 6,407,909 bytes; SHA-256 `9ed0d4e3fd02e6a31cf19deff5e3a39d5c4b813ab88dab50fa017d640458cc36` |
| Installer-reported files | 5,890 |
| Source/runtime Python files | 1,077 / 1,077 |
| Module/helper proposal output | identical SHA-256 `49dee810a4c56027f2000d5d5180d17e519ce1b2cfd8319535db8c916fd1ddb0`; 31,744 bytes each |
| Nested after audit | 17 `EXACTLY_BOUND`; 0 `MISSING`, `DUPLICATE`, `MISMATCH`, `GAP_RECORDED` |

The proposal artifact itself remained `DRAFT_UNAPPROVED`, `NOT_EXECUTED`, and
`NOT_APPLIED` as required. This is test evidence only; it is not project Gate
or human acceptance evidence.

## Later CI fixture correction

Initial CI `40079455590` first exposed this test-fixture assertion on Linux and
later confirmed the same leaf in Windows Python 3.12 job `120829761748` and
Python 3.10 job `120829761754` (each 910 passed, 1 failure, 0 errors, 3 skips):
an already-existing output symlink is rejected as `OUTPUT_EXISTS`, not
`LINK_PATH_REJECTED`. The same leaf caused all four initial job failures. The
product protected-core files were not changed. The independent test was corrected
to expect `OUTPUT_EXISTS` for that collision and to test a separate symlinked
input for `LINK_PATH_REJECTED`; its subsequent local source-only run completed
11/11 in 1.248 seconds. Corrected CI `40080022358` subsequently completed PASS
on all four jobs at `83afa58`: each reported 910 tests run, 0 failures and 0 errors;
Ubuntu jobs had 12 skips and Windows jobs had 3 skips. Complete readback is in
`docs/verification/evidence/cr036/corrected-ci.json`. No second archive/wheel
attempt was run.
