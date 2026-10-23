"""Independent black-box conformance tests for CR-033 / TASK-135.

The corpus and expected observations here are tester-owned.  It deliberately
does not import the developer test helpers or fixtures.
"""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

from qa_master.case_conformance import (
    CaseConformanceError,
    audit_method_cases,
    render_audit_markdown,
    write_case_audit,
)
from qa_master.design_methods import design_methods


def independent_bundle():
    """A compact valid corpus covering every deterministic design method."""
    return {
        "requirements": [{"id": "REQ-AUDIT", "priority": "P1"}],
        "design_models": {
            "schema_version": 1,
            "source_refs": [
                {"id": "SRC-REQ", "kind": "requirement", "locator": "facts/req"},
                {"id": "SRC-RULE", "kind": "model", "locator": "facts/rule"},
                {"id": "SRC-STATE", "kind": "model", "locator": "facts/state"},
                {"id": "SRC-EFFECT", "kind": "effect", "locator": "facts/effect"},
            ],
            "oracle_refs": [
                {"id": "OR-VALID", "kind": "valid", "locator": "oracle/valid"},
                {"id": "OR-INVALID", "kind": "invalid", "locator": "oracle/invalid"},
                {"id": "OR-OUT", "kind": "outcome", "locator": "oracle/out"},
                {"id": "OR-TRANS", "kind": "transition", "locator": "oracle/trans"},
                {"id": "OR-DENY", "kind": "denial", "locator": "oracle/deny"},
            ],
            "models": [
                {"id": "M-BOUND", "method": "boundary", "title": "Decimal amount",
                 "dimension": "functional", "requirement_ids": ["REQ-AUDIT"],
                 "source_refs": ["SRC-REQ"], "spec": {
                     "numeric_type": "decimal", "precision": 4, "scale": 1,
                     "origin": "0", "step": "0.1",
                     "lower": {"value": "0", "inclusive": True},
                     "upper": {"value": "0.2", "inclusive": True},
                     "oracle_by_class": {"IN_DOMAIN": "OR-VALID",
                                           "LOWER_INVALID": "OR-INVALID",
                                           "UPPER_INVALID": "OR-INVALID",
                                           "BOTH_INVALID": "OR-INVALID"},
                 }},
                {"id": "M-DEC", "method": "decision_table", "title": "Typed choice",
                 "dimension": "functional", "requirement_ids": ["REQ-AUDIT"],
                 "source_refs": ["SRC-REQ", "SRC-RULE"], "spec": {
                     "conditions": [{"id": "typed", "values": [True, 1]}],
                     "constraints": [], "rules": [
                         {"id": "R-BOOL", "when": {"typed": True}, "outcome_id": "bool",
                          "source_refs": ["SRC-RULE"], "oracle_ref": "OR-OUT"},
                         {"id": "R-INT", "when": {"typed": 1}, "outcome_id": "int",
                          "source_refs": ["SRC-RULE"], "oracle_ref": "OR-OUT"},
                     ],
                 }},
                {"id": "M-STATE", "method": "state_transition", "title": "Submit order",
                 "dimension": "functional", "requirement_ids": ["REQ-AUDIT"],
                 "source_refs": ["SRC-REQ", "SRC-STATE"], "spec": {
                     "states": [
                         {"id": "draft", "terminal": False, "source_refs": ["SRC-STATE"]},
                         {"id": "done", "terminal": True, "source_refs": ["SRC-STATE"]},
                     ], "initial_state": "draft", "triggers": ["submit"],
                     "transitions": [{"id": "T-SUBMIT", "validity": "valid",
                         "from_state": "draft", "to_state": "done", "trigger": "submit",
                         "guard_refs": [], "effect_refs": ["SRC-EFFECT"],
                         "source_refs": ["SRC-STATE"], "oracle_ref": "OR-TRANS"}],
                     "closed_world": True, "closed_world_deny_oracle_ref": "OR-DENY",
                 }},
                {"id": "M-PAIR", "method": "pairwise", "title": "Pair options",
                 "dimension": "functional", "requirement_ids": ["REQ-AUDIT"],
                 "source_refs": ["SRC-REQ"], "spec": {
                     "parameters": [{"id": "colour", "values": ["red", "blue"]},
                                    {"id": "size", "values": [1, 2]}],
                     "oracle_ref": "OR-OUT",
                 }},
                {"id": "M-COMB", "method": "combinatorial", "title": "Combination",
                 "dimension": "functional", "requirement_ids": ["REQ-AUDIT"],
                 "source_refs": ["SRC-REQ"], "spec": {
                     "parameters": [{"id": "channel", "values": ["web", "api"]},
                                    {"id": "enabled", "values": [False, True]}],
                     "strength": 2, "oracle_ref": "OR-OUT",
                 }},
            ],
        },
    }


