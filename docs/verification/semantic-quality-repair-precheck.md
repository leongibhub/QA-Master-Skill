# CR-013 semantic-quality repair precheck

- Artifact ID: `DOC-SEMANTIC-QUALITY-REPAIR-PRECHECK-001`
- Review phase: `PREFREEZE_REPAIR_OBSERVATION`
- Document State: `DRAFT`
- Evaluation State: `IN_REVIEW`
- Evidence Status: `OBSERVED`
- Reviewer: `/root/workflow_review`
- Reviewed repair commit: `9085c5fdb2df72303ecd478542037c98637d3a6c`
- Reviewed source: `qa_master/semantic_quality.py`
- Source SHA-256: `189835888693AD727C8FC1DEA269FE99CB7672D025872E85FE962877875070D8`
- Design baseline: `DES-060` v4, commit `38f5073`, SHA-256 `4611C6C9ADD08AE913E25512361B45369C1F439715CF620FCF875D7B51148B42`
- Predecessor finding record: `DOC-SEMANTIC-QUALITY-PREFREEZE-FINDINGS-001`
- Date: 2026-10-15

This is a bounded, read-only precheck of the repair for the three P2 findings
recorded against commit `6905e02`. It does not overwrite that historical
record. It is not the formal TASK-063 review, an independent TASK-062 test
conclusion, defect closure, acceptance, release recommendation, or Gate
decision. TASK-062 attempt 2 was still running when this record was written.

## Disposition

| Original finding | Targeted precheck disposition | Severity still open |
|---|---|---:|
| P2-1 — `STRING_SET` maximum missing | Repair is present and the focused 256/257 paths pass | 0 in this bounded precheck |
| P2-2 — invalid manifest misclassified | Strict structure and installed-deriver reason boundaries are present; focused mutations pass | 0 in this bounded precheck |
| P2-3 — non-linear case/gap evaluation | Partially repaired; multi-obligation fan-out still repeatedly validates the same serialized references | P2 |

No P0 or P1 finding was observed in this bounded repair precheck. The remaining
P2 must be repaired and independently retested before it can be treated as
closed.

## Corrected boundaries observed

### P2-1 targeted correction

`_typed` now applies the 256-member maximum to `STRING_SET`. The developer
regression exercises a valid 256-member fact and observation, an invalid
257-member observation, and a rejected 257-member fact. The independent
attempt-2 suite also contains separate fact and observation boundary cases.
This is evidence for the targeted correction only; final closure belongs to
the completed independent test and formal review chain.

### P2-2 targeted correction

`_sq_manifest_structure` now checks the exact top-level and nested retained
manifest structures before inspection applies missing, mismatch, undeclared,
or intact outcomes. Focused mutations cover wrong scalar types, booleans in
integer fields, contract/asset structures, category rows, result rows,
diagnostics, limitations, ledger roles, and mixed-precedence cases. A validly
shaped changed identity remains `MISMATCH`, while malformed structure is
`INCOMPLETE`. Current installed implementation/asset binding errors are mapped
to `INSTALLED_DERIVER_MISMATCH` rather than profile derivation drift.

## P2 — multi-obligation fan-out still violates the linear join contract

### Contract and failure mode

DES-060 requires ID indexes before joins and evaluation in
`O(facts + obligations + observations + cases + gaps + references)` time. The
repair eliminates the original case-by-gap rescan for a single obligation, but
it caches validity by `(obligation_id, item_index)` and calls validators once
for every mapping edge. Those validators still rescan reference arrays and
case sections that are identical for every mapped obligation:

- `_gap_valid` (`semantic_quality.py:571-579`) revalidates the complete
  `obligation_ids`, fact IDs, source IDs, and all mapped obligations' required
  reasons for each mapped obligation;
- `_case_valid` (`semantic_quality.py:582-613`) revalidates the complete
  `obligation_ids`, category agreement, source/gap/missing references, claims,
  sections, and oracle references for each mapped obligation;
- `_artifact_provenance` (`semantic_quality.py:616-638`) again revalidates the
  complete item binding, top-level references, every section claim, and oracle
  references for each mapped obligation; and
- `derive_profile` (`semantic_quality.py:649-656`, `698-703`) invokes these
  paths for every item-to-obligation mapping.

The item-wide structure and serialized reference lists therefore cost roughly
fan-out times list length rather than being validated once.

### Reviewer reproduction

The reviewer changed no repository file. A test fixture was expanded in memory
to 64 obligations, one case referencing all 64 obligations, and one matching
observation per obligation. `_valid_refs` was wrapped only to count calls and
list elements examined while `derive_profile` ran:

