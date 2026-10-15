# CR-012 Codex Core Skill Adoption Record

- Artifact ID: `DOC-CR012-CODEX-CORE-ADOPTION-001`
- Document State: `DRAFT`
- Evaluation State: `IN_REVIEW`
- Change: `CR-012`
- Observed base: `codex/pr2-integration` at `0ae0ec0287a62d1b91e0c108c5d9def377cd70a2`
- Source relationship: the user identified a colleague-generated continuation; its
  implementation commit is `b18099a`, with Windows path correction `0ae0ec0`.

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
| PRD-001 | A single installed QA Master entry can carry the required local Skill assets without a separate QA-Skill repository. | `b18099a` package resources and `install-codex`; developer observations in `docs/verification/codex-core-installation.md`; TASK-047 independent install from a disposable directory. | PARTIAL | OBSERVED |
| REQ-010 | Installation is documented and invalid or locally modified managed installs are rejected with an actionable result. | Installer tests cover first install, idempotence, modified/unknown install refusal including arbitrary data beneath `__pycache__`, persistent previous-directory and ZIP preservation outside the discovery directory, publication rollback, and an explicit recovery locator if rollback itself fails. TASK-047 must reproduce through public CLI/package interfaces. | PARTIAL | OBSERVED |
| NFR-001 | A local helper or CI exit code is not described as model-task completion, acceptance, or release. | This record and TASK-048 check that documentation keeps the execution and approval boundaries. | PARTIAL | OBSERVED |
| NFR-003 | Installer artifacts must not introduce credentials, tokens, cookies, or private keys into the package or installer records. | TASK-047 performs a bounded package/install inspection and verifies that symlink/reparse-point destinations are rejected without following external content; TASK-048 reviews the result and source diff. | PARTIAL | PENDING |

## Observed evidence and limits

1. `tests/test_codex_skill.py` is a contributor-run developer check. Its reported
   nine focused tests, wheel install, and selected 493-test regression are
   `OBSERVED` statements in the developer record. The reported first 499-test
   socket failure, incomplete full-suite attempt, native-probe access denial and
   missing PyYAML validator dependency remain retained limitations.
2. GitHub API readback recorded workflow `38706851785` successful at the stated
   subject, with Windows/Ubuntu and Python 3.10/3.12 job success. It establishes
   only that remote CI executed its configured steps successfully; it does not
   establish the contributor's local count, independent test, model behaviour,
   enterprise compatibility, release, or acceptance.
3. The initial full independent discovery observed `557` tests with `2` skipped
   symbolic-link branches, therefore 555 successful tests. That was before the
   four preservation defects were identified, so it is retained only as a
   pre-repair baseline and is not the repaired-subject verification result.
4. `tests/test_codex_skill_independent.py` now contains tester-owned repair cases
   for persistent previous-directory/ZIP preservation, `__pycache__` unknown
   content, reparse points, late archive edits, and rollback-failure recovery.
   Its post-repair focused raw output and final report are still being prepared;
   neither is represented here as a completed independent conclusion.

## Registered continuation work

| Task | Required role / actual host identity | Work boundary | Required result | Current status |
|---|---|---|---|---|
| TASK-047 | tester `/root/pr2_test` | Late-registered independent test of the repaired PR2 working-tree subject, bound to the base SHA plus current modified-file hashes. Use a disposable project and public package/CLI interfaces. Preserve any fixture or environment failure; do not run model calls, enterprise operations, or remote targets. | `DOC-CODEX-CORE-INDEPENDENT-TEST-001` and `EVD-CODEX-CORE-INDEPENDENT-TEST-001`, with source binding, commands, environment, counts or explicit unavailable status, and raw-log locator. | Runtime claim is made after refreshed inputs; no completion is recorded. |
| TASK-048 | reviewer `/root/pr2_review` | Review the exact implementation, test source and TASK-047 evidence after the independent test work is DONE. Classify findings by severity and separately check source/claim boundaries. | `DOC-CODEX-CORE-INDEPENDENT-REVIEW-001` and `EVD-CODEX-CORE-INDEPENDENT-REVIEW-001`. | Dependency-gated; no review conclusion is recorded. |

TASK-047 is late registered because tester-owned preparation was observed before
its work-order registration. Late registration records timing only; it does not
backdate a claim, execution, or independent conclusion. Its Runtime inputs are
refreshed to this document version before the actual tester claim.

## Integration disposition

The fork/PR2 checkout contains the candidate commits, but this record does not
merge them into the upstream development branch or alter the existing CR-011
paired-runtime continuation. Integration may be considered only after TASK-047
and TASK-048 produce current, subject-bound evidence and remaining review
findings are dispositioned through a follow-up change record.
