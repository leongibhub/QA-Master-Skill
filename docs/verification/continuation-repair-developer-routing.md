# TASK-115 / TASK-116 developer verification

- Change: CR-028 continuation routing repairs.
- Source subject: `0ff9ad47ab0d442dff2157f6bf7d10e322a83f75` (root froze the implemented sources after the checks below).
- Evidence classification: developer-observed local checks; not independent acceptance, a Gate decision, business-test execution, or a comparison winner.

## Implemented contract

Explicit negative execution, regression and external-write instructions constrain their respective scopes. An affirmative execution request with a denied defect submission retains execution planning but forbids external writes. The application continues to preserve existing restrictive task contracts; this change grants no execution authority.

Specialist selection accepts actual catalog canonical names and a bounded curated bilingual alias set for property-based testing, chaos testing, Playwright and RAG. Prompt-based selection prefers Chinese for Chinese text and English otherwise. Existing stage-only callers retain bilingual results. Missing resources or unknown requested names produce gaps; broad RAG requests expose both retrieval and answer-quality candidates with an ambiguity gap. This is deterministic lexical routing, not general natural-language understanding. Bare specialist end-to-end wording does not expand the entire QA lifecycle. The precise combined phrase `编写测试计划和用例` selects planning and design without execution.

The installed Skill entry explains the bundled catalog location, returned selection paths, direct file reading without Python, and the distinction between reading guidance and executing its commands.

Owned changes: `qa_master/intent.py`, `qa_master/skill_registry.py`, the planning integration in `qa_master/application.py`, the specialist section in `qa_master/skills/codex/SKILL.md`, and `tests/test_routing_repairs.py`.

## Actual local results

Executed from `D:\QA-Master-PR2`:

```powershell
python -m unittest tests.test_routing_repairs tests.test_intent tests.test_vendor_skills tests.test_application tests.test_safety_regressions -q
```

Observed terminal result: `Ran 56 tests in 16.126s`, `OK`, process exit 0. The eight new test methods include subtests exercising all 165 actual canonical catalog names, language preference, RAG ambiguity, Chinese/English exclusions, separate execution/write scopes, full versus specialist workflow selection, combined planning/design, and persistence of application restrictions. This does not mean 165 separately counted unittest methods.

Also executed:

```powershell
git diff --check -- qa_master/intent.py qa_master/skill_registry.py qa_master/application.py qa_master/skills/codex/SKILL.md tests/test_routing_repairs.py
```

Observed: no output, exit 0.

## Retained failure history and limits

The first expanded targeted run reported `Ran 46 tests in 9.864s`, `FAILED (failures=1)`: `不要使用Playwright` incorrectly selected the specialist because the denial grammar did not recognize `使用`. The repair added bounded action prefixes, including Chinese use/run terms, and an English word boundary to avoid suffix matches. The next run passed 46 tests in 10.527s; a separate nine-test safety run passed in 1.590s. The final 56-test run above additionally covers the combined planning/design phrase. These are actual sequential developer observations, not a reconstructed all-green first attempt.

Checks ran before the root source freeze; the frozen subject records the checked source changes. No source files were edited when writing this report. Fresh-wheel delivery, full regression and independent review are separate responsibilities and are not asserted by these results. No external service, product test, or defect submission was executed.
