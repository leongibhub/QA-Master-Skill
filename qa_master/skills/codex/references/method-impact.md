# Finite-model change impact

Use this after a saved finite design model changes and there is an existing
case library. The QA user stays in normal chat: ask the Agent to prepare the
old bundle, new bundle and old case-library JSON, compare them, then return
review proposals. The user does not hand-fill these files.

The comparison matches only identical typed formal vectors in the same model:
method, dimension and `method_data`. It separately reports changed requirement,
source, oracle and model context. It therefore avoids treating whole-model
candidate-ID churn as new test points, but does not infer that a renamed or
changed business requirement has the same meaning.

## Agent workflow

1. Keep the old bundle and its old case library together. The library must bind
   to the old design digest.
2. Prepare the new bundle from the updated declared facts. Refresh source or
   oracle descriptors when those facts changed; this command does not open
   external paths or URLs.
3. Run the comparison. Review every selected case, added vector, explicit gap,
   unresolved obligation and unmodeled changed requirement against the actual
   sources and case prose.
4. Return draft review proposals and unresolved items. Decide test execution or
   regression scope separately under the user's authorization.

From a source checkout:

```text
python -m qa_master impact-method-cases --before old-bundle.json --after new-bundle.json --cases old-cases.json --output impact.json
python -m qa_master impact-method-cases --before old-bundle.json --after new-bundle.json --cases old-cases.json --output impact.md --format markdown
```

From an installed Skill, resolve the Skill directory and use its helper:

```text
python -I "<skill>/scripts/qa.py" impact-method-cases --before old-bundle.json --after new-bundle.json --cases old-cases.json --output impact.json
python -I "<skill>/scripts/qa.py" impact-method-cases --before old-bundle.json --after new-bundle.json --cases old-cases.json --output impact.md --format markdown
```

Each of `--before`, `--after`, `--cases` and `--output` is required exactly
once. JSON is the default; Markdown presents the same generated report for
reading. Choose a new output path: the command refuses an existing output and
does not overwrite inputs. Exit 0 means only that the report was created; input
or I/O rejection returns exit 2 and is not a quality result.

## Read the proposal

`candidate_deltas` groups formal points as `RETAINED_VECTOR`, `ADDED`,
`REMOVED` or `AMBIGUOUS`. A unique retained pair can have different candidate
IDs because its complete model hash changed. `RETAINED_VECTOR` is not semantic
equivalence and does not by itself make existing evidence current.

`case_row_actions` gives every old scenario row one action. Review actions cover
changed binding/context, removed points, ambiguous matches and nonconformant
baseline rows. `review_case_ids` is the sorted set of cases selected by those
actions or case-level findings. `new_candidate_ids` identifies added points that
need a new case or an explicit gap; it does not create either automatically.

The report keeps `baseline_findings`, `obligation_deltas` and `gap_followups`
separate so that old missing coverage is not hidden by an update. An old
obligation appearing only before the change is not called resolved. `unknowns`
lists changed requirements outside both finite models.

## Packaged teaching example

The bundled `examples/design-methods.json` and `examples/method-cases.json`
form an old model/library pair. The library deliberately represents nine of ten
candidates and records no gap. `examples/design-methods-after.json` differs
only by a declared SHA-256 descriptor on `SRC-REQ`.

From a source checkout, this is a copyable command:

```text
python -m qa_master impact-method-cases --before qa_master/skills/codex/examples/design-methods.json --after qa_master/skills/codex/examples/design-methods-after.json --cases qa_master/skills/codex/examples/method-cases.json --output .qa-master/method-impact.json
```

From an installed Skill, use the same bundled paths relative to its directory:

```text
python -I "<skill>/scripts/qa.py" impact-method-cases --before "<skill>/examples/design-methods.json" --after "<skill>/examples/design-methods-after.json" --cases "<skill>/examples/method-cases.json" --output impact.json
```

The source descriptor change changes whole-model candidate IDs, but the formal
vectors remain paired: the result must not present those vectors as `ADDED` or
`REMOVED`. It should still request review/rebinding for affected old cases. The
teaching library produces ten retained-vector deltas and a baseline summary with
`MISSING: 1`; the affected delta preserves its old candidate ID and carries
`BASELINE_NONCONFORMANT` for review. It is not an explicit gap followup. These
are teaching findings, not executed defects or permission to skip regression.

## Limits

The analysis is bounded to strict local JSON inputs and compares declared
finite-model facts only. It does not read source bytes behind a locator, infer
renames or business semantics, assess code-only changes, judge case prose,
modify cases, execute tests, approve a baseline, or close a defect. A
`NO_DECLARED_IMPACT` row means only that this comparison found no declared
finite-model difference; it never means that regression is safe to skip.
