# CR-028 independent verification — 2026-10-19

State: attempt 1 FAIL retained; attempt 2 bounded repair verification PASS. Independent execution began after root's freeze of `0ff9ad47ab0d442dff2157f6bf7d10e322a83f75`; corrected attempt 2 is frozen at `6907fd4819daf931061fbbc69bcbdead51026208`. This document is not a Gate or acceptance decision.

## Attempt 2 — corrected package and independent retest

Fresh copied-source wheel build, fresh virtual environment, no-index/no-dependency package installation and separate standalone Skill installation all completed successfully outside the repository. The independent manifest compares the exact relative-path set and every file's bytes: **5,819 vendor files source = wheel = standalone**, including all five previously omitted hidden files. Wheel SHA-256: `af2a4b9a7da20d695afcd36ba39436887632411ae62095a76a6e0459ce445fce`. The wheel is retained locally in the scratch location identified by [delivery summary](evidence/continuation-repair-independent-2026-10-19/attempt2/delivery-summary.json); its contents are evidenced by the committed manifest, not a claimed committed binary.

Separate `-I` interpreter processes ran all five independent behavioral test methods against the wheel (48.348 seconds) and standalone helper package (45.502 seconds), both PASS without skips. Each includes all 165 canonical names in both languages, curated long-tail/ambiguous/negative requests, persisted negative stage/write scope, positive execution planning and independent 2/3-way interaction enumeration with missing-oracle variants. Explicit import and 330 discovered-path checks confirm wheel paths stay in the fresh virtual environment and standalone paths stay inside the installed Skill; neither resolves assets from the checkout.

The corrected managed-update/backup test passed separately in 134.105 seconds. It requires the exact managed root-plus-vendor entry set, one immediate discoverable root entry, no extra sibling/staging Skill entries, and the full original backup bytes. The original failed assertion and complete attempt-1 test run remain retained rather than erased.

README examples actually executed locally: package `init`, combined `plan`, `skills`, `design` with the supplied teaching input and `status`; standalone `skills`, negative `plan`, `pause`, `resume`, and managed update invocation. All exited zero; planning retained no-execution, design returned `DRAFT_UNAPPROVED` / `NOT_EXECUTED`, discovery returned EN 165 + ZH 165. The 366 local link targets across README, Getting Started and catalog exist. This verifies Windows commands and equivalent CLI arguments, not an interactive Agent's substantive QA output or a Linux shell installation transcript.

Environment: Windows 11, Python 3.13.5; test environment cryptography 50.0.0, setuptools 84.0.0, wheel 0.48.0 and packaging 26.3. The isolated wheel builder used the separately available system Python/build backend, recorded in command evidence. The fresh consumer installation used no dependency or network resolution. The initial local full suite is retained as FAIL; it is not retroactively upgraded. Final broad regression uses the new four-job CI matrix instead of duplicating the long local full run.