```python
from tests.test_semantic_quality import SemanticQualityTests
from pathlib import Path
import qa_master.semantic_quality as sq

t = SemanticQualityTests(); t.setUp()
base_ob = t.bundle["obligations"][0]
t.bundle["obligations"] = [
    dict(base_ob, id=f"OB-{i}", check_id=f"CHECK-{i}") for i in range(64)
]
t.response["observations"] = [
    {"check_id": f"CHECK-{i}", "value_type": "STRING", "value": "yes",
     "source_fact_ids": ["F-1"]}
    for i in range(64)
]
case = t.complete_case()
case["obligation_ids"] = [f"OB-{i}" for i in range(64)]
t.response["cases"] = [case]
t.update_response()
state = sq._validate_bundle(t.write_bundle())
state["implementation_raw"] = Path(sq.__file__).read_bytes()

original = sq._valid_refs
stats = {"calls": 0, "elements": 0}
def counted(value):
    stats["calls"] += 1
    if isinstance(value, list):
        stats["elements"] += len(value)
    return original(value)

sq._valid_refs = counted
try:
    profile = sq.derive_profile(state)
    print(len(profile["rows"]), len(case["obligation_ids"]), stats)
finally:
    sq._valid_refs = original
    t.tearDown()
```

Observed result:

```text
profile_rows=256 case_input_refs=64
valid_refs_calls=1217 reference_elements_revisited=9152
```

The independent tester reproduced the same structural growth with a separate
fixture and retained it at
`docs/verification/evidence/cr013-semantic-independent-attempt2/multi-obligation-fanout.json`:

| Obligations referenced by one case | Same mapping-list validations | Same mapping elements visited |
|---:|---:|---:|
| 4 | 10 | 40 |
| 8 | 18 | 144 |
| 16 | 34 | 544 |
| 64 | 130 | 8,320 |

This is a structural call/reference-count observation, not a timing or service
level benchmark. It shows the current developer test is insufficient: counting
one `_case_valid` and one `_gap_valid` call per mapped item for a single
obligation does not exercise multi-obligation fan-out inside those calls.

### Bounded complexity definition

For this contract, use these input/output size terms:

- `V`: the number of facts, obligations, observations, cases, and gaps;
- `E`: the number of serialized reference occurrences across `source_ids`,
  `source_fact_ids`, `expected_fact_ids`, `obligation_ids`, `gap_ids`,
  `fact_ids`, `oracle_fact_ids`, claim references, and section items; and
- `R`: the result actually materialized, including four rows per obligation and
  each emitted evidence pointer.

The implementation target is `O(V + E + R)`. `R` makes necessary output work
explicit; it does not permit input validation to rescan the same serialized
reference array once per mapping. In the 64-obligation reproduction, output
must contain 256 rows and the mapped case pointer may legitimately appear once
per applicable output row. That required output does not account for more than
8,000 visits to the same 64-element input list.

Obligation-specific semantic work is allowed once per explicit mapping edge
when the result really depends on that obligation. Each such check must use
precomputed sets or indexes. The contract does not require a constant-time
whole evaluation and does not prohibit the necessary `R` output work.

### Repair criteria

1. Parse and validate each item's identity, fixed member set, reference-list
   shape, claims, sections, and oracle structure once per item.
2. Canonicalize reference lists once and build forward/reverse indexes once.
   Membership and category/readiness checks for one mapping edge must use those
   sets/indexes rather than rescan serialized lists.
3. Separate item-wide case validity from obligation-specific checks. Cache
   item-wide provenance validity once; evaluate the obligation-specific subset,
   readiness, category, exact-gap, and expected-oracle relationship once per
   explicit edge.
4. Apply the same split to gaps. Validate the item-wide gap contract once, then
   compare a mapped obligation's required reason and required fact/source sets
   through indexed membership.
5. Precompute each obligation's required fact/source sets and typed expected
   values once. Preserve all current per-obligation row outcomes, reasons,
   diagnostics, and evidence pointers.
6. Add a structural regression with one case and one gap at substantial
   multi-obligation fan-out. Instrument serialized-list element visits, or an
   equivalent lower-level operation, and demonstrate growth bounded by
   `O(V + E + R)`. Single-obligation call counts alone are not sufficient.
7. Recheck the same join pattern in `_gap_valid`, `_case_valid`, and
   `_artifact_provenance` together so the repair does not move the repeated
   scan from one dimension to another.

## Review boundary

This precheck did not rerun the full developer or independent suites, execute a
fresh-wheel workflow, change source/tests, or make a TASK-063, Gate, acceptance,
release, or quality conclusion. The prior 6905 finding record and TASK-062
attempt-1 failure evidence remain historical. TASK-062 attempt 2 must retain
the current fan-out failure, test the next repair against multi-obligation input,
and publish its own final evidence before formal independent review begins.
