"""Bounded, offline conformance audit for finite design-method candidates (CR-033)."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

from .design_methods import DesignMethodError, design_methods, load_bundle_json

_MAX_BYTES = 5_000_000
_MAX_DEPTH = 32
_MAX_CASES = 10_000
_MAX_CANDIDATES = 10_000
_MAX_ROWS = 50_000
_GAP_REASONS = {"SOURCE_MISSING", "ORACLE_MISSING", "SETUP_MISSING", "OBSERVABLE_MISSING", "CLEANUP_MISSING", "OTHER"}
_STATES = ("EXACTLY_BOUND", "GAP_RECORDED", "MISSING", "DUPLICATE", "MISMATCH")
_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$")


class CaseConformanceError(ValueError):
    """A stable, value-free rejection code for the audit boundary."""
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


def _fail(code):
    raise CaseConformanceError(code)


def _walk(value, depth=0):
    if depth > _MAX_DEPTH:
        _fail("JSON_DEPTH_EXCEEDED")
    if isinstance(value, float):
        _fail("FLOAT_FORBIDDEN")
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                _fail("INVALID_JSON_VALUE")
            _walk(item, depth + 1)
    elif isinstance(value, list):
        for item in value:
            _walk(item, depth + 1)
    elif not isinstance(value, (str, int, bool, type(None))):
        _fail("INVALID_JSON_VALUE")


def _canonical(value):
    _walk(value)
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    except (TypeError, ValueError, UnicodeError):
        _fail("INVALID_JSON_VALUE")


def _digest(value):
    return hashlib.sha256(_canonical(value)).hexdigest()


def _typed_equal(left, right):
    return _canonical(left) == _canonical(right)


def _id_set(value, code="INVALID_REFERENCE_SET"):
    if not isinstance(value, list) or any(not isinstance(item, str) or not _ID.fullmatch(item) for item in value):
        _fail(code)
    if len(value) != len(set(value)):
        _fail("DUPLICATE_REFERENCE")
    return sorted(value)


def _strict_keys(value, keys, code="INVALID_CASE_LIBRARY"):
    if not isinstance(value, dict) or set(value) != set(keys):
        _fail(code)


def _nonempty_text(value):
    return isinstance(value, str) and bool(value.strip())


def _is_link_or_reparse(path):
    try:
        return path.is_symlink() or bool(os.lstat(path).st_file_attributes & 0x400)
    except (AttributeError, OSError):
        return path.is_symlink()


def _load_json(payload):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                _fail("DUPLICATE_JSON_KEY")
            result[key] = value
        return result

    def constant(_):
        _fail("INVALID_JSON")
    try:
        value = json.loads(payload.decode("utf-8"), object_pairs_hook=pairs, parse_constant=constant)
    except CaseConformanceError:
        raise
    except (UnicodeDecodeError, ValueError, RecursionError):
        _fail("INVALID_JSON")
    _walk(value)
    if not isinstance(value, dict):
        _fail("INVALID_JSON")
    return value


def _preflight(bundle):
    """Bound aggregate finite replay before asking the existing engine to allocate rows."""
    try:
        models = bundle["design_models"]["models"]
    except (TypeError, KeyError):
        return
    if not isinstance(models, list):
        return
    total = 0
    for model in models:
        if not isinstance(model, dict) or not isinstance(model.get("spec"), dict):
            continue  # The authoritative engine reports the schema error.
        spec = model["spec"]
        method = model.get("method")
        if method == "boundary":
            total += 6
        elif method == "decision_table":
            conditions = spec.get("conditions")
            count = 1
            for item in conditions if isinstance(conditions, list) else [None]:
                count *= len(item.get("values", [])) if isinstance(item, dict) and isinstance(item.get("values"), list) else 4097
            total += count
        elif method == "state_transition":
            states = spec.get("states", [])
            triggers = spec.get("triggers", [])
            transitions = spec.get("transitions", [])
            total += ((len(states) * len(triggers) + len(transitions))
                      if isinstance(states, list) and isinstance(triggers, list) and isinstance(transitions, list)
                      else 4097)
        elif method in {"pairwise", "combinatorial"}:
            parameters = spec.get("parameters")
            count = 1
            for item in parameters if isinstance(parameters, list) else [None]:
                count *= len(item.get("values", [])) if isinstance(item, dict) and isinstance(item.get("values"), list) else 4097
            total += count
        else:
            total += 4097
        if total > _MAX_CANDIDATES:
            _fail("CANDIDATE_LIMIT_EXCEEDED")


def _validate_library(library, expected_digest):
    _walk(library)
    _strict_keys(library, {"schema_version", "design_input_sha256", "cases", "gaps"})
    if library["schema_version"] != 1 or isinstance(library["schema_version"], bool):
        _fail("UNSUPPORTED_SCHEMA_VERSION")
    digest = library["design_input_sha256"]
    if not isinstance(digest, str) or len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
        _fail("INVALID_DESIGN_DIGEST")
    if digest != expected_digest:
        _fail("STALE_DESIGN_INPUT")
    cases = library["cases"]
    gaps = library["gaps"]
    if not isinstance(cases, list) or len(cases) > _MAX_CASES or not isinstance(gaps, list):
        _fail("CASE_LIMIT_EXCEEDED")
    case_ids = set(); rows = []; normalized_cases = []
    for case in cases:
        _strict_keys(case, {"id", "title", "preconditions", "steps", "expected", "scenarios"})
        case_id = case["id"]
        if not isinstance(case_id, str) or not _ID.fullmatch(case_id) or case_id in case_ids:
            _fail("DUPLICATE_CASE_ID")
        case_ids.add(case_id)
        if not isinstance(case["steps"], list):
            _fail("INVALID_CASE_DOCUMENTATION")
        documentation_complete = bool(case["steps"]) and not any(not _nonempty_text(step) for step in case["steps"])
        documentation_complete = documentation_complete and all(_nonempty_text(case[key]) for key in ("title", "preconditions", "expected"))
        if not isinstance(case["scenarios"], list):
            _fail("INVALID_SCENARIO")
        if not case["scenarios"]:
            normalized_cases.append((case_id, False))
        for scenario in case["scenarios"]:
            _strict_keys(scenario, {"candidate_id", "method_data", "requirement_ids", "source_ref_ids", "oracle_ref_ids"}, "INVALID_SCENARIO")
            if not isinstance(scenario["candidate_id"], str) or not _ID.fullmatch(scenario["candidate_id"]):
                _fail("INVALID_SCENARIO")
            _walk(scenario["method_data"])
            _id_set(scenario["requirement_ids"])
            _id_set(scenario["source_ref_ids"])
            _id_set(scenario["oracle_ref_ids"])
            rows.append((case_id, documentation_complete, scenario))
        if case["scenarios"]:
            normalized_cases.append((case_id, documentation_complete))
    if len(rows) + len(gaps) > _MAX_ROWS:
        _fail("ROW_LIMIT_EXCEEDED")
    normalized_gaps = []
    for gap in gaps:
        _strict_keys(gap, {"candidate_id", "reason_code"}, "INVALID_GAP")
        if not isinstance(gap["candidate_id"], str) or not _ID.fullmatch(gap["candidate_id"]) or gap["reason_code"] not in _GAP_REASONS:
            _fail("INVALID_GAP")
        normalized_gaps.append(gap)
    return rows, normalized_gaps, normalized_cases


def _normalized_library(library):
    """Canonical library identity: declared sets are unordered, steps remain ordered."""
    result = {"schema_version": library["schema_version"], "design_input_sha256": library["design_input_sha256"],
              "cases": [], "gaps": []}
    for case in library["cases"]:
        normalized = {key: case[key] for key in ("id", "title", "preconditions", "steps", "expected")}
        scenarios = []
        for item in case["scenarios"]:
            scenarios.append({"candidate_id": item["candidate_id"], "method_data": item["method_data"],
                              "requirement_ids": sorted(item["requirement_ids"]), "source_ref_ids": sorted(item["source_ref_ids"]),
                              "oracle_ref_ids": sorted(item["oracle_ref_ids"])})
        normalized["scenarios"] = sorted(scenarios, key=_canonical)
        result["cases"].append(normalized)
    result["cases"].sort(key=lambda item: item["id"])
    result["gaps"] = sorted(({"candidate_id": item["candidate_id"], "reason_code": item["reason_code"]}
                             for item in library["gaps"]), key=_canonical)
    return result


def _candidate_refs(candidate, key):
    return sorted(item["id"] for item in candidate[key])


def audit_method_cases(campaign_bundle: dict, case_library: dict) -> dict:
    """Compare explicit authored scenario rows with fresh finite design candidates."""
    if not isinstance(campaign_bundle, dict) or not isinstance(case_library, dict):
        _fail("INVALID_SCHEMA")
    _walk(campaign_bundle)
    _preflight(campaign_bundle)
    try:
        design = design_methods(campaign_bundle)
    except DesignMethodError as error:
        _fail(error.code)
    candidates = design["candidates"]
    if len(candidates) > _MAX_CANDIDATES:
        _fail("CANDIDATE_LIMIT_EXCEEDED")
    rows, gaps, authored_cases = _validate_library(case_library, design["input_sha256"])
    known = {item["id"]: item for item in candidates}
    row_index = {candidate_id: [] for candidate_id in known}
    gap_index = {candidate_id: [] for candidate_id in known}
    findings = []
    cases_with_rows = {row_case_id for row_case_id, _, _ in rows}
    for case_id, _ in authored_cases:
        if case_id not in cases_with_rows:
            findings.append({"code": "ORPHAN_CASE", "case_id": case_id})
    for case_id, documented, scenario in rows:
        candidate_id = scenario["candidate_id"]
        if candidate_id not in known:
            findings.append({"code": "ORPHAN_CANDIDATE", "candidate_id": candidate_id, "case_id": case_id})
        else:
            row_index[candidate_id].append((case_id, documented, scenario))
    for gap in gaps:
        candidate_id = gap["candidate_id"]
        if candidate_id not in known:
            findings.append({"code": "ORPHAN_CANDIDATE", "candidate_id": candidate_id})
        else:
            gap_index[candidate_id].append(gap["reason_code"])
    output = []
    states = {state: 0 for state in _STATES}
    per_model = {}
    for candidate in candidates:
        candidate_id = candidate["id"]
        bound_rows = row_index[candidate_id]
        recorded_gaps = gap_index[candidate_id]
        codes = []
        if recorded_gaps and bound_rows:
            state = "MISMATCH"; codes.append("GAP_CASE_CONFLICT")
        elif len(bound_rows) > 1:
            state = "DUPLICATE"
        elif len(recorded_gaps) > 1:
            state = "DUPLICATE"; codes.append("GAP_DUPLICATE")
        elif recorded_gaps:
            state = "GAP_RECORDED"
        elif not bound_rows:
            state = "MISSING"
        else:
            case_id, documented, scenario = bound_rows[0]
            expected = {
                "method_data": candidate["method_data"], "requirement_ids": sorted(candidate["trace"]),
                "source_ref_ids": _candidate_refs(candidate, "source_refs"), "oracle_ref_ids": _candidate_refs(candidate, "oracle_refs"),
            }
            if not documented:
                codes.append("CASE_DOCUMENTATION_INCOMPLETE")
            for field, code in (("method_data", "DATA_MISMATCH"), ("oracle_ref_ids", "ORACLE_MISMATCH"),
                                ("source_ref_ids", "SOURCE_MISMATCH"), ("requirement_ids", "TRACE_MISMATCH")):
                actual = scenario[field] if field == "method_data" else _id_set(scenario[field])
                if not _typed_equal(actual, expected[field]):
                    codes.append(code)
            state = "EXACTLY_BOUND" if not codes else "MISMATCH"
        case_ids = sorted({item[0] for item in bound_rows})
        record = {"id": candidate_id, "model_id": candidate["model_id"], "method": candidate["method"],
                  "state": state, "case_ids": case_ids, "gap_reasons": sorted(set(recorded_gaps)), "codes": sorted(codes)}
        output.append(record); states[state] += 1
        per_model.setdefault(candidate["model_id"], {state: 0 for state in _STATES})[state] += 1
        for code in codes:
            findings.append({"code": code, "candidate_id": candidate_id, "case_ids": case_ids})
    output.sort(key=lambda item: item["id"])
    findings.sort(key=lambda item: (item["code"], item.get("candidate_id", ""), ",".join(item.get("case_ids", [item.get("case_id", "")] ))))
    return {"schema_version": 1, "status": "DRAFT_UNAPPROVED", "execution": "NOT_EXECUTED",
            "design_input_sha256": design["input_sha256"], "case_library_sha256": _digest(_normalized_library(case_library)),
            "candidates": output,
            "obligations": [{"id": item["id"], "code": item["code"], "model_id": item["model_id"], "method": item["method"]}
                            for item in design["obligations"]],
            "findings": findings,
            "summary": {"candidate_denominator": len(output), "states": states,
                        "assessment": "UNASSESSED" if not output else "ASSESSED", "state": "UNASSESSED" if not output else "ASSESSED",
                        "by_model": {result["model_id"]: per_model.get(result["model_id"], {state: 0 for state in _STATES})
                                     for result in design["model_results"]},
                        "obligation_count": len(design["obligations"]), "finding_count": len(findings)},
            "limitations": ["Exact binding establishes formal representation of declared finite candidates only.",
                            "It does not establish business correctness, prose quality, executability, approval, or a pass result."]}


def render_audit_markdown(report: dict) -> str:
    """Render the same report without adding a quality or execution claim."""
    if not isinstance(report, dict) or report.get("schema_version") != 1:
        _fail("INVALID_REPORT")
    lines = ["# QA Master case conformance audit", "", "Status: `DRAFT_UNAPPROVED`", "Execution: `NOT_EXECUTED`", "",
             "Exact binding establishes formal representation of declared finite candidates only; it does not establish business correctness, prose quality, executability, approval, or a pass result.", "",
             "## Candidate reconciliation", "", "| Candidate | Model | State | Cases | Diagnostics |", "| --- | --- | --- | --- | --- |"]
    for item in report["candidates"]:
        lines.append("| {id} | {model_id} | {state} | {cases} | {codes} |".format(
            id=item["id"], model_id=item["model_id"], state=item["state"],
            cases=", ".join(item["case_ids"]) or "-", codes=", ".join(item["codes"] + item.get("gap_reasons", [])) or "-"))
    lines.extend(["", "## Unresolved design obligations", ""])
    if report["obligations"]:
        lines.extend("- `{id}`: `{code}` ({model_id})".format(**item) for item in report["obligations"])
    else:
        lines.append("- None declared by the finite design engine.")
    lines.extend(["", "## Findings", ""])
    if report["findings"]:
        for item in report["findings"]:
            subject = item.get("candidate_id", item.get("case_id", "-"))
            lines.append("- `{}`: `{}`".format(item["code"], subject))
    else:
        lines.append("- None.")
    return "\n".join(lines) + "\n"


def _source(path):
    raw = Path(path).absolute()
    if any(parent.exists() and _is_link_or_reparse(parent) for parent in (raw, raw.parent, *raw.parent.parents)):
        _fail("LINK_PATH_REJECTED")
    try:
        result = raw.resolve(strict=True)
    except (OSError, RuntimeError):
        _fail("INPUT_IO_ERROR")
    if not result.is_file():
        _fail("INPUT_IO_ERROR")
    return result


def _safe_output(path, inputs):
    raw = Path(path).absolute()
    for parent in (raw.parent, *raw.parent.parents):
        if parent.exists() and _is_link_or_reparse(parent):
            _fail("LINK_PATH_REJECTED")
    resolved = raw.resolve()
    if any(resolved == item for item in inputs):
        _fail("OUTPUT_INPUT_CONFLICT")
    if raw.exists() or raw.is_symlink():
        _fail("OUTPUT_EXISTS")
    return resolved


def _write_exclusive(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".qa-master-audit-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(content)
        try:
            os.link(temporary, path)
        except FileExistsError:
            _fail("OUTPUT_EXISTS")
    except OSError:
        _fail("OUTPUT_IO_ERROR")
    finally:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass


def _read_bounded(path):
    try:
        if path.stat().st_size > _MAX_BYTES:
            _fail("INPUT_TOO_LARGE")
        with path.open("rb") as handle:
            value = handle.read(_MAX_BYTES + 1)
    except CaseConformanceError:
        raise
    except OSError:
        _fail("INPUT_IO_ERROR")
    if len(value) > _MAX_BYTES:
        _fail("INPUT_TOO_LARGE")
    return value


def write_case_audit(input_path, cases_path, output_path, *, format="json") -> dict:
    """Load bounded JSON inputs and write one new, exclusive report file."""
    if format not in {"json", "markdown"}:
        _fail("INVALID_FORMAT")
    source = _source(input_path); cases = _source(cases_path)
    output = _safe_output(output_path, (source, cases))
    bundle_bytes = _read_bounded(source); case_bytes = _read_bounded(cases)
    bundle = _load_json(bundle_bytes); library = _load_json(case_bytes)
    report = audit_method_cases(bundle, library)
    content = (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8") if format == "json" else render_audit_markdown(report).encode("utf-8")
    _write_exclusive(output, content)
    return report
