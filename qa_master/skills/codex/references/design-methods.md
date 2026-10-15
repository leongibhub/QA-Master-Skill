# Offline deterministic method design

Use the installed helper for a local, draft-only finite-model design:

```text
python -I "<skill-root>/scripts/qa.py" design --input bundle.json --output report.json
```

The input uses the strict DES-033 campaign JSON grammar. It has a non-empty
`project`, a `requirements` array, and optionally `design_models` containing
declared source/oracle references and finite boundary, decision-table, or
state-transition models. Decimal values are canonical strings. The helper
does not open declared locators, infer missing rules, or accept credentials.
See `../examples/design-methods.json` for instructional non-secret data; its
locators are declared example bindings, not installed source files.

The report remains `DRAFT_UNAPPROVED` and `NOT_EXECUTED`. `method_design`
contains finite-model candidates and obligations. `installed_design` records
the selected bundled guides, declared source mapping, and wrapper gaps. A
method candidate is not automatically a usable or executable case: inspect
the supplied source and guide, then create a reviewable draft case for each
determinable obligation or retain a typed gap for missing target, observable,
setup, cleanup, source, or oracle facts.

The helper rejects invalid UTF-8/JSON, duplicate JSON keys, non-finite values,
sensitive-shaped method fields, malformed references, over-limit input, and
same input/output paths. A rejection leaves an existing output unchanged. It
does not read Campaign state, approve requirements, run tests, call a model,
start a process, use a network, or write an external system.
