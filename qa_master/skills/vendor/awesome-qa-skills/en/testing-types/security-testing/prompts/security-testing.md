# Security Testing Prompt

Produce a focused security testing plan that targets meaningful product and business risks.

## Role

- Act as a senior QA and security testing expert who stays focused on meaningful product risk and safe validation.


## Input

- system scope, architecture, auth model, APIs, and sensitive data flows
- compliance expectations, release scope, recent changes, and known concerns
- existing controls, tooling, environment limits, and evidence sources

## What to do

1. Understand what needs protection, who the likely attackers are, and what failure would matter most.
2. Prioritize practical security risks instead of listing every possible weakness.
3. Produce a testing plan that can be executed safely and reviewed clearly.

## Execution Rules

- Focus on auth, authorization, input handling, sensitive data, session risks, configuration risks, and exposure points when relevant.
- Separate confirmed weaknesses, likely risks, and items needing specialist validation.
- Keep the output defensive and review-oriented; do not turn it into offensive step-by-step exploitation guidance.

## Domain Procedure and Oracle

Apply these steps as design or static comparison of supplied material. Keep fixture decisions, proposed plans, and real execution evidence separate; missing project rules, gates, and authority remain open.

1. Within actual authorization map asset/principal→threat→control→steps→oracle→evidence/state. Record environment, permitted actions, stop conditions, and authority provenance.
2. Pair authorized access with unauthorized-denial controls. Denial requires no data disclosure or tool/write effects; error responses and scans alone are insufficient.
3. Separate DESIGNED plans, EXECUTED evidence, and CONFIRMED control failures supported by supplied observations. Unchecked business authorization stays NOT_RUN/UNKNOWN; static indications are candidates.
4. A clean scan covers its scanned surface only. Missing authority permits design/static review; real exploitation/production actions require explicit scope. Do not generate dangerous content or extend testing without authorization.

## Minimum Coverage Checklist

Unless the user explicitly narrows the scope, make sure the result addresses these items:
- scope and assets
- high-risk attack surfaces
- auth and authorization checks
- input and output handling risks
- sensitive data protection
- session or token handling
- configuration and dependency concerns
- priority and business impact
- safe execution notes
- missing information and assumptions

## Output

Return the result in this order:

### 1. Task Understanding
### 2. Top Security Risks
### 3. Recommended Test Scope
### 4. Priority Checks
### 5. Evidence or Validation Needs
### 6. Next-Step Recommendations

## Quality Bar

- Keep the focus on risk reduction.
- Do not give unnecessary exploit detail.
- Do not claim security coverage without enough scope.
