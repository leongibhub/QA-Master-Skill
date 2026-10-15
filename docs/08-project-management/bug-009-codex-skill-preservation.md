# BUG-009 to BUG-012 — Codex Skill installer preservation defects

- Change: `CR-012`
- Source subject: `0ae0ec0287a62d1b91e0c108c5d9def377cd70a2` before the current working-tree repair
- Finding source: initial independent reviewer findings reported during PR2 review; formal reviewer report remains pending
- Evidence Status: `OBSERVED`
- Disposition: the repaired working-tree subject has current independent tester evidence and a formal `PASS WITH P3 FOLLOW-UP` review. The findings remain retained, rather than marked closed, because no committed-subject CI, release, acceptance, or formal defect-closure chain exists.

| Defect | Affected trace | Observation | Current repair mapping | Required closure evidence |
|---|---|---|---|---|
| BUG-009 | REQ-010, NFR-001 | During update, the managed tree was moved into a `TemporaryDirectory`. A later write or failure could leave the real previous tree tied to staging cleanup rather than a durable recovery location. | Move the old tree to `.agents/.qa-master-recovery/qa-master.previous-*` for standard discovery installs, outside `.agents/skills`; archive it only after re-verification and return the recovery directory in the result. | Tester must show current update/late-write behavior, complete ZIP contents and non-discoverable recovery location for the source-bound repaired subject. |
| BUG-010 | REQ-010, NFR-003 | Existing-install scanning ignored every path beneath `__pycache__`. A non-`.pyc` user file could be silently treated as managed content and omitted from protection. | Ignore only an immediate `__pycache__/*.pyc` cache artifact; make any other content an unknown-content refusal. | Tester must preserve a non-`.pyc` `__pycache__` file and observe refusal without mutation. |
| BUG-011 | REQ-010, NFR-003 | `Path.is_symlink()` alone does not reject all Windows junction/reparse paths. A target, manifest or nested traversal could follow an external directory. | `_linked()` rejects symlinks and `FILE_ATTRIBUTE_REPARSE_POINT` entries for target, manifest, tree entries and recovery root. | Tester must exercise available symlink and Windows-junction cases, retain permission-denied setup as `NOT_EXECUTED`, and show no external mutation where a case can run. |
| BUG-012 | REQ-010, NFR-001 | If publication failed and restoration also failed, the earlier flow did not return a stable locator for the retained data. | Preserve the detached tree under the recovery root and raise `SKILL_INSTALL_RECOVERY_REQUIRED:<path>` when its restoration fails. | Tester must inject publication plus restoration failure and verify the target is not falsely reported published and that the recovery directory contains the prior bytes. |

The prior full-suite observation of 557 tests with two skipped link-creation cases
means 555 successful tests on the pre-repair source. It does not verify these
repairs. The current repaired source is independently covered by 11 focused tests
and a 562-test strict run with two ordinary symbolic-link setup branches
`NOT_EXECUTED`; a Windows junction case passed. The current review reports no
remaining P0/P1/P2 and retains P3 manual cleanup/lifecycle management of recovery
trees. The contributor's nine focused developer checks and successful remote CI
matrix precede the working-tree repair and remain separate evidence.
