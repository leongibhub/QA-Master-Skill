# CR-034 bounded defect and follow-up record

Document State: DRAFT. Initial source before repair: `ebfc947`; first repaired
runtime `58c73ec`, initial frozen delivery `5c516a6`. Late source repair
`c2e7957` supersedes that product freeze; fresh installed evidence passed at
`../verification/evidence/cr034/delivery-repair/delivery-metadata.json`.
These are local engineering findings,
not enterprise tracker issues or project Gate decisions.

| ID | Severity | Reproduction / consequence | Repair / verification | State |
| --- | --- | --- | --- | --- |
| BUG-016 | P2 | A valid old gap for unknown candidate TC-MD-UNKNOWN with reason OTHER produced ORPHAN_CANDIDATE but no gap_followup, losing the declared reason/action. | Iterate each old explicit gap, including orphan/duplicate occurrences; developer and independent TC-IMPACT-007 regression. | REPAIRED_AND_RETESTED in bounded offline scope |
| BUG-017 | P2 | An unresolved model obligation plus source SHA change yielded only UNRESOLVED_MODEL_OBLIGATION in the row action, hiding concurrent context reasons. | Action precedence no longer discards reasons; independently retain obligation reasons for baseline/removal as applicable; developer regressions and TC-IMPACT-004/007. | REPAIRED_AND_RETESTED in bounded offline scope |
| BUG-018 | P2 | MethodImpactError inherits ValueError and the adapter swallowed it; direct oversized input and nested writer stale-baseline errors became INVALID_SCHEMA. | Pass through MethodImpactError before generic adaptation; developer direct/writer/CLI exact-code regressions and independent strict writer/CLI checks. | REPAIRED_AND_RETESTED in bounded offline scope |
| BUG-019 | P2 | Baseline MISSING=1 had no candidate identity in the impact report, contradicting the claimed actionable missing-point followup. | Reviewed DES-063 clarification: controlled BASELINE_NONCONFORMANT marker on specific MISSING/DUPLICATE/MISMATCH candidate groups; no fabricated authored gap. Packaged example/developer and independent regressions identify the exact candidate. | REPAIRED_AND_RETESTED in bounded offline scope |
| BUG-020 | P2 | At 55594d7 a 2-before/1-after AMBIGUOUS group populated singular after_candidate_id on both old rows, implying an unproven mapping. | c2e7957 emits a singular after ID only for a unique RETAINED_VECTOR; developer and independently authored ambiguity fixtures pass. Fresh archive wheel/module/Skill helper verification also passes. | REPAIRED_AND_RETESTED in bounded offline scope |
| CR034-R-P3 | P3 | Markdown code spans for the three digests included a cosmetic trailing space; JSON identities were exact. | c2e7957 removes the spaces; developer exact-digest regression and independent review passed. | REPAIRED_AND_RETESTED in source scope |

Retained root preflight issues also included initially incomplete Markdown,
insufficient escaping, quadratic gap lookup and one-sided ambiguous grouping.
These were repaired before `ebfc947`; developer tests and independent reviewer
multiplicity probes support the repair within the stated contract.

Evidence: `../verification/method-impact-delivery-2026-10-23.md`,
`../verification/method-impact-independent-test-2026-10-23.md`, and
`../verification/method-impact-independent-review-2026-10-23.md`.
No actual regression run, acceptance, release, external defect closure or
whole-product superiority follows from these engineering results.
