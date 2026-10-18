# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

A refund query retrieves C1-v2: returns within 14 days if unused; shipping is not refunded. The rubric requires time and unused conditions. A-1 says shipping is refundable within 14 days and cites C1. A-2 includes both conditions and excludes shipping. A-3 says only 'within 14 days', omitting unused. A-4 asks a warranty question outside the corpus and correctly states insufficient evidence, requesting policy. Decide CONTRADICTED/PASS/INCOMPLETE/APPROPRIATE_REFUSAL with claim/citation mapping; citation presence alone cannot pass.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| A-1 | CONTRADICTED |
| A-2 | PASS |
| A-3 | INCOMPLETE |
| A-4 | APPROPRIATE_REFUSAL |

## Verification Method

1. Fix query/sample, knowledge/index/retrieval/model/prompt versions. Map queries to retrieved chunks, atomic claims and citations with support/contradiction/gap labels.
2. Judge citation accuracy, claim support and completeness separately. Supported claims may omit required conditions; use the task and project rubric.
3. Pair answerable in-corpus cases with out-of-corpus refusal controls. Assess task correctness, over-refusal and unsupported answers separately; refusal rate is no quality proxy.
4. Missing chunks, ground truth, permissions or gates remain UNKNOWN/NOT_RUN. Distinguish retrieval failure from generation misreading, retaining evidence boundaries and responsible stages.
