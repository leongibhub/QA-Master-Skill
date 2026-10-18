# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

R1-v2 says 'Cancellation is allowed 24 hours after payment' (within the first 24 hours or only after 24 hours). R2 allows authenticated refunds but defines no anonymous-refund rule. R3 has same-version statements 'free shipping for amount>=100' and 'amount>100'. R4 explicitly allows cancellation within 24h inclusive from the payment-success event. Decide AMBIGUOUS/MISSING_RULE/CONFLICT/CLEAR for R1–R4. Give two R1 consequences and one distinguishing question; do not invent ambiguity for R4.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| R1 | AMBIGUOUS |
| R2 | MISSING_RULE |
| R3 | CONFLICT |
| R4 | CLEAR |

## Verification Method

Uppercase decisions belong to a per-item decision view; RA findings retain ambiguous/missing/untestable/conflict/stale/out_of_scope. CLEAR is a valid control: show its testability in the overview rather than inventing a finding.

1. Retain requirement ID, source, version, and wording. Separate AMBIGUOUS (multiple meanings), MISSING_RULE (undefined behavior), CONFLICT (opposing sources), and CLEAR (testable wording); do not flag normal shorthand to manufacture findings.
2. For ambiguity show at least two plausible interpretations, conditions, different business/test consequences, and supporting wording. Without a plausible alternative, check whether material is merely missing.
3. Ask the smallest discriminating question about start event, comparison, commit point, or scope. Offer options while leaving the product decision with its owner.
4. Mark explicit criteria CLEAR with observable oracles. Do not fill gaps with invented limits or policy. Prioritize clarification by impact and implementation blockage.
