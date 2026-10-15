# Offline QA task: document release policy

This is a design-only task. All facts below are supplied by the product owner for draft review, not an approved requirement baseline. Do not execute product tests, contact external services, create state/approval records, or infer interfaces.

- F-01: A document batch size is a strict integer. The declared policy accepts sizes from 2 through 6 inclusive, on step 1 with origin 0. Values below 2 and above 6 are invalid. No API endpoint, UI control, rejection code/message, or validation implementation is provided.
- F-02: The rebate decision has two independent boolean inputs: member and settled. Rebate is allowed only when both are true; all other combinations result in no rebate. There are no excluded combinations and no additional rules.
- F-03: The document lifecycle has DRAFT, REVIEW, PUBLISHED. Initial state is DRAFT; PUBLISHED is terminal.
- F-04: Event submit in DRAFT is a valid transition to REVIEW; its declared effect is status becomes REVIEW. No guard is declared.
- F-05: Event publish in REVIEW is a valid transition to PUBLISHED; its declared effect is status becomes PUBLISHED. No guard is declared.
- F-06: Event publish in DRAFT is explicitly invalid; the document stays DRAFT. No persisted-data side-effect statement or error signal is supplied. Other state/event combinations are unspecified; absence is not a denial rule.
- F-07: Target interface, environment, setup fixtures, observable locators, cleanup obligations, performance thresholds and user authorization mechanics are not supplied. Record dependent gaps; do not create invented facts.

Requested deliverables: use the installed QA Master Skill to design boundary, decision-table and state-transition work from these facts. Invoke its installed offline design command. Retain the authored input and helper report, then deliver reviewable draft cases or explicit typed gaps for the source-determined obligations. Cite source IDs, show applicable guide use, state readiness and no-execution status, and distinguish helper candidates from completed cases. All final files belong under the provided task-output directory.
