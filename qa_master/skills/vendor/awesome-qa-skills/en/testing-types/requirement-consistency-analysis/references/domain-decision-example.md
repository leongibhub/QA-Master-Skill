# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Dictionary v2: member is the alias of the supplied membership term; cents=currency units×100. C-1 same v2 limit 100 units versus 10000 cents. C-2 same v2 refund limit 100 versus120 units. C-3 'active' means v1 account state in one source and v2 subscription state in another, with no identity/migration mapping. C-4 v2 state dictionary explicitly maps done=refunded. Decide EQUIVALENT/CONTRADICTED/NOT_COMPARABLE with unit/version/entity evidence; wording differences or cross-version names alone are no contradiction.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| C-1 | EQUIVALENT |
| C-2 | CONTRADICTED |
| C-3 | NOT_COMPARABLE |
| C-4 | EQUIVALENT |

## Verification Method

These decisions do not replace RC/BR fields: EQUIVALENT maps to aligned/assessed; same-scope CONTRADICTED maps to conflict/assessed; NOT_COMPARABLE retains unassessed or stale evidence without asserting aligned/conflict. Keep the decision view separate from Relation/Status.

1. Fix sources, versions, and effective dates. Build evidenced aliases, entity IDs, units, and state mappings; equal names are not automatically equivalent.
2. Compare rules with matched scope, version, and conditions. Convert units with documented factors and normalize states only through explicit mappings; never silently merge versions or entities.
3. EQUIVALENT needs traceable semantic/numeric equality. CONTRADICTED means rules cannot both hold under the same conditions. NOT_COMPARABLE means missing identity/version/unit mapping prevents comparison.
4. Show originals, normalized values, mapping sources, impact, and minimal clarification. One source cannot establish cross-document consistency; no stated authority means no automatic overwrite.
