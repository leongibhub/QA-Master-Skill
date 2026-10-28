The following drafts use supplied synthetic facts, not observations from a real test run.

## TC-DRAFT-001 — Reject a zero-byte attachment and keep the attachments list unchanged

**Source:** `DOC-FILE-EMPTY`: reject a 0-byte file with the exact error `EMPTY_FILE`; the attachments list must remain unchanged.

**Environment and preconditions:** SampleVault test build `sv-2`. Account Jo is already logged in on the **Attachments** page. The selected file is `blank.txt`, size **0 bytes**. Jo's role and browser/OS were not supplied.

**Steps and expected results:**

1. Record the current attachments list as the comparison baseline (preparation).
   - Expected: no product assertion at this preparation step; retain the baseline for comparison after the upload attempt.
2. Click **Upload**.
   - Expected: the upload is rejected with the exact error `EMPTY_FILE`, as required by `DOC-FILE-EMPTY`.
3. Compare the attachments list with the recorded baseline.
   - Expected: the list is unchanged; the upload attempt has not added `blank.txt`, as required by `DOC-FILE-EMPTY`.

**Cleanup:** No cleanup method was supplied. If the attempt adds an attachment, record the changed state and obtain the approved cleanup procedure before resetting it.

**Relevant gaps:** The full contract/version and its approval were not supplied; the oracle above is the supplied statement of `DOC-FILE-EMPTY`. Before execution, confirm the test target and capture the baseline, resulting error and resulting list. No screenshot or log is currently available. Cleanup instructions are needed if the reported failure occurs.

**Status:** Draft; `NOT_EXECUTED`. **execution:** `NOT_RUN`.

## BUG-DRAFT-001 — Zero-byte attachment shows “Upload complete” and is added to the attachments list

**Environment and preconditions:** SampleVault test build `sv-2`. Jo is logged in on the **Attachments** page with `blank.txt` (**0 bytes**) selected. Browser/OS and account role were not supplied.

**Steps to reproduce:**

1. Click **Upload**.
2. Inspect the button text.
3. Inspect the attachments list for the added `blank.txt` entry.

**Expected:** The upload is rejected with the exact error `EMPTY_FILE`, and the attachments list remains unchanged (`DOC-FILE-EMPTY`).

**Actual — supplied synthetic user report:** On `sv-2`, the button shows **Upload complete**, and the attachments list adds `blank.txt`. The agent has not reproduced this report.

**Impact:** In the reported scenario, a file prohibited by `DOC-FILE-EMPTY` is accepted into the list and receives success feedback. Wider impact is unknown; storage or downstream effects have not been established.

**Evidence:** No actual screenshot or log was supplied. Reproduction evidence should capture build identity, the file's 0-byte size, the button text, and the attachments list before and after the attempt.

**Frequency:** Unknown; no occurrence count or repeatability data supplied.

**Severity/priority:** Unassigned; no severity policy or prioritization decision supplied. **Root cause:** Unknown.

**Cleanup:** Procedure not supplied; confirm an approved method before resetting any added attachment.

**Status:** Draft / `NEEDS_REPRODUCTION`; agent execution `NOT_EXECUTED`. This draft has not been submitted to a tracker.
