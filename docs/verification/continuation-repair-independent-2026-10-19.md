# CR-028 independent verification — 2026-10-19

State: NOT_EXECUTED. Independent tester plan prepared while implementation is moving. Root source-freeze signal is required before execution; this document is not a Gate or acceptance decision.

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
