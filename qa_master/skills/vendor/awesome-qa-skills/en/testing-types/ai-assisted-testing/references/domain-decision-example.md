# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Same 10 checkout cases: manual baseline 60 minutes; AI generation 10, review 25, rework 35, acceptance 10. I-1: sanitized input, QA R1 reviews D1 assertions, adopted V2 executes and acceptance is 10/10. I-2: D2 is called adopted without Human review. I-3: team claims total time improved using generation time alone. Decide I-1/I-2 ACCEPTED/DRAFT, I-3 UNSUPPORTED/SUPPORTED, showing total labor and provenance.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| I-1 | ACCEPTED |
| I-2 | DRAFT |
| I-3 | UNSUPPORTED |

## Verification Method

1. Record input classification, sanitization, and allowed use. Replace identities, tokens, and personal data with non-reversible placeholders while retaining schema/business constraints.
2. Trace input snapshot→model/prompt version→AI draft ID→Human review→adopted version ID→acceptance evidence. Drafts do not automatically become execution assets.
3. Name the reviewers of business oracles, assertions, privacy, and high-risk tradeoffs. Unreviewed work remains draft, unexecuted work NOT_RUN; AI does not accept on behalf of Human.
4. Compare equal tasks/complexity/windows: manual baseline versus AI generation+review+rework+acceptance time. Track defects/rework separately; generation time alone cannot prove productivity gains.
