# OpenCode continuation comparison — 2026-10-19

Review subject: `c52f34c1a30f278e44ef483bb6cfdb5c7bfba130`; earlier checkpoint: `2f9ec205446b03f1871dc5e5784e8d3724c90ad3`.
Mode: source review and local reproduction, with separate read-only code/evidence reviewers. This report is not a Gate, acceptance, release approval or superiority decision.

## Current state and material additions

Live `git ls-remote` returned the review subject for both `main` and `pr-2`. The local working tree was clean before review. PR #1 still references the historical `e610d1d` continuation head, so it is not the current review subject.

The recovered OpenCode session is titled `继续分析 QA Skill 能力`; its recorded assistant models include GLM-5.3 and DeepSeek-v4-pro. The user's recorded requests include supporting individual, combined and full QA stages, adding test planning before cases, incorporating the upstream breadth, and removing a formal superiority claim from the README. Those requests inform this comparison; generated descriptions are not evidence of implementation correctness.

Material additions since the checkpoint include pairwise/combinatorial design, attestation verification, revised Skill guidance and retained comparison runs, a bilingual vendored skill catalog and planning projection, expanded intent routing, the test-plan stage, packaging/test dependency changes, and version 1.0.0 documentation. The catalog's 330 language directories represent 165 logical skills, not 330 distinct capabilities.

## Confirmed findings

### P1 — Standalone installation omits the new breadth library

`qa_master/codex_skill.py:42-55` builds the standalone installation from the canonical entry, Python modules, professional guides and semantic assets, but never includes `skills/vendor`. An independent temporary installation produced 61 files and only one `SKILL.md`. Invoking its helper outside the repository returned `vendor_skill_count=0`, `count=0` and `selected=[]`, while source discovery finds 330 catalog entries. Thus the repository's breadth is not delivered through its advertised standalone Skill installation.

Remedy: include the complete required vendor assets and notices in the standalone bundle, then independently exercise routing and referenced assets from an installed location outside the checkout. Source-directory discovery tests alone do not cover this boundary.

### P2 — Negated requests enable an execution stage in the plan

`qa_master/intent.py:12-17,37-46` matches newly added execution aliases inside negated phrases. Reproductions:

- `不提交bug，只生成测试报告` → `execution, report`, `no_execution=false`.
- `不要提交缺陷，只评审用例` → `case_review, execution`, `no_execution=false`.
- Independent reviewer also reproduced `不回归，只写测试报告` → `regression, report`, `no_execution=false`.

These observations concern the planner and saved scope; no actual external execution occurred. A request limited to review/report must not acquire execution permission from the words it negates. Preserve negative intent before positive alias matching and test persisted scope as well as the parser.

### P2 — Long-tail skills are present but not reached by corresponding requests

`qa_master/skill_registry.py:220-242` selects only the static stage/dimension mappings. The intent parser does not identify long-tail skill requests. Independent reproduction of property-based testing, chaos engineering and RAG testing returned discovery with no selected vendor skills; a Playwright end-to-end request selected the generic flow rather than the Playwright skill. Therefore catalog inclusion does not yet establish the claimed breadth of request routing.

Remedy: define and verify a discoverable specialist-routing contract, preserving user scope and returning explicit unresolved choices rather than silently dropping capabilities.

### P2 — Pairwise coverage mixes test-row and interaction counts

`qa_master/design_methods.py:521` supplies the number of generated rows as the numerator of an interaction-coverage ratio. The packaged combinatorial example generates six pairwise rows; independently enumerating those rows proves all 16 unique parameter pairs are present, but the report says `6/16`. The algorithm's row reduction works in this example; its coverage metric is incorrect.

Remedy: report distinct covered interactions over required interactions and keep row count as a separate metric. Validate missing-oracle and partial-coverage semantics using the same units.

## Comparison interpretation

CR-027 reports corrected semantic checks of A 16/16 and B 13/16 on eight scenarios after an explicitly disclosed oracle correction. Its own boundary is `PUBLIC_DEVELOPMENT` / `EXPLORATORY_CONFIGURED_SAME_MODEL`, using a fixed older upstream revision and a pre-current QA Master subject. Earlier fresh-set results include a tie and a B advantage. This is useful bounded evidence for instruction changes, not proof that the current full product exceeds the whole upstream library. Vendoring that library also changes the comparison into an integration-plus-additions question; copied breadth is not independently developed superiority.

## Current regression execution

A fresh run of `D:\codex-rd-platform\.venv\Scripts\python.exe tools/ci_test_runner.py` against the review subject completed: **781 tests, 409.645 seconds, zero failures/errors, eight skips; `OK (skipped=8)`**. Raw runner summary: `::notice::ran=781 failures=0 errors=0 skipped=8`. This is the current local Windows run, not a new Linux/Windows CI matrix. Skips are not executed passes. The separate code reviewer also ran 46 focused tests successfully. Neither result disproves the four separately reproduced findings above: those behaviors are absent from the corresponding assertions. Previously recorded OpenCode test totals were not substituted for this run.

## Recommended order

Retained current-run log: `evidence/continuation-review-2026-10-19/strict-tests.log`, SHA-256 `7FCF4339212513FC2D37FD7CFD885B41588B744B4B66893CF04EB468CF41A1A9`.

Repair installed delivery and negative-intent handling first, then specialist reachability and coverage accounting. Independently verify those boundaries on the installed product before extending comparison claims. Existing enterprise/remote execution and acceptance limitations remain governed by their actual evidence.
