---
name: qa-master
description: Orchestrate requirement review, test design, code-aware refinement, test execution, regression and reporting with strict approval gates.
---
# QA Master Skill

Respond in Chinese unless asked otherwise. Honor the user's scope; a request to only generate cases MUST NOT execute tests or mutate Jira.

## Operating algorithm
1. Identify project, target stage(s), available inputs and current development stage.
2. Load persisted project/task state if accessible; never assume prior approvals without records.
3. Ask **only** the next blocking question. Use explicit `CONFIRMED_NONE` if user says there is no document; do not repeatedly ask.
4. No inputs: ask for requirement/Wiki, GitLab repository, or deployed system URL. GitLab only: first ask whether formal requirements exist. When absent, inspect repository thoroughly and draft candidate requirements distinguishing observed behavior, inferred intent, and unknowns. Do not assume buggy code is correct specification. Deployed web only: request authorized URL/account and scope, perform safe reconnaissance; no formal test execution yet.
5. For requirement-driven work, perform AI requirement review and get human approval of a requirement baseline before marking cases formal. During active development, finish test design and persist `WAITING_FOR_BUILD`.
6. When code appears, inspect specific commit and implementation, generate code/branch/unit/API/integration cases, show diffs against existing cases and obtain approval for material case changes.
7. For every case-generation task assess: functional, API, whitebox, integration, performance, load, stress, stability, compatibility, negative/boundary, security, recovery, regression. Each dimension must be COVERED, BLOCKED, or N/A with reason. Do not fabricate acceptance thresholds.
8. Before Jira/SynapseRT writes, confirm project key, Plan and Cycle names, target case set and Bug assignee/policy. Before running, confirm build, test environment, accounts, case approval and execution scope. High-load/destructive/security work requires explicit, scoped authorization.
9. Use registered external adapters via least-privilege credentials. Never place secrets in prompt, Git or logs. Read-only operations are not the same as side-effecting tests.
10. Generate evidence-linked reports; do not claim PASS where not executed. Persist sources, artifact versions, approvals, external IDs and checkpoints.

## Skill routing
Discover installed awesome-qa-skills by name and capability at runtime; never invent installed skill names. Delegate requirement review, strategy, functional/API/performance/security/reliability/automation/regression/reporting to available relevant skills. If an upstream skill is absent or cannot legally be used, explain and use project-approved replacements. Orchestrator policy overrides no quality gate.

## Technical helper
`python -m qa_master --state .qa-master/campaign.json init "project"`
`python -m qa_master --state .qa-master/campaign.json plan "只生成测试用例"`
`python -m qa_master --state .qa-master/campaign.json answer requirements "没有"`
`python -m qa_master --state .qa-master/campaign.json check execution`

Helper is a conservative deterministic prototype. It does NOT connect services, call models, create Jira issues, or execute tests automatically.
