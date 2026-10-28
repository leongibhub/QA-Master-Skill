# CR-037 readable cases and defect drafts — pre-publication delivery

Document State: DRAFT. Source baseline: `8a22a9f`.
Instruction freeze: `94fd0b90e6a52d5e8e3391e6d78b135de498e767`.
REQ-041–042; DES-065; TASK-154–156.

## Changes

The first-party Skill now requires readable-artifacts.md before case/bug drafting
or review, including specialist and tracker-packet work. Cases lead with concrete
scenario/setup and separate numbered actions/observables. Defects separate the
reported actual result from the expected rule. Supplied observations retain their
source even when the Agent has not reproduced them. Required technical values,
commands and fields are preserved; concise presentation does not change schemas.

Narrow case/bug requests no longer imply a full QA strategy, all-dimension matrix
or JSON handoff. Project-required fields still remain available in case detail or
compact supporting metadata. Incomplete facts stay plain-language questions; no
threshold, screen, error message, cause, frequency or evidence is invented.

The generator, quality engine, audit/impact/proposal modules, tracker adapters,
permissions and vendored sources are unchanged. Generated placeholders remain
candidates to be authored against real sources, never usable-case proof.

## Verification and retained history

- Baseline unchanged output is retained with its hash. It preserves facts and
  permission boundaries but fails the frozen presentation criterion R-READ-09:
  actions are packed inside lengthy metadata-table cells.
- An initial evidence-location grading error was corrected: a supplied filename
  without bytes/path is an honest declared gap, not a writer failure. That
  correction is retained rather than fabricated into a product finding.
- Fresh same-facts Chinese and separate English probes at `a30e541` passed the
  applicable rubric. A later focused-output refinement is separately attributed
  to the final freeze; these are synthetic agent samples, not a human study or
  a universal model-quality claim.
- Three source-review P2 findings (language override, technical-detail placement,
  required-field preservation) were repaired before final freeze. Reported-result
  attribution and the fictional worked example were also clarified.
- Final root instruction/registry/catalogue/installation-document checks:
  29 tests, exit 0, 2.235 seconds. Relevant whitespace checks passed.

Independent detail: readable-artifacts-test-2026-10-28.md and the original outputs
and classifications under evidence/cr037/. Final focused English probe at `94fd0b9` also passed the applicable rubric and
narrow-request guard. Independent managed installation is PASS; final independent review is bounded PASS, with zero open P0–P3 findings,
in readable-artifacts-review-2026-10-28.md.

## Local propagation and BUG-032

Initial uv foreground session `11491` exited 0 using the previous documented
`--force` update command, but an isolated installed-package resource readback
reported both the new reference and canonical entry rule absent. The cached old
wheel had been reused. This attempt is FAIL for delivery and is not counted as
a successful local Skill update; no managed target update was run from it.

BUG-032 (P2): existing-user tool refresh can reuse stale local-source content.
README and GETTING_STARTED now add `--reinstall` to the existing-user refresh
command; initial installation commands are unchanged. Local `uv tool install
--help` states that `--reinstall` reinstalls packages and implies refresh. The
corrected foreground session `22757` explicitly built the current package and
exited 0 (preparation 1m51s; installation 14.58s). Isolated installed-package
readback now reports the new reference and canonical rule present. Managed
update session `34031` exited 0: `UPDATED`, 5,891 files, target
`~/.agents/skills/qa-master`. It retained backup archive
`qa-master.backup-e4812dcbf9ae46ab9863466b2a83a6a9.zip` and prior tree
`.agents/.qa-master-recovery/qa-master.previous-e4812dcbf9ae46ab9863466b2a83a6a9`.
Execution remains NOT_EXECUTED. Independent source/manifest/installed hash maps match exactly across all 5,891
entries. The backup ZIP exists (6,651,879 bytes), as does the retained prior tree
(5,904 files including harmless prior runtime caches). The isolated installed
helper lists 330 vendor resources (165 per language), exit 0. BUG-032 is repaired
and retested in this bounded delivery, without claiming an external issue closure.
No runtime algorithm was changed for this delivery-method repair.

## Boundaries and publication

The user supplied no real unreadable artifact for rewriting; examples are openly
synthetic. Readability instructions and bounded sample checks do not establish
human acceptance or correctness of every future generated case. No business test,
remote case/bug edit or issue submission was authorized or executed.

All project Gates remain unchanged. Internal knowledge guidance was consulted
read-only; no internal document body, URL, product data or command was copied into
the public assets. Publication is PENDING at document freeze; subsequent PR/main
identity is recorded by Git and the PR receipt, not invented in this snapshot.

Captured synthetic author outputs retain their original bytes via a scoped
.gitattributes rule; reported SHA-256 values refer to those exact saved bytes.

Final root managed-installer repeat returned UNCHANGED (5,891 files), exit 0.
Only annotation Markdown whitespace was normalized before publication; the four
captured author outputs retain their original bytes and reported hashes.
