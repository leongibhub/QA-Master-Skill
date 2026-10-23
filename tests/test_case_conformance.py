"""Developer tests for TASK-133's finite-model case audit."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from qa_master.case_conformance import (
    CaseConformanceError,
    audit_method_cases,
    render_audit_markdown,
    write_case_audit,
)
from qa_master.design_methods import design_methods


EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "design-methods.json"


def library(bundle, rows=()):
    digest = design_methods(bundle)["input_sha256"]
    return {"schema_version": 1, "design_input_sha256": digest, "cases": [
        {"id": "CASE-1", "title": "Concrete case", "preconditions": "Prepared", "steps": ["Act"],
         "expected": "Observed", "scenarios": list(rows)}], "gaps": []}


def row(candidate):
    return {"candidate_id": candidate["id"], "method_data": copy.deepcopy(candidate["method_data"]),
            "requirement_ids": list(candidate["trace"]),
            "source_ref_ids": [item["id"] for item in candidate["source_refs"]],
            "oracle_ref_ids": [item["id"] for item in candidate["oracle_refs"]]}


class CaseConformanceTests(unittest.TestCase):
    def setUp(self):
        self.bundle = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        self.design = design_methods(self.bundle)

    def test_missing_candidate_reconciles_the_full_denominator(self):
        result = audit_method_cases(self.bundle, library(self.bundle))
        self.assertEqual(result["summary"]["states"]["MISSING"], len(result["candidates"]))
        self.assertEqual(result["status"], "DRAFT_UNAPPROVED")
        self.assertEqual(result["execution"], "NOT_EXECUTED")

    def test_exact_binding_requires_all_typed_values_and_references(self):
        candidate = self.design["candidates"][0]
        result = audit_method_cases(self.bundle, library(self.bundle, [row(candidate)]))
        found = next(item for item in result["candidates"] if item["id"] == candidate["id"])
        self.assertEqual(found["state"], "EXACTLY_BOUND")
        broken = row(candidate); broken["method_data"] = {"value": True}
        result = audit_method_cases(self.bundle, library(self.bundle, [broken]))
        found = next(item for item in result["candidates"] if item["id"] == candidate["id"])
        self.assertEqual(found["state"], "MISMATCH")
        self.assertIn("DATA_MISMATCH", found["codes"])

    def test_engine_safe_leading_punctuation_ids_bind_exactly(self):
        remapped = json.loads(json.dumps(self.bundle).replace("REQ-EXAMPLE", "需求 标识").replace("SRC-REQ", "._SRC").replace("OR-VALID", ":OR"))
        candidate = design_methods(remapped)["candidates"][0]
        data = library(remapped, [row(candidate)])
        data["cases"][0]["id"] = "-CASE"
        result = audit_method_cases(remapped, data)
        found = next(item for item in result["candidates"] if item["id"] == candidate["id"])
        self.assertEqual(found["state"], "EXACTLY_BOUND")
        self.assertEqual(found["case_ids"], ["-CASE"])

    def test_markdown_keeps_every_orphan_case_identity(self):
        candidate = self.design["candidates"][0]
        unknown = row(candidate); unknown["candidate_id"] = "_UNKNOWN"
        data = library(self.bundle, [unknown])
        second = copy.deepcopy(data["cases"][0]); second["id"] = "CASE-2"; second["scenarios"] = [copy.deepcopy(unknown)]
        data["cases"].append(second)
        markdown = render_audit_markdown(audit_method_cases(self.bundle, data))
        self.assertIn("case_id=`CASE-1`", markdown)
        self.assertIn("case_id=`CASE-2`", markdown)

    def test_stale_duplicate_orphan_and_incomplete_documentation_are_explicit(self):
        candidate = self.design["candidates"][0]
        copied = row(candidate)
        data = library(self.bundle, [copied, copied])
        result = audit_method_cases(self.bundle, data)
        found = next(item for item in result["candidates"] if item["id"] == candidate["id"])
        self.assertEqual(found["state"], "DUPLICATE")
        data = library(self.bundle, [row(candidate)])
        data["cases"][0]["expected"] = ""
        result = audit_method_cases(self.bundle, data)
        found = next(item for item in result["candidates"] if item["id"] == candidate["id"])
        self.assertIn("CASE_DOCUMENTATION_INCOMPLETE", found["codes"])
        data = library(self.bundle)
        data["design_input_sha256"] = "0" * 64
        with self.assertRaisesRegex(CaseConformanceError, "^STALE_DESIGN_INPUT$"):
            audit_method_cases(self.bundle, data)
        data = library(self.bundle, [{"candidate_id": "TC-MD-NOTREAL", "method_data": {},
                                      "requirement_ids": [], "source_ref_ids": [], "oracle_ref_ids": []}])
        result = audit_method_cases(self.bundle, data)
        self.assertIn("ORPHAN_CANDIDATE", [item["code"] for item in result["findings"]])

    def test_incomplete_documentation_is_found_even_when_candidate_is_duplicate(self):
        candidate = self.design["candidates"][0]
        data = library(self.bundle, [row(candidate), row(candidate)])
        data["cases"][0]["expected"] = ""
        result = audit_method_cases(self.bundle, data)
        entry = next(item for item in result["candidates"] if item["id"] == candidate["id"])
        self.assertEqual(entry["state"], "DUPLICATE")
        self.assertIn({"code": "CASE_DOCUMENTATION_INCOMPLETE", "case_id": "CASE-1"}, result["findings"])

    def test_gap_and_engine_obligations_are_retained_without_coverage_claim(self):
        candidate = self.design["candidates"][0]
        data = library(self.bundle, [row(candidate)])
        data["gaps"] = [{"candidate_id": candidate["id"], "reason_code": "ORACLE_MISSING"}]
        result = audit_method_cases(self.bundle, data)
        found = next(item for item in result["candidates"] if item["id"] == candidate["id"])
        self.assertIn("GAP_CASE_CONFLICT", found["codes"])
        self.assertTrue(all(set(item) >= {"id", "code", "model_id"} for item in result["obligations"]))
        markdown = render_audit_markdown(result)
        self.assertIn("does not establish", markdown)
        self.assertIn("Candidate denominator", markdown)
        self.assertIn("EXACTLY_BOUND", markdown)
        self.assertIn("Obligations", markdown)

    def test_duplicate_identical_gaps_render_from_their_own_report(self):
        candidate = self.design["candidates"][0]
        gap = {"candidate_id": candidate["id"], "reason_code": "ORACLE_MISSING"}
        data = library(self.bundle)
        data["gaps"] = [gap, copy.deepcopy(gap)]
        report = audit_method_cases(self.bundle, data)
        entry = next(item for item in report["candidates"] if item["id"] == candidate["id"])
        self.assertEqual(entry["state"], "DUPLICATE")
        self.assertEqual(entry["gap_reasons"], ["ORACLE_MISSING"])
        self.assertIn(candidate["id"], render_audit_markdown(report))

    def test_public_api_rejects_an_oversized_canonical_input(self):
        oversized = library(self.bundle)
        oversized["cases"][0]["title"] = "x" * (5 * 1024 * 1024 + 1)
        with self.assertRaisesRegex(CaseConformanceError, "^INPUT_TOO_LARGE$"):
            audit_method_cases(self.bundle, oversized)

    def test_public_markdown_renderer_rejects_malformed_or_injected_reports(self):
        candidate = self.design["candidates"][0]
        report = audit_method_cases(self.bundle, library(self.bundle, [row(candidate)]))
        report["candidates"][0]["id"] = "SAFE|INJECTED\n| forged"
        with self.assertRaisesRegex(CaseConformanceError, "^INVALID_REPORT$"):
            render_audit_markdown(report)
        with self.assertRaisesRegex(CaseConformanceError, "^INVALID_REPORT$"):
            render_audit_markdown({"schema_version": 1})

    def test_markdown_includes_digests_and_rejects_forged_pass_code(self):
        candidate = self.design["candidates"][0]
        report = audit_method_cases(self.bundle, library(self.bundle, [row(candidate)]))
        markdown = render_audit_markdown(report)
        self.assertIn(report["design_input_sha256"], markdown)
        self.assertIn(report["case_library_sha256"], markdown)
        report["candidates"][0]["codes"] = ["PASS"]
        with self.assertRaisesRegex(CaseConformanceError, "^INVALID_REPORT$"):
            render_audit_markdown(report)

    def test_file_io_is_exclusive_and_atomic(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root / "bundle.json"; cases = root / "cases.json"; output = root / "audit.json"
            source.write_text(json.dumps(self.bundle), encoding="utf-8")
            payload = library(self.bundle); cases.write_text(json.dumps(payload), encoding="utf-8")
            result = write_case_audit(source, cases, output)
            self.assertEqual(result["case_library_sha256"], audit_method_cases(self.bundle, payload)["case_library_sha256"])
            before = output.read_bytes()
            with self.assertRaisesRegex(CaseConformanceError, "^OUTPUT_EXISTS$"):
                write_case_audit(source, cases, output)
            self.assertEqual(output.read_bytes(), before)
            with self.assertRaisesRegex(CaseConformanceError, "^OUTPUT_INPUT_CONFLICT$"):
                write_case_audit(source, cases, source)

    def test_cli_does_not_load_campaign_state_and_rejects_duplicate_flags(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root / "bundle.json"; cases = root / "cases.json"; output = root / "audit.md"
            source.write_text(json.dumps(self.bundle), encoding="utf-8")
            cases.write_text(json.dumps(library(self.bundle)), encoding="utf-8")
            run = subprocess.run([sys.executable, "-m", "qa_master", "--state", str(root / "absent.json"),
                                  "audit-method-cases", "--input", str(source), "--cases", str(cases),
                                  "--output", str(output), "--format", "markdown"], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertFalse((root / "absent.json").exists())
            self.assertIn("DRAFT_UNAPPROVED", output.read_text(encoding="utf-8"))
            duplicate = subprocess.run([sys.executable, "-m", "qa_master", "audit-method-cases",
                                        "--input", str(source), "--input", str(source), "--cases", str(cases),
                                        "--output", str(root / "duplicate.json")], capture_output=True, text=True)
            self.assertEqual(duplicate.returncode, 2)
            self.assertFalse((root / "duplicate.json").exists())


if __name__ == "__main__":
    unittest.main()
