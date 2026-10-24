"""Independent adversarial regressions for finite audit public boundaries (TASK-142)."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from qa_master.case_conformance import CaseConformanceError, audit_method_cases, render_audit_markdown, write_case_audit
from qa_master.design_methods import design_methods
from qa_master.method_impact import MethodImpactError, analyze_method_impact, write_method_impact


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "qa_master" / "skills" / "codex" / "examples" / "design-methods.json"
COMBINATIONS = ROOT / "qa_master" / "skills" / "codex" / "examples" / "design-methods-combinatorial.json"


def scenario(candidate):
    return {
        "candidate_id": candidate["id"],
        "method_data": copy.deepcopy(candidate["method_data"]),
        "requirement_ids": list(candidate["trace"]),
        "source_ref_ids": [item["id"] for item in candidate["source_refs"]],
        "oracle_ref_ids": [item["id"] for item in candidate["oracle_refs"]],
    }


def five_method_bundle():
    """Compose independent published inputs into one minimal five-method model."""
    bundle = json.loads(BASE.read_text(encoding="utf-8"))
    combinations = json.loads(COMBINATIONS.read_text(encoding="utf-8"))
    bundle["design_models"]["source_refs"].extend(
        item for item in combinations["design_models"]["source_refs"] if item["id"] == "SRC-MODEL"
    )
    bundle["design_models"]["oracle_refs"].extend(combinations["design_models"]["oracle_refs"])
    for model in combinations["design_models"]["models"]:
        item = copy.deepcopy(model)
        item["requirement_ids"] = ["REQ-EXAMPLE"]
        bundle["design_models"]["models"].append(item)
    return bundle


def complete_library(bundle):
    design = design_methods(bundle)
    return {
        "schema_version": 1,
        "design_input_sha256": design["input_sha256"],
        "cases": [{
            "id": "CASE-HARDENING",
            "title": "Finite-model regression review",
            "preconditions": "Declared model is available.",
            "steps": ["Perform each declared scenario."],
            "expected": "Record the declared oracle observation.",
            "scenarios": [scenario(candidate) for candidate in design["candidates"]],
        }],
        "gaps": [],
    }


def open_world_state_bundle():
    """A valid sparse state model; open-world must not preflight its unused grid."""
    bundle = json.loads(BASE.read_text(encoding="utf-8"))
    model = next(item for item in bundle["design_models"]["models"] if item["method"] == "state_transition")
    bundle["design_models"]["models"] = [model]
    model["spec"] = {
        "states": [{"id": f"S{index}", "terminal": False, "source_refs": ["SRC-STATE"]}
                   for index in range(128)],
        "initial_state": "S0",
        "triggers": [f"T{index}" for index in range(100)],
        "transitions": [{
            "id": "T-ONE", "validity": "valid", "from_state": "S0", "to_state": "S1", "trigger": "T0",
            "guard_refs": [], "effect_refs": ["SRC-EFFECT"], "source_refs": ["SRC-STATE"], "oracle_ref": "OR-SUBMITTED",
        }],
        "closed_world": False,
        "closed_world_deny_oracle_ref": None,
    }
    return bundle


def closed_world_state_bundle():
    bundle = open_world_state_bundle()
    spec = bundle["design_models"]["models"][0]["spec"]
    spec["closed_world"] = True
    spec["closed_world_deny_oracle_ref"] = "OR-DENY"
    return bundle


def aggregate_decision_bundle():
    """Four individually valid decision models whose aggregate exceeds the audit cap."""
    seed = json.loads(BASE.read_text(encoding="utf-8"))
    template = next(model for model in seed["design_models"]["models"] if model["method"] == "decision_table")
    models = []
    for model_number in range(4):
        model = copy.deepcopy(template)
        model["id"] = f"DM-AGGREGATE-{model_number}"
        model["title"] = f"Aggregate finite model {model_number}"
        model["spec"] = {
            "conditions": [{"id": "value", "values": [f"V{index:04d}" for index in range(2501)]}],
            "constraints": [],
            "rules": [{"id": "R-ALL", "when": {}, "outcome_id": "review",
                       "source_refs": ["SRC-RULE"], "oracle_ref": "OR-DISCOUNT"}],
        }
        models.append(model)
    seed["design_models"]["models"] = models
    return seed


class FiniteAuditHardeningIndependentTests(unittest.TestCase):
    def setUp(self):
        self.bundle = five_method_bundle()
        self.library = complete_library(self.bundle)
        self.design = design_methods(self.bundle)

    def assert_domain_error(self, call, expected_type, expected_code):
        with self.assertRaises(expected_type) as caught:
            call()
        self.assertEqual(caught.exception.code, expected_code)

    def test_tc_fah_001_all_five_methods_keep_typed_context_changes_out_of_no_declared_impact(self):
        report = analyze_method_impact(self.bundle, self.bundle, self.library)
        self.assertEqual({item["method"] for item in self.design["candidates"]},
                         {"boundary", "decision_table", "state_transition", "pairwise", "combinatorial"})
        self.assertTrue(report["case_row_actions"])
        self.assertTrue(all(item["action"] == "NO_DECLARED_IMPACT" for item in report["case_row_actions"]))

        changed = copy.deepcopy(self.bundle)
        changed["requirements"][0]["text"] = "Same formal model, changed declared requirement context."
        report = analyze_method_impact(self.bundle, changed, self.library)
        self.assertTrue(report["case_row_actions"])
        self.assertTrue(all(item["action"] == "REVIEW_BINDING" for item in report["case_row_actions"]))
        self.assertTrue(all("REQUIREMENT_CONTEXT_CHANGED" in item["reason_codes"]
                            for item in report["case_row_actions"]))

    def test_tc_fah_002_baseline_missing_and_explicit_gap_remain_distinct_followups(self):
        candidates = self.design["candidates"]
        library = complete_library(self.bundle)
        missing, gap = candidates[0], candidates[1]
        library["cases"][0]["scenarios"] = [item for item in library["cases"][0]["scenarios"]
                                               if item["candidate_id"] not in {missing["id"], gap["id"]}]
        library["gaps"] = [{"candidate_id": gap["id"], "reason_code": "OTHER"}]
        report = analyze_method_impact(self.bundle, self.bundle, library)
        missing_delta = next(item for item in report["candidate_deltas"] if missing["id"] in item["before_candidate_ids"])
        gap_delta = next(item for item in report["candidate_deltas"] if gap["id"] in item["before_candidate_ids"])
        self.assertIn("BASELINE_NONCONFORMANT", missing_delta["reason_codes"])
        self.assertNotIn("BASELINE_NONCONFORMANT", gap_delta["reason_codes"])
        self.assertEqual(report["gap_followups"], [{
            "before_candidate_id": gap["id"], "reason_code": "OTHER",
            "after_candidate_ids": [gap["id"]], "action": "REVIEW_GAP",
        }])

    def test_tc_fah_003_typed_scenario_mutation_never_becomes_no_declared_impact(self):
        candidate = next(item for item in self.design["candidates"]
                         if item["method"] in {"pairwise", "combinatorial"}
                         and any(isinstance(value, bool) for value in item["method_data"]["assignment"].values()))
        library = complete_library(self.bundle)
        row = next(item for item in library["cases"][0]["scenarios"] if item["candidate_id"] == candidate["id"])
        boolean_name = next(name for name, value in row["method_data"]["assignment"].items() if isinstance(value, bool))
        row["method_data"]["assignment"][boolean_name] = int(row["method_data"]["assignment"][boolean_name])
        audit = audit_method_cases(self.bundle, library)
        entry = next(item for item in audit["candidates"] if item["id"] == candidate["id"])
        self.assertEqual(entry["state"], "MISMATCH")
        self.assertIn("DATA_MISMATCH", entry["codes"])
        impact = analyze_method_impact(self.bundle, self.bundle, library)
        action = next(item for item in impact["case_row_actions"] if item["before_candidate_id"] == candidate["id"])
        self.assertEqual(action["action"], "REVIEW_BASELINE")

    def test_tc_fah_004_invalid_gap_reason_is_a_stable_audit_rejection_in_api_and_cli(self):
        library = complete_library(self.bundle)
        library["gaps"] = [{"candidate_id": self.design["candidates"][0]["id"], "reason_code": {}}]
        self.assert_domain_error(lambda: audit_method_cases(self.bundle, library), CaseConformanceError, "INVALID_GAP")
        self.assert_domain_error(lambda: analyze_method_impact(self.bundle, self.bundle, library), MethodImpactError, "INVALID_GAP")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle_path, cases_path, output = root / "bundle.json", root / "cases.json", root / "report.json"
            bundle_path.write_text(json.dumps(self.bundle), encoding="utf-8")
            cases_path.write_text(json.dumps(library), encoding="utf-8")
            run = subprocess.run([sys.executable, "-m", "qa_master", "audit-method-cases", "--input", str(bundle_path),
                                  "--cases", str(cases_path), "--output", str(output)], capture_output=True, text=True,
                                 encoding="utf-8", errors="replace")
            self.assertEqual(run.returncode, 2, run.stderr)
            self.assertEqual(json.loads(run.stdout), {"status": "REJECTED", "error": "INVALID_GAP"})
            self.assertFalse(output.exists())

    def test_tc_fah_005_unhashable_method_is_a_stable_schema_rejection(self):
        malformed = copy.deepcopy(self.bundle)
        malformed["design_models"]["models"][0]["method"] = {}
        self.assert_domain_error(lambda: audit_method_cases(malformed, self.library), CaseConformanceError, "INVALID_SCHEMA")
        self.assert_domain_error(lambda: analyze_method_impact(malformed, self.bundle, self.library), MethodImpactError, "INVALID_SCHEMA")

    def test_tc_fah_006_existing_regular_file_parent_is_safe_domain_io_rejection_for_both_writers_and_clis(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            before, cases, blocker = root / "bundle.json", root / "cases.json", root / "blocker"
            output = blocker / "audit.json"
            before.write_text(json.dumps(self.bundle), encoding="utf-8")
            cases.write_text(json.dumps(self.library), encoding="utf-8")
            blocker.write_bytes(b"must-remain")
            self.assert_domain_error(lambda: write_case_audit(before, cases, output), CaseConformanceError, "OUTPUT_IO_ERROR")
            self.assert_domain_error(lambda: write_method_impact(before, before, cases, output), MethodImpactError, "OUTPUT_IO_ERROR")
            self.assertEqual(blocker.read_bytes(), b"must-remain")
            self.assertFalse(output.exists())
            for command in (
                ["audit-method-cases", "--input", str(before), "--cases", str(cases), "--output", str(output)],
                ["impact-method-cases", "--before", str(before), "--after", str(before), "--cases", str(cases), "--output", str(output)],
            ):
                with self.subTest(command=command[0]):
                    run = subprocess.run([sys.executable, "-m", "qa_master", *command], capture_output=True, text=True,
                                         encoding="utf-8", errors="replace")
                    self.assertEqual(run.returncode, 2, run.stderr)
                    self.assertEqual(json.loads(run.stdout), {"status": "REJECTED", "error": "OUTPUT_IO_ERROR"})
                    self.assertEqual(blocker.read_bytes(), b"must-remain")

    def test_tc_fah_007_unhashable_public_format_is_a_stable_format_rejection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            before, cases = root / "bundle.json", root / "cases.json"
            before.write_text(json.dumps(self.bundle), encoding="utf-8")
            cases.write_text(json.dumps(self.library), encoding="utf-8")
            self.assert_domain_error(lambda: write_case_audit(before, cases, root / "audit.json", format={}),
                                     CaseConformanceError, "INVALID_FORMAT")
            self.assert_domain_error(lambda: write_method_impact(before, before, cases, root / "impact.json", format={}),
                                     MethodImpactError, "INVALID_FORMAT")

    def test_tc_fah_008_open_world_state_model_is_not_rejected_by_closed_world_preflight(self):
        bundle = open_world_state_bundle()
        design = design_methods(bundle)
        self.assertEqual((len(design["candidates"]), len(design["obligations"])), (1, 0))
        library = {"schema_version": 1, "design_input_sha256": design["input_sha256"], "cases": [], "gaps": []}
        report = audit_method_cases(bundle, library)
        self.assertEqual(report["summary"]["candidate_denominator"], 1)
        self.assertEqual(report["summary"]["states"]["MISSING"], 1)

    def test_tc_fah_009_renderer_rejects_forged_impossible_state_and_finding_variants(self):
        target = self.design["candidates"][0]
        missing_library = complete_library(self.bundle)
        missing_library["cases"][0]["scenarios"] = [item for item in missing_library["cases"][0]["scenarios"]
                                                       if item["candidate_id"] != target["id"]]
        report = audit_method_cases(self.bundle, missing_library)
        missing = next(item for item in report["candidates"] if item["id"] == target["id"])
        self.assertEqual(missing["state"], "MISSING")

        forged_state = copy.deepcopy(report)
        candidate = next(item for item in forged_state["candidates"] if item["id"] == target["id"])
        candidate.update({"state": "MISMATCH", "codes": ["GAP_DUPLICATE"], "case_ids": [], "gap_reasons": []})
        forged_state["summary"]["states"]["MISSING"] -= 1
        forged_state["summary"]["states"]["MISMATCH"] += 1
        forged_state["summary"]["by_model"][candidate["model_id"]]["MISSING"] -= 1
        forged_state["summary"]["by_model"][candidate["model_id"]]["MISMATCH"] += 1

        forged_finding = copy.deepcopy(report)
        forged_finding["findings"].append({"code": "ORPHAN_CASE", "candidate_id": target["id"]})
        forged_finding["summary"]["finding_count"] += 1
        malformed_findings = []
        for code, case_ids in (
            ("DATA_MISMATCH", []),
            ("GAP_CASE_CONFLICT", []),
            ("GAP_DUPLICATE", ["CASE-X"]),
            ("GAP_CASE_CONFLICT", ["CASE-X", "CASE-X"]),
        ):
            forged = copy.deepcopy(report)
            forged["findings"].append({"code": code, "candidate_id": target["id"], "case_ids": case_ids})
            forged["summary"]["finding_count"] += 1
            malformed_findings.append(forged)
        for index, forged in enumerate((forged_state, forged_finding, *malformed_findings), start=1):
            with self.subTest(kind=index):
                self.assert_domain_error(lambda: render_audit_markdown(forged), CaseConformanceError, "INVALID_REPORT")

        duplicate_gap_library = complete_library(self.bundle)
        duplicate_gap_library["cases"][0]["scenarios"] = [item for item in duplicate_gap_library["cases"][0]["scenarios"]
                                                             if item["candidate_id"] != target["id"]]
        duplicate_gap_library["gaps"] = [
            {"candidate_id": target["id"], "reason_code": "OTHER"},
            {"candidate_id": target["id"], "reason_code": "OTHER"},
        ]
        genuine = audit_method_cases(self.bundle, duplicate_gap_library)
        entry = next(item for item in genuine["candidates"] if item["id"] == target["id"])
        self.assertEqual((entry["state"], entry["codes"], entry["gap_reasons"]),
                         ("DUPLICATE", ["GAP_DUPLICATE"], ["OTHER"]))
        self.assertIn(target["id"], render_audit_markdown(genuine))

    def test_tc_fah_010_injected_output_setup_failures_are_domain_errors_without_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            before, cases, guard, output = root / "bundle.json", root / "cases.json", root / "guard.txt", root / "report.json"
            before.write_text(json.dumps(self.bundle), encoding="utf-8")
            cases.write_text(json.dumps(self.library), encoding="utf-8")
            guard.write_bytes(b"must-remain")
            for label, patcher in (
                ("mkdir", mock.patch("qa_master.case_conformance.Path.mkdir", side_effect=OSError("injected mkdir failure"))),
                ("mkstemp", mock.patch("qa_master.case_conformance.tempfile.mkstemp", side_effect=OSError("injected mkstemp failure"))),
            ):
                with self.subTest(label=label, api="audit"):
                    with patcher:
                        self.assert_domain_error(lambda: write_case_audit(before, cases, output), CaseConformanceError, "OUTPUT_IO_ERROR")
                    self.assertEqual(guard.read_bytes(), b"must-remain")
                    self.assertFalse(output.exists())
                with self.subTest(label=label, api="impact"):
                    with patcher:
                        self.assert_domain_error(lambda: write_method_impact(before, before, cases, output), MethodImpactError, "OUTPUT_IO_ERROR")
                    self.assertEqual(guard.read_bytes(), b"must-remain")
                    self.assertFalse(output.exists())

    def test_tc_fah_011_closed_world_oversize_is_rejected_before_design_replay(self):
        bundle = closed_world_state_bundle()
        library = {"schema_version": 1, "design_input_sha256": "0" * 64, "cases": [], "gaps": []}
        with mock.patch("qa_master.case_conformance.design_methods", side_effect=AssertionError("must not replay design")):
            self.assert_domain_error(lambda: audit_method_cases(bundle, library), CaseConformanceError, "CANDIDATE_LIMIT_EXCEEDED")
        with mock.patch("qa_master.method_impact.design_methods", side_effect=AssertionError("must not replay design")):
            self.assert_domain_error(lambda: analyze_method_impact(bundle, bundle, library), MethodImpactError, "CANDIDATE_LIMIT_EXCEEDED")

    def test_tc_fah_012_cleanup_failure_is_stable_and_does_not_override_primary_write_error(self):
        original_unlink = __import__("os").unlink

        def deny_temporary(path, *args, **kwargs):
            if Path(path).name.startswith(".qa-master-audit-"):
                raise PermissionError("injected temporary cleanup failure")
            return original_unlink(path, *args, **kwargs)

        def remove_verified_temporaries(root):
            for temporary in root.glob(".qa-master-audit-*.tmp"):
                original_unlink(temporary)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            before, cases = root / "bundle.json", root / "cases.json"
            before.write_text(json.dumps(self.bundle), encoding="utf-8")
            cases.write_text(json.dumps(self.library), encoding="utf-8")
            for label, call, expected_type in (
                ("audit", lambda output: write_case_audit(before, cases, output), CaseConformanceError),
                ("impact", lambda output: write_method_impact(before, before, cases, output), MethodImpactError),
            ):
                output = root / f"{label}-published.json"
                try:
                    with mock.patch("qa_master.case_conformance.os.unlink", side_effect=deny_temporary):
                        self.assert_domain_error(lambda: call(output), expected_type, "OUTPUT_IO_ERROR")
                finally:
                    remove_verified_temporaries(root)
                self.assertTrue(output.exists())
                published = json.loads(output.read_text(encoding="utf-8"))
                self.assertEqual((published["status"], published["execution"]), ("DRAFT_UNAPPROVED", "NOT_EXECUTED"))

                race_output = root / f"{label}-race.json"
                try:
                    with mock.patch("qa_master.case_conformance.os.link", side_effect=FileExistsError("injected link race")), \
                         mock.patch("qa_master.case_conformance.os.unlink", side_effect=deny_temporary):
                        self.assert_domain_error(lambda: call(race_output), expected_type, "OUTPUT_EXISTS")
                finally:
                    remove_verified_temporaries(root)
                self.assertFalse(race_output.exists())

    def test_tc_fah_013_aggregate_valid_models_are_rejected_before_engine_replay(self):
        bundle = aggregate_decision_bundle()
        # Four valid decision models have 2,501 typed assignments apiece. Each is
        # under the engine's 4,096-row bound while their 10,004-row aggregate
        # must be rejected by the audit boundary without allocating candidates.
        self.assertLess(len(json.dumps(bundle, separators=(",", ":")).encode("utf-8")), 5 * 1024 * 1024)
        for model in bundle["design_models"]["models"]:
            one_model = copy.deepcopy(bundle)
            one_model["design_models"]["models"] = [model]
            self.assertEqual(len(design_methods(one_model)["candidates"]), 2501)
        library = {"schema_version": 1, "design_input_sha256": "0" * 64, "cases": [], "gaps": []}
        with mock.patch("qa_master.case_conformance.design_methods", side_effect=AssertionError("must not replay design")):
            self.assert_domain_error(lambda: audit_method_cases(bundle, library), CaseConformanceError, "CANDIDATE_LIMIT_EXCEEDED")
        with mock.patch("qa_master.method_impact.design_methods", side_effect=AssertionError("must not replay design")):
            self.assert_domain_error(lambda: analyze_method_impact(bundle, bundle, library), MethodImpactError, "CANDIDATE_LIMIT_EXCEEDED")


if __name__ == "__main__":
    unittest.main()
