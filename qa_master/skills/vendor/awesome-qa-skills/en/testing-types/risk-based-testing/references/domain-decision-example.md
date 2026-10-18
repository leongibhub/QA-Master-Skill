# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Window30min. Project requires duplicate-debit protection:20min for same-ID retry, one ledger entry, and reconciled balance; tenant authorization also requires20min. Copy check takes5min. R1 has a known loss escape; R2 lacks authorization evidence; R3 is minor copy change. Decide MUST_PROTECT for R1/R2, DEFER for R3, and ESCALATE for BUDGET with concrete minimum evidence;30min cannot satisfy both mandatory checks and is no waiver.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| R1 | MUST_PROTECT |
| R2 | MUST_PROTECT |
| R3 | DEFER |
| BUDGET | ESCALATE |

## Verification Method

1. Anchor qualitative risk in observable impact, exposure/occurrence evidence, detectability, and control gaps. Without a project numeric model do not invent score products; unknown likelihood remains uncertain.
2. Link each risk to objective, layer/platform, depth, data, minimum observable evidence, sourced duration, and residual risk. High risk needs falsifiable business assertions, not merely more cases.
3. Allocate the constrained window with mandatory protection/authority first. Expose deferrals, alternatives, owners, and Human risk acceptance; time shortage never automatically waives gates.
4. Retain benign/low-risk controls, selection reasons, and scope expansion triggers. Planned priority is no execution or risk-elimination evidence.
