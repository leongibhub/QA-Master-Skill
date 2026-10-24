# README local installed-skill update — independent validation

**Owner:** TASK-153 independent tester  
**Scope:** read-only comparison of the managed user install with the local source
bundle, and an isolated installed-helper teaching smoke.  
**Source identity:** `89d095f0dee555d3b51601e24a88e29bfd781a7f` (runtime proposal
module unchanged from `ddb2fc2`).  
**Overall result:** `PASS` for the bounded checks below. This is neither business
test execution nor a host UI claim.

## Preconditions observed

Root reported a successful local package update with Python 3.13 and successful
managed installer invocation. The installer reported `INSTALLED`, target
`C:\Users\leon.wang\.agents\skills\qa-master`, 5,890 files, no backup or
recovery directory, and `execution: NOT_EXECUTED`. The default user skill
directory was initially empty, so this was a fresh complete managed bundle rather
than an overwrite of a modified old target.

## Results

| Check | Command / observation | Exit | Result |
| --- | --- | ---: | --- |
| Runtime identity | `py -3.13 --version` | 0 | Python 3.13.5. |
| Complete managed integrity | Source `qa_master.codex_skill.skill_bundle()` SHA-256 map compared with `.qa-master-install.json` and all installed files. | 0 | Schema 1; manifest/source/installed each 5,890 files; both maps exactly equal. |
| New reference parity | SHA-256 source vs installed `references/case-library-proposal.md`. | 0 | Equal: `3b23460d3d0b6bc0e86fb795ec85739a6f16da6d368116e2ec3df91fc3a881eb`. |
| New runtime parity | SHA-256 source vs installed `case_library_proposal.py`. | 0 | Equal: `147ba0348f12bac0fb5e1e364f50c2329a884a7a1868d5ca9f5efb0d5f1c9eec`. |
| Installed CLI help | From a non-repository temporary directory: `py -3.13 -I ...\\scripts\\qa.py audit-method-cases --help`, `impact-method-cases --help`, and `propose-method-case-library --help`. | 0 / 0 / 0 | All three public routes were available through the installed helper. |
| Installed catalog | From that same directory: `py -3.13 -I ...\\scripts\\qa.py skills`. | 0 | Vendor catalog count 330, with 165 English and 165 Chinese resources (165 logical bilingual skills). |
| Installed teaching proposal | Same isolated helper with installed `examples/design-methods.json`, `design-methods-after.json`, and `method-cases.json`; a new disposable output path was used. | 0 | Output exists (28,284 bytes); 9 proposed cases and 1 missing vector; status `DRAFT_UNAPPROVED`, execution `NOT_EXECUTED`, application state `NOT_APPLIED`. |

The isolated probe directory was
`C:\Users\leon.wang\AppData\Local\Temp\qa-master-readme-local-e192e21abc144cb5ab545e5584ca879b`.
Its teaching output is intentionally preserved there; no installed target files
were changed by this validation.

## Boundaries

The proposal smoke generated a review artifact only. It did not execute business
tests, update a campaign, apply cases, create external objects, or validate any
host UI discovery behavior. No defects were observed in this bounded validation.
