"""Pure, non-applied after-design case-library proposals (CR-036)."""
from __future__ import annotations

import copy
import json
from collections import Counter, defaultdict

from . import case_conformance as _cc
from .case_conformance import CaseConformanceError, audit_method_cases
from .design_methods import DesignMethodError, design_methods
from .method_impact import MethodImpactError, analyze_method_impact


class CaseLibraryProposalError(ValueError):
    """Stable, value-free public rejection code."""
    def __init__(self, code):
        self.code = code
        super().__init__(code)


def _fail(code):
    raise CaseLibraryProposalError(code)


def _adapt(call):
    try:
        return call()
    except CaseLibraryProposalError:
        raise
    except (CaseConformanceError, DesignMethodError, MethodImpactError) as error:
        _fail(error.code)
    except (AttributeError, KeyError, TypeError, ValueError, RecursionError):
        _fail("INVALID_SCHEMA")


def _json(value):
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8") + b"\n"
    except (TypeError, ValueError, UnicodeError):
        _fail("INVALID_SCHEMA")


def _scenario(candidate):
    return {"candidate_id": candidate["id"], "method_data": copy.deepcopy(candidate["method_data"]),
            "requirement_ids": sorted(candidate["trace"]),
            "source_ref_ids": sorted(item["id"] for item in candidate["source_refs"]),
            "oracle_ref_ids": sorted(item["id"] for item in candidate["oracle_refs"])}


def _scenario_key(scenario):
    return _cc._digest({"candidate_id": scenario["candidate_id"], "method_data": scenario["method_data"],
                        "requirement_ids": sorted(scenario["requirement_ids"]), "source_ref_ids": sorted(scenario["source_ref_ids"]),
                        "oracle_ref_ids": sorted(scenario["oracle_ref_ids"])})


def _case_hash(case):
    normalized = {key: copy.deepcopy(case[key]) for key in ("id", "title", "preconditions", "steps", "expected")}
    normalized["scenarios"] = sorted(({"candidate_id": row["candidate_id"], "method_data": row["method_data"],
                                        "requirement_ids": sorted(row["requirement_ids"]), "source_ref_ids": sorted(row["source_ref_ids"]),
                                        "oracle_ref_ids": sorted(row["oracle_ref_ids"])} for row in case["scenarios"]), key=_cc._canonical)
    return _cc._digest(normalized)


def _finding_indexes(findings):
    """Index baseline diagnostics once; proposal generation must stay linear."""
    by_case, by_candidate = defaultdict(set), defaultdict(set)
    for item in findings:
        code = item["code"]
        if item.get("case_id") is not None:
            by_case[item["case_id"]].add(code)
        for case_id in item.get("case_ids", []):
            by_case[case_id].add(code)
        if item.get("candidate_id") is not None:
            by_candidate[item["candidate_id"]].add(code)
    return by_case, by_candidate


def _counts(values, names):
    return {name: sum(value == name for value in values) for name in names}


