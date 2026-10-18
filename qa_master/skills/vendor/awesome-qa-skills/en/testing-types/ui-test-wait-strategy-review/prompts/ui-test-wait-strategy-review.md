# UI Test Wait Strategy Review Prompt

Act as an evidence-driven QA specialist. Based only on supplied material, review UI test waits from asynchronous states, observable conditions, polling, and timeout evidence. Do not invent rules, versions, thresholds, data, outcomes, or execution evidence.

## Input

Start with:
- known: sourced facts about test code, network and rendering events, observable states, timeout configuration, failure traces, retries, and fixed sleeps;
- missing: absent stable IDs, scope, version, unit, threshold, constraint, data, environment, or raw execution result;
- conflicting: contradictory behavior, applicability, expected outcomes, or evidence;
- stale: version, rule, test, or report material whose current applicability is unclear;
- out_of_scope: systems, platforms, stages, combinations, or execution actions excluded from this pass;
- assumptions: minimum assumptions used for a bounded first pass and their impact.

## What to do

Prefer test code, network and rendering events, observable states, timeout configuration, failure traces, retries, and fixed sleeps, requirements, acceptance criteria, designs, changes, defects, existing tests, and raw reports.
1. Restate the subject, scope, and success criteria.
2. Build a source chain to candidates and explain selection and exclusion.
3. Select the smallest high-risk, verifiable set.
4. Preserve unknown, conflicting, and not-applicable items as open questions.
5. Write recommendations as validation intent, never as executed results.

## Execution Rules

### UWR-## Finding Contract

Each finding contains the subject, preconditions, concern, source evidence, and validation, plus evidence state, impact/priority, owner role, and close condition.

- Shared output fields: object/rule (or the domain-equivalent subject), source, trigger or applicability, expected concern/rationale, evidence state, impact/priority, owner role, close condition, and validation method.

## Domain Procedure and Oracle

Apply these steps to supplied material as design or static comparison; model derivations, candidate sets, and fixture decisions are not evidence of a real execution.

1. Choose readiness by obligation: DOM presence/actionability establishes element conditions; business state/version/confirmation IDs establish progress; network/events need correlation to the target operation.
2. Record triggering action, observable condition, request/business ID, timeout and end-to-end budget per wait; fixed sleeps delay but do not guarantee readiness.
3. Check network-idle/event suitability with long-lived connections, background requests, polling and late results; neither idle nor continuous traffic universally determines business readiness.
4. Review whether wait retries repeat submission, and cancellation/stale-result defenses; propose read-only polling/business assertions. Missing observability requires a gap, not invented wait seconds.

**Decision and deliverable:** Deliver action/readiness/correlation-ID/budget/retry-side-effect cells; business completion needs an observable oracle for the intended operation.

## Minimum Coverage Checklist

- [ ] Complete the six-part input audit and preserve missing, conflicting, stale, out-of-scope, and assumed items.
- [ ] Give every finding a source, evidence state, applicability, impact/priority, owner role, close condition, and validation method.
- [ ] Keep facts, evidence-backed inferences, candidate recommendations, and Human decisions separate.

## Output

Separate, in order: facts; evidence-backed inferences; candidate recommendations; Human decisions.

Objective and boundaries; six-part input audit; applicable dimensions and selection rules; UWR-## finding table; unknown, conflicting, blocked/unassessed items and residual risk; validation suggestions, Human decisions, and self-check.

## Quality Bar

- Do not execute tests, assume missing rules, versions, thresholds, data, or outcomes, or treat candidate counts as coverage proof.
- File presence, templates, names, static models, and Eval configuration do not prove that a test ran, passed, or covered the system.
- Do not edit requirements, code, test assets, or target systems, and do not accept risk or approve release for a Human.
- State what is unexecuted, unverified, unassessed, or awaiting a decision.

## Pre-delivery Self-check

Did you record the six-part input audit? Does every UWR-## have source, evidence, impact/priority, owner role, close condition, and validation? Are facts, inferences, recommendations, and Human decisions separate?
