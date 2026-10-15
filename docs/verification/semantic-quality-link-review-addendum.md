# TASK-068 semantic-quality link/reparse review addendum

- Artifact ID: `DOC-SEMANTIC-QUALITY-REVIEW-ADDENDUM-001`
- Proposed Evidence ID: `EVD-SEMANTIC-QUALITY-REVIEW-ADDENDUM-001`
- Parent review: `DOC-SEMANTIC-QUALITY-FINAL-REVIEW-001`, SHA-256 `BC6FE94790A1BF508E2FE541DE33870FB8021C39A46C990FD15A9F6424ED13DE`
- Change: `CR-013`
- Reviewer: `/root/workflow_review`
- Runtime work: `work-5302662bc52c46c78d4b080242ad31eb`, attempt 1 / version 1
- Review result: `SPECIFIC P3 EVIDENCE GAP RESOLVED IN BOUNDED SCOPE`
- New finding counts: `P0=0`, `P1=0`, `P2=0`, `P3=0`
- Document State: `DRAFT`
- Evidence Status: `OBSERVED`
- Date: 2026-10-15

This addendum reviews only the path-fixture P3 retained by TASK-063. It does not
alter the parent report, product source, test evidence or historical local
skips. It does not decide a Gate, acceptance, release, full REQ-025 or V1,
defect closure, broader filesystem security, or hostile concurrent-filesystem
behavior.

## Fixed subject and follow-up evidence

| Subject | Revision / SHA-256 |
|---|---|
| Product source | commit `a9df28513d4ae808d687718bfc4f6069a32ee767`; `qa_master/semantic_quality.py` `D567D26110EACA5637F54C0DC48994E881BFEDCE69EAFD0C8AA809C41331018A` |
| TASK-064 test source | `tests/test_semantic_quality_links_independent.py` `B51F64E5AC47A4D5D29AAE822D5322ACEACC9660DF38CDF1D8A54D1D920D21E1` |
| TASK-064 report | `docs/verification/semantic-quality-links-independent.md` `9F1BEF0241364C6C35902046C0A57DCD30A1FDD57290DF22AFF3DE5BF86096E2` |
| TASK-064 manifest | `docs/verification/evidence/cr013-semantic-links-independent/manifest.json` `0E6ED722D2F218E65609545DD57E84CE8E94FC4FC6CDCE9A50D5B46496ACB721` |
| Final CI jobs readback | run `38739167991`; retained JSON `791C01987028AF23999138435B6C12878D253932DC9797A98CA4DDA6F9B65749` |

The reviewer reconciled all 11 manifest rows with the retained files: every
byte count and SHA-256 matched. A path-scoped Git comparison found no product
module change between the frozen subject and the TASK-064 evidence commit.
No test was rerun under TASK-068.

## Test-design assessment

The tester uses real filesystem links rather than mocks or injected product
results. The matrix covers five parent-path positions separately:

1. bundle input directory, through both validation and evaluation;
2. referenced source directory, through both validation and evaluation;
3. referenced response directory, through both validation and evaluation;
4. output parent directory, through evaluation; and
5. retained result parent directory, through inspection.

Every executed scenario requires the stable `LINK_FORBIDDEN` error. It also
checks that source and response bytes, an unrelated sentinel and an already
published inspected result remain unchanged, and that rejected evaluation does
not create an output child. Junction fixtures verify the Windows
`FILE_ATTRIBUTE_REPARSE_POINT` bit. Cleanup removes only the verified link
inside the temporary root and does not traverse the target.

This design directly addresses the parent review's requested bundle/source
input, output reservation and result-inspection boundaries, including typed
rejection, no following, no partial publication and preservation checks.

## Executed evidence

| Environment | Actual link cases | Result | Full-suite context |
|---|---:|---|---|
| Local Windows | 5 junctions | 5 PASS | Dedicated run: 10 tests in 1.193 seconds; 5 real symlink cases remained `NOT_EXECUTED` because Windows returned error 1314. |
| Ubuntu, Python 3.10 | 5 symlinks | 5 PASS | Job `116436073554`: 699 tests, success; Windows junction cases were `NOT_APPLICABLE`. |
| Ubuntu, Python 3.12 | 5 symlinks | 5 PASS | Job `116436074129`: 699 tests, success; Windows junction cases were `NOT_APPLICABLE`. |
| Windows, Python 3.10 | 5 junctions + 5 symlinks | 10 PASS | Job `116436073865`: 699 tests, success with no skips. |
| Windows, Python 3.12 | 5 junctions + 5 symlinks | 10 PASS | Job `116436073916`: 699 tests, success with no skips. |

The retained decoded excerpts name every semantic evaluator case and result.
The final jobs API record identifies all four jobs as completed successfully.
The local workstation's five symlink attempts remain `NOT_EXECUTED`; the later
CI executions are separate evidence and do not rewrite those skips.

## Disposition of the TASK-063 P3

TASK-063 retained one P3 because the semantic evaluator had no product-specific
executed link/reparse fixture. TASK-064 supplies that missing evidence across
real Windows junctions and permitted Windows/Linux symlinks, for all five path
positions identified by the finding. The frozen product source is unchanged.

The specific regression-evidence gap is therefore resolved in this bounded
scope. No new P0, P1, P2 or P3 finding was observed in the reviewed follow-up.
This conclusion is an evidence disposition for the parent review; it is not a
defect closure or a revision of the original TASK-063 report.

## Remaining boundary

The evidence does not cover arbitrary Windows reparse subtypes, mount-point
variants beyond the tested junctions, link swaps after validation, hostile
TOCTOU races, every crash/filesystem failure, network storage, enterprise
authorization, or production deployment. Linux junctions are
`NOT_APPLICABLE`. Local Windows symlink execution remains historical
`NOT_EXECUTED` evidence even though the same five symlink cases passed on both
Windows CI hosts.
