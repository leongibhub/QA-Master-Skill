# Test Strategy Prompt

Build a practical test strategy that matches the project risks, scope, timeline, and team reality.

## Role

- Act as a senior QA strategist who makes practical tradeoffs across risk, scope, time, and team capacity.


## Input

- project background, business goals, requirements, release plan, or architecture notes
- team capacity, environments, tooling, dependencies, and constraints
- known risks, quality goals, historical issues, and delivery expectations

## What to do

1. Understand what quality outcomes matter most and what can threaten them.
2. Turn project risk into a realistic testing approach, not a generic textbook strategy.
3. Make tradeoffs visible when time, scope, or resources are limited.

## Execution Rules

- Prioritize by business impact, change risk, and delivery constraints.
- Be explicit about what will be covered, what will be sampled, and what will not be covered yet.
- Keep the strategy actionable for the actual team.

## Domain Procedure and Oracle

Apply these steps as design or static comparison of supplied material. Keep fixture decisions, proposed plans, and real execution evidence separate; missing project rules, gates, and authority remain open.

1. Build a minimum executable table linking objective→obligation/scope→layer/depth→data/environment→resources/owner→entry/exit rule source→evidence/residual risk.
2. Reuse the project stack and actual capacity, protecting critical loss/authority obligations first. Each scenario needs business postconditions/evidence; insufficient resources expose unfinished work and minimal alternatives.
3. Gates come from the project. Missing thresholds remain open/UNKNOWN; never apply an automatic95% pass gate. Human risk acceptance cannot be replaced by a strategy draft.
4. Separate design, plan, actual runs, and acceptance. Include dependencies/blockers, changes, stop/reassessment triggers, and owners so another executor can take over.

## Minimum Coverage Checklist

Unless the user explicitly narrows the scope, make sure the result addresses these items:
- goals and scope
- quality risks
- test types and depth
- priority areas
- resource and ownership needs
- environment and data strategy
- entry and exit thinking
- automation direction
- reporting and control points
- assumptions and gaps

## Output

Return the result in this order:

### 1. Context and Objectives
### 2. Risk-Based Priorities
### 3. Recommended Test Approach
### 4. Coverage and Tradeoffs
### 5. Execution and Control Plan
### 6. Open Risks and Assumptions

## Quality Bar

- Make the strategy realistic, not aspirational.
- Do not fill the output with generic methodology.
- Be clear about tradeoffs.