Final CI run [39211999256](https://github.com/leongibhub/QA-Master-Skill/actions/runs/39211999256): independent connector job-state and decoded-log readback confirms all four jobs completed successfully. Ubuntu 3.10: 799 tests / 122.072 seconds / nine skips; Ubuntu 3.12: 799 / 202.099 seconds / nine skips; Windows 3.10: 799 / 941.562 seconds / three skips; Windows 3.12: 799 / 901.577 seconds / three skips. All have zero failures and errors. Actual CI checkout is merge `791e599` incorporating source `6907fd4` into base `c52f34c`; it is not described as a direct source-head checkout. Exact job IDs, URLs, terminal status and matching decoded-log excerpts are retained in [independent CI readback](evidence/continuation-repair-independent-2026-10-19/attempt2/ci-readback.json). Skips remain unexecuted, not passes.

## Bounded conclusion

| Check | Final result | Evidence interpretation |
| --- | --- | --- |
| TC-CR028-I01 delivery | PASS | All 5,819 vendor files equal across source/wheel/standalone, fresh isolated install succeeds; exact imported and discovered paths remain inside each delivery |
| TC-CR028-I02 intent | PASS | Original negative examples, English/Chinese denials, persisted restrictions and positive execution planning verified; no business execution performed |
| TC-CR028-I03 routing | PASS | All 165 names in both languages reachable; curated examples and ambiguous RAG visible; additional installed negative canonical and unknown-request checks remain unresolved without execution |
| TC-CR028-I04 coverage | PASS | Required and covered interactions independently enumerated, including original six-row 16/16 example, 3-way coverage and missing oracle; duplicate/partial-row oracle demonstration is not a nonexistent engine API claim |
| TC-CR028-I05 documentation | PASS within local scope | 366 local link targets and documented local CLI examples verified; no invented interactive Agent or Linux shell-session validation |
| TC-CR028-I06 regression | PASS on corrected CI subject | New four-job strict CI is green; original local 798-test FAIL is retained as attempt 1; corrected independent update/backup test passes locally |

The four reproduced defects are repaired within this scope and the README onboarding is materially verifiable. Catalog availability and routing do not prove professional output quality across 165 domains, external integrations, release readiness, human acceptance or superiority over Awesome QA Skills. No such conclusion is made here. No new unresolved defect was established by this tester's bounded checks; independent reviewer findings remain separately governed.

## Attempt 1 finding — standalone installation still fails from a clean wheel

P1, TASK-113 / REQ-010: a fresh isolated copied-source build and no-index/no-dependency wheel install both succeeded, but invoking `python -I -m qa_master install-codex --project <fresh consumer>` outside the checkout returned exit 2 and `SKILL_VENDOR_RESOURCE_INVALID`. The source inventory requires 5,819 vendor files. The wheel omits five tracked `.gitignore` support files: English Gatling and k6 report folders, Chinese Gatling and k6 report folders, and the Chinese accessibility axe-playwright example. Setuptools wildcard package data did not include these hidden files, so the installer rejects its own packaged manifest.

Wheel SHA-256: `2e1d8100328bff053267d56a43b69a4d57bee1159b96c4e93edf16a847041998`. Package import provenance was independently confirmed under the fresh virtual environment's `Lib/site-packages/qa_master`, not the checkout. Exact missing paths and installation result are retained in [failure evidence](evidence/continuation-repair-independent-2026-10-19/wheel-hidden-assets-failure.json), with complete [command records](evidence/continuation-repair-independent-2026-10-19/delivery-commands.json). The delivery process terminated with exit 1 after detecting this failed command; it was not restarted or reported as passing.

The five-method source behavioral suite passed in 21.183 seconds, including 330 canonical-name/language subcases, persisted negative requests and independently enumerated interactions. The original packaged pairwise example now reports 16/16 for six rows, independently checked; the 3-way example reports 8/8. These passing source checks do not resolve the wheel failure. Strict regression terminated with exit 1: 798 tests in 1629.814 seconds, one failure, zero errors and eight skips. Its sole failure is the obsolete recursive SKILL.md assertion, which rejects the intentional 330 vendor leaves. This is distinct from the real wheel omission. The correction preserves the exact managed entry set, one immediate discoverable entry, and complete backup byte verification. The original failure log remains retained. Remaining installed Skill and README command checks have not executed because installation failed.

## Planned checks

| Check | Requirement / defect | Method | Expected observable evidence |
| --- | --- | --- | --- |
| TC-CR028-I01 | Standalone missing vendor library | Build fresh wheel in a private copied source directory; install to private environment; install Skill outside repository; compare every tracked vendor file byte-for-byte across source, wheel and standalone | Complete relative-path set and matching SHA-256, including notices and non-Markdown supporting assets; installed discovery returns 330 language entries / 165 names |
| TC-CR028-I02 | Negated execution/write intent | Five ordinary negative prompts through parser and persisted campaign service, plus explicit execution positive control | Exact requested stages; saved no-execution/no-write flags; no executable capabilities |
| TC-CR028-I03 | Long-tail reachability | Every discovered canonical name in EN and ZH; curated property/chaos/Playwright and ambiguous RAG prompts | Required skill selected in requested language; ambiguity visible; no unintended execution |
| TC-CR028-I04 | Wrong interaction ratio | Independently enumerate required 2-way and 3-way interactions over four heterogeneous parameter domains, then enumerate candidate rows; repeat without oracle | Reported covered / required numbers equal independent set cardinalities; missing oracle is obligation count in interaction units, not executed coverage |
| TC-CR028-I05 | README usability | Check repository-local Markdown links and execute documented local examples from isolated state directories | Existing targets; example commands produce described planning/design artifacts without remote activity |
| TC-CR028-I06 | Regression | Run strict test runner once on frozen final source | Retain stdout/stderr, exit code, environment and complete skip accounting |

Independent test file: `tests/test_continuation_repair_independent.py`. Developer tests are complementary evidence, not substituted for this tester's execution. No network business-system testing, human acceptance or comparative superiority is implied. Source-directory discovery and wheel/standalone evidence will be reported separately.

README, Getting Started and Skill Catalog: 366 repository-local Markdown link targets checked, zero missing. Anchor semantics, remote HTTP URLs and Agent task quality are outside this link-existence check.
