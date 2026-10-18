# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Policy D1-v2 section 2 permits returns within 14 days of receipt; section 3 excludes shipping refunds. H-1 claims returns within 14 days. H-2 claims shipping is refunded. H-3 claims section 9 grants lifetime warranty, although the supplied document contains only sections 1–3 and no warranty information. H-4 claims an overseas clause was added today, but the current source is inaccessible. Map each to SUPPORTED/CONTRADICTED/MISSING_SOURCE/UNASSESSABLE; do not let one supported claim approve the whole answer.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| H-1 | SUPPORTED |
| H-2 | CONTRADICTED |
| H-3 | MISSING_SOURCE |
| H-4 | UNASSESSABLE |

## Verification Method

1. Split independently checkable claims including numbers/units, entities, conditions, dates, and citations. Assign IDs, retaining original answer text and evidence version/location.
2. SUPPORTED means evidence supports the same scope; CONTRADICTED means explicit opposing evidence; MISSING_SOURCE means no supplied support or direct contradiction; UNASSESSABLE means inaccessible, unclear-scope, or outdated evidence prevents comparison. Missing support alone does not prove fabrication.
3. Check citation existence, accessibility, relevance, and claim support separately. A real source with an opposing number is a contradiction; do not label an entire mixed paragraph at once.
4. Preserve claim denominators and separate supported rates from unknown proportions. Without ground truth or adequate sampling provide the check plan, not factual-accuracy proof.
