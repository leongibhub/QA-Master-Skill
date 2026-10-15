# BUG-014 — installed design reference omits legacy requirement semantic fields

- Document State: `DRAFT`
- Evidence Status: `VERIFIED` for the independent attempt record below
- Change / task: `CR-013` / `TASK-057` attempt 2
- Initial failing subject: `f62932b1cce8471c929632fced8909a7a277a2ba`
- Repaired reviewed subject: `8b5017af42c7675cd32f941b71c85cf79b30d499`
- Severity: `P2`
- Status: `CLOSED_FOR_BOUNDED_PACKAGED_REFERENCE_SCOPE`

## Observed finding

The independent installed-task run completed the helper successfully, but its
source-grounded legacy requirement fields were not sufficiently specified in
the packaged reference/example. It yielded 13 method candidates and zero legacy
generic cases, with six each of `EMPTY_REQUIREMENT`, `NO_PROVENANCE`, and
`NO_ACCEPTANCE` findings. The retained actual task shows 18 requirement
findings and 12 generic gaps.

The initial report and all output bytes are retained by
`EVD-INSTALLED-METHOD-INDEPENDENT-ATTEMPT2-001`. Passing focused, fresh-wheel
and strict regression counts do not close this usability defect.

## Bounded closure evidence

The permitted repair was limited to packaged reference/example/assertions for
legacy requirement `id`, `text`, `source`, and `acceptance` semantics. TASK-057
attempt 3 independently exercised the repaired installed subject: it retained
three generic drafts, zero requirement findings, 13 candidates completed to 14
policy drafts and 15 explicit gaps, with `UNAPPROVED_TRACE` preserved.

`DOC-INSTALLED-METHOD-REVIEW-001` / `EVD-INSTALLED-METHOD-REVIEW-001` then
independently reviewed the exact subject and evidence as `PASS WITH P3
FOLLOW-UP`, P0/P1/P2=0. It verified the attempt-3 manifest's 42 retained
entries. This closes only this documented packaged-reference omission.

The attempt-2 P2 evidence remains immutable. The remaining P3 is that an
isolated `case_review.pass` can be misread without companion fields; the
packaged reference and reports label it structural only and retain
`UNAPPROVED_TRACE`, `PENDING_HUMAN`, `DRAFT_UNAPPROVED`, and `NOT_EXECUTED`.
This limited closure does not complete REQ-025, Phase 2, human assessment,
comparison, a Gate, acceptance, or release.
