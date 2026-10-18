# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Project target: WCAG 2.2 AA, checkout dialog only. S-1: automated scan has zero findings. K-1: keyboard opens the dialog but Tab cannot reach Confirm payment; the project maps this to 2.1.1. K-2: closing restores focus to the trigger; project maps this to 2.4.3. R-1: screen-reader testing was not performed. Decide SCAN_CLEAR/FAIL/PASS/NOT_RUN per evidence ID with criterion and evidence type, without site-wide conformance claims.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| S-1 | SCAN_CLEAR |
| K-1 | FAIL |
| K-2 | PASS |
| R-1 | NOT_RUN |

## Verification Method

1. Record the project-supplied WCAG version/level, scope, and success criterion IDs. Missing targets stay open; never choose a level or claim conformance by default.
2. Build criterion ID | user task/state | input/assistive technology/version | steps | evidence type | outcome. Keep automated scan, keyboard, screen-reader, and manual visual evidence separate.
3. Exercise keyboard navigation, opening, operation, closing, and focus restoration. Check screen-reader name/role/state and dynamic announcements. Prioritize inaccessible critical actions by user impact.
4. A scan with zero findings establishes only the scanned result. Preserve manual FAIL and unexecuted NOT_RUN; aggregate evidence by criterion without promoting a partial scan to conformance.
