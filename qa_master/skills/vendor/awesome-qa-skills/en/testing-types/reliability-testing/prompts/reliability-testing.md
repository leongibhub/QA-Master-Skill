# Reliability Testing Prompt

## Input

Start with an input audit and record known, missing, conflicting, stale, out_of_scope, and assumptions:

- known: scope, reliability objective, or constraints directly supported by a source.
- missing: material needed to judge availability objectives, failure modes, exposure windows, and evidence readiness that has not been supplied.
- conflicting: incompatible objectives, conditions, or behaviors across sources.
- stale: architecture, version, metric, or run evidence that may be out of date.
- out_of_scope: work outside this Skill, unauthorized actions, or actions requiring a real environment.
- assumptions: temporary assumptions used for a bounded draft; include a validation method.

## What to do

1. Restate the objective, object, scope, and success criteria in one sentence.
2. Model failure scenarios, triggers, expected concerns, and evidence needs around availability objectives, failure modes, exposure windows, and evidence readiness.
3. Assign priority, owner role, close condition, and the smallest validation method to each scenario.
4. Separate confirmed facts, evidence-backed inferences, candidate recommendations, and Human decisions.
5. State which material is design preparation and which needs isolated validation; never claim that tests ran.

## Execution Rules

- Audit known, missing, conflicting, stale, out_of_scope, and assumptions before analysis.
- Trace every conclusion to a source; mark unsupported content as pending or a validation recommendation.
- Use reliability objective as the domain anchor and RLT-## as the finding identifier.
- Each scenario needs preconditions, stimulus or action, expected result, evidence, and stop condition.
- Do not inject faults, access real dependencies, read credentials, or call production systems.
- Do not upgrade file presence, names, templates, or dry-runs into execution, passing, coverage, or release evidence.

## Domain Procedure and Oracle

Apply these steps to supplied material as design or static comparison; model derivations, candidate sets, and fixture decisions are not evidence of a real execution.

1. Define SLI event/time basis, success/failure, denominator, exclusions, observation window and sourced targets; request success and time availability are different metrics.
2. Recalculate success/total or available/eligible time per window, retaining missing observations, retries, duplicate events and denominator conflicts. Merge only compatible definitions.
3. List failure frequency/duration/recurrence and recovery criteria, checking incident deduplication and representativeness of load.
4. Separate window observations from long-term inference; short failure-free periods do not prove long-term reliability. Absent targets/windows permit limited distributions and observation needs only.

**Decision and deliverable:** Deliver window/denominator-defined SLIs and failure timelines, stating applicability for target comparisons and extrapolation.

## Minimum Coverage Checklist

- reliability objective and applicability
- Primary failure modes and triggers
- Exposure window, impact, and priority
- Existing controls, dependencies, and isolation boundary
- Expected result, evidence state, and validation method
- Close condition, residual risk, and Human decision
- facts, evidence-backed inferences, candidate recommendations, Human decisions

## Output

### 1. Scope and Task Understanding

State the objective, object, included and excluded work, success criteria, and unauthorized actions.

### 2. Input Audit

List known, missing, conflicting, stale, out_of_scope, and assumptions with source and freshness.

### 3. reliability objective and Failure Model

Describe availability objectives, failure modes, exposure windows, and evidence readiness scenarios, triggers, expected behavior, impact, priority, and evidence gaps.

### RLT-## Finding Contract

Every finding must include:

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

Separate candidate recommendations from completed execution. State the smallest validation action, stop/escalation conditions, residual risks, and open questions.

### 5. Human Decisions

List only items requiring Human confirmation, risk acceptance, authorization, or release judgment.

The output must preserve these sections: facts, evidence-backed inferences, candidate recommendations, Human decisions.

## Quality Bar

- The content must target availability objectives, failure modes, exposure windows, and evidence readiness, not be a generic template with a substituted title.
- Never write “tests were executed”, “all tests passed”, or “release approved” without direct evidence.
- Numbers, thresholds, root causes, recovery capability, and security claims require sources.
- Make the next action clear to the executor and the boundaries of facts, inferences, recommendations, and Human decisions reviewable.