def propose_method_case_library(before_bundle: dict, after_bundle: dict, case_library: dict) -> dict:
    """Build a bounded, review-only overlay; it never updates a source library."""
    def build():
        if not all(isinstance(value, dict) for value in (before_bundle, after_bundle, case_library)):
            _fail("INVALID_SCHEMA")
        # These public boundaries retain the inherited size, depth and replay limits.
        impact = analyze_method_impact(before_bundle, after_bundle, case_library)
        after_design = design_methods(after_bundle)
        if impact["after_design_input_sha256"] != after_design["input_sha256"]:
            _fail("PROPOSAL_INVARIANT_FAILED")
        # Impact owns the one fresh baseline audit in the fixed five-replay budget.
        baseline_findings = impact["baseline_findings"]
        finding_by_case, finding_by_candidate = _finding_indexes(baseline_findings)
        deltas = impact["candidate_deltas"]
        delta_by_old = {candidate_id: delta for delta in deltas for candidate_id in delta["before_candidate_ids"]}
        delta_by_after = {candidate_id: delta for delta in deltas for candidate_id in delta["after_candidate_ids"]}
        action_by_locator = {(item["case_id"], item["scenario_sha256"], item["occurrence"]): item
                             for item in impact["case_row_actions"]}
        after_candidates = {item["id"]: item for item in after_design["candidates"]}
        obligation_models = {item["model_id"] for item in impact["obligation_deltas"]}

        case_decisions, row_decisions, proposed_cases = [], [], []
        held_row_sources = []
        for case in sorted(case_library["cases"], key=lambda item: item["id"]):
            occurrences = Counter()
            raw_rows = []
            for original in case["scenarios"]:
                digest = _scenario_key(original); occurrences[digest] += 1
                locator = (case["id"], digest, occurrences[digest])
                action = action_by_locator.get(locator)
                if action is None:
                    _fail("PROPOSAL_INVARIANT_FAILED")
                delta = delta_by_old.get(original["candidate_id"])
                possible = sorted(delta["after_candidate_ids"]) if delta else []
                baseline_codes = sorted(finding_by_case[case["id"]] | finding_by_candidate[original["candidate_id"]])
                unique_retained = (delta is not None and delta["pair_state"] == "RETAINED_VECTOR" and
                                   len(delta["before_candidate_ids"]) == len(delta["after_candidate_ids"]) == 1)
                candidate = after_candidates.get(possible[0]) if unique_retained else None
                if action["action"] in {"NO_DECLARED_IMPACT", "REVIEW_BINDING"}:
                    if (not unique_retained or delta["before_candidate_ids"] != [original["candidate_id"]] or candidate is None or
                            action["before_candidate_id"] != original["candidate_id"] or action["after_candidate_id"] != candidate["id"] or
                            candidate["model_id"] != delta["model_id"] or
                            _cc._digest({"model_id": candidate["model_id"], "method": candidate["method"],
                                        "dimension": candidate["dimension"], "method_data": candidate["method_data"]}) != delta["formal_fingerprint"]):
                        _fail("PROPOSAL_INVARIANT_FAILED")
                eligible = (action["action"] in {"NO_DECLARED_IMPACT", "REVIEW_BINDING"} and unique_retained and candidate is not None and
                            "UNRESOLVED_MODEL_OBLIGATION" not in action["reason_codes"] and candidate["model_id"] not in obligation_models and
                            not baseline_codes)
                reasons = sorted(set(action["reason_codes"] + baseline_codes))
                if eligible:
                    decision = "CARRY_PROPOSED" if reasons == ["FORMAL_VECTOR_UNCHANGED"] else "REBIND_PROPOSED_REVIEW_REQUIRED"
                elif baseline_codes or action["action"] == "REVIEW_BASELINE":
                    decision = "HELD_BASELINE"
                elif delta is None or delta["pair_state"] == "AMBIGUOUS" or action["action"] == "REVIEW_AMBIGUOUS":
                    decision = "HELD_AMBIGUOUS"
                elif delta["pair_state"] == "REMOVED" or action["action"] == "REVIEW_REMOVAL":
                    decision = "HELD_REMOVAL"
                else:
                    decision = "HELD_OBLIGATION"
                raw_rows.append({"original": original, "digest": digest, "occurrence": occurrences[digest], "action": action,
                                 "possible": possible, "candidate": candidate, "eligible": eligible, "decision": decision, "reasons": reasons})
            mixed = bool(raw_rows) and any(row["eligible"] for row in raw_rows) and not all(row["eligible"] for row in raw_rows)
            eligible_case = bool(raw_rows) and all(row["eligible"] for row in raw_rows)
            if not raw_rows:
                eligible_case = False
            if eligible_case:
                proposal = {key: copy.deepcopy(case[key]) for key in ("id", "title", "preconditions", "steps", "expected")}
                proposal["scenarios"] = [_scenario(row["candidate"]) for row in raw_rows]
                proposed_cases.append(proposal)
                case_decision = "CARRY_PROPOSED" if all(row["decision"] == "CARRY_PROPOSED" for row in raw_rows) else "REBIND_PROPOSED_REVIEW_REQUIRED"
            else:
                proposal = None
                row_kinds = {row["decision"] for row in raw_rows}
                if finding_by_case[case["id"]]:
                    case_decision = "HELD_BASELINE"
                elif "HELD_BASELINE" in row_kinds:
                    case_decision = "HELD_BASELINE"
                elif "HELD_AMBIGUOUS" in row_kinds:
                    case_decision = "HELD_AMBIGUOUS"
                elif "HELD_REMOVAL" in row_kinds:
                    case_decision = "HELD_REMOVAL"
                else:
                    case_decision = "HELD_OBLIGATION"
            final_rows = []
            for row in raw_rows:
                final_decision = row["decision"] if not eligible_case else row["decision"]
                if not eligible_case and row["eligible"]:
                    final_decision = "HELD_CASE_ATOMICITY"
                reasons = set(row["reasons"])
                if not eligible_case:
                    reasons.add("CASE_HELD")
                if mixed:
                    reasons.add("CASE_PARTIAL_REBIND_FORBIDDEN")
                result = {"case_id": case["id"], "scenario_sha256": row["digest"], "occurrence": row["occurrence"],
                          "before_candidate_id": row["original"]["candidate_id"],
                          "after_candidate_id": row["candidate"]["id"] if eligible_case else None,
                          "possible_after_candidate_ids": row["possible"], "decision": final_decision,
                          "review_required": True, "reason_codes": sorted(reasons),
                          "proposed_scenario": _scenario(row["candidate"]) if eligible_case else None}
                final_rows.append(result)
                if not eligible_case:
                    held_row_sources.append(result)
            case_reasons = set(code for row in final_rows for code in row["reason_codes"])
            case_reasons.update(finding_by_case[case["id"]])
            if not eligible_case:
                case_reasons.add("CASE_HELD")
            if mixed:
                case_reasons.add("CASE_PARTIAL_REBIND_FORBIDDEN")
            case_decisions.append({"case_id": case["id"], "source_case_sha256": _case_hash(case), "decision": case_decision,
                                   "review_required": True, "reason_codes": sorted(case_reasons), "original_case": copy.deepcopy(case),
                                   "proposed_case_sha256": _case_hash(proposal) if proposal is not None else None})
            row_decisions.extend(final_rows)

        held_gaps = []
        held_reasons_by_after, gap_reasons_by_after = defaultdict(set), defaultdict(set)
        gap_occurrences = Counter()
        for gap in sorted(case_library["gaps"], key=_cc._canonical):
            projection = {"candidate_id": gap["candidate_id"], "reason_code": gap["reason_code"]}
            digest = _cc._digest(projection); gap_occurrences[digest] += 1
            delta = delta_by_old.get(gap["candidate_id"])
            reasons = set(delta["reason_codes"] if delta else [])
            reasons.update(finding_by_candidate[gap["candidate_id"]])
            reasons.update({"GAP_HELD", "GAP_REASON_REVIEW_REQUIRED"})
            possible = sorted(delta["after_candidate_ids"]) if delta else []
            held_gaps.append({"gap_sha256": digest, "occurrence": gap_occurrences[digest], "original_gap": copy.deepcopy(gap),
                              "possible_after_candidate_ids": possible, "decision": "HELD_GAP_REVIEW_REQUIRED", "reason_codes": sorted(reasons)})
            for after_id in possible:
                gap_reasons_by_after[after_id].update(reasons)

        case_reasons_by_id = {item["case_id"]: set(item["reason_codes"]) for item in case_decisions}
        for row in held_row_sources:
            for after_id in row["possible_after_candidate_ids"]:
                held_reasons_by_after[after_id].update(row["reason_codes"])
                held_reasons_by_after[after_id].update(case_reasons_by_id[row["case_id"]])

        nested = {"schema_version": 1, "design_input_sha256": after_design["input_sha256"],
                  "cases": sorted(proposed_cases, key=lambda item: item["id"]), "gaps": []}
        if len(_json(nested)) > _cc._MAX_BYTES:
            _fail("OUTPUT_TOO_LARGE")
        post = audit_method_cases(after_bundle, nested)
        post_ids = {item["id"] for item in post["candidates"]}
        post_states = Counter(item["state"] for item in post["candidates"])
        normalized_nested_hash = _cc._digest(_cc._normalized_library(nested))
        if (len(post["candidates"]) != len(after_candidates) or post_ids != set(after_candidates) or post["case_library_sha256"] != normalized_nested_hash or
                post["summary"]["states"] != {state: post_states[state] for state in ("EXACTLY_BOUND", "GAP_RECORDED", "MISSING", "DUPLICATE", "MISMATCH")} or
                post["findings"] or any(item["state"] in {"DUPLICATE", "MISMATCH", "GAP_RECORDED"} for item in post["candidates"])):
            _fail("PROPOSAL_INVARIANT_FAILED")
        exact_ids = {item["id"] for item in post["candidates"] if item["state"] == "EXACTLY_BOUND"}
        followups = []
        for candidate in sorted((item for item in after_design["candidates"] if item["id"] not in exact_ids), key=lambda item: item["id"]):
            delta = delta_by_after.get(candidate["id"])
            reasons = set(delta["reason_codes"] if delta else [])
            reasons.update(held_reasons_by_after[candidate["id"]])
            reasons.update(gap_reasons_by_after[candidate["id"]])
            if candidate["model_id"] in obligation_models:
                reasons.add("UNRESOLVED_MODEL_OBLIGATION")
            followups.append({"candidate_id": candidate["id"], "model_id": candidate["model_id"], "method": candidate["method"],
                              "dimension": candidate["dimension"], "method_data": copy.deepcopy(candidate["method_data"]),
                              "requirement_ids": sorted(candidate["trace"]), "source_ref_ids": sorted(item["id"] for item in candidate["source_refs"]),
                              "oracle_ref_ids": sorted(item["id"] for item in candidate["oracle_refs"]),
                              "source_refs": sorted(copy.deepcopy(candidate["source_refs"]), key=lambda item: item["id"]),
                              "oracle_refs": sorted(copy.deepcopy(candidate["oracle_refs"]), key=lambda item: item["id"]),
                              "action": "AUTHOR_CASE_OR_RECORD_GAP", "reason_codes": sorted(reasons)})
        row_decisions.sort(key=lambda item: (item["case_id"], item["scenario_sha256"], item["occurrence"]))
        case_names = ("CARRY_PROPOSED", "REBIND_PROPOSED_REVIEW_REQUIRED", "HELD_BASELINE", "HELD_AMBIGUOUS", "HELD_REMOVAL", "HELD_OBLIGATION")
        row_names = ("CARRY_PROPOSED", "REBIND_PROPOSED_REVIEW_REQUIRED", "HELD_BASELINE", "HELD_AMBIGUOUS", "HELD_REMOVAL", "HELD_OBLIGATION", "HELD_CASE_ATOMICITY")
        source_row_count = sum(len(case["scenarios"]) for case in case_library["cases"])
        summary = {"source_case_count": len(case_library["cases"]), "source_row_count": source_row_count, "source_gap_count": len(case_library["gaps"]),
                   "proposed_case_count": len(nested["cases"]), "proposed_row_count": sum(len(case["scenarios"]) for case in nested["cases"]),
                   "proposed_gap_count": 0, "held_case_count": sum(item["decision"].startswith("HELD_") for item in case_decisions),
                   "held_row_count": sum(item["decision"].startswith("HELD_") for item in row_decisions), "held_gap_count": len(held_gaps),
                   "after_candidate_count": len(after_design["candidates"]), "exact_after_candidate_count": len(exact_ids),
                   "missing_after_candidate_count": len(followups), "case_decision_counts": _counts([item["decision"] for item in case_decisions], case_names),
                   "row_decision_counts": _counts([item["decision"] for item in row_decisions], row_names), "assessment": post["summary"]["assessment"]}
        if not (summary["source_case_count"] == summary["proposed_case_count"] + summary["held_case_count"] and
                summary["source_row_count"] == summary["proposed_row_count"] + summary["held_row_count"] and
                summary["source_gap_count"] == summary["held_gap_count"] and
                summary["after_candidate_count"] == summary["exact_after_candidate_count"] + summary["missing_after_candidate_count"] and
                len(followups) == summary["missing_after_candidate_count"] and
                sum(summary["case_decision_counts"].values()) == summary["source_case_count"] and
                sum(summary["row_decision_counts"].values()) == summary["source_row_count"] and
                len({item["case_id"] for item in case_decisions}) == summary["source_case_count"] and
                len({(item["case_id"], item["scenario_sha256"], item["occurrence"]) for item in row_decisions}) == summary["source_row_count"]):
            _fail("PROPOSAL_INVARIANT_FAILED")
        report = {"schema_version": 1, "status": "DRAFT_UNAPPROVED", "execution": "NOT_EXECUTED", "application_state": "NOT_APPLIED",
                  "before_design_input_sha256": impact["before_design_input_sha256"], "after_design_input_sha256": after_design["input_sha256"],
                  "baseline_case_library_sha256": impact["case_library_sha256"], "proposed_case_library_sha256": post["case_library_sha256"],
                  "proposed_case_library": nested, "candidate_deltas": copy.deepcopy(deltas), "case_decisions": case_decisions,
                  "row_decisions": row_decisions, "held_gaps": held_gaps, "missing_vector_followups": followups,
                  "baseline_audit_summary": copy.deepcopy(impact["baseline_audit_summary"]), "baseline_findings": copy.deepcopy(baseline_findings),
                  "obligation_deltas": copy.deepcopy(impact["obligation_deltas"]), "unknowns": copy.deepcopy(impact["unknowns"]),
                  "post_proposal_audit": post, "summary": summary,
                  "limitations": ["This is a non-applied draft requiring human review; formal pairing is not prose correctness or semantic equivalence.",
                                  "Held gaps remain review work and do not establish execution, approval, or a regression skip."]}
        if len(_json(report)) > _cc._MAX_BYTES:
            _fail("OUTPUT_TOO_LARGE")
        return report
    return _adapt(build)


def write_method_case_library_proposal(before_path, after_path, cases_path, output_path) -> dict:
    """Load strict bounded JSON and exclusively publish one compact proposal."""
    def write():
        before_source = _cc._source(before_path); after_source = _cc._source(after_path); cases_source = _cc._source(cases_path)
        output = _cc._safe_output(output_path, (before_source, after_source, cases_source))
        result = propose_method_case_library(_cc._load_json(_cc._read_bounded(before_source)), _cc._load_json(_cc._read_bounded(after_source)),
                                             _cc._load_json(_cc._read_bounded(cases_source)))
        content = _json(result)
        if len(content) > _cc._MAX_BYTES:
            _fail("OUTPUT_TOO_LARGE")
        _cc._write_exclusive(output, content)
        return result
    try:
        return _adapt(write)
    except CaseLibraryProposalError:
        raise
    except (OSError, RuntimeError):
        _fail("OUTPUT_IO_ERROR")
