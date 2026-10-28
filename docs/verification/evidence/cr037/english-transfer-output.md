## 1. Task understanding

One draft test case and one bug draft for SampleVault test build `sv-2`, based on the supplied contract `DOC-FILE-EMPTY` and user report. Neither has been executed or reproduced by the agent.

## 2. Coverage strategy

Cover the negative input boundary of `0 bytes`: reject the file with exact error `EMPTY_FILE` and leave the attachments list unchanged. Other file sizes and test types are outside this one-case request.

## 3. Test case

### TC-001 — Uploading a 0-byte file is rejected without changing the attachments list

- **Status:** Draft / `NOT_EXECUTED`
- **Priority:** Pending; no priority policy supplied.
- **source_role:** `[direct_input]`
- **Trace / oracle:** `DOC-FILE-EMPTY`, as supplied in the request.
- **Environment:** SampleVault test build `sv-2`.
- **Preconditions:** Account `Jo` is already logged in on the `Attachments` page. File `blank.txt`, size `0 bytes`, is selected. Account permissions beyond the supplied logged-in state are unknown.
- **Test data:** `blank.txt`, `0 bytes`.

**Steps and expected results**

1. Record the current attachments list as the comparison baseline.
   Preparation: preserve what is currently listed; no particular starting contents are specified.
2. Click `Upload`.
   Expected, per `DOC-FILE-EMPTY`: the upload is rejected with exact error `EMPTY_FILE`, and the attachments list matches the baseline from step 1 with no changes.

**Cleanup:** Not provided. A reset/removal method is needed if the reported unexpected addition occurs, before repeating the test.

## 4. Bug draft

### BUG-001 — Uploading 0-byte blank.txt shows “Upload complete” and adds it to the attachments list

**Status:** Draft / Needs reproduction; agent execution `NOT_EXECUTED`.

**Environment and preconditions:** SampleVault test build `sv-2`; account `Jo` already logged in on the `Attachments` page; `blank.txt`, size `0 bytes`, selected.

**Reproduction step**

1. Click `Upload`.

**Expected:** Per supplied contract `DOC-FILE-EMPTY`, reject the `0-byte` file with exact error `EMPTY_FILE` and leave the attachments list unchanged.

**Actual — user report, not reproduced by the agent:** On `sv-2`, the button instead shows `Upload complete`, and the attachments list adds `blank.txt`.

**Impact:** The reported result violates the empty-file rejection rule and changes the list when it should remain unchanged. Wider impact and persistence beyond the displayed list are unknown.

**Evidence:** User report only; no actual screenshot or log was supplied. Before/after list evidence and a capture of the button result are still needed for independent verification.

**Frequency:** Not provided.

**Severity / priority / routing:** Pending; no severity or priority policy or routing information supplied.

**Root cause:** Unknown.

## 5. Gaps and execution notes

The contract identifier and its expected behavior are supplied; no source link or contract revision was provided. Platform/browser details, repeatability, execution evidence, and cleanup/reset instructions are unknown. These drafts contain no execution result, confirmed defect conclusion, or regression claim. The next QA can use TC-001 to check the report on `sv-2` once the comparison baseline and any required reset are available.