"""Independent black-box tests for CR-034 / TASK-140.

This corpus deliberately owns its fixtures and does not import the developer
test module.  It exercises the public Python and CLI boundaries only.
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
import zipfile

from qa_master.design_methods import design_methods
from qa_master.method_impact import MethodImpactError, analyze_method_impact, write_method_impact


def impact_bundle():
    """A small, independently maintained corpus using every supported method."""
    return {
        "requirements": [{"id": "REQ-IMPACT", "priority": "P1", "text": "declared finite inputs"}],
        "design_models": {
            "schema_version": 1,
            "source_refs": [
                {"id": "SRC-REQ", "kind": "requirement", "locator": "facts/requirements"},
                {"id": "SRC-RULE", "kind": "model", "locator": "facts/rules"},
                {"id": "SRC-STATE", "kind": "model", "locator": "facts/states"},
                {"id": "SRC-EFFECT", "kind": "effect", "locator": "facts/effects"},
            ],
            "oracle_refs": [
                {"id": "OR-VALID", "kind": "valid", "locator": "oracle/valid"},
                {"id": "OR-INVALID", "kind": "invalid", "locator": "oracle/invalid"},
                {"id": "OR-OUT", "kind": "outcome", "locator": "oracle/outcome"},
                {"id": "OR-TRANS", "kind": "transition", "locator": "oracle/transition"},
                {"id": "OR-DENY", "kind": "denial", "locator": "oracle/deny"},
            ],
            "models": [
                {"id": "M-BOUND", "method": "boundary", "title": "Amount", "dimension": "functional",
                 "requirement_ids": ["REQ-IMPACT"], "source_refs": ["SRC-REQ"], "spec": {
                     "numeric_type": "decimal", "precision": 4, "scale": 1, "origin": "0", "step": "0.1",
                     "lower": {"value": "0", "inclusive": True},
                     "upper": {"value": "0.2", "inclusive": True},
                     "oracle_by_class": {"IN_DOMAIN": "OR-VALID", "LOWER_INVALID": "OR-INVALID",
                                           "UPPER_INVALID": "OR-INVALID", "BOTH_INVALID": "OR-INVALID"},
                 }},
                {"id": "M-DEC", "method": "decision_table", "title": "Typed choice", "dimension": "functional",
                 "requirement_ids": ["REQ-IMPACT"], "source_refs": ["SRC-REQ", "SRC-RULE"], "spec": {
                     "conditions": [{"id": "typed", "values": [True, 1]}], "constraints": [],
                     "rules": [
                         {"id": "R-BOOL", "when": {"typed": True}, "outcome_id": "bool",
                          "source_refs": ["SRC-RULE"], "oracle_ref": "OR-OUT"},
                         {"id": "R-INT", "when": {"typed": 1}, "outcome_id": "integer",
                          "source_refs": ["SRC-RULE"], "oracle_ref": "OR-OUT"},
                     ],
                 }},
                {"id": "M-STATE", "method": "state_transition", "title": "Submit", "dimension": "functional",
                 "requirement_ids": ["REQ-IMPACT"], "source_refs": ["SRC-REQ", "SRC-STATE"], "spec": {
                     "states": [{"id": "draft", "terminal": False, "source_refs": ["SRC-STATE"]},
                                {"id": "done", "terminal": True, "source_refs": ["SRC-STATE"]}],
                     "initial_state": "draft", "triggers": ["submit"],
                     "transitions": [{"id": "T-SUBMIT", "validity": "valid", "from_state": "draft",
                                      "to_state": "done", "trigger": "submit", "guard_refs": [],
                                      "effect_refs": ["SRC-EFFECT"], "source_refs": ["SRC-STATE"],
                                      "oracle_ref": "OR-TRANS"}],
                     "closed_world": True, "closed_world_deny_oracle_ref": "OR-DENY",
                 }},
                {"id": "M-PAIR", "method": "pairwise", "title": "Pair", "dimension": "functional",
                 "requirement_ids": ["REQ-IMPACT"], "source_refs": ["SRC-REQ"], "spec": {
                     "parameters": [{"id": "colour", "values": ["blue", "red"]},
                                    {"id": "size", "values": [1, 2]}], "oracle_ref": "OR-OUT",
                 }},
                {"id": "M-COMB", "method": "combinatorial", "title": "Combination", "dimension": "functional",
                 "requirement_ids": ["REQ-IMPACT"], "source_refs": ["SRC-REQ"], "spec": {
                     "parameters": [{"id": "channel", "values": ["api", "web"]},
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


def case_library(bundle, rows=None, *, gaps=(), extra_cases=()):
    candidates = design_methods(bundle)["candidates"]
    rows = [scenario(candidate) for candidate in candidates] if rows is None else copy.deepcopy(rows)
    return {
        "schema_version": 1,
        "design_input_sha256": design_methods(bundle)["input_sha256"],
        "cases": [{"id": "CASE-IMPACT", "title": "Finite scenarios", "preconditions": "review ready",
                   "steps": ["perform declared scenario"], "expected": "observe declared oracle", "scenarios": rows},
                  *copy.deepcopy(list(extra_cases))],
        "gaps": copy.deepcopy(list(gaps)),
    }


class MethodImpactIndependentTests(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.before = impact_bundle()
        self.before_design = design_methods(self.before)
        self.library = case_library(self.before)

    def report(self, after=None, library=None):
        return analyze_method_impact(self.before, after or self.before, library or self.library)

    def model(self, bundle, model_id):
        return next(model for model in bundle["design_models"]["models"] if model["id"] == model_id)

    def test_tc_impact_001_unchanged_all_five_methods_keep_explicit_vectors(self):
        report = self.report()
        self.assertEqual(report["status"], "DRAFT_UNAPPROVED")
        self.assertEqual(report["execution"], "NOT_EXECUTED")
        self.assertEqual({candidate["method"] for candidate in self.before_design["candidates"]},
                         {"boundary", "decision_table", "state_transition", "pairwise", "combinatorial"})
        self.assertTrue(report["candidate_deltas"])
        self.assertTrue(all(delta["pair_state"] == "RETAINED_VECTOR" for delta in report["candidate_deltas"]))
        self.assertTrue(all(action["action"] == "NO_DECLARED_IMPACT" for action in report["case_row_actions"]))
        self.assertEqual(report["review_case_ids"], [])
        self.assertFalse(report["library_rebinding_required"])
        counts = report["summary"]["candidate_group_states"]
        self.assertEqual(sum(counts.values()), len(report["candidate_deltas"]))

    def test_tc_impact_002_source_descriptor_churn_changes_ids_without_false_add_remove(self):
        after = copy.deepcopy(self.before)
        after["design_models"]["source_refs"][0]["sha256"] = "a" * 64
        before_ids = {candidate["id"] for candidate in self.before_design["candidates"]}
        after_ids = {candidate["id"] for candidate in design_methods(after)["candidates"]}
        self.assertNotEqual(before_ids, after_ids)
        report = self.report(after)
        self.assertTrue(report["library_rebinding_required"])
        self.assertTrue(all(delta["pair_state"] == "RETAINED_VECTOR" for delta in report["candidate_deltas"]))
        self.assertFalse(any(delta["pair_state"] in {"ADDED", "REMOVED"} for delta in report["candidate_deltas"]))
        self.assertTrue(all("CANDIDATE_REBIND_REQUIRED" in delta["reason_codes"] for delta in report["candidate_deltas"]))
        self.assertTrue(all("SOURCE_DESCRIPTORS_CHANGED" in delta["reason_codes"] for delta in report["candidate_deltas"]))
        self.assertEqual(report["review_case_ids"], ["CASE-IMPACT"])
        self.assertTrue(all(action["action"] == "REVIEW_BINDING" for action in report["case_row_actions"]))

    def test_tc_impact_003_typed_boolean_integer_and_decimal_changes_are_not_coerced(self):
        after = copy.deepcopy(self.before)
        decision = self.model(after, "M-DEC")["spec"]
        decision["conditions"][0]["values"][0] = False
        decision["rules"][0]["when"]["typed"] = False
        boundary = self.model(after, "M-BOUND")["spec"]
        boundary["lower"]["value"] = "0.1"
        report = self.report(after)
        states = {delta["pair_state"] for delta in report["candidate_deltas"]}
        self.assertIn("ADDED", states)
        self.assertIn("REMOVED", states)
        self.assertTrue(any("FINITE_VECTOR_ADDED" in item["reason_codes"] for item in report["candidate_deltas"]))
        self.assertTrue(any("FINITE_VECTOR_REMOVED" in item["reason_codes"] for item in report["candidate_deltas"]))

    def test_tc_impact_004_oracle_requirement_and_source_context_changes_require_review(self):
        after = copy.deepcopy(self.before)
        after["requirements"][0]["text"] = "changed declared requirement context"
        next(item for item in after["design_models"]["oracle_refs"] if item["id"] == "OR-OUT")["locator"] = "oracle/changed"
        next(item for item in after["design_models"]["source_refs"] if item["id"] == "SRC-RULE")["locator"] = "facts/changed-rules"
        report = self.report(after)
        self.assertTrue(all(delta["pair_state"] == "RETAINED_VECTOR" for delta in report["candidate_deltas"]))
        reasons = {code for delta in report["candidate_deltas"] for code in delta["reason_codes"]}
        self.assertIn("REQUIREMENT_CONTEXT_CHANGED", reasons)
        self.assertIn("ORACLE_DESCRIPTORS_CHANGED", reasons)
        self.assertIn("SOURCE_DESCRIPTORS_CHANGED", reasons)
        self.assertIn("CASE-IMPACT", report["review_case_ids"])

    def test_tc_impact_005_model_rename_and_new_model_do_not_get_guessed_pairs(self):
        after = copy.deepcopy(self.before)
        self.model(after, "M-PAIR")["id"] = "M-PAIR-RENAMED"
        extra = copy.deepcopy(self.model(after, "M-COMB"))
        extra["id"] = "M-COMB-NEW"
        after["design_models"]["models"].append(extra)
        report = self.report(after)
        states = {delta["pair_state"] for delta in report["candidate_deltas"]}
        self.assertIn("REMOVED", states)
        self.assertIn("ADDED", states)
        renamed = [delta for delta in report["candidate_deltas"] if delta["model_id"] in {"M-PAIR", "M-PAIR-RENAMED"}]
        self.assertTrue(renamed)
        self.assertTrue(all(delta["pair_state"] != "RETAINED_VECTOR" for delta in renamed))
        self.assertTrue(report["new_candidate_ids"])

    def test_tc_impact_006_stale_and_nonconformant_baseline_remains_visible(self):
        stale = copy.deepcopy(self.library)
        stale["design_input_sha256"] = "0" * 64
        with self.assertRaises(MethodImpactError) as caught:
            self.report(library=stale)
        self.assertTrue(caught.exception.code)

        target = self.before_design["candidates"][0]
        nonconformant = case_library(
            self.before,
            [scenario(target), scenario(target)],
            extra_cases=[{"id": "CASE-ORPHAN", "title": "", "preconditions": "", "steps": [],
                          "expected": "", "scenarios": []}],
        )
        report = self.report(library=nonconformant)
        self.assertTrue(report["baseline_findings"])
        self.assertIn("CASE-IMPACT", report["review_case_ids"])
        self.assertIn("CASE-ORPHAN", report["review_case_ids"])
        self.assertTrue(any(action["action"] == "REVIEW_BASELINE" for action in report["case_row_actions"]))
        affected = {target["id"]}
        deltas = [item for item in report["candidate_deltas"] if affected & set(item["before_candidate_ids"])]
        self.assertEqual(len(deltas), 1)
        self.assertIn("BASELINE_NONCONFORMANT", deltas[0]["reason_codes"])

    def test_tc_impact_007_obligations_gaps_and_unmodeled_requirement_changes_are_followups(self):
        before = copy.deepcopy(self.before)
        # Keep regular rows in M-BOUND while making one finite boundary point an explicit obligation.
        self.model(before, "M-BOUND")["spec"]["oracle_by_class"].pop("LOWER_INVALID")
        before_design = design_methods(before)
        library = case_library(before, gaps=[{"candidate_id": "TC-MD-UNKNOWN", "reason_code": "OTHER"}])
        after = copy.deepcopy(before)
        next(item for item in after["design_models"]["source_refs"] if item["id"] == "SRC-REQ")["sha256"] = "b" * 64
        after["requirements"].append({"id": "REQ-<unknown>", "priority": "P2", "text": "not modeled"})
        report = analyze_method_impact(before, after, library)
        self.assertTrue(report["obligation_deltas"])
        self.assertTrue(any(item["state"] == "PRESENT_BOTH" for item in report["obligation_deltas"]))
        self.assertIn({"before_candidate_id": "TC-MD-UNKNOWN", "reason_code": "OTHER",
                       "after_candidate_ids": [], "action": "REVIEW_GAP"}, report["gap_followups"])
        self.assertIn({"code": "UNMODELED_REQUIREMENT_CHANGE", "requirement_ids": ["REQ-<unknown>"]},
                      report["unknowns"])
        self.assertGreater(before_design["summary"]["obligation_count"], 0)
        self.assertIn("CASE-IMPACT", report["review_case_ids"])
        bound_ids = {item["id"] for item in before_design["candidates"] if item["model_id"] == "M-BOUND"}
        bound_actions = [item for item in report["case_row_actions"] if item["before_candidate_id"] in bound_ids]
        self.assertTrue(bound_actions)
        self.assertTrue(all("UNRESOLVED_MODEL_OBLIGATION" in item["reason_codes"] for item in bound_actions))
        self.assertTrue(all("SOURCE_DESCRIPTORS_CHANGED" in item["reason_codes"] for item in bound_actions))

    def test_tc_impact_008_row_identity_reference_order_and_input_order_are_deterministic(self):
        first = copy.deepcopy(self.library)
        second = copy.deepcopy(first)
        second["cases"][0]["scenarios"].reverse()
        for row in second["cases"][0]["scenarios"]:
            row["requirement_ids"].reverse()
            row["source_ref_ids"].reverse()
            row["oracle_ref_ids"].reverse()
        first_report = self.report(library=first)
        second_report = self.report(library=second)
        self.assertEqual(first_report["case_library_sha256"], second_report["case_library_sha256"])
        self.assertEqual(first_report["case_row_actions"], second_report["case_row_actions"])
        self.assertEqual(first_report["summary"], second_report["summary"])

    def test_tc_impact_009_safe_file_boundary_cli_and_markdown_escaping(self):
        with tempfile.TemporaryDirectory(prefix="impact-independent-") as directory:
            root = Path(directory)
            before_path, after_path, cases_path = root / "before.json", root / "after.json", root / "cases.json"
            before_path.write_text(json.dumps(self.before), encoding="utf-8")
            after_path.write_text(json.dumps(self.before), encoding="utf-8")
            cases_path.write_text(json.dumps(self.library), encoding="utf-8")
            output = root / "existing.json"
            output.write_bytes(b"sentinel")
            with self.assertRaises(MethodImpactError):
                write_method_impact(before_path, after_path, cases_path, output)
            self.assertEqual(output.read_bytes(), b"sentinel")

            for payload in (b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":' + b"[" * 33 + b"]" * 33 + b"}"):
                before_path.write_bytes(payload)
                new_output = root / ("bad-" + str(len(payload)) + ".json")
                with self.assertRaises(MethodImpactError) as caught:
                    write_method_impact(before_path, after_path, cases_path, new_output)
                self.assertTrue(caught.exception.code)
                self.assertFalse(new_output.exists())
            before_path.write_bytes(b'{"x":1,"x":2}')
            with self.assertRaises(MethodImpactError) as writer_error:
                write_method_impact(before_path, after_path, cases_path, root / "writer-rejected.json")
            self.assertEqual(writer_error.exception.code, "DUPLICATE_JSON_KEY")
            with self.assertRaises(MethodImpactError) as format_error:
                write_method_impact(before_path, after_path, cases_path, root / "format-rejected.json", format="yaml")
            self.assertEqual(format_error.exception.code, "INVALID_FORMAT")
            before_path.write_text(json.dumps(self.before), encoding="utf-8")

            hostile = copy.deepcopy(self.before)
            hostile_id = "REQ-`quote`\r\n[link](x)<script>&"
            hostile["requirements"].append({"id": hostile_id, "priority": "P2", "text": "unmodeled"})
            after_path.write_text(json.dumps(hostile), encoding="utf-8")
            markdown = root / "impact.md"
            report = write_method_impact(before_path, after_path, cases_path, markdown, format="markdown")
            content = markdown.read_text(encoding="utf-8")
            self.assertEqual(report["execution"], "NOT_EXECUTED")
            self.assertIn("&lt;script&gt;&amp;", content)
            self.assertNotIn("<script>", content)
            self.assertNotIn("\r", content)
            self.assertNotIn("\n[link](x)", content)
            self.assertIn("\\`quote\\`", content)

            original_before, original_after, original_library = copy.deepcopy(self.before), copy.deepcopy(hostile), copy.deepcopy(self.library)
            analyze_method_impact(self.before, hostile, self.library)
            self.assertEqual(self.before, original_before)
            self.assertEqual(hostile, original_after)
            self.assertEqual(self.library, original_library)

            duplicate = subprocess.run([sys.executable, "-m", "qa_master", "impact-method-cases",
                                        "--before", str(before_path), "--before", str(before_path),
                                        "--after", str(after_path), "--cases", str(cases_path),
                                        "--output", str(root / "cli.json")],
                                       capture_output=True, text=True, encoding="utf-8", errors="replace")
            self.assertEqual(duplicate.returncode, 2)
            before_path.write_bytes(b'{"x":1,"x":2}')
            cli_rejected = subprocess.run([sys.executable, "-m", "qa_master", "impact-method-cases",
                                            "--before", str(before_path), "--after", str(after_path),
                                            "--cases", str(cases_path), "--output", str(root / "cli-rejected.json")],
                                           capture_output=True, text=True, encoding="utf-8", errors="replace")
            self.assertEqual(cli_rejected.returncode, 2)
            self.assertEqual(json.loads(cli_rejected.stdout), {"status": "REJECTED", "error": "DUPLICATE_JSON_KEY"})

    @unittest.skipUnless(os.name == "nt", "native Windows junction semantics only")
    def test_tc_impact_009a_windows_junction_ancestor_rejected_without_touching_target(self):
        with tempfile.TemporaryDirectory(prefix="impact-junction-") as directory:
            root = Path(directory)
            target, junction = root / "target", root / "junction"
            target.mkdir()
            created = subprocess.run(["cmd", "/d", "/c", "mklink", "/J", str(junction), str(target)],
                                     capture_output=True, text=True, encoding="utf-8", errors="replace")
            self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
            try:
                for name, payload in (("before.json", self.before), ("after.json", self.before),
                                      ("cases.json", self.library)):
                    (junction / name).write_text(json.dumps(payload), encoding="utf-8")
                with self.assertRaises(MethodImpactError):
                    write_method_impact(junction / "before.json", junction / "after.json", junction / "cases.json",
                                        root / "impact.json")
                protected = target / "impact.json"
                protected.write_bytes(b"protected")
                root_before, root_after, root_cases = root / "before.json", root / "after.json", root / "cases.json"
                root_before.write_text(json.dumps(self.before), encoding="utf-8")
                root_after.write_text(json.dumps(self.before), encoding="utf-8")
                root_cases.write_text(json.dumps(self.library), encoding="utf-8")
                with self.assertRaises(MethodImpactError):
                    write_method_impact(root_before, root_after, root_cases, junction / "impact.json")
                self.assertEqual(protected.read_bytes(), b"protected")
            finally:
                if junction.exists():
                    os.rmdir(junction)

    def test_tc_impact_009b_symbolic_link_input_is_rejected_when_test_account_allows_links(self):
        with tempfile.TemporaryDirectory(prefix="impact-symlink-") as directory:
            root = Path(directory)
            before, after, cases = root / "before.json", root / "after.json", root / "cases.json"
            before.write_text(json.dumps(self.before), encoding="utf-8")
            after.write_text(json.dumps(self.before), encoding="utf-8")
            cases.write_text(json.dumps(self.library), encoding="utf-8")
            linked = root / "linked-before.json"
            try:
                os.symlink(before, linked)
            except (OSError, NotImplementedError):
                self.skipTest("symbolic links are unavailable to this test account")
            with self.assertRaises(MethodImpactError):
                write_method_impact(linked, after, cases, root / "impact.json")
            self.assertFalse((root / "impact.json").exists())

    def test_tc_impact_010_clean_archive_wheel_module_and_installed_helper(self):
        """One frozen consumer run; execute only after root has committed the implementation."""
        with tempfile.TemporaryDirectory(prefix="impact-wheel-") as directory:
            root = Path(directory)
            repo = Path(__file__).resolve().parents[1]
            archive, source, wheel_dir, venv_dir, consumer = (root / "source.zip", root / "source", root / "wheel",
                                                               root / "venv", root / "consumer")
            wheel_dir.mkdir(); consumer.mkdir()
            evidence_variable = os.environ.get("QA_MASTER_IMPACT_EVIDENCE_DIR")
            evidence = Path(evidence_variable) if evidence_variable else None
            metadata = {"test_case": "TC-IMPACT-010", "status": "IN_PROGRESS", "commands": {}}
            if evidence:
                evidence.mkdir(parents=True, exist_ok=True)

            def persist():
                if evidence:
                    (evidence / "delivery-metadata.json").write_text(
                        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

            def invoke(label, command, *, cwd):
                completed = subprocess.run(command, cwd=cwd, capture_output=True)
                stdout = (completed.stdout or b"").decode("utf-8", "replace")
                stderr = (completed.stderr or b"").decode("utf-8", "replace")
                metadata["commands"][label] = {"returncode": completed.returncode, "stdout": stdout, "stderr": stderr}
                persist()
                return subprocess.CompletedProcess(command, completed.returncode, stdout, stderr)

            frozen = invoke("source_freeze", ["git", "rev-parse", "HEAD"], cwd=repo)
            self.assertEqual(frozen.returncode, 0, frozen.stdout + frozen.stderr)
            metadata["source_freeze_sha"] = frozen.stdout.strip()
            persist()
            archived = invoke("archive", ["git", "archive", "--format=zip", "--output", str(archive), "HEAD"], cwd=repo)
            self.assertEqual(archived.returncode, 0, archived.stdout + archived.stderr)
            with zipfile.ZipFile(archive) as frozen:
                frozen.extractall(source)
            build = invoke("wheel_build", [sys.executable, "-m", "pip", "wheel", str(source), "--no-deps", "--no-build-isolation",
                                             "-w", str(wheel_dir)], cwd=consumer)
            self.assertEqual(build.returncode, 0, build.stdout + build.stderr)
            create = invoke("venv_create", [sys.executable, "-m", "venv", str(venv_dir)], cwd=consumer)
            self.assertEqual(create.returncode, 0, create.stdout + create.stderr)
            vpython = venv_dir / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
            wheel = next(wheel_dir.glob("*.whl"))
            metadata["wheel_sha256"] = hashlib.sha256(wheel.read_bytes()).hexdigest()
            persist()
            install = invoke("wheel_install", [str(vpython), "-m", "pip", "install", "--no-index", "--no-deps", str(wheel)],
                             cwd=consumer)
            self.assertEqual(install.returncode, 0, install.stdout + install.stderr)
            skill = consumer / "skill"
            skill_install = invoke("skill_install", [str(vpython), "-I", "-m", "qa_master", "install-codex", "--target", str(skill)],
                                  cwd=consumer)
            self.assertEqual(skill_install.returncode, 0, skill_install.stdout + skill_install.stderr)
            before = skill / "examples" / "design-methods.json"
            after = skill / "examples" / "design-methods-after.json"
            cases = skill / "examples" / "method-cases.json"
            self.assertTrue(after.exists(), "installed impact example is missing")
            module_output, helper_output = consumer / "module.json", consumer / "helper.md"
            module = invoke("module_cli", [str(vpython), "-I", "-m", "qa_master", "impact-method-cases", "--before", str(before),
                                             "--after", str(after), "--cases", str(cases), "--output", str(module_output)], cwd=consumer)
            self.assertEqual(module.returncode, 0, module.stdout + module.stderr)
            helper = invoke("installed_helper", [str(vpython), "-I", str(skill / "scripts" / "qa.py"), "impact-method-cases",
                                                   "--before", str(before), "--after", str(after), "--cases", str(cases),
                                                   "--output", str(helper_output), "--format", "markdown"], cwd=consumer)
            self.assertEqual(helper.returncode, 0, helper.stdout + helper.stderr)
            self.assertTrue(module_output.exists())
            self.assertTrue(helper_output.exists())
            report = json.loads(module_output.read_text(encoding="utf-8"))
            metadata["report"] = {"status": report["status"], "execution": report["execution"],
                                  "review_case_count": report["summary"]["review_case_count"],
                                  "before_design_input_sha256": report["before_design_input_sha256"],
                                  "after_design_input_sha256": report["after_design_input_sha256"],
                                  "case_library_sha256": report["case_library_sha256"]}
            metadata["module_output_sha256"] = hashlib.sha256(module_output.read_bytes()).hexdigest()
            metadata["helper_output_sha256"] = hashlib.sha256(helper_output.read_bytes()).hexdigest()
            metadata["status"] = "PASS"
            persist()
