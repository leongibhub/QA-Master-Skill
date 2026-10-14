# QA Master Skill — v0.1 prototype

Original QA workflow guardrail and orchestration Skill. Public repository maintained under `leongibhub`.

**Status:** prototype, **not** a fully operational autonomous testing platform. No actual GitLab/Jira/Confluence/SynapseRT/SSH or upstream-skill-dispatch integration yet.

## Install and run on Windows (PowerShell)

```powershell
git clone https://github.com/leongibhub/QA-Master-Skill.git
cd QA-Master-Skill
py -3.10 -m unittest discover -s tests -v
py -3.10 -m qa_master init "my-project"
py -3.10 -m qa_master plan "只生成测试用例，不执行测试"
py -3.10 -m qa_master check design
```

Alternatively, use a Python 3.10+ interpreter with `python -m ...`.

The project-level `AGENTS.md` references `skills/qa-master/SKILL.md`. Open this repository as the working directory in Codex/OpenCode, and ask the agent to read the files and follow the QA Master workflow. The Python CLI is only a deterministic policy/state helper; it is **not** an LLM or live executor.

## How to use with Awesome QA Skills

Use **two separately installed components**:

- **QA Master:** planning, conversational scope, approvals, stages, persistence and coverage gates.
- **[awesome-qa-skills](https://github.com/naodeng/awesome-qa-skills):** specialized skills for requirements, functional/API, performance, reliability, security, regression and reports.

Install authorized upstream skills separately in the *same agent environment*, confirm they are discoverable, then direct QA Master to route requests to the available specialists. Merely cloning both repositories does **not** automatically provide runtime dispatch. The v0.1 Skill specifies selection rules, but actual dynamic invocation has not yet been implemented and verified.

**License caution:** check the upstream repository's full LICENSE and commercial-use permissions before importing/copying/using upstream assets in a company workflow. This repository does not redistribute them.

## Included

- `skills/qa-master/SKILL.md`: conversational orchestration rules
- `qa_master/core.py`: campaign state, intent routing, approval and coverage checks
- `qa_master/__main__.py`: state helper CLI
- `config/example.json`: non-secret integration placeholders
- `tests/test_core.py`: 21 unit tests
- `docs/TEST_REPORT.md`: verification scope
- `.github/workflows/test.yml`: CI unit test workflow

## Current limitations

No actual third-party API adapters or remote execution runner; no automatic user-interface exploration or code-to-requirements analysis; no evidence-linked report generator. These are target capabilities for future versions. Do not claim tests have executed until real execution evidence exists.

Never upload real passwords, personal tokens, SSH keys, or environment secrets into this Public repository.
