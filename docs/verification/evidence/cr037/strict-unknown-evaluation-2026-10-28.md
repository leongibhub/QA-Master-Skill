# CR-037 strict unknown-preparation probe — independent classification

Artifact: `strict-unknown-output.md`
Artifact SHA-256: `715ebe41c7674ea0ca722bca9d53cf361b32d8dd8fef0fdf65569bb287cd6230`
Result: `PASS` for STRICT-WRITE-01, STRICT-WRITE-02, STRICT-WRITE-05 and
STRICT-WRITE-06; STRICT-WRITE-03/04 are not applicable to this case-only,
non-schema, non-bug probe.

Step 1 selects `invalid.csv` and has its own exact pending expectation: the
source does not provide the observable result of file selection and identifies
that it affects step 1. Step 2 preserves `MISSING_NAME` and no-new-records from
REQ-IMPORT-01. No unrequested machine field, UI behavior, account/OS/browser,
cleanup procedure, execution result, or external action is invented or claimed.
