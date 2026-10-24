"""Bounded offline finite-design change impact analysis (CR-034)."""
from __future__ import annotations

import json
from collections import Counter, defaultdict

from . import case_conformance as _cc
from .case_conformance import CaseConformanceError, audit_method_cases
from .design_methods import DesignMethodError, design_methods


class MethodImpactError(ValueError):
    """Stable, value-free error at the public impact boundary."""
    def __init__(self, code):
        self.code = code
        super().__init__(code)


def _fail(code):
    raise MethodImpactError(code)


def _adapt(call):
    try:
        return call()
    except MethodImpactError:
        raise
    except (CaseConformanceError, DesignMethodError) as error:
        _fail(error.code)
    except (KeyError, TypeError, ValueError, RecursionError):
        _fail("INVALID_SCHEMA")


def _formal(candidate):
    return {"model_id": candidate["model_id"], "method": candidate["method"],
            "dimension": candidate["dimension"], "method_data": candidate["method_data"]}


def _key(value):
    return _cc._canonical(value)


def _refs(candidate, name):
    return sorted(candidate[name], key=_key)


def _requirements(bundle):
    result = {}
    for item in bundle.get("requirements", []):
        if isinstance(item, dict) and isinstance(item.get("id"), str):
            result[item["id"]] = item
    return result


def _model_metadata(bundle):
    models = bundle.get("design_models", {}).get("models", [])
    result = {}
    if isinstance(models, list):
        for item in models:
            if isinstance(item, dict) and isinstance(item.get("id"), str):
                result[item["id"]] = {k: v for k, v in item.items()
                                       if k not in {"spec", "requirement_ids", "source_refs"}}
    return result


def _context_codes(before, after, before_requirements, after_requirements, before_metadata, after_metadata):
    codes = []
    if sorted(before["trace"]) != sorted(after["trace"]):
        codes.append("REQUIREMENT_BINDINGS_CHANGED")
    before_records = [before_requirements.get(x) for x in sorted(before["trace"])]
    after_records = [after_requirements.get(x) for x in sorted(after["trace"])]
    if not _cc._typed_equal(before_records, after_records):
        codes.append("REQUIREMENT_CONTEXT_CHANGED")
    if sorted(x["id"] for x in before["source_refs"]) != sorted(x["id"] for x in after["source_refs"]):
        codes.append("SOURCE_BINDINGS_CHANGED")
    if not _cc._typed_equal(_refs(before, "source_refs"), _refs(after, "source_refs")):
        codes.append("SOURCE_DESCRIPTORS_CHANGED")
    if sorted(x["id"] for x in before["oracle_refs"]) != sorted(x["id"] for x in after["oracle_refs"]):
        codes.append("ORACLE_BINDINGS_CHANGED")
    if not _cc._typed_equal(_refs(before, "oracle_refs"), _refs(after, "oracle_refs")):
        codes.append("ORACLE_DESCRIPTORS_CHANGED")
    if not _cc._typed_equal(before_metadata.get(before["model_id"]), after_metadata.get(after["model_id"])):
        codes.append("MODEL_CONTEXT_CHANGED")
    return sorted(codes)


def _candidate_deltas(before, after, before_bundle, after_bundle):
    groups = defaultdict(lambda: {"before": [], "after": []})
    for side, design in (("before", before), ("after", after)):
        for candidate in design["candidates"]:
            groups[_key(_formal(candidate))][side].append(candidate)
    before_req, after_req = _requirements(before_bundle), _requirements(after_bundle)
    before_meta, after_meta = _model_metadata(before_bundle), _model_metadata(after_bundle)
    result = []
    for encoded, group in groups.items():
        old, new = sorted(group["before"], key=lambda x: x["id"]), sorted(group["after"], key=lambda x: x["id"])
        formal = _formal((old or new)[0])
        if old and new and len(old) == len(new) == 1:
            codes = ["FORMAL_VECTOR_UNCHANGED"]
            codes += _context_codes(old[0], new[0], before_req, after_req, before_meta, after_meta)
            if old[0]["id"] != new[0]["id"]:
                codes.append("CANDIDATE_REBIND_REQUIRED")
            state = "RETAINED_VECTOR"
        elif old and new:
            state, codes = "AMBIGUOUS", ["AMBIGUOUS_FORMAL_MATCH"]
        elif new:
            state, codes = ("ADDED", ["FINITE_VECTOR_ADDED"]) if len(new) == 1 else ("AMBIGUOUS", ["AMBIGUOUS_FORMAL_MATCH"])
        else:
            state, codes = ("REMOVED", ["FINITE_VECTOR_REMOVED"]) if len(old) == 1 else ("AMBIGUOUS", ["AMBIGUOUS_FORMAL_MATCH"])
        result.append({"model_id": formal["model_id"], "formal_fingerprint": _cc._digest(formal),
                       "pair_state": state, "before_candidate_ids": [x["id"] for x in old],
                       "after_candidate_ids": [x["id"] for x in new], "reason_codes": sorted(set(codes))})
    return sorted(result, key=lambda x: (x["model_id"], x["formal_fingerprint"]))


