# CR-012 Codex Core Skill Adoption Record

- Artifact ID: `DOC-CR012-CODEX-CORE-ADOPTION-001`
- Document State: `DRAFT`
- Evaluation State: `IN_REVIEW`
- Change: `CR-012`
- Historical base: `codex/pr2-integration` at `0ae0ec0287a62d1b91e0c108c5d9def377cd70a2`
- Repaired source: `5ca82a368a7089207cc753afdad4bb3450b7db3c` (parent `0ae0ec0`), retaining the colleague-generated implementation `b18099a` and Windows correction `0ae0ec0`.
- Remote synchronization: the installer repair and final independent evidence were synchronized to PR1; the later CI `38717537656` concerns a CR-011 paired-runtime fixture and is not installer evidence.

## Scope and adoption decision

This record prepares a bounded adoption review for the self-contained Codex QA
Skill installer. The proposed change packages the canonical `qa-master` Skill,
its references and local helper in the Python distribution, and installs it to a
project or user Codex discovery location. It is an adoption candidate on the PR2
branch, not a product baseline, merge decision, release, human approval, or
claim that Codex has selected the Skill during a real task.

Independent preparation subsequently found four data-preservation defects in the
base subject: the previous tree only existed inside the ephemeral staging area,
unknown user content could be hidden below `__pycache__`, Windows reparse points
were not rejected everywhere, and rollback failure did not provide a durable
recovery locator. The current uncommitted repair in `qa_master/codex_skill.py`
uses a sibling `qa-master.previous-*` recovery directory, archives from that
directory after re-verification, treats non-`.pyc` content below `__pycache__` as
unknown, rejects symlinks and Windows reparse points, and raises a typed
`SKILL_INSTALL_RECOVERY_REQUIRED:<path>` error if restoration fails. These are
implementation observations pending current independent testing; the repair is
not yet a new committed or approved subject. For a standard
`.agents/skills/qa-master` installation, the retained directory is placed under
`.agents/.qa-master-recovery/qa-master.previous-*`, outside the skill-discovery
directory, so it cannot appear as a second active `qa-master` Skill.

The contributor document states that Linux is the only intended remote target and
that there is no model-budget limit. Those statements are contributor-reported
scope context only; they have not been adopted as a current human-approved
requirement. No remote host, model call, Linux native run, or enterprise system
is in this change's test scope.

## Requirement and acceptance trace

| Existing requirement | Bounded acceptance criterion for CR-012 | Subject / planned verification | Traceability | Evidence Status |
|---|---|---|---|---|
| PRD-001 | A single installed QA Master entry can carry the required local Skill assets without a separate QA-Skill repository. | TASK-047 independently exercised the repaired package/install interfaces from a disposable directory and preserved raw evidence. | PARTIAL | VERIFIED |
| REQ-010 | Installation is documented and invalid or locally modified managed installs are rejected with an actionable result. | TASK-047 verified first install, idempotence, modified/unknown refusal including non-`.pyc` `__pycache__`, persistent previous-directory/ZIP preservation outside discovery, rollback and recovery locator behavior through public CLI/package interfaces. | PARTIAL | VERIFIED |
| NFR-001 | A local helper or CI exit code is not described as model-task completion, acceptance, or release. | TASK-048 bounded review confirmed the claim boundary; no model-task, acceptance, release or Gate result was created. | PARTIAL | VERIFIED |
| NFR-003 | Installer artifacts must not introduce credentials, tokens, cookies, or private keys into the package or installer records. | TASK-047 bounded package/install inspection and TASK-048 source review covered the repaired subject and reparse rejection without asserting enterprise scope. | PARTIAL | VERIFIED |

## Observed evidence and limits

1. `tests/test_codex_skill.py` is a contributor-run developer check. Its reported
   nine focused tests, wheel install, and selected 493-test regression are
   `OBSERVED` statements in the developer record. The reported first 499-test
   socket failure, incomplete full-suite attempt, native-probe access denial and
   missing PyYAML validator dependency remain retained limitations.
2. GitHub API readback recorded workflow `38706851785` successful at the historical stated subject. A later remote run `38713544622` succeeded for all configured Windows/Ubuntu Python 3.10/3.12 jobs at `f54f85d3b81c32831370a4f2dd8a9955aed0341d`; its read logs show 562 tests with no skips on Windows 3.12 and 562 tests with one Windows-only junction skip on Ubuntu 3.12. These CI observations establish only configured remote test execution, not a model task, enterprise compatibility, release or acceptance. The later CI `38717537656` concerns a CR-011 paired-runtime fixture and is recorded there; it does not alter this installer evidence.
3. The initial full independent discovery observed `557` tests with `2` skipped symbolic-link branches, therefore 555 successful tests. That was before the four preservation defects were identified, so it is retained only as a pre-repair baseline and is not the repaired-subject verification result.
4. `tests/test_codex_skill_independent.py` contains tester-owned repair cases for persistent previous-directory/ZIP preservation, `__pycache__` unknown content, reparse points, late archive edits, and rollback-failure recovery. TASK-047 completed its repaired-subject final focused 11 checks and strict 562-test execution; two ordinary symbolic-link setup branches remain `NOT_EXECUTED`, the Windows junction case passed, and fresh-wheel/isolated-helper smoke passed. TASK-048 independently reviewed that exact bounded evidence as `PASS WITH P3 FOLLOW-UP`; P3 is manual recovery-tree lifecycle management.

## Registered continuation work

| Task | Required role / actual host identity | Work boundary | Required result | Current status |
|---|---|---|---|---|
| TASK-047 | tester `/root/pr2_test` | Late-registered independent test of the repaired PR2 subject through disposable public package/CLI interfaces. | `DOC-CODEX-CORE-INDEPENDENT-TEST-001` and `EVD-CODEX-CORE-INDEPENDENT-TEST-001`. | Runtime DONE with repaired-subject 11 focused and 562 strict tests, two symbolic-link setup branches `NOT_EXECUTED`, Windows junction PASS, and fresh-wheel/isolated-helper smoke PASS. |
| TASK-048 | reviewer `/root/pr2_review` | Review the exact implementation, test source and TASK-047 evidence after the independent test work is DONE. | `DOC-CODEX-CORE-INDEPENDENT-REVIEW-001` and `EVD-CODEX-CORE-INDEPENDENT-REVIEW-001`. | Runtime DONE: `PASS WITH P3 FOLLOW-UP`; P0/P1/P2=0, P3 manual recovery-tree lifecycle management; no Gate or release conclusion. |

TASK-047 was late registered because tester-owned preparation was observed before
work-order registration. That timing note does not backdate its later actual claim,
execution or independent conclusion.

## Integration disposition

The repaired candidate is committed at `5ca82a3` and its implementation plus final
independent evidence are synchronized to remote PR1 head `7913fd6`; this record does
not treat that synchronization as a release, acceptance or Gate decision. It does not
alter the CR-011 paired-runtime continuation. The remaining P3 recovery-tree lifecycle
follow-up and any future merge/release decision require their own current evidence and
human decision.