def scenario(candidate):
    return {
        "candidate_id": candidate["id"],
        "method_data": copy.deepcopy(candidate["method_data"]),
        "requirement_ids": list(candidate["trace"]),
        "source_ref_ids": [ref["id"] for ref in candidate["source_refs"]],
        "oracle_ref_ids": [ref["id"] for ref in candidate["oracle_refs"]],
    }


def library(bundle, rows, *, gaps=(), documented=True):
    return {
        "schema_version": 1,
        "design_input_sha256": design_methods(bundle)["input_sha256"],
        "cases": [{
            "id": "CASE-INDEPENDENT", "title": "Audited scenario" if documented else "",
            "preconditions": "The declared model is prepared" if documented else "",
            "steps": ["Perform the declared scenario"] if documented else [],
            "expected": "Observe the declared oracle" if documented else "",
            "scenarios": copy.deepcopy(list(rows)),
        }],
        "gaps": copy.deepcopy(list(gaps)),
    }


class CaseConformanceIndependentTests(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.bundle = independent_bundle()
        self.design = design_methods(self.bundle)
        self.candidates = self.design["candidates"]

    def report_for_all(self):
        return audit_method_cases(self.bundle, library(self.bundle, [scenario(c) for c in self.candidates]))

    def candidate(self, method):
        return next(c for c in self.candidates if c["method"] == method)

    def reported(self, report, candidate):
        return next(item for item in report["candidates"] if item["id"] == candidate["id"])

    def test_tc_cc_001_all_five_methods_have_exact_typed_rows_and_reconciling_denominator(self):
        report = self.report_for_all()
        self.assertEqual({c["method"] for c in self.candidates},
                         {"boundary", "decision_table", "state_transition", "pairwise", "combinatorial"})
        self.assertEqual(report["status"], "DRAFT_UNAPPROVED")
        self.assertEqual(report["execution"], "NOT_EXECUTED")
        self.assertEqual(len(report["candidates"]), len(self.candidates))
        self.assertTrue(all(item["state"] == "EXACTLY_BOUND" for item in report["candidates"]))
        counts = report["summary"]["states"]
        self.assertEqual(sum(counts.values()), len(report["candidates"]))
        self.assertEqual(sum(model["EXACTLY_BOUND"] for model in report["summary"]["by_model"].values()),
                         len(self.candidates))

    def test_tc_cc_002_requirement_trace_cannot_hide_an_omitted_candidate(self):
        omitted = self.candidates[-1]
        rows = [scenario(c) for c in self.candidates if c["id"] != omitted["id"]]
        report = audit_method_cases(self.bundle, library(self.bundle, rows))
        entry = self.reported(report, omitted)
        self.assertEqual(entry["state"], "MISSING")
        self.assertIn("REQ-AUDIT", omitted["trace"])
        self.assertEqual(report["summary"]["states"]["MISSING"], 1)

    def test_tc_cc_003_typed_bool_integer_and_decimal_strings_do_not_coerce(self):
        boolean = next(c for c in self.candidates if c["method"] == "decision_table" and
                       c["method_data"]["assignment"]["typed"] is True)
        decimal = self.candidate("boundary")
        rows = [scenario(boolean), scenario(decimal)]
        rows[0]["method_data"]["assignment"]["typed"] = 1
        rows[1]["method_data"]["value"] = rows[1]["method_data"]["value"] + "0"
        report = audit_method_cases(self.bundle, library(self.bundle, rows))
        for candidate in (boolean, decimal):
            entry = self.reported(report, candidate)
            self.assertEqual(entry["state"], "MISMATCH")
            self.assertIn("DATA_MISMATCH", entry["codes"])

    def test_tc_cc_004_state_oracle_source_and_trace_changes_are_individually_diagnosed(self):
        target = next(c for c in self.candidates if c["method"] == "state_transition" and
                      c["method_data"].get("validity") == "valid")
        mutations = (
            ("state", lambda row: row["method_data"].update({"from_state": "done"}), "DATA_MISMATCH"),
            ("oracle", lambda row: row.update({"oracle_ref_ids": ["OR-OUT"]}), "ORACLE_MISMATCH"),
            ("source", lambda row: row.update({"source_ref_ids": ["SRC-REQ"]}), "SOURCE_MISMATCH"),
            ("trace", lambda row: row.update({"requirement_ids": ["REQ-OTHER"]}), "TRACE_MISMATCH"),
        )
        for name, mutate, expected in mutations:
            with self.subTest(binding=name):
                row = scenario(target)
                mutate(row)
                entry = self.reported(audit_method_cases(self.bundle, library(self.bundle, [row])), target)
                self.assertEqual(entry["state"], "MISMATCH")
                self.assertIn(expected, entry["codes"])

    def test_tc_cc_005_duplicate_gap_conflict_and_orphan_do_not_count_as_representation(self):
        target = self.candidates[0]
        duplicate_report = audit_method_cases(self.bundle, library(self.bundle, [scenario(target), scenario(target)]))
        duplicate = self.reported(duplicate_report, target)
        self.assertEqual(duplicate["state"], "DUPLICATE")

        gap = {"candidate_id": target["id"], "reason_code": "ORACLE_MISSING"}
        gap_report = audit_method_cases(self.bundle, library(self.bundle, [], gaps=[gap]))
        self.assertEqual(self.reported(gap_report, target)["state"], "GAP_RECORDED")
        conflict_report = audit_method_cases(self.bundle, library(self.bundle, [scenario(target)], gaps=[gap]))
        conflict = self.reported(conflict_report, target)
        self.assertEqual(conflict["state"], "MISMATCH")
        self.assertIn("GAP_CASE_CONFLICT", conflict["codes"])

        orphan = scenario(target)
        orphan["candidate_id"] = "TC-MD-UNKNOWN"
        orphan_report = audit_method_cases(self.bundle, library(self.bundle, [orphan]))
        self.assertIn("ORPHAN_CANDIDATE", {code for finding in orphan_report["findings"]
                                             for code in finding.get("codes", [finding.get("code")])})

    def test_tc_cc_005a_duplicate_precedence_retains_empty_expected_documentation_finding(self):
        target = self.candidates[0]
        case_library = library(self.bundle, [scenario(target), scenario(target)])
        case_library["cases"][0]["expected"] = ""
        report = audit_method_cases(self.bundle, case_library)
        self.assertEqual(self.reported(report, target)["state"], "DUPLICATE")
        self.assertIn({"code": "CASE_DOCUMENTATION_INCOMPLETE", "case_id": "CASE-INDEPENDENT"},
                      report["findings"])

    def test_tc_cc_005b_repeated_identical_gap_is_renderable_as_one_reason(self):
        target = self.candidates[0]
        gap = {"candidate_id": target["id"], "reason_code": "ORACLE_MISSING"}
        report = audit_method_cases(self.bundle, library(self.bundle, [], gaps=[gap, gap]))
        entry = self.reported(report, target)
        self.assertEqual(entry["state"], "DUPLICATE")
        self.assertIn("GAP_DUPLICATE", entry["codes"])
        self.assertEqual(entry["gap_reasons"], ["ORACLE_MISSING"])
        markdown = render_audit_markdown(report)
        self.assertIn("ORACLE_MISSING", markdown)

    def test_tc_cc_006_stale_empty_and_incomplete_libraries_never_claim_coverage(self):
        stale = library(self.bundle, [])
        stale["design_input_sha256"] = "0" * 64
        with self.assertRaises(CaseConformanceError) as caught:
            audit_method_cases(self.bundle, stale)
        self.assertTrue(caught.exception.code)

        incomplete = library(self.bundle, [scenario(self.candidates[0])], documented=False)
        report = audit_method_cases(self.bundle, incomplete)
        entry = self.reported(report, self.candidates[0])
        self.assertNotEqual(entry["state"], "EXACTLY_BOUND")
        self.assertIn("CASE_DOCUMENTATION_INCOMPLETE", entry["codes"])

        empty_bundle = copy.deepcopy(self.bundle)
        empty_bundle["design_models"]["models"] = []
        empty_library = {"schema_version": 1,
                         "design_input_sha256": design_methods(empty_bundle)["input_sha256"],
                         "cases": [], "gaps": []}
        empty_report = audit_method_cases(empty_bundle, empty_library)
        self.assertEqual(empty_report["summary"].get("assessment"), "UNASSESSED")
        self.assertFalse(empty_report["summary"].get("complete", False))

    def test_tc_cc_006a_set_order_does_not_change_a_case_library_identity(self):
        first = library(self.bundle, [])
        case_a = copy.deepcopy(first["cases"][0])
        case_b = copy.deepcopy(first["cases"][0])
        case_a.update({"id": "CASE-A", "scenarios": [scenario(self.candidate("state_transition"))]})
        case_b.update({"id": "CASE-B", "scenarios": [scenario(self.candidate("pairwise"))]})
        first["cases"] = [case_a, case_b]
        second = copy.deepcopy(first)
        second["cases"].reverse()
        for row in second["cases"][0]["scenarios"]:
            row["requirement_ids"].reverse()
            row["source_ref_ids"].reverse()
            row["oracle_ref_ids"].reverse()
        pure = audit_method_cases(self.bundle, first)
        self.assertEqual(pure["case_library_sha256"], audit_method_cases(self.bundle, second)["case_library_sha256"])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle_path, cases_path, output_path = root / "bundle.json", root / "cases.json", root / "audit.json"
            bundle_path.write_text(json.dumps(self.bundle), encoding="utf-8")
            cases_path.write_text(json.dumps(second), encoding="utf-8")
            self.assertEqual(pure["case_library_sha256"],
                             write_case_audit(bundle_path, cases_path, output_path)["case_library_sha256"])

    def test_tc_cc_006b_zero_scenario_case_is_an_orphan_not_coverage(self):
        report = audit_method_cases(self.bundle, library(self.bundle, []))
        self.assertEqual(report["summary"]["states"]["EXACTLY_BOUND"], 0)
        self.assertIn("ORPHAN_CASE", {finding["code"] for finding in report["findings"]})

    def test_tc_cc_007_markdown_is_deterministic_and_does_not_echo_case_secret(self):
        marker = "case-secret-DO-NOT-ECHO"
        case_library = library(self.bundle, [scenario(self.candidates[0])])
        case_library["cases"][0]["title"] = marker
        report = audit_method_cases(self.bundle, case_library)
        first = render_audit_markdown(report)
        second = render_audit_markdown(copy.deepcopy(report))
        self.assertEqual(first, second)
        self.assertNotIn(marker, first)
        self.assertIn(self.candidates[0]["id"], first)
        self.assertIn("NOT_EXECUTED", first)
        self.assertIn("does not establish business correctness", first)

    def test_tc_cc_007a_markdown_exposes_gap_reasons_and_orphan_findings(self):
        target = self.candidates[0]
        orphan = scenario(target)
        orphan["candidate_id"] = "TC-MD-UNKNOWN"
        report = audit_method_cases(self.bundle, library(
            self.bundle, [orphan], gaps=[{"candidate_id": target["id"], "reason_code": "CLEANUP_MISSING"}]))
        markdown = render_audit_markdown(report)
        self.assertIn(target["id"], markdown)
        self.assertIn("CLEANUP_MISSING", markdown)
        self.assertIn("ORPHAN_CANDIDATE", markdown)

    def test_tc_cc_007b_renderer_rejects_malformed_public_reports_without_keyerror(self):
        malformed = {"schema_version": 1, "candidates": [{"id": "<script>alert(1)</script>"}]}
        with self.assertRaises(CaseConformanceError) as caught:
            render_audit_markdown(malformed)
        self.assertTrue(caught.exception.code)
        self.assertNotIn("KeyError", caught.exception.code)

    def test_tc_cc_007ba_renderer_rejects_forged_pass_and_inconsistent_summary(self):
        report = self.report_for_all()
        variants = []
        forged_code = copy.deepcopy(report)
        forged_code["candidates"][0]["codes"] = ["PASS"]
        variants.append(forged_code)
        boolean_schema = copy.deepcopy(report)
        boolean_schema["schema_version"] = True
        variants.append(boolean_schema)
        boolean_count = copy.deepcopy(report)
        boolean_count["summary"]["states"]["EXACTLY_BOUND"] = True
        variants.append(boolean_count)
        extra_model = copy.deepcopy(report)
        extra_model["summary"]["by_model"]["M-FORGED"] = {"EXACTLY_BOUND": 1, "GAP_RECORDED": 0,
                                                               "MISSING": 0, "DUPLICATE": 0, "MISMATCH": 0}
        variants.append(extra_model)
        for forged in variants:
            with self.subTest(forged=forged is forged_code):
                with self.assertRaises(CaseConformanceError) as caught:
                    render_audit_markdown(forged)
                self.assertTrue(caught.exception.code)

    def test_tc_cc_007c_markdown_identifies_owning_case_and_both_input_identities(self):
        report = self.report_for_all()
        markdown = render_audit_markdown(report)
        self.assertIn("CASE-INDEPENDENT", markdown)
        self.assertIn(report["design_input_sha256"], markdown)
        self.assertIn(report["case_library_sha256"], markdown)

    def test_tc_cc_007d_requirement_and_reference_identifiers_are_data_not_markup(self):
        bundle = copy.deepcopy(self.bundle)
        bundle["requirements"][0]["id"] = "需求 空格"
        for model in bundle["design_models"]["models"]:
            model["requirement_ids"] = ["需求 空格"]
        bundle["design_models"]["source_refs"][0]["id"] = ".SRC"
        for model in bundle["design_models"]["models"]:
            model["source_refs"] = [".SRC" if item == "SRC-REQ" else item for item in model["source_refs"]]
            spec = model["spec"]
            for record in spec.get("rules", []) + spec.get("states", []) + spec.get("transitions", []):
                for key in ("source_refs", "guard_refs", "effect_refs"):
                    if key in record:
                        record[key] = [".SRC" if item == "SRC-REQ" else item for item in record[key]]
        bundle["design_models"]["oracle_refs"][0]["id"] = ":VALID"
        bundle["design_models"]["models"][0]["spec"]["oracle_by_class"]["IN_DOMAIN"] = ":VALID"
        design = design_methods(bundle)
        report = audit_method_cases(bundle, library(bundle, [scenario(candidate) for candidate in design["candidates"]]))
        self.assertTrue(all(item["state"] == "EXACTLY_BOUND" for item in report["candidates"]))

    def test_tc_cc_008_file_loader_rejects_malformed_json_and_keeps_existing_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle_path = root / "bundle.json"
            cases_path = root / "cases.json"
            output = root / "existing.json"
            bundle_path.write_text(json.dumps(self.bundle), encoding="utf-8")
            output.write_bytes(b"sentinel")
            bad_inputs = (
                b'{"schema_version":1,"schema_version":1}',
                b'{"schema_version":NaN,"design_input_sha256":"0","cases":[],"gaps":[]}',
                (b'{"schema_version":1,"design_input_sha256":"0","cases":[],"gaps":' +
                 b"[" * 33 + b"]" * 33 + b"}"),
            )
            for raw in bad_inputs:
                with self.subTest(raw=raw[:24]):
                    cases_path.write_bytes(raw)
                    with self.assertRaises(CaseConformanceError) as caught:
                        write_case_audit(bundle_path, cases_path, output)
                    self.assertTrue(caught.exception.code)
                    self.assertEqual(output.read_bytes(), b"sentinel")

            oversized = b"{" + b'"x":"' + b"a" * 5_242_881 + b'"}'
            cases_path.write_bytes(oversized)
            with self.assertRaises(CaseConformanceError):
                write_case_audit(bundle_path, cases_path, output)
            self.assertEqual(output.read_bytes(), b"sentinel")

            boundary = json.dumps(library(self.bundle, []), separators=(",", ":")).encode("utf-8")
            self.assertLessEqual(len(boundary), 5_242_880)
            cases_path.write_bytes(boundary + b" " * (5_242_880 - len(boundary)))
            boundary_output = root / "boundary.json"
            write_case_audit(bundle_path, cases_path, boundary_output)
            self.assertTrue(boundary_output.exists())

    def test_tc_cc_008a_malformed_design_preflight_is_a_value_free_domain_rejection(self):
        malformed = copy.deepcopy(self.bundle)
        malformed["design_models"]["models"] = [{"id": "M-BAD", "method": "decision_table", "spec": None}]
        with self.assertRaises(CaseConformanceError) as caught:
            audit_method_cases(malformed, library(self.bundle, []))
        self.assertTrue(caught.exception.code)
        self.assertNotIn("TypeError", caught.exception.code)

    def test_tc_cc_009_cardinality_and_linked_destinations_reject_without_clobbering(self):
        too_many_cases = library(self.bundle, [])
        too_many_cases["cases"] = [copy.deepcopy(too_many_cases["cases"][0]) for _ in range(10_001)]
        with self.assertRaises(CaseConformanceError):
            audit_method_cases(self.bundle, too_many_cases)
        too_many_rows = library(self.bundle, [])
        too_many_rows["cases"][0]["scenarios"] = [scenario(self.candidates[0]) for _ in range(50_001)]
        with self.assertRaises(CaseConformanceError):
            audit_method_cases(self.bundle, too_many_rows)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle_path, cases_path = root / "bundle.json", root / "cases.json"
            bundle_path.write_text(json.dumps(self.bundle), encoding="utf-8")
            cases_path.write_text(json.dumps(library(self.bundle, [])), encoding="utf-8")
            with self.assertRaises(CaseConformanceError):
                write_case_audit(bundle_path, cases_path, bundle_path)

            protected, link = root / "protected.json", root / "linked.json"
            protected.write_bytes(b"protected")
            try:
                os.symlink(protected, link)
            except (OSError, NotImplementedError):
                self.skipTest("symbolic links are unavailable to this test account")
            with self.assertRaises(CaseConformanceError):
                write_case_audit(bundle_path, cases_path, link)
            self.assertEqual(protected.read_bytes(), b"protected")

    @unittest.skipUnless(os.name == "nt", "native Windows junction semantics only")
    def test_tc_cc_009a_windows_junction_ancestor_is_rejected_without_touching_target(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target, junction = root / "target", root / "junction"
            target.mkdir()
            created = subprocess.run(["cmd", "/d", "/c", "mklink", "/J", str(junction), str(target)],
                                     capture_output=True, text=True, encoding="utf-8", errors="replace")
            self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
            try:
                linked_bundle, linked_cases = junction / "bundle.json", junction / "cases.json"
                linked_bundle.write_text(json.dumps(self.bundle), encoding="utf-8")
                linked_cases.write_text(json.dumps(library(self.bundle, [])), encoding="utf-8")
                with self.assertRaises(CaseConformanceError):
                    write_case_audit(linked_bundle, linked_cases, root / "audit.json")
                bundle_path, cases_path = root / "bundle.json", root / "cases.json"
                bundle_path.write_text(json.dumps(self.bundle), encoding="utf-8")
                cases_path.write_text(json.dumps(library(self.bundle, [])), encoding="utf-8")
                protected = target / "audit.json"
                protected.write_bytes(b"protected")
                with self.assertRaises(CaseConformanceError):
                    write_case_audit(bundle_path, cases_path, junction / "audit.json")
                self.assertEqual(protected.read_bytes(), b"protected")
            finally:
                if junction.exists():
                    os.rmdir(junction)

    def test_tc_cc_010_cli_is_offline_and_safe_from_a_consumer_directory(self):
        """E2E package check from a fresh wheel, outside the source checkout."""
        with tempfile.TemporaryDirectory(prefix="cc-audit-") as directory:
            root = Path(directory)
            wheel_dir, venv_dir, consumer = root / "wheel", root / "venv", root / "consumer"
            wheel_dir.mkdir()
            consumer.mkdir()
            repo = Path(__file__).resolve().parents[1]
            archive = root / "source.zip"
            archived = subprocess.run(["git", "archive", "--format=zip", "--output", str(archive), "HEAD"],
                                      cwd=repo, capture_output=True, text=True, encoding="utf-8", errors="replace")
            self.assertEqual(archived.returncode, 0, archived.stdout + archived.stderr)
            source = root / "source"
            with zipfile.ZipFile(archive) as frozen:
                frozen.extractall(source)
            build = subprocess.run([sys.executable, "-m", "pip", "wheel", str(source), "--no-deps",
                                    "--no-build-isolation", "-w", str(wheel_dir)], cwd=consumer,
                                   capture_output=True, text=True, encoding="utf-8", errors="replace")
            self.assertEqual(build.returncode, 0, build.stdout + build.stderr)
            create = subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], cwd=consumer,
                                    capture_output=True, text=True, encoding="utf-8", errors="replace")
            self.assertEqual(create.returncode, 0, create.stdout + create.stderr)
            vpython = venv_dir / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
            wheel = next(wheel_dir.glob("*.whl"))
            install = subprocess.run([str(vpython), "-m", "pip", "install", "--no-index", "--no-deps", str(wheel)],
                                     cwd=consumer, capture_output=True, text=True, encoding="utf-8", errors="replace")
            self.assertEqual(install.returncode, 0, install.stdout + install.stderr)
            bundle_path, cases_path, output_path = consumer / "bundle.json", consumer / "cases.json", consumer / "audit.md"
            bundle_path.write_text(json.dumps(self.bundle), encoding="utf-8")
            cases_path.write_text(json.dumps(library(self.bundle, [scenario(c) for c in self.candidates])), encoding="utf-8")
            command = [str(vpython), "-I", "-m", "qa_master", "audit-method-cases", "--input", str(bundle_path),
                       "--cases", str(cases_path), "--output", str(output_path), "--format", "markdown"]
            completed = subprocess.run(command, cwd=consumer, capture_output=True, text=True, encoding="utf-8", errors="replace")
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertTrue(output_path.exists())
            self.assertNotIn("case-secret", completed.stdout + completed.stderr)
