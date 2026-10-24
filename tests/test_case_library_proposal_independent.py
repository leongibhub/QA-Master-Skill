"""Independent black-box tests for CR-036 / TASK-150.

This corpus owns its finite-model fixtures.  It intentionally imports no
developer test helpers and exercises the published Python and CLI boundaries.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from uuid import uuid4
import zipfile
from unittest.mock import patch

from qa_master.case_library_proposal import (
    CaseLibraryProposalError,
    propose_method_case_library,
    write_method_case_library_proposal,
)
from qa_master.design_methods import design_methods


def five_method_bundle():
    """A self-contained, deliberately small corpus for every supported method."""
    def model(identifier, method, spec, refs):
        return {"id": identifier, "method": method, "title": identifier,
                "dimension": "functional", "requirement_ids": ["REQ-PROP"],
                "source_refs": refs, "spec": spec}
    return {"requirements": [{"id": "REQ-PROP", "priority": "P1", "text": "finite proposal input"}],
            "design_models": {"schema_version": 1,
                "source_refs": [{"id": "SRC-REQ", "kind": "requirement", "locator": "requirements"},
                                {"id": "SRC-RULE", "kind": "model", "locator": "rules"},
                                {"id": "SRC-STATE", "kind": "model", "locator": "states"},
                                {"id": "SRC-EFFECT", "kind": "effect", "locator": "effects"}],
                "oracle_refs": [{"id": "OR-VALID", "kind": "valid", "locator": "valid"},
                                {"id": "OR-INVALID", "kind": "invalid", "locator": "invalid"},
                                {"id": "OR-OUT", "kind": "outcome", "locator": "outcome"},
                                {"id": "OR-TRANS", "kind": "transition", "locator": "transition"},
                                {"id": "OR-DENY", "kind": "denial", "locator": "deny"}],
                "models": [
                    model("M-BOUND", "boundary", {"numeric_type": "integer", "origin": 0, "step": 1,
                        "lower": {"value": 1, "inclusive": True}, "upper": {"value": 3, "inclusive": True},
                        "oracle_by_class": {"IN_DOMAIN": "OR-VALID", "LOWER_INVALID": "OR-INVALID",
                            "UPPER_INVALID": "OR-INVALID", "BOTH_INVALID": "OR-INVALID"}}, ["SRC-REQ"]),
                    model("M-DEC", "decision_table", {"conditions": [{"id": "member", "values": [False, True]}],
                        "constraints": [], "rules": [{"id": "yes", "when": {"member": True}, "outcome_id": "yes",
                            "source_refs": ["SRC-RULE"], "oracle_ref": "OR-OUT"},
                            {"id": "no", "when": {"member": False}, "outcome_id": "no",
                             "source_refs": ["SRC-RULE"], "oracle_ref": "OR-OUT"}]}, ["SRC-REQ", "SRC-RULE"]),
                    model("M-STATE", "state_transition", {"states": [{"id": "draft", "terminal": False, "source_refs": ["SRC-STATE"]},
                        {"id": "done", "terminal": True, "source_refs": ["SRC-STATE"]}], "initial_state": "draft",
                        "triggers": ["submit"], "transitions": [{"id": "go", "validity": "valid", "from_state": "draft",
                            "to_state": "done", "trigger": "submit", "guard_refs": [], "effect_refs": ["SRC-EFFECT"],
                            "source_refs": ["SRC-STATE"], "oracle_ref": "OR-TRANS"}], "closed_world": True,
                        "closed_world_deny_oracle_ref": "OR-DENY"}, ["SRC-REQ", "SRC-STATE"]),
                    model("M-PAIR", "pairwise", {"parameters": [{"id": "colour", "values": ["red", "blue"]},
                        {"id": "size", "values": [1, 2]}], "oracle_ref": "OR-OUT"}, ["SRC-REQ"]),
                    model("M-COMB", "combinatorial", {"parameters": [{"id": "channel", "values": ["api", "web"]},
                        {"id": "enabled", "values": [False, True]}], "strength": 2, "oracle_ref": "OR-OUT"}, ["SRC-REQ"]),
                ]}}


def scenario(candidate):
    return {"candidate_id": candidate["id"], "method_data": copy.deepcopy(candidate["method_data"]),
            "requirement_ids": list(candidate["trace"]),
            "source_ref_ids": [item["id"] for item in candidate["source_refs"]],
            "oracle_ref_ids": [item["id"] for item in candidate["oracle_refs"]]}


def strict_library(bundle, *, cases=None, gaps=None):
    design = design_methods(bundle)
    if cases is None:
        cases = [{"id": "CASE-PROP", "title": "Authored prose", "preconditions": "ready",
                  "steps": ["perform finite scenario", "observe result"], "expected": "declared outcome",
                  "scenarios": [scenario(item) for item in design["candidates"]]}]
    return {"schema_version": 1, "design_input_sha256": design["input_sha256"],
            "cases": copy.deepcopy(cases), "gaps": copy.deepcopy(gaps or [])}


def compact(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8") + b"\n"


class CaseLibraryProposalIndependentTests(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.before = five_method_bundle()
        self.library = strict_library(self.before)
        self.before_design = design_methods(self.before)

    def result(self, after=None, library=None):
        return propose_method_case_library(self.before, after or self.before, library or self.library)

    def assert_draft_contract(self, report):
        required = {"schema_version", "status", "execution", "application_state", "before_design_input_sha256",
            "after_design_input_sha256", "baseline_case_library_sha256", "proposed_case_library_sha256",
            "proposed_case_library", "candidate_deltas", "case_decisions", "row_decisions", "held_gaps",
            "missing_vector_followups", "baseline_audit_summary", "baseline_findings", "obligation_deltas",
            "unknowns", "post_proposal_audit", "summary", "limitations"}
        self.assertEqual(set(report), required)
        self.assertEqual((report["schema_version"], report["status"], report["execution"], report["application_state"]),
                         (1, "DRAFT_UNAPPROVED", "NOT_EXECUTED", "NOT_APPLIED"))
        self.assertEqual(set(report["proposed_case_library"]), {"schema_version", "design_input_sha256", "cases", "gaps"})
        self.assertEqual(report["proposed_case_library"]["gaps"], [])

    def test_tc_prop_001_unchanged_all_five_methods_and_hash_audit_hold(self):
        report = self.result()
        self.assert_draft_contract(report)
        self.assertEqual({item["method"] for item in self.before_design["candidates"]},
                         {"boundary", "decision_table", "state_transition", "pairwise", "combinatorial"})
        self.assertEqual([item["case_id"] for item in report["case_decisions"]], ["CASE-PROP"])
        self.assertEqual(report["case_decisions"][0]["decision"], "CARRY_PROPOSED")
        self.assertTrue(all(item["decision"] == "CARRY_PROPOSED" for item in report["row_decisions"]))
        self.assertEqual(report["proposed_case_library_sha256"], report["post_proposal_audit"]["case_library_sha256"])
        self.assertEqual(report["summary"]["proposed_gap_count"], 0)
        summary = report["summary"]
        self.assertEqual(summary["source_case_count"], summary["proposed_case_count"] + summary["held_case_count"])
        self.assertEqual(summary["source_row_count"], summary["proposed_row_count"] + summary["held_row_count"])
        self.assertEqual(summary["source_gap_count"], summary["held_gap_count"])
        self.assertEqual(summary["after_candidate_count"], summary["exact_after_candidate_count"] + summary["missing_after_candidate_count"])
        self.assertEqual(sum(summary["case_decision_counts"].values()), summary["source_case_count"])
        self.assertEqual(sum(summary["row_decision_counts"].values()), summary["source_row_count"])

    def test_tc_prop_002_source_sha_churn_rebinds_without_add_remove(self):
        after = copy.deepcopy(self.before)
        after["design_models"]["source_refs"][0]["sha256"] = "a" * 64
        report = self.result(after)
        self.assertTrue(all(item["pair_state"] == "RETAINED_VECTOR" for item in report["candidate_deltas"]))
        decision = report["case_decisions"][0]
        self.assertEqual(decision["decision"], "REBIND_PROPOSED_REVIEW_REQUIRED")
        self.assertTrue(decision["review_required"])
        self.assertIn("SOURCE_DESCRIPTORS_CHANGED", decision["reason_codes"])
        self.assertTrue(all(item["decision"] == "REBIND_PROPOSED_REVIEW_REQUIRED" for item in report["row_decisions"]))

    def test_tc_prop_003_context_binding_changes_preserve_types_and_prose(self):
        after = copy.deepcopy(self.before)
        after["requirements"][0]["text"] = "changed requirement context"
        next(item for item in after["design_models"]["oracle_refs"] if item["id"] == "OR-OUT")["locator"] = "changed/outcome"
        next(item for item in after["design_models"]["source_refs"] if item["id"] == "SRC-RULE")["locator"] = "changed/rule"
        report = self.result(after)
        proposed = report["proposed_case_library"]["cases"][0]
        original = self.library["cases"][0]
        self.assertEqual([proposed[key] for key in ("id", "title", "preconditions", "steps", "expected")],
                         [original[key] for key in ("id", "title", "preconditions", "steps", "expected")])
        self.assertTrue(all(item["review_required"] for item in report["case_decisions"] + report["row_decisions"]))
        self.assertTrue(all(set(item["proposed_scenario"]) == {"candidate_id", "method_data", "requirement_ids", "source_ref_ids", "oracle_ref_ids"}
                            for item in report["row_decisions"]))
        self.assertTrue(any("REQUIREMENT_CONTEXT_CHANGED" in item["reason_codes"] for item in report["row_decisions"]))

    def test_tc_prop_004_whole_case_hold_removal_and_ambiguous_two_old_one_new(self):
        after = copy.deepcopy(self.before)
        after["design_models"]["models"] = [item for item in after["design_models"]["models"] if item["id"] != "M-PAIR"]
        report = self.result(after)
        self.assertEqual(report["case_decisions"][0]["decision"], "HELD_REMOVAL")
        self.assertEqual(report["proposed_case_library"]["cases"], [])
        self.assertTrue(all(item["after_candidate_id"] is None and item["proposed_scenario"] is None for item in report["row_decisions"]))
        self.assertTrue(all("CASE_HELD" in item["reason_codes"] for item in report["row_decisions"]))
        self.assertTrue(report["missing_vector_followups"])
        self.assertTrue(all("FINITE_VECTOR_REMOVED" in item["reason_codes"] for item in report["missing_vector_followups"]))

        # Synthetic impact is limited to the public proposal boundary: it asserts that an
        # ambiguous 2-old/1-new locator never causes the implementation to choose a new ID.
        old_a, old_b = self.before_design["candidates"][:2]
        fake = {"after_design_input_sha256": design_methods(self.before)["input_sha256"], "candidate_deltas": [{
            "pair_state": "AMBIGUOUS", "before_candidate_ids": [old_a["id"], old_b["id"]],
            "after_candidate_ids": ["TC-MD-NEW"], "reason_codes": ["AMBIGUOUS_MAPPING"]}],
            "case_row_actions": [{"case_id": "CASE-PROP", "scenario_sha256": "0" * 64, "occurrence": 1,
                                  "before_candidate_id": old_a["id"], "after_candidate_id": None,
                                  "possible_after_candidate_ids": ["TC-MD-NEW"], "action": "REVIEW_AMBIGUOUS",
                                  "reason_codes": ["AMBIGUOUS_MAPPING"]}],
            "baseline_audit_summary": {}, "baseline_findings": [], "obligation_deltas": [], "unknowns": []}
        with patch("qa_master.case_library_proposal.analyze_method_impact", return_value=fake):
            with self.assertRaises(CaseLibraryProposalError) as caught:
                self.result()
        self.assertTrue(caught.exception.code)

    def test_tc_prop_005_bad_baseline_and_empty_case_are_held_and_identifiable(self):
        empty = {"id": "CASE-EMPTY", "title": "Empty", "preconditions": "ready", "steps": ["act"],
                 "expected": "observe", "scenarios": []}
        library = strict_library(self.before, cases=[self.library["cases"][0], empty])
        report = self.result(library=library)
        empty_decision = next(item for item in report["case_decisions"] if item["case_id"] == "CASE-EMPTY")
        self.assertEqual(empty_decision["decision"], "HELD_BASELINE")
        self.assertEqual(empty_decision["original_case"], empty)
        stale = copy.deepcopy(library); stale["design_input_sha256"] = "0" * 64
        with self.assertRaises(CaseLibraryProposalError) as caught:
            self.result(library=stale)
        self.assertEqual(caught.exception.code, "STALE_DESIGN_INPUT")

    def test_tc_prop_006_obligations_hold_entire_case_and_retain_reasons(self):
        before = copy.deepcopy(self.before)
        next(item for item in before["design_models"]["models"] if item["id"] == "M-BOUND")["spec"]["oracle_by_class"].pop("LOWER_INVALID")
        report = propose_method_case_library(before, before, strict_library(before))
        self.assertEqual(report["case_decisions"][0]["decision"], "HELD_OBLIGATION")
        self.assertIn("UNRESOLVED_MODEL_OBLIGATION", report["case_decisions"][0]["reason_codes"])
        self.assertTrue(all(item["decision"] in {"HELD_OBLIGATION", "HELD_CASE_ATOMICITY"} for item in report["row_decisions"]))
        self.assertTrue(all("CASE_HELD" in item["reason_codes"] for item in report["row_decisions"]))

    def test_tc_prop_007_every_original_gap_occurrence_is_held(self):
        gaps = [{"candidate_id": self.before_design["candidates"][0]["id"], "reason_code": "OTHER"},
                {"candidate_id": self.before_design["candidates"][0]["id"], "reason_code": "OTHER"},
                {"candidate_id": "TC-MD-ORPHAN", "reason_code": "SOURCE_MISSING"}]
        report = self.result(library=strict_library(self.before, gaps=gaps))
        self.assertEqual(len(report["held_gaps"]), 3)
        self.assertEqual([item["occurrence"] for item in report["held_gaps"][:2]], [1, 2])
        self.assertTrue(all(item["decision"] == "HELD_GAP_REVIEW_REQUIRED" for item in report["held_gaps"]))
        self.assertTrue(all(item["original_gap"] in gaps for item in report["held_gaps"]))
        self.assertTrue(all({"GAP_HELD", "GAP_REASON_REVIEW_REQUIRED"} <= set(item["reason_codes"])
                            for item in report["held_gaps"]))
        self.assertTrue(all(item["possible_after_candidate_ids"] == sorted(item["possible_after_candidate_ids"])
                            for item in report["held_gaps"]))

    def test_tc_prop_008_exact_missing_after_contexts_and_counts(self):
        after = copy.deepcopy(self.before)
        extra = copy.deepcopy(next(item for item in after["design_models"]["models"] if item["id"] == "M-COMB")); extra["id"] = "M-COMB-EXTRA"
        after["design_models"]["models"].append(extra)
        report = self.result(after)
        missing = report["missing_vector_followups"]
        self.assertEqual(len(missing), report["summary"]["missing_after_candidate_count"])
        self.assertEqual(report["summary"]["after_candidate_count"], report["summary"]["exact_after_candidate_count"] + len(missing))
        for item in missing:
            self.assertEqual(set(item), {"candidate_id", "model_id", "method", "dimension", "method_data", "requirement_ids",
                                         "source_ref_ids", "oracle_ref_ids", "source_refs", "oracle_refs", "action", "reason_codes"})
            self.assertEqual(item["action"], "AUTHOR_CASE_OR_RECORD_GAP")
            self.assertEqual(item["source_refs"], sorted(item["source_refs"], key=lambda ref: ref["id"]))
            self.assertEqual(item["oracle_refs"], sorted(item["oracle_refs"], key=lambda ref: ref["id"]))

    def test_tc_prop_009_order_identity_no_alias_and_determinism(self):
        original = copy.deepcopy(self.library)
        snapshot = copy.deepcopy(original)
        first = self.result(library=original)
        self.assertEqual(original, snapshot)
        first["case_decisions"][0]["original_case"]["title"] = "mutated return only"
        self.assertEqual(original, snapshot)
        self.assertEqual(compact(self.result(library=copy.deepcopy(self.library))),
                         compact(self.result(library=copy.deepcopy(self.library))))
        permuted = copy.deepcopy(self.library)
        permuted["cases"][0]["scenarios"].reverse()
        for row in permuted["cases"][0]["scenarios"]:
            row["requirement_ids"].reverse(); row["source_ref_ids"].reverse(); row["oracle_ref_ids"].reverse()
        second = self.result(library=permuted)
        self.assertEqual(first["baseline_case_library_sha256"], second["baseline_case_library_sha256"])
        self.assertEqual([(r["case_id"], r["scenario_sha256"], r["occurrence"]) for r in first["row_decisions"]],
                         [(r["case_id"], r["scenario_sha256"], r["occurrence"]) for r in second["row_decisions"]])
        self.assertEqual([item["case_id"] for item in second["case_decisions"]], sorted(item["case_id"] for item in second["case_decisions"]))

    def test_tc_prop_010_strict_parse_limits_io_and_cli_contract(self):
        with tempfile.TemporaryDirectory(prefix="proposal-independent-") as directory:
            root = Path(directory); before, after, cases, output = (root / name for name in ("before.json", "after.json", "cases.json", "proposal.json"))
            marked_library = copy.deepcopy(self.library)
            marker = "CASE_PROSE_MARKER_9e956e9f"
            marked_library["cases"][0]["title"] = marker
            before.write_bytes(compact(self.before)); after.write_bytes(compact(self.before)); cases.write_bytes(compact(marked_library))
            output.write_bytes(b"SENTINEL")
            with self.assertRaises(CaseLibraryProposalError) as caught:
                write_method_case_library_proposal(before, after, cases, output)
            self.assertEqual(caught.exception.code, "OUTPUT_EXISTS"); self.assertEqual(output.read_bytes(), b"SENTINEL")
            output.unlink()
            for raw in (b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":' + b"[" * 33 + b"]" * 33 + b"}"):
                before.write_bytes(raw)
                with self.assertRaises(CaseLibraryProposalError) as rejected:
                    write_method_case_library_proposal(before, after, cases, output)
                self.assertTrue(rejected.exception.code); self.assertFalse(output.exists())
            before.write_bytes(compact(self.before))
            # File-wrapper input boundary, raw parser/depth and cardinality failures
            # must leave a not-yet-created target absent.
            cases.write_bytes(b"{" + b'\"x\":\"' + b"x" * (5 * 1024 * 1024) + b'\"}')
            with self.assertRaises(CaseLibraryProposalError) as oversized:
                write_method_case_library_proposal(before, after, cases, output)
            self.assertEqual(oversized.exception.code, "INPUT_TOO_LARGE")
            self.assertFalse(output.exists())
            cases.write_bytes(compact(marked_library))
            too_many_cases = {"schema_version": 1, "design_input_sha256": self.library["design_input_sha256"],
                              "cases": [{"id": "CASE-%05d" % index, "title": "x", "preconditions": "x",
                                         "steps": ["x"], "expected": "x", "scenarios": []} for index in range(10_001)], "gaps": []}
            with self.assertRaises(CaseLibraryProposalError) as case_limit:
                self.result(library=too_many_cases)
            self.assertEqual(case_limit.exception.code, "CASE_LIMIT_EXCEEDED")
            too_many_gaps = {"schema_version": 1, "design_input_sha256": self.library["design_input_sha256"], "cases": [],
                             "gaps": [{"candidate_id": self.before_design["candidates"][0]["id"], "reason_code": "OTHER"}] * 50_001}
            with self.assertRaises(CaseLibraryProposalError) as row_limit:
                self.result(library=too_many_gaps)
            self.assertEqual(row_limit.exception.code, "ROW_LIMIT_EXCEEDED")
            over_budget = copy.deepcopy(self.before)
            decision = next(item for item in over_budget["design_models"]["models"] if item["id"] == "M-DEC")["spec"]
            decision["conditions"] = [{"id": "left", "values": list(range(101))}, {"id": "right", "values": list(range(100))}]
            decision["rules"] = []
            with self.assertRaises(CaseLibraryProposalError) as candidate_limit:
                self.result(after=over_budget)
            self.assertEqual(candidate_limit.exception.code, "CANDIDATE_LIMIT_EXCEEDED")
            with patch("qa_master.case_library_proposal._cc._write_exclusive", side_effect=RuntimeError("fixture")):
                with self.assertRaises(CaseLibraryProposalError) as io_error:
                    write_method_case_library_proposal(before, after, cases, output)
            self.assertEqual(io_error.exception.code, "OUTPUT_IO_ERROR")
            self.assertFalse(output.exists())
            marker_error = "SOURCE_RUNTIME_MARKER_5f56e65d"
            with patch("qa_master.case_library_proposal._cc._source", side_effect=RuntimeError(marker_error)):
                with self.assertRaises(CaseLibraryProposalError) as source_error:
                    write_method_case_library_proposal(before, after, cases, output)
            self.assertEqual(source_error.exception.code, "OUTPUT_IO_ERROR")
            self.assertNotIn(marker_error, str(source_error.exception))
            first_written, second_written = root / "first-written.json", root / "second-written.json"
            write_method_case_library_proposal(before, after, cases, first_written)
            write_method_case_library_proposal(before, after, cases, second_written)
            self.assertEqual(first_written.read_bytes(), second_written.read_bytes())
            protected, link = root / "protected.json", root / "linked-output.json"
            protected.write_bytes(b"PROTECTED")
            try:
                os.symlink(protected, link)
            except (OSError, NotImplementedError):
                pass
            else:
                with self.assertRaises(CaseLibraryProposalError) as linked:
                    write_method_case_library_proposal(before, after, cases, link)
                self.assertEqual(linked.exception.code, "OUTPUT_EXISTS")
                self.assertEqual(protected.read_bytes(), b"PROTECTED")
                linked_input = root / "linked-before.json"
                os.symlink(before, linked_input)
                with self.assertRaises(CaseLibraryProposalError) as input_linked:
                    write_method_case_library_proposal(linked_input, after, cases, root / "linked-input-output.json")
                self.assertEqual(input_linked.exception.code, "LINK_PATH_REJECTED")
            if os.name == "nt":
                junction_target, junction = root / "junction-target", root / "junction"
                junction_target.mkdir()
                created = subprocess.run(["cmd", "/d", "/c", "mklink", "/J", str(junction), str(junction_target)],
                                         capture_output=True, text=True, encoding="utf-8", errors="replace")
                if created.returncode == 0:
                    try:
                        with self.assertRaises(CaseLibraryProposalError) as reparse:
                            write_method_case_library_proposal(before, after, cases, junction / "proposal.json")
                        self.assertEqual(reparse.exception.code, "LINK_PATH_REJECTED")
                        self.assertFalse((junction_target / "proposal.json").exists())
                    finally:
                        os.rmdir(junction)
            # Source-level CLI exercise belongs to the checkout.  `-I -m` is
            # intentionally reserved for the post-freeze installed consumer fixture.
            cmd = [sys.executable, "-m", "qa_master", "propose-method-case-library", "--before", str(before),
                   "--after", str(after), "--cases", str(cases), "--output", str(output)]
            source = Path(__file__).resolve().parents[1]
            completed = subprocess.run(cmd, cwd=source, capture_output=True, text=True, encoding="utf-8", errors="replace")
            self.assertEqual(completed.returncode, 0, completed.stderr + completed.stdout)
            stdout = json.loads(completed.stdout); self.assertEqual(set(stdout), {"status", "execution", "application_state", "proposed_case_count", "held_case_count", "missing_vector_count", "output"})
            self.assertNotIn(marker, completed.stdout + completed.stderr)
            self.assertIn(marker, output.read_text(encoding="utf-8")); self.assertTrue(output.read_bytes().endswith(b"\n"))
            dup = subprocess.run([*cmd, "--before", str(before)], cwd=source, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(dup.returncode, 2)
            self.assertNotIn(marker, dup.stdout + dup.stderr)

    def test_tc_prop_011_output_limit_no_state_or_apply_and_installed_consumer(self):
        large = copy.deepcopy(self.library)
        large["cases"][0]["title"] = "x" * 2_700_000
        self.assertLess(len(compact(large)), 5 * 1024 * 1024)
        with self.assertRaises(CaseLibraryProposalError) as oversized:
            self.result(library=large)
        self.assertEqual(oversized.exception.code, "OUTPUT_TOO_LARGE")
        frozen_sha = os.environ.get("QA_MASTER_PROPOSAL_FROZEN_SHA")
        if not frozen_sha:
            return  # Final archive/wheel consumer delivery is coordinator-freeze gated.
        repo = Path(__file__).resolve().parents[1]
        self.assertEqual(subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True,
                                        text=True, encoding="utf-8").stdout.strip(), frozen_sha)
        evidence_root = os.environ.get("QA_MASTER_PROPOSAL_EVIDENCE_DIR")
        attempt = None
        if evidence_root:
            attempt = Path(evidence_root).resolve() / ("installed-attempt-" + uuid4().hex)
            attempt.mkdir(parents=True, exist_ok=False)
            (attempt / "source-freeze.json").write_text(json.dumps({"source_freeze": frozen_sha}, sort_keys=True) + "\n", encoding="utf-8")
        with tempfile.TemporaryDirectory(prefix="p036-") as directory:
            root = Path(directory); consumer = root / "consumer"; consumer.mkdir()
            archive, source, wheels, venv = root / "source.zip", root / "source", root / "wheel", root / "venv"
            wheels.mkdir()
            sequence = 0
            def run(args, *, cwd=consumer):
                nonlocal sequence
                completed = subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                                           encoding="utf-8", errors="replace")
                if attempt is not None:
                    sequence += 1
                    (attempt / ("%02d-command.json" % sequence)).write_text(json.dumps({
                        "args": [str(arg) for arg in args], "cwd": str(cwd), "exit": completed.returncode,
                        "stdout": completed.stdout, "stderr": completed.stderr}, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
                self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
                return completed
            run(["git", "archive", "--format=zip", "--output", str(archive), frozen_sha], cwd=repo)
            with zipfile.ZipFile(archive) as zipped:
                zipped.extractall(source)
            source_py_files = len(list((source / "qa_master").rglob("*.py")))
            run([sys.executable, "-m", "pip", "wheel", str(source), "--no-deps", "--no-build-isolation", "--wheel-dir", str(wheels)])
            run([sys.executable, "-m", "venv", str(venv)])
            vpython = venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
            wheel = next(wheels.glob("*.whl"))
            run([str(vpython), "-m", "pip", "install", "--no-index", "--no-deps", str(wheel)])
            runtime = run([str(vpython), "-I", "-c",
                           "import pathlib,qa_master; p=pathlib.Path(qa_master.__file__).parent; print(p); print(len(list(p.rglob('*.py'))))"])
            runtime_path, runtime_count = runtime.stdout.splitlines()
            self.assertTrue(Path(runtime_path).is_relative_to(venv))
            self.assertGreater(int(runtime_count), 0)
            self.assertGreater(source_py_files, 0)
            before, after, cases, module_output = (consumer / name for name in ("before.json", "after.json", "cases.json", "module.json"))
            installed_after = copy.deepcopy(self.before)
            installed_after["design_models"]["source_refs"][0]["sha256"] = "c" * 64
            before.write_bytes(compact(self.before)); after.write_bytes(compact(installed_after)); cases.write_bytes(compact(self.library))
            run([str(vpython), "-I", "-m", "qa_master", "propose-method-case-library", "--before", str(before),
                 "--after", str(after), "--cases", str(cases), "--output", str(module_output)])
            skill = consumer / "skill"
            installed = run([str(vpython), "-I", "-m", "qa_master", "install-codex", "--target", str(skill)])
            helper_output = consumer / "helper.json"
            run([str(vpython), "-I", str(skill / "scripts" / "qa.py"), "propose-method-case-library", "--before", str(before),
                 "--after", str(after), "--cases", str(cases), "--output", str(helper_output)])
            self.assertEqual(module_output.read_bytes(), helper_output.read_bytes())
            audit = run([str(vpython), "-I", "-c",
                "import json,sys; from qa_master.case_conformance import audit_method_cases; "
                "from pathlib import Path; p=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8')); "
                "b=json.loads(Path(sys.argv[2]).read_text(encoding='utf-8')); "
                "r=audit_method_cases(b,p['proposed_case_library']); print(r['case_library_sha256']); print(r['summary']['states'])",
                str(module_output), str(after)])
            proposal = json.loads(module_output.read_text(encoding="utf-8"))
            self.assertEqual(audit.stdout.splitlines()[0], proposal["proposed_case_library_sha256"])
            self.assertTrue(any(item["decision"] == "REBIND_PROPOSED_REVIEW_REQUIRED" for item in proposal["case_decisions"]))
            if attempt is not None:
                installer = json.loads(installed.stdout)
                artifacts = {"archive": {"sha256": hashlib.sha256(archive.read_bytes()).hexdigest(), "bytes": archive.stat().st_size},
                    "wheel": {"sha256": hashlib.sha256(wheel.read_bytes()).hexdigest(), "bytes": wheel.stat().st_size},
                    "source_python_file_count": source_py_files, "runtime_python_file_count": int(runtime_count),
                    "installer_reported_file_count": installer["files"],
                    "module_output": {"sha256": hashlib.sha256(module_output.read_bytes()).hexdigest(), "bytes": module_output.stat().st_size},
                    "helper_output": {"sha256": hashlib.sha256(helper_output.read_bytes()).hexdigest(), "bytes": helper_output.stat().st_size},
                    "proposal_status": proposal["status"], "proposal_execution": proposal["execution"],
                    "proposal_application_state": proposal["application_state"], "post_audit_states": proposal["post_proposal_audit"]["summary"]["states"]}
                (attempt / "artifacts.json").write_text(json.dumps(artifacts, sort_keys=True, indent=2) + "\n", encoding="utf-8")
            self.assertFalse(hasattr(propose_method_case_library, "apply"))
