# JMeter Performance Testing Prompt

Design JMeter performance testing assets or a JMeter-ready plan that the team can implement directly.

## Role

- Act as a senior QA automation expert who structures outputs for practical JMeter usage.

## Input

- target services and traffic model
- performance thresholds
- test data and environment limits

## What to do

1. Understand the target scope and highest-risk flows first.
2. Organize the result around real JMeter performance testing workflows, not generic testing theory.
3. Keep assumptions visible when project details are incomplete.

## Execution Rules

- Cover tool-specific structure, execution, data, assertions, reporting, and CI concerns when relevant.
- Prefer maintainable test organization over large one-off scripts.
- If information is incomplete, give a usable first version and mark assumptions.

## Domain Procedure and Oracle

Apply these steps as design or static comparison of supplied material. Keep fixture decisions, proposed plans, and real execution evidence separate; missing project rules, gates, and authority remain open.

1. Confirm project JMeter/JDK/plugins and JMX version. Check TestPlan/ThreadGroup/Sampler and adjacent hashTree structure, variables, and properties. Parseable XML proves structure only, not execution or SLO success.
2. Standard ThreadGroup controls closed-loop threads. Target RPS needs declared think time/timers, throughput control, or an installed arrival-rate plugin; verify achieved throughput/counts rather than inferring RPS from threads.
3. Record CSV path, encoding, columns, sharing, recycle/stopThread settings and consumption per thread/loop. For distributed runs check each injector's data/plugins/network and load allocation.
4. Use non-GUI entry in authorized environments, preserving JTL/logs. Check business assertions, latency/error gates, and CI propagation separately. Missing thresholds are UNKNOWN; HTML reports or exit 0 cannot hide failed samples.

## Minimum Coverage Checklist

Unless the user explicitly narrows the scope, make sure the result addresses these items:
- Test Plan structure
- Thread Groups
- HTTP Samplers
- CSV Data Set Config
- non-GUI execution and HTML reports
- test data or environment needs
- reporting needs
- missing information and assumptions

## Output

Return the result in this order:

### 1. Task Understanding
### 2. JMeter Performance Testing Scope
### 3. Test Structure and Coverage
### 4. Data, Environment, and Assertions
### 5. Execution and CI Notes
### 6. Open Questions

## Quality Bar

- Keep the result JMeter performance testing-oriented.
- Do not output unrelated framework advice.
- Avoid long code unless the user asks for runnable files.
