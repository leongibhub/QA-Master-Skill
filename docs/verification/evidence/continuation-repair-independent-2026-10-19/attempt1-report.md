# CR-028 independent verification — 2026-10-19

State: FAIL / verification in progress. Independent execution began after root's freeze of `0ff9ad47ab0d442dff2157f6bf7d10e322a83f75`. Later documentation-only commits do not change the source subject. This document is not a Gate or acceptance decision.

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
