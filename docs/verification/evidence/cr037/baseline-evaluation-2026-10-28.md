# CR-037 baseline independent classification

Artifact: `baseline-output.md`
Artifact SHA-256: `2fb8d82a6b4677436b795314d5009639155fed7b85c476541314d40f88b106ff`
Evaluation result: `FAIL` for R-READ-09 (reader-unfriendly presentation).
R-READ-01–08 and R-READ-10 pass; R-READ-07 passes specifically because the
artifact declares the unavailable evidence location rather than fabricating one.

The baseline preserves supplied facts and carefully labels missing details. The
failure is limited to readability acceptance; it is not a business test failure,
evidence of a real defect, model benchmark, or human acceptance.

## Classification correction

The first independent classification treated R-READ-07 as a failure because
`demo-cart.png` had no supplied byte, hash, or storage path. That was corrected:
REQ-042 requires a plain declared gap when information is missing and prohibits
inventing a locator. The baseline explicitly declares this evidence unavailable
and unverified, so it passes R-READ-07 with a declared gap. R-READ-09 remains
the sole baseline failure.
