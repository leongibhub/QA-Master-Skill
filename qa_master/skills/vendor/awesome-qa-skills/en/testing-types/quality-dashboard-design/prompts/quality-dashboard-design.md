# Quality Dashboard Design Prompt

Build an executable, reviewable, and traceable evidence boundary for quality dashboard audiences, decision questions, panels, drill-downs, freshness, and alert boundaries.

## Input

Start with an input audit and record known, missing, conflicting, stale, out_of_scope, and assumptions:

- known: scope, quality dashboard material, constraints, or results directly supported by a source.
- missing: material needed to assess quality dashboard audiences, decision questions, panels, drill-downs, freshness, and alert boundaries that has not been supplied.
- conflicting: inconsistent goals, definitions, conditions, or behaviors across sources.
- stale: architecture, version, metric, sample, or record that may be out of date.
- out_of_scope: actions outside this Skill, unauthorized actions, or actions requiring a real environment.
- assumptions: temporary assumptions for a bounded first pass, each with a validation method.

## What to do

1. Restate the objective, subject, scope, and success criteria in one sentence.
2. Audit completeness, credibility, recency, and comparability, focusing on audience, decision question, panel, drill-down path, freshness and alerting.
3. Build a risk or failure model for quality dashboard, including triggers, expected concerns, impact, and evidence needs.
4. Convert the analysis into concrete scenarios, assertions, validation steps, decision gates, or improvement experiments.
5. Report residual risk, evidence gaps, and next actions without presenting assumptions as facts.

## Execution Rules

- Give a source, evidence state, and validation method for every important conclusion.
- Each scenario must include preconditions, action or stimulus, expected behavior or decision criterion, required evidence, and a stop condition.
- Use P0/P1/P2/P3 or an equivalent scale and explain business impact, likelihood, detectability, or decision cost.
- Make quality dashboard audiences, decision questions, panels, drill-downs, freshness, and alert boundaries concrete; do not substitute adjacent test types, tool names, or one example for domain reasoning.
- Never invent numbers, thresholds, root causes, system behavior, execution records, all-passed claims, or release approval.
- For production, privacy, or security work, default to least privilege, masked data, mocks, dry runs, or isolation.
- Separate facts, inferences, candidate recommendations, and Human decisions; only Human can confirm risk acceptance, exceptions, and release decisions.

## Domain Procedure and Oracle

Apply these steps as design or static comparison of supplied material. Keep fixture decisions, proposed plans, and real execution evidence separate; missing project rules, gates, and authority remain open.

1. Map audience decisions to metrics, definitions/windows, source versions, actions and owners; available data alone must not decide what matters.
2. Show numerator/denominator, refresh time and source status. Distinguish zero, null, NOT_RUN, BLOCKED and stale data; never fill gaps with zero or reuse stale green.
3. Preserve P0 blockers and small high-risk groups in summaries. Overall pass rates cannot override individual blockers; aggregation follows project rules.
4. Provide drill-down to run/obligation/defect evidence, refresh contracts and action triggers. Missing sources or gates yield design and gaps, not a current pass.

## Minimum Coverage Checklist

- audience, decision question, panel, drill-down path, freshness and alerting
- confirmed facts, working assumptions, open questions, evidence quality, and recency
- high-risk paths, blockers, stop/escalation/rollback or human-handoff conditions
- smallest validation action, owner role, close condition, residual risk, and Human decision
- facts, evidence-backed inferences, candidate recommendations, Human decisions

## Output

### 1. Task Understanding and Scope

State the objective, subject, inclusions, exclusions, success criteria, and unauthorized actions.

### 2. Input Audit

List known, missing, conflicting, stale, out_of_scope, and assumptions with source, recency, and evidence quality.

### 3. quality dashboard Analysis and Priorities

Describe scenarios, triggers, expected behavior, impact, priority, and evidence gaps for quality dashboard audiences, decision questions, panels, drill-downs, freshness, and alert boundaries.

### QDD-## Finding Contract

Each finding must include:

- object/rule
- source
- trigger or applicability
- expected concern/rationale
- evidence state
- impact/priority
- owner role
- close condition
- validation method

### 4. Candidate Validation and Residual Risk

Separate candidate recommendations from actual execution and state the smallest validation action, stop/escalation conditions, residual risk, and open questions.

### 5. Human Decisions

List only items requiring Human confirmation, risk acceptance, exception authorization, rollback, or release judgment.

The output must keep these sections separate: facts, evidence-backed inferences, candidate recommendations, Human decisions.

## Quality Bar

- Tailor the content to quality dashboard; do not merely rename a generic template.
- Make high-risk paths concrete with failure modes, expected behavior, and evidence.
- Never infer numbers, root causes, or system behavior without support.
- Static analysis, plans, or dry runs are not proof of real execution, all tests passing, or release approval.
- Let an executor act without guessing and a reviewer trace the boundary between facts, inferences, recommendations, and Human decisions.
