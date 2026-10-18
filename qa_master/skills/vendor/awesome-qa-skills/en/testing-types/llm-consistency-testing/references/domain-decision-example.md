# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Same sample S, model M1, prompt P2, temperature 0 and seed 7. The contract requires JSON fields decision=APPROVE and amount=20; reason may use equivalent wording. L-1: three valid outputs with amount 20 and equivalent reasons. L-2: the third of three outputs omits amount. L-3: one output is called stable. L-4: three valid structures lack a semantic oracle. Decide PASS/FAIL/INSUFFICIENT_EVIDENCE/UNKNOWN and show L-2's structural failure count and trial denominator.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| L-1 | PASS |
| L-2 | FAIL |
| L-3 | INSUFFICIENT_EVIDENCE |
| L-4 | UNKNOWN |

## Verification Method

1. Fix sample ID, model/prompt/tool/data versions, temperature, seed where supported, and other sampling parameters, with project-supplied repetition counts. Equal seeds do not establish reproducibility across versions.
2. Check structural invariants first: schema, required fields, enums, and policy. Then compare semantic decisions using the project rubric; permitted paraphrases/order changes are not failures.
3. Report repeated-trial denominators, structural/semantic failure counts, and intermittent failures per sample. Variance needs a named numeric variable, unit, and formula; wording difference rates are not quality variance.
4. Single observations establish no repeated consistency. Missing rubrics leave semantic consistency UNKNOWN. Separate parameter/version groups rather than pooling them as stability evidence.
