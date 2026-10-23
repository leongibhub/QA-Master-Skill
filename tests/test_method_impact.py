import copy
import json
from pathlib import Path
import tempfile
import unittest

from qa_master.design_methods import design_methods
from qa_master.method_impact import analyze_method_impact


EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "design-methods.json"


def row(candidate):
    return {"candidate_id": candidate["id"], "method_data": copy.deepcopy(candidate["method_data"]),
            "requirement_ids": list(candidate["trace"]), "source_ref_ids": [x["id"] for x in candidate["source_refs"]],
            "oracle_ref_ids": [x["id"] for x in candidate["oracle_refs"]]}


def library(bundle, rows=(), gaps=()):
    design = design_methods(bundle)
    return {"schema_version": 1, "design_input_sha256": design["input_sha256"],
            "cases": [{"id": "CASE-1", "title": "case", "preconditions": "ready",
                       "steps": ["act"], "expected": "observe", "scenarios": list(rows)}], "gaps": list(gaps)}


class MethodImpactTests(unittest.TestCase):
    def test_source_digest_only_churn_retains_formal_vectors_and_requires_review(self):
        before = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        after = copy.deepcopy(before)
        after["design_models"]["source_refs"][0]["sha256"] = "1" * 64
        bound = row(design_methods(before)["candidates"][0])
        report = analyze_method_impact(before, after, library(before, [bound]))
        self.assertTrue(report["library_rebinding_required"])
        self.assertTrue(report["candidate_deltas"])
        self.assertTrue(all(row["pair_state"] == "RETAINED_VECTOR" for row in report["candidate_deltas"]))
        self.assertFalse(any(row["pair_state"] in {"ADDED", "REMOVED"} for row in report["candidate_deltas"]))
        self.assertTrue(all("CANDIDATE_REBIND_REQUIRED" in row["reason_codes"] for row in report["candidate_deltas"]))
        self.assertTrue(all("SOURCE_DESCRIPTORS_CHANGED" in row["reason_codes"] for row in report["candidate_deltas"]))
        self.assertEqual(report["review_case_ids"], ["CASE-1"])
        self.assertEqual(report["case_row_actions"][0]["action"], "REVIEW_BINDING")

    def test_changed_typed_vector_is_added_and_removed_not_fuzzily_matched(self):
        before = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        after = copy.deepcopy(before)
        after["design_models"]["models"][0]["spec"]["upper"]["value"] = "101"
        report = analyze_method_impact(before, after, library(before))
        states = {item["pair_state"] for item in report["candidate_deltas"]}
        self.assertIn("ADDED", states)
        self.assertIn("REMOVED", states)

    def test_file_writer_and_cli_reject_duplicate_flags_without_campaign_state(self):
        import subprocess
        import sys
        from qa_master.method_impact import write_method_impact
        before = json.loads(EXAMPLE.read_text(encoding="utf-8")); after = copy.deepcopy(before)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); old = root / "old.json"; new = root / "new.json"; cases = root / "cases.json"; output = root / "impact.json"
            old.write_text(json.dumps(before), encoding="utf-8"); new.write_text(json.dumps(after), encoding="utf-8")
            cases.write_text(json.dumps(library(before)), encoding="utf-8")
            report = write_method_impact(old, new, cases, output)
            self.assertEqual(report["status"], "DRAFT_UNAPPROVED")
            run = subprocess.run([sys.executable, "-m", "qa_master", "--state", str(root / "missing.json"),
                                  "impact-method-cases", "--before", str(old), "--before", str(old), "--after", str(new),
                                  "--cases", str(cases), "--output", str(root / "second.json")], capture_output=True, text=True)
            self.assertEqual(run.returncode, 2)
            self.assertFalse((root / "missing.json").exists())

    def test_context_obligation_gap_and_unmodeled_requirement_are_retained(self):
        before = json.loads(EXAMPLE.read_text(encoding="utf-8")); after = copy.deepcopy(before)
        candidate = design_methods(before)["candidates"][0]
        before["requirements"].append({"id": "未建模 requirement", "text": "old", "source": "x", "approved": False,
                                       "dimension": "functional", "acceptance": "x", "priority": "P1"})
        after["requirements"][-1]["text"] = "changed"
        after["design_models"]["oracle_refs"][0]["locator"] = "changed.md"
        del after["design_models"]["models"][0]["spec"]["oracle_by_class"]["UPPER_INVALID"]
        report = analyze_method_impact(before, after, library(before, [row(candidate)], [{"candidate_id": candidate["id"], "reason_code": "OTHER"}]))
        self.assertEqual(report["unknowns"], [{"code": "UNMODELED_REQUIREMENT_CHANGE", "requirement_ids": ["未建模 requirement"]}])
        self.assertEqual(report["gap_followups"][0]["action"], "REVIEW_GAP")
        self.assertTrue(report["obligation_deltas"])
        self.assertIn("ORACLE_DESCRIPTORS_CHANGED", {code for delta in report["candidate_deltas"] for code in delta["reason_codes"]})
