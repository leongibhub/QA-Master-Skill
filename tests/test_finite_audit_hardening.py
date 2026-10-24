"""Developer regressions for CR-035 public finite-audit boundaries."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from qa_master.case_conformance import CaseConformanceError, audit_method_cases, render_audit_markdown, write_case_audit
from qa_master.design_methods import design_methods
from qa_master.method_impact import MethodImpactError, analyze_method_impact, write_method_impact


EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "design-methods.json"


def library(bundle):
    return {"schema_version": 1, "design_input_sha256": design_methods(bundle)["input_sha256"], "cases": [], "gaps": []}


def open_world(bundle):
    result = copy.deepcopy(bundle); model = next(x for x in result["design_models"]["models"] if x["method"] == "state_transition")
    result["design_models"]["models"] = [model]
    model["spec"] = {"states": [{"id": "S{}".format(i), "terminal": False, "source_refs": ["SRC-STATE"]} for i in range(128)],
                     "initial_state": "S0", "triggers": ["T{}".format(i) for i in range(100)],
                     "transitions": [{"id": "ONE", "validity": "valid", "from_state": "S0", "to_state": "S1", "trigger": "T0", "guard_refs": [], "effect_refs": ["SRC-EFFECT"], "source_refs": ["SRC-STATE"], "oracle_ref": "OR-SUBMITTED"}],
                     "closed_world": False, "closed_world_deny_oracle_ref": None}
    return result


class FiniteAuditHardeningTests(unittest.TestCase):
    def setUp(self): self.bundle = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def test_invalid_gap_reason_and_unhashable_method_have_stable_codes(self):
        bad = library(self.bundle); bad["gaps"] = [{"candidate_id": design_methods(self.bundle)["candidates"][0]["id"], "reason_code": {}}]
        with self.assertRaisesRegex(CaseConformanceError, "^INVALID_GAP$"): audit_method_cases(self.bundle, bad)
        malformed = copy.deepcopy(self.bundle); malformed["design_models"]["models"][0]["method"] = []
        with self.assertRaisesRegex(CaseConformanceError, "^INVALID_SCHEMA$"): audit_method_cases(malformed, library(self.bundle))

    def test_writers_convert_parent_io_and_format_types_to_domain_errors(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); bundle, cases, parent = root / "bundle.json", root / "cases.json", root / "parent"
            bundle.write_text(json.dumps(self.bundle), encoding="utf-8"); cases.write_text(json.dumps(library(self.bundle)), encoding="utf-8"); parent.write_bytes(b"sentinel")
            with self.assertRaisesRegex(CaseConformanceError, "^OUTPUT_IO_ERROR$"): write_case_audit(bundle, cases, parent / "out.json")
            with self.assertRaisesRegex(MethodImpactError, "^OUTPUT_IO_ERROR$"): write_method_impact(bundle, bundle, cases, parent / "out.json")
            self.assertEqual(parent.read_bytes(), b"sentinel")
            with self.assertRaisesRegex(CaseConformanceError, "^INVALID_FORMAT$"): write_case_audit(bundle, cases, root / "a.json", format={})
            with self.assertRaisesRegex(MethodImpactError, "^INVALID_FORMAT$"): write_method_impact(bundle, bundle, cases, root / "i.json", format={})

    def test_open_world_preflight_charges_only_explicit_records(self):
        bundle = open_world(self.bundle)
        report = audit_method_cases(bundle, library(bundle))
        self.assertEqual(report["summary"]["candidate_denominator"], 1)

    def test_renderer_rejects_non_emitter_mismatch_and_finding_shapes(self):
        candidate = design_methods(self.bundle)["candidates"][0]; report = audit_method_cases(self.bundle, library(self.bundle))
        report["candidates"][0].update({"state": "MISMATCH", "codes": ["GAP_DUPLICATE"], "case_ids": [], "gap_reasons": []})
        report["summary"]["states"]["MISSING"] -= 1; report["summary"]["states"]["MISMATCH"] += 1
        report["summary"]["by_model"][report["candidates"][0]["model_id"]]["MISSING"] -= 1; report["summary"]["by_model"][report["candidates"][0]["model_id"]]["MISMATCH"] += 1
        with self.assertRaisesRegex(CaseConformanceError, "^INVALID_REPORT$"): render_audit_markdown(report)
        clean = audit_method_cases(self.bundle, library(self.bundle)); clean["findings"].append({"code": "ORPHAN_CASE", "candidate_id": candidate["id"]}); clean["summary"]["finding_count"] += 1
        with self.assertRaisesRegex(CaseConformanceError, "^INVALID_REPORT$"): render_audit_markdown(clean)

    def test_renderer_enforces_candidate_finding_case_id_cardinality(self):
        candidate = design_methods(self.bundle)["candidates"][0]
        report = audit_method_cases(self.bundle, library(self.bundle))
        for code, case_ids in (("DATA_MISMATCH", []), ("GAP_CASE_CONFLICT", []), ("GAP_DUPLICATE", ["CASE-X"])):
            forged = copy.deepcopy(report)
            forged["findings"].append({"code": code, "candidate_id": candidate["id"], "case_ids": case_ids})
            forged["summary"]["finding_count"] += 1
            with self.subTest(code=code):
                with self.assertRaisesRegex(CaseConformanceError, "^INVALID_REPORT$"):
                    render_audit_markdown(forged)
        genuine = library(self.bundle)
        scenario = {"candidate_id": candidate["id"], "method_data": copy.deepcopy(candidate["method_data"]),
                    "requirement_ids": list(candidate["trace"]), "source_ref_ids": [x["id"] for x in candidate["source_refs"]],
                    "oracle_ref_ids": [x["id"] for x in candidate["oracle_refs"]]}
        genuine["cases"] = [{"id": "CASE-X", "title": "x", "preconditions": "x", "steps": ["x"], "expected": "x", "scenarios": [scenario]}]
        genuine["gaps"] = [{"candidate_id": candidate["id"], "reason_code": "OTHER"}]
        self.assertIn(candidate["id"], render_audit_markdown(audit_method_cases(self.bundle, genuine)))

    def test_cleanup_failure_is_domain_error_but_never_masks_link_race(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); bundle, cases, output = root / "bundle.json", root / "cases.json", root / "report.json"
            bundle.write_text(json.dumps(self.bundle), encoding="utf-8"); cases.write_text(json.dumps(library(self.bundle)), encoding="utf-8")
            with patch("qa_master.case_conformance.os.unlink", side_effect=PermissionError):
                with self.assertRaisesRegex(CaseConformanceError, "^OUTPUT_IO_ERROR$"):
                    write_case_audit(bundle, cases, output)
            self.assertTrue(output.is_file())
            self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["status"], "DRAFT_UNAPPROVED")

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); bundle, cases, output = root / "bundle.json", root / "cases.json", root / "report.json"
            bundle.write_text(json.dumps(self.bundle), encoding="utf-8"); cases.write_text(json.dumps(library(self.bundle)), encoding="utf-8")
            with patch("qa_master.case_conformance.os.link", side_effect=FileExistsError), patch("qa_master.case_conformance.os.unlink", side_effect=PermissionError):
                with self.assertRaisesRegex(CaseConformanceError, "^OUTPUT_EXISTS$"):
                    write_case_audit(bundle, cases, output)
            self.assertFalse(output.exists())
