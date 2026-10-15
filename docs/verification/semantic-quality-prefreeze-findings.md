# CR-013 semantic-quality implementation prefreeze findings

- Artifact ID: `DOC-SEMANTIC-QUALITY-PREFREEZE-FINDINGS-001`
- Review phase: `PREFREEZE_OBSERVATION`
- Document State: `DRAFT`
- Evaluation State: `IN_REVIEW`
- Evidence Status: `OBSERVED`
- Reviewer: `/root/workflow_review`
- Reviewed implementation commit: `6905e0209b1159c8a8fd2b5799a74cf22adea240`
- Reviewed source: `qa_master/semantic_quality.py`
- Source SHA-256: `65DD50954784B6EB8D632869CD95162B6F028FF6F63618DDD83739658A220295`
- Design baseline: `DES-060` v4, commit `38f5073`, SHA-256 `4611C6C9ADD08AE913E25512361B45369C1F439715CF620FCF875D7B51148B42`
- Date: 2026-10-15

This record preserves implementation defects found before independent TASK-062
testing. It is not the formal TASK-063 review, an independent test conclusion,
a defect closure, an acceptance or release recommendation, or a Gate decision.
The reviewer did not edit source or tests and did not rerun the developer's
full regression suite. The observations below come from static review plus
bounded read-only reproduction scripts against the frozen subject.

## Severity summary

| Severity | Open findings |
|---|---:|
| P0 | 0 |
| P1 | 0 |
| P2 | 3 |
| P3 | 0 |

## P2-1 — `STRING_SET` accepts more than 256 members

The shared typed-value contract allows a `STRING_SET` to contain zero through
256 unique nonempty strings. In `semantic_quality.py:241-243`, `_typed` checks
only that the value is a list of nonempty strings and equals its sorted unique
form. It does not enforce the 256-member limit.

A bundle with a 257-member sorted unique set in both the visible fact and the
matching observation was accepted by `validate_bundle`, and its SEMANTIC row
was reported as `SATISFIED`:

```text
validate_257_string_set VALIDATED_NOT_EVALUATED
semantic_257_string_set SATISFIED
```

This violates `DOC-PAIRED-VALUE-ENCODING-CLARIFICATION-001` and the DES-060
typed-value binding. It also leaves the declared capacity boundary untested;
the developer suite covers JSON node count but not `STRING_SET` 256/257.

Repair criteria:

1. accept exactly 256 valid set members and reject 257 without coercion;
2. apply the same rule to bundle facts and response observations;
3. preserve sorted, unique, nonempty-string and per-string length rules; and
4. add focused 256/257 regressions through the public validation/evaluation
   paths, not only a direct helper assertion.

## P2-2 — `inspect` does not strictly classify an invalid manifest

DES-060 v4 requires a strict manifest parse before retained-file integrity
classification. An absent or invalid manifest is `INCOMPLETE`; a valid manifest
whose retained bytes or deterministic derivation differ is `MISMATCH`.

`inspect_result_state` at `semantic_quality.py:922-952` validates the manifest's
top-level member set, schema/result ID and shallow file-ledger shape, but does
not validate the types and nested contracts for `evaluation_id`,
`fixture_class`, contract/asset hashes, category rows, diagnostics, result rows,
limitations, or several other fixed members. Those defects flow into the later
expected-manifest comparison at lines 962-996 and are classified as
`MISMATCH / PROFILE_DERIVATION_MISMATCH`.

The reviewer changed only the retained manifest's `evaluation_id` to an array.
The observed result was:

```text
manifest_invalid_field {'status': 'MISMATCH',
 'reason': 'PROFILE_DERIVATION_MISMATCH'}
```

The same broad exception path also converts failures while loading or binding
the current installed six assets into `PROFILE_DERIVATION_MISMATCH`, rather
than the design's `INSTALLED_DERIVER_MISMATCH`. This weakens the stable status
boundary and can misclassify an invalid evidence root as a valid manifest with
changed derived content.

Repair criteria:

1. validate every manifest member and nested row against the exact frozen
   result contract before applying file/status precedence;
2. return `INCOMPLETE` for malformed JSON, duplicate keys, wrong member sets,
   invalid types/enums, invalid nested diagnostics/rows/ledger, and impossible
   manifest invariants;
3. retain `MISSING` for files declared by a valid manifest but absent,
   `MISMATCH` for byte/hash/identity/profile derivation differences, and
   `UNDECLARED` only after higher-precedence checks pass;
4. map a current installed evaluator or asset absence/drift to
   `MISMATCH / INSTALLED_DERIVER_MISMATCH`; and
5. add independent mutations for top-level and nested manifest types plus the
   installed-deriver reason boundary.

## P2-3 — case/gap evaluation is quadratic despite the linear design contract

DES-060 section 3 requires indexing before joins and evaluation in
`O(facts + obligations + observations + cases + gaps + references)` time.
The implementation instead rebuilds and revalidates all mapped gaps inside
every `_case_valid` call (`semantic_quality.py:591-592`). `derive_profile` then
calls `_case_valid` once during usability selection at line 682 and again for
each case during provenance diagnostics at line 689.

The reviewer instrumented `_gap_valid` in memory without changing repository
files. A single valid obligation with 256 mapped cases and 256 mapped gaps
produced:

```text
rows 4 gap_valid_calls 131584 cases 256 gaps 256
```

This is a cases-by-gaps join before accounting for multi-obligation reference
fan-out, rather than work proportional to declared rows and references. The
finite caps prevent an unbounded loop but do not satisfy the frozen complexity
contract and create avoidable worst-case regression risk.

Repair criteria:

1. precompute unique item identity, per-obligation exact-gap state, case
   validity and provenance validity once;
2. reuse those indexed results across USABILITY, PROVENANCE and diagnostics;
3. avoid rescanning all gaps from each case or recomputing the same case twice;
   and
4. add a maximum-fan-out structural test or call-count assertion demonstrating
   work proportional to rows plus reference edges rather than case-gap pairs.

## Review boundary and next evidence

The remainder of the reviewed source showed no P0/P1 issue in the frozen
projection registry, typed boolean/integer/JSON comparison, obligation-local
outcome ordering, source-byte retention, result-ID derivation, exclusive
reservation/manifest publication, no-overwrite behavior, or process/network
side-effect boundary.

These P2 findings remain open until a separately owned implementation repair is
frozen and TASK-062 independently verifies the exact repair criteria. Formal
TASK-063 review must bind that final source, all retained failure evidence and
the completed TASK-062 report; this document cannot substitute for it.