def _obligation_deltas(before, after):
    groups = defaultdict(lambda: {"before": [], "after": []})
    for side, design in (("before", before), ("after", after)):
        for item in design["obligations"]:
            identity = {"model_id": item["model_id"], "method": item["method"], "code": item["code"], "subject": item["subject"]}
            groups[_key(identity)][side].append(item)
    output = []
    for group in groups.values():
        old, new = sorted(group["before"], key=lambda x: x["id"]), sorted(group["after"], key=lambda x: x["id"])
        identity = {"model_id": (old or new)[0]["model_id"], "method": (old or new)[0]["method"],
                    "code": (old or new)[0]["code"], "subject": (old or new)[0]["subject"]}
        state = ("PRESENT_BOTH" if len(old) == len(new) == 1 else
                 "AFTER_ONLY" if len(new) == 1 and not old else
                 "BEFORE_ONLY" if len(old) == 1 and not new else "AMBIGUOUS")
        output.append({"model_id": identity["model_id"], "formal_fingerprint": _cc._digest(identity), "state": state,
                       "before_obligation_ids": [x["id"] for x in old], "after_obligation_ids": [x["id"] for x in new], "code": identity["code"]})
    return sorted(output, key=lambda x: (x["model_id"], x["formal_fingerprint"]))


def _unknowns(before_bundle, after_bundle):
    before, after = _requirements(before_bundle), _requirements(after_bundle)
    changed = {rid for rid in set(before) | set(after) if not _cc._typed_equal(before.get(rid), after.get(rid))}
    linked = set()
    for bundle in (before_bundle, after_bundle):
        for model in bundle.get("design_models", {}).get("models", []):
            if isinstance(model, dict):
                linked.update(x for x in model.get("requirement_ids", []) if isinstance(x, str))
    unmodeled = sorted(changed - linked)
    return [] if not unmodeled else [{"code": "UNMODELED_REQUIREMENT_CHANGE", "requirement_ids": unmodeled}]


def _rows_and_actions(library, baseline, deltas, obligations):
    by_old = {cid: d for d in deltas for cid in d["before_candidate_ids"]}
    baseline_by_candidate = {item["id"]: item for item in baseline["candidates"]}
    finding_cases = {item.get("case_id") for item in baseline["findings"] if item.get("case_id")}
    finding_cases.update(case for item in baseline["findings"] for case in item.get("case_ids", []))
    obligation_models = {item["model_id"] for item in obligations}
    old_model = {item["id"]: item["model_id"] for item in baseline["candidates"]}
    actions = []
    for case in library["cases"]:
        occurrences = Counter()
        for scenario in sorted(case["scenarios"], key=_key):
            normalized = {"candidate_id": scenario["candidate_id"], "method_data": scenario["method_data"],
                          "requirement_ids": sorted(scenario["requirement_ids"]), "source_ref_ids": sorted(scenario["source_ref_ids"]),
                          "oracle_ref_ids": sorted(scenario["oracle_ref_ids"])}
            digest = _cc._digest(normalized); occurrences[digest] += 1
            cid = scenario["candidate_id"]; delta = by_old.get(cid); baseline_item = baseline_by_candidate.get(cid)
            delta_reasons = list(delta["reason_codes"]) if delta else []
            reasons = []
            if case["id"] in finding_cases or (baseline_item and baseline_item["state"] != "EXACTLY_BOUND"):
                action, reasons = "REVIEW_BASELINE", delta_reasons + ["BASELINE_NONCONFORMANT"]
            elif not delta or delta["pair_state"] == "AMBIGUOUS":
                action, reasons = "REVIEW_AMBIGUOUS", delta_reasons + ["AMBIGUOUS_FORMAL_MATCH"]
            elif delta["pair_state"] == "REMOVED":
                action, reasons = "REVIEW_REMOVAL", delta_reasons
            elif old_model.get(cid) in obligation_models:
                action, reasons = "REVIEW_BINDING", delta_reasons + ["UNRESOLVED_MODEL_OBLIGATION"]
            elif set(delta["reason_codes"]) - {"FORMAL_VECTOR_UNCHANGED"}:
                action, reasons = "REVIEW_BINDING", delta_reasons
            else:
                action, reasons = "NO_DECLARED_IMPACT", delta_reasons
            if old_model.get(cid) in obligation_models:
                reasons.append("UNRESOLVED_MODEL_OBLIGATION")
            after_ids = delta["after_candidate_ids"] if delta else []
            actions.append({"case_id": case["id"], "scenario_sha256": digest, "occurrence": occurrences[digest],
                            "before_candidate_id": cid,
                            "after_candidate_id": after_ids[0] if delta and delta["pair_state"] == "RETAINED_VECTOR" and len(after_ids) == 1 else None,
                            "action": action, "reason_codes": sorted(set(reasons))})
    return sorted(actions, key=lambda x: (x["case_id"], x["scenario_sha256"], x["occurrence"]))


