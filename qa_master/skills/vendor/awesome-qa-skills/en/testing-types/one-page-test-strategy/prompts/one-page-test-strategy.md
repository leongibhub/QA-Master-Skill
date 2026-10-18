# One-Page Test Strategy Prompt

Use supplied project material to create a goal-driven, risk-focused one-page test strategy for team discussion and iteration. Default to English Markdown; use a compact Mermaid lifecycle diagram when supported, or a phase table otherwise. The page must cover every strategy module below; do not drop the quadrants, test layers, or iteration feedback to make it shorter. When data is missing, retain the module and mark it “Open”; never invent project facts. Do not copy the source article's figure, examples, or wording.

## Input Review

Extract the following from project material where available; do not invent missing details:

- Project/product, release or strategy period, audience, business goal, and quality outcome.
- Priority risks across functionality, performance, and security; include other relevant quality attributes as needed.
- Activities across all seven lifecycle stages: requirements analysis, before development, development, development complete, testing, before release, and released.
- Architecture, technical constraints, delivery cadence, environments, data, team capability, automation/manual approaches, and tools.
- The team's adopted test-quadrant definitions, test levels, and iteration/continuous-delivery cadence.
- Approved entry/exit rules, release decision ownership, and production monitoring, support, and quality-analysis signals.

Separate **known facts, strategy recommendations/inferences, and assumptions/open questions**. Missing information does not block a draft; keep the relevant module and use a concise placeholder. Activities from the image are candidates, not claims about existing or completed team practice unless the input supports them.

## Required Strategy Modules

1. **Guiding principle and goal:** Prominently state “The whole team owns quality.” Summarize the business goal or quality outcome in one sentence; mark it Open when absent.
2. **What to test:** Always show functionality, performance, and security with each area's priority risks/status (in scope, deferred, risk-based, or Open). Select scope from the project context; do not force all three to be mandatory. Add other relevant quality attributes as needed.
3. **Lifecycle and shift-left/right:** Show the full sequence: requirements analysis → before development → development → development complete → testing → before release → released. Add activities by stage and show early feedback in requirements/design/development (shift-left) and post-release observation (shift-right). Candidate activities include story review, estimation, solution design, iteration planning; feature/story kickoff, test design/plan; unit/component/integration tests; lower-level test review, testable build, and test handoff; story testing, exploratory testing, defect management, risk-based testing, regression; release guidance, UAT, version confirmation; monitoring, support, and quality analysis. Select applicable activities; label unknown ones as recommendations or Open.
4. **Test quadrants:** Explicitly show all four quadrants and their axes/labels so readers can see business-facing vs technology-facing and supporting the team vs evaluating the product. Candidate examples: Q1 unit/component/integration, Q2 user-story/acceptance examples, Q3 exploratory/UAT/usability, Q4 performance/load/security/reliability. If the team uses another quadrant convention, preserve and name it. Mark project-unsupported quadrants Open. Annotate automation/manual and tools as activity attributes, not as quadrant axes. The quadrants are a discussion map; they do not require equal investment in every project.
5. **Lean test layers:** Explicitly show the image's three candidate layers: unit tests at the base, API/integration tests in the middle, and exploratory tests at the top. Explain the feedback or risk each layer serves and adapt it to architecture and risk. Automation, manual work, and tools may be labeled. Do not prescribe fixed ratios, a universal pyramid shape, or mandatory gates for every layer.
6. **Iterations, release, and feedback loop:** Show the ongoing strategy cadence as “Iteration 1 → Iteration 2 → … → Iteration n → Release/production.” Explain how each iteration selects lifecycle activities, quadrants, and test layers based on risk, and how test results, production signals, or user feedback inform the next iteration's goals and risks. Mark cadence, monitoring, or support mechanisms Open when unknown; do not claim they already exist.
7. **Gates, ownership, and gaps:** Repeat only sourced release gates and named owners; quality remains a whole-team responsibility. Collect unconfirmed decisions without presenting recommendations as approved decisions.

## Output Structure

```markdown
# <Project/release> | One-Page Test Strategy
Period: <known or Open> · Status: Draft/Discussed · Audience: <known or team>

**Guiding principle:** The whole team owns quality.

**Goal:** <business goal/quality outcome; Open if unknown>

### What to test | Functionality · Performance · Security
| Functionality | Performance | Security | Other relevant attributes, if any |
| --- | --- | --- | --- |
| Priority risk/status | Priority risk/status | Priority risk/status | Priority risk/status |

### Test enablers and constraints | Environment · Data · Tools · Team
<Environment/infrastructure, test data and access limits, automation/manual approach and tools, relevant roles/capability; label each as a known fact, recommendation, or Open.>

### How to test | Lifecycle and shift-left/right
<Requirements analysis → Before development → Development → Development complete → Testing → Before release → Released; add relevant project activities. Show early feedback and post-release feedback.>

### Test quadrants
|  | Supports the team | Evaluates the product |
| --- | --- | --- |
| Business-facing | Q2: story/acceptance examples | Q3: exploratory/UAT/usability |
| Technology-facing | Q1: unit/component/integration | Q4: performance/load/security/reliability |

### Lean test layers
- Top: Exploratory testing (manual/tools and purpose)
- Middle: API/integration testing (feedback and purpose)
- Base: Unit testing (fast feedback and purpose)

### Iterations and feedback
Iteration 1 → Iteration 2 → … → Iteration n → Release/production; <explain how known test results/production signals inform the next iteration; label unknown user-feedback channels or other signals as recommendations/Open>

**Open questions:** <only gaps, gates, and decisions that affect the strategy>
```

Compress these modules into one working page using short phrases, a matrix, and a compact diagram; do not repeat the same activity. Use one compact line for test enablers and constraints, distinguishing known environment/data/tool/team conditions from Open items. Lay out quadrants with business-facing vs technology-facing vertically and supports-the-team vs evaluates-the-product horizontally. Quadrants and test layers are selection frameworks, not fixed checklists, execution order, or ratios. Cells may be marked “applicable/deferred/Open.” Keep all lifecycle stages visible; mark a stage Open when its activities are unknown. For production, state only known signals or clearly label proposed feedback mechanisms as recommendations/Open.

## Pre-delivery Check

- Does the page explicitly show the guiding principle, goal, functionality/performance/security, test enablers/constraints, all seven lifecycle stages, shift-left/right, four quadrants, exploratory/API/unit layers, iteration cadence, and feedback loop?
- Are quadrants and layers treated as selection frameworks instead of mandatory checklists, execution order, or fixed ratios?
- Are the quadrant axes oriented correctly: business/technology vertically and supports/evaluates horizontally?
- Are facts, recommendations, inferences, and open items distinct, with no invented gates, ratios, schedules, tools, owners, or production capabilities?
- Is this still a one-page strategy summary rather than a full test plan, case list, or execution conclusion?

## Source Basis

This skill draws on [BY Linzi, “One-Page Test Strategy”](https://www.bylinzi.com/2020/01/10/one-page-test-strategy/) for its presentation of shared team ownership, what/how to test, lifecycle shift-left/right, quadrants, lean test layers, and iterative feedback. Current project evidence determines activities and priorities.
