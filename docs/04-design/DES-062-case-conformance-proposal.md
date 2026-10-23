# DES-062: deterministic test-case conformance audit

- Document State: DRAFT
- Evaluation State: IN_REVIEW
- Change: CR-033
- Requirements: REQ-029–031, NFR-013
- Implementation, independent test and product evaluation: NOT_EXECUTED
- Human design direction: explicit `ok` on 2026-10-23; scoped implementation
  authorized. Formal baseline/Gate/acceptance/release decisions NOT_AVAILABLE.

## Recommended approach

Add a small offline module alongside the existing deterministic design engine.
It recomputes `design_methods(bundle)` and checks authored case scenario rows
against that authoritative result. Extend the installed CLI with:

```text
qa-master audit-method-cases --input campaign.json --cases cases.json --output audit.json
```

The installed Skill instructs the host Agent to use it after authoring cases,
inspect the findings, repair source-determined omissions, and retain genuine
unknowns. The QA user continues to ask for cases in ordinary chat.

## Options considered

| Approach | Benefit | Limitation | Decision |
| --- | --- | --- | --- |
| More specialist prompts or broad bilingual aliases | Low implementation cost | Duplicates much of the inherited library; does not check the deliverable | Defer |
| Typed scenario conformance against the existing finite design engine | Reproducible missing/value/oracle/staleness diagnostics without a model API | Does not establish completeness of the authored model or prose semantics | Recommended first increment |
| Extend the semantic evaluator into a general document judge | Potential broader quality analysis | Requires evaluator-owned facts/oracles and representative external ratings; greater interface coupling | Keep separate; evaluate later |

## Data flow and boundaries

1. Read the existing campaign bundle and a versioned case library.
2. Run `design_methods(bundle)`; bind the library to its `input_sha256`.
3. Build indexes for current candidates and existing unresolved obligations.
4. Compare the typed scenario rows in authored cases with candidate data and the
   exact sets of requirement/source/oracle IDs. These rows are the documented
   scenario inputs, not a replacement coverage claim inferred from a title.
5. Reconcile every candidate and preserve all engine obligations. Report missing,
   duplicate, orphaned, stale and mismatched rows separately.
6. Render JSON and a readable Markdown audit from the same result object. Do not
   generate a success score from the number of linked requirement IDs.

Proposed files: `qa_master/case_conformance.py` for the pure audit contract;
`qa_master/__main__.py` for an additive subcommand; a short bundled reference and
example under `qa_master/skills/codex/`; corresponding source entry instructions;
developer and independent tests in separately owned files. Field/error names are
fixed in the CR-033 implementation plan.

Proposed case library fields: schema identity/version, design input digest, and
unique case IDs with normal manual-case documentation plus explicit scenario
rows. A row contains a candidate ID, typed method data, requirement/source/oracle
ID sets and a concrete expected-result description. Multiple rows permit a
parameterized case. Extra expected-result prose is inspected for presence only;
no string-similarity rule claims to validate its business meaning.

The audit may say a scenario is exactly represented. It must never label the case
business-correct, executable, approved, passed, or semantically complete on that
basis. Generic prose with copied bindings still needs human/Agent content review.

## Compatibility and failure handling

Use the Python standard library and existing JSON/design helpers. Keep the
existing design output, semantic evaluator and campaign authority unchanged.
Proposed upper bounds are 5 MiB per input, 10,000 cases/candidates and 50,000 rows,
with explicit nesting and aggregate work limits. Validate engine-side limits
first; never reimplement its finite-model enumeration.

Reject duplicate keys, nonfinite numbers, stale input digests and invalid schema
identities. Compare typed JSON without Python bool/int coercion. Keep declared
decimal strings exact. Sort identity sets and diagnostics for stable output.
Output must not overwrite inputs or existing files; use the repository's reviewed
atomic-write/path policy, with no shell, network, adapter or campaign-state call.

Audit diagnostics contain IDs/codes/digests rather than source prose. User-visible
Markdown includes the relevant candidate IDs and reasons. Omitted or unavailable
business facts remain gaps. No model credentials or real test environment is
required for the audit itself.

## Delivery and evidence

Implementer, tester and reviewer remain separate. Development includes a source
example and a user-facing before/after demonstration: a requirement trace remains
present while one finite scenario disappears, and the audit exposes the omission.
Independent testing mutates each binding dimension, checks denominator arithmetic
and performs a fresh installed invocation. Independent review checks claim
boundaries, schema compatibility and file safety.

This design proposes an observable runtime capability beyond Awesome's guidance
library. It does not predeclare any comparative output-quality result. The
project's G0–G11 statuses remain unchanged.
