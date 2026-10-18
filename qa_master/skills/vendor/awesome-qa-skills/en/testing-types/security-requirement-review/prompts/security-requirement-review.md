# Security-Requirement Review Prompt

## Input

Start with an input audit and record known, missing, conflicting, stale, out_of_scope, and assumptions:

- known: scope, security requirement, roles, or constraints directly supported by a source.
- missing: material needed to judge security objectives, testability, trace links, acceptance conditions, and evidence gaps that has not been supplied.
- conflicting: incompatible objectives, conditions, roles, or behaviors across sources.
- stale: architecture, version, policy, log, or scan evidence that may be out of date.
- out_of_scope: work outside this Skill, unauthorized actions, or actions requiring a real environment.
- assumptions: temporary assumptions used for a bounded draft; include a validation method.

## What to do

1. Restate the security objective, object, scope, and success criteria.
2. Model scenarios, triggers, expected concerns, and evidence needs around security objectives, testability, trace links, acceptance conditions, and evidence gaps.
3. Separate static review, candidate validation, and unauthorized real-system actions.
4. Record priority, owner role, close condition, and validation method for every finding.
5. Separate facts, evidence-backed inferences, candidate recommendations, and Human decisions.

## Execution Rules

- Audit known, missing, conflicting, stale, out_of_scope, and assumptions first.
- Trace every conclusion to a source; mark unsupported evidence as pending, blocked, or a validation recommendation.
- Use security requirement as the domain anchor and SRR-## as the finding identifier.
- Each scenario needs preconditions, stimulus or action, expected result, evidence, and stop condition.
- Do not log in, call real APIs, read credentials, or perform destructive security actions.
- Do not upgrade files, names, templates, or dry-runs into absence-of-vulnerability, exploit success, or release-approval evidence.

## Domain Procedure and Oracle

Apply these steps to supplied material as design or static comparison; model derivations, candidate sets, and fixture decisions are not evidence of a real execution.

1. Map asset→threat actor/path→security obligation→control→verifiable acceptance, retaining scope, sources and project-supplied standard/version; do not select an unsupplied compliance baseline.
2. Turn vague secure/encrypted wording into questions about subject/action/boundary/timing/observable outcome; thresholds/algorithms must be sourced or labeled proposals.
3. Check allow/deny controls, failure paths, evidence and owner per obligation, identifying unimplemented obligations or untestable acceptance.
4. Separate requirement completeness, design controls, test results and standards conformity. Material review cannot establish certification, compliance or overall security approval.

**Decision and deliverable:** Deliver obligation/acceptance/evidence mappings and testability gaps; drafted requirements remain proposals rather than approved obligations.

## Minimum Coverage Checklist

- security requirement and applicability
- Primary risks or failure modes and triggers
- Data, permissions, impact, and priority
- Existing controls, dependencies, trust boundaries, and evidence freshness
- Expected result, evidence state, and validation method
- Close condition, residual risk, and Human decision
- facts, evidence-backed inferences, candidate recommendations, Human decisions

## Output

### 1. Scope and Task Understanding

State the objective, object, included and excluded work, success criteria, and unauthorized actions.

### 2. Input Audit

List known, missing, conflicting, stale, out_of_scope, and assumptions with source and freshness.

### 3. security requirement and Security Risk Model

Describe security objectives, testability, trace links, acceptance conditions, and evidence gaps scenarios, triggers, expected behavior, impact, priority, and evidence gaps.

### SRR-## Finding Contract

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

Separate candidate recommendations from completed execution. State the smallest isolated validation, stop/escalation conditions, residual risks, and open questions.

### 5. Human Decisions

List only items requiring Human confirmation, risk acceptance, exception authorization, or release judgment.

The output must preserve: facts, evidence-backed inferences, candidate recommendations, Human decisions.

## Quality Bar

- The content must target security objectives, testability, trace links, acceptance conditions, and evidence gaps, not a generic template with a substituted title.
- Without direct evidence, never write “tests were executed”, “all tests passed”, or “release approved”.
- Vulnerabilities, impact, thresholds, exploit success, and remediation status require sources.
- Make the next action clear to the executor and the boundaries of facts, inferences, recommendations, and Human decisions reviewable.