def analyze_method_impact(before_bundle: dict, after_bundle: dict, case_library: dict) -> dict:
    """Compare declared finite designs; returns review proposals only, never execution."""
    def build():
        if not all(isinstance(x, dict) for x in (before_bundle, after_bundle, case_library)):
            _fail("INVALID_SCHEMA")
        for value in (before_bundle, after_bundle, case_library):
            if len(_cc._canonical(value)) > _cc._MAX_BYTES:
                _fail("INPUT_TOO_LARGE")
        _cc._preflight(before_bundle); _cc._preflight(after_bundle)
        before, after = design_methods(before_bundle), design_methods(after_bundle)
        if len(before["candidates"]) > _cc._MAX_CANDIDATES or len(after["candidates"]) > _cc._MAX_CANDIDATES:
            _fail("CANDIDATE_LIMIT_EXCEEDED")
        baseline = audit_method_cases(before_bundle, case_library)
        deltas = _candidate_deltas(before, after, before_bundle, after_bundle)
        baseline_by_candidate = {item["id"]: item for item in baseline["candidates"]}
        for delta in deltas:
            states = {baseline_by_candidate[candidate_id]["state"] for candidate_id in delta["before_candidate_ids"]
                      if candidate_id in baseline_by_candidate}
            if states & {"MISSING", "DUPLICATE", "MISMATCH"}:
                delta["reason_codes"] = sorted(set(delta["reason_codes"] + ["BASELINE_NONCONFORMANT"]))
        obligations = _obligation_deltas(before, after)
        actions = _rows_and_actions(case_library, baseline, deltas, obligations)
        review_ids = sorted({item["case_id"] for item in actions if item["action"] != "NO_DECLARED_IMPACT"} |
                            {item.get("case_id") for item in baseline["findings"] if item.get("case_id")})
        new_ids = sorted(cid for item in deltas if item["pair_state"] == "ADDED" for cid in item["after_candidate_ids"])
        gaps = []
        by_old = {cid: delta for delta in deltas for cid in delta["before_candidate_ids"]}
        for gap in sorted(case_library["gaps"], key=_cc._canonical):
            mapped = by_old.get(gap["candidate_id"])
            gaps.append({"before_candidate_id": gap["candidate_id"], "reason_code": gap["reason_code"],
                         "after_candidate_ids": mapped["after_candidate_ids"] if mapped else [], "action": "REVIEW_GAP"})
        states = {name: sum(1 for item in deltas if item["pair_state"] == name) for name in ("RETAINED_VECTOR", "ADDED", "REMOVED", "AMBIGUOUS")}
        return {"schema_version": 1, "status": "DRAFT_UNAPPROVED", "execution": "NOT_EXECUTED",
                "before_design_input_sha256": before["input_sha256"], "after_design_input_sha256": after["input_sha256"],
                "case_library_sha256": baseline["case_library_sha256"], "library_rebinding_required": before["input_sha256"] != after["input_sha256"],
                "baseline_audit_summary": baseline["summary"], "baseline_findings": baseline["findings"], "candidate_deltas": deltas,
                "case_row_actions": actions, "review_case_ids": review_ids, "new_candidate_ids": new_ids,
                "obligation_deltas": obligations, "gap_followups": gaps, "unknowns": _unknowns(before_bundle, after_bundle),
                "summary": {"before_candidate_count": len(before["candidates"]), "after_candidate_count": len(after["candidates"]),
                            "candidate_group_states": states, "before_obligation_count": len(before["obligations"]),
                            "after_obligation_count": len(after["obligations"]), "case_count": len(case_library["cases"]),
                            "row_count": len(actions), "review_case_count": len(review_ids), "new_candidate_count": len(new_ids),
                            "baseline_finding_count": len(baseline["findings"]), "unknown_count": len(_unknowns(before_bundle, after_bundle)),
                            "assessment": "UNASSESSED" if not before["candidates"] and not after["candidates"] else "ASSESSED"},
                "limitations": ["Formal-vector continuity is not semantic equivalence or permission to skip regression.",
                                "Code changes and external source bytes without refreshed descriptors are not analyzed."]}
    return _adapt(build)


def _markdown(report):
    """Private renderer for the internally produced result object only."""
    def esc(value):
        return (str(value).replace("\\", "\\\\").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                .replace("|", "\\|").replace("`", "\\`").replace("[", "\\[").replace("]", "\\]")
                .replace("\r", " ").replace("\n", " "))
    def table(title, headers, rows):
        lines.extend(["", "## " + title, "", "| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"])
        lines.extend("| " + " | ".join(esc(value) for value in row) + " |" for row in rows)
        if not rows:
            lines.append("| " + " | ".join("-" for _ in headers) + " |")
    summary = report["summary"]
    lines = ["# QA Master method change impact", "", "Status: `DRAFT_UNAPPROVED`", "Execution: `NOT_EXECUTED`", "",
             "This is a review proposal only; it does not establish correctness, execution, approval, or a safe regression skip.", "",
             "## Summary", "", "- Before design SHA-256: `{}`".format(esc(report["before_design_input_sha256"])),
             "- After design SHA-256: `{}`".format(esc(report["after_design_input_sha256"])),
             "- Case library SHA-256: `{}`".format(esc(report["case_library_sha256"])),
             "- Library rebinding required: `{}`".format(report["library_rebinding_required"]),
             "- Assessment: `{}`".format(summary["assessment"]),
             "- Candidates: before `{}`, after `{}`; groups `{}`".format(summary["before_candidate_count"], summary["after_candidate_count"], esc(summary["candidate_group_states"])),
             "- Cases `{}`, rows `{}`, review cases `{}`, new candidates `{}`".format(summary["case_count"], summary["row_count"], summary["review_case_count"], summary["new_candidate_count"]),
             "- Obligations: before `{}`, after `{}`; baseline findings `{}`, unknowns `{}`".format(summary["before_obligation_count"], summary["after_obligation_count"], summary["baseline_finding_count"], summary["unknown_count"])]
    table("Candidate deltas", ["Model", "Formal fingerprint", "State", "Before IDs", "After IDs", "Reasons"],
          [(x["model_id"], x["formal_fingerprint"], x["pair_state"], ", ".join(x["before_candidate_ids"]) or "-", ", ".join(x["after_candidate_ids"]) or "-", ", ".join(x["reason_codes"])) for x in report["candidate_deltas"]])
    table("Case review proposals", ["Case", "Scenario SHA-256", "Occurrence", "Before candidate", "After candidate", "Action", "Reasons"],
          [(x["case_id"], x["scenario_sha256"], x["occurrence"], x["before_candidate_id"], x["after_candidate_id"] or "-", x["action"], ", ".join(x["reason_codes"])) for x in report["case_row_actions"]])
    table("Baseline findings", ["Code", "Candidate", "Case or cases"],
          [(x["code"], x.get("candidate_id", "-"), x.get("case_id", ", ".join(x.get("case_ids", []))) or "-") for x in report["baseline_findings"]])
    table("Obligation deltas", ["Model", "Fingerprint", "State", "Code", "Before IDs", "After IDs"],
          [(x["model_id"], x["formal_fingerprint"], x["state"], x["code"], ", ".join(x["before_obligation_ids"]) or "-", ", ".join(x["after_obligation_ids"]) or "-") for x in report["obligation_deltas"]])
    table("Gap followups", ["Before candidate", "Reason", "After candidate IDs", "Action"],
          [(x["before_candidate_id"], x["reason_code"], ", ".join(x["after_candidate_ids"]) or "-", x["action"]) for x in report["gap_followups"]])
    table("Unmodeled changes", ["Code", "Requirement IDs"], [(x["code"], ", ".join(x["requirement_ids"])) for x in report["unknowns"]])
    lines.extend(["", "## Limitations", ""])
    lines.extend("- " + esc(item) for item in report["limitations"])
    return "\n".join(lines) + "\n"


def write_method_impact(before_path, after_path, cases_path, output_path, *, format="json") -> dict:
    if not isinstance(format, str) or format not in {"json", "markdown"}:
        _fail("INVALID_FORMAT")
    def write():
        before_source = _cc._source(before_path); after_source = _cc._source(after_path); cases_source = _cc._source(cases_path)
        output = _cc._safe_output(output_path, (before_source, after_source, cases_source))
        report = analyze_method_impact(_cc._load_json(_cc._read_bounded(before_source)), _cc._load_json(_cc._read_bounded(after_source)),
                                       _cc._load_json(_cc._read_bounded(cases_source)))
        content = (_markdown(report) if format == "markdown" else json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        _cc._write_exclusive(output, content)
        return report
    return _adapt(write)
