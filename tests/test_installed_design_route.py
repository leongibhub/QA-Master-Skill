import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from qa_master.campaign_cli import write_campaign
from qa_master.codex_skill import install_skill


class InstalledDesignRouteTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.target = self.root / "install" / ".agents" / "skills" / "qa-master"
        install_skill(self.target)
        self.work = self.root / "unrelated-working-directory"
        self.work.mkdir()

    def run_helper(self, *arguments):
        return subprocess.run(
            [sys.executable, "-I", str(self.target / "scripts" / "qa.py"), *arguments],
            cwd=self.work, text=True, capture_output=True, timeout=20,
        )

    def run_design(self, source, output, *before):
        return self.run_helper(*before, "design", "--input", str(source), "--output", str(output))

    def test_tc_imd_001_002_005_installed_route_is_self_contained_and_mapped(self):
        source = self.target / "examples" / "design-methods.json"
        output = self.work / "report.json"
        state = self.work / "must-not-exist.json"
        result = self.run_design(source, output, "--state", str(state))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(state.exists())
        self.assertNotIn("declared/example", result.stdout)
        summary = json.loads(result.stdout)
        self.assertEqual((summary["status"], summary["execution"]), ("DRAFT_UNAPPROVED", "NOT_EXECUTED"))
        report = json.loads(output.read_text(encoding="utf-8"))
        projection = report["installed_design"]
        self.assertEqual((projection["entry_point"], projection["state_access"]), ("scripts/qa.py design", "NONE"))
        self.assertEqual(projection["method_output"]["candidate_ids"],
                         sorted(item["id"] for item in report["method_design"]["candidates"]))
        self.assertEqual(projection["method_output"]["obligation_ids"],
                         sorted(item["id"] for item in report["method_design"]["obligations"]))
        guide = next(item for item in projection["guides"] if item["id"] == "functional-api-design")
        self.assertEqual(guide["locator"], "scripts/qa_master/skills/professional/functional-api.md")
        expected = hashlib.sha256((self.target / "scripts" / "qa_master" / "skills" / "professional" /
                                   guide["file"]).read_bytes()).hexdigest()
        self.assertEqual(guide["sha256"], expected)
        self.assertFalse(projection["method_output"]["usable_case_claim"])
        self.assertFalse(projection["method_output"]["executable_case_claim"])
        all_methods = Path(__file__).resolve().parents[1] / "examples" / "design-methods.json"
        all_methods_output = self.work / "all-methods.json"
        all_methods_result = self.run_design(all_methods, all_methods_output)
        self.assertEqual(all_methods_result.returncode, 0, all_methods_result.stderr)
        all_methods_report = json.loads(all_methods_output.read_text(encoding="utf-8"))
        self.assertEqual({item["method"] for item in all_methods_report["method_design"]["model_results"]},
                         {"boundary", "decision_table", "state_transition"})
        effect = next(item for item in all_methods_report["installed_design"]["source_mapping"]
                      if item["source_id"] == "SRC-EFFECT")
        self.assertEqual((effect["requirement_ids"], effect["model_ids"]),
                         (["REQ-EXAMPLE"], ["DM-ORDER"]))

    def test_tc_imd_003_004_missing_context_is_a_draft_gap_and_invalid_input_is_atomic(self):
        missing = self.work / "missing.json"
        missing.write_text(json.dumps({"project": "gaps", "requirements": [
            {"id": "REQ-GAP", "text": "review", "approved": False}
        ]}), encoding="utf-8")
        output = self.work / "report.json"
        result = self.run_design(missing, output)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(output.read_text(encoding="utf-8"))
        self.assertFalse(report["formal_baseline_approved"])
        self.assertEqual(report["test_cases"], [])
        self.assertEqual({item["code"] for item in report["installed_design"]["gaps"]}, {
            "METHOD_MODELS_NOT_SUPPLIED", "GUIDE_DIMENSION_NOT_SUPPLIED", "SOURCE_NOT_SUPPLIED"})
        empty = self.work / "empty.json"
        empty.write_text(json.dumps({"project": "empty", "requirements": [
            {"id": "REQ-EMPTY", "text": "review", "approved": False}
        ], "design_models": {"schema_version": 1, "source_refs": [], "oracle_refs": [], "models": []}}),
                         encoding="utf-8")
        empty_output = self.work / "empty-report.json"
        empty_result = self.run_design(empty, empty_output)
        self.assertEqual(empty_result.returncode, 0, empty_result.stderr)
        self.assertEqual({item["code"] for item in json.loads(empty_output.read_text(encoding="utf-8"))["installed_design"]["gaps"]}, {
            "METHOD_MODELS_EMPTY", "GUIDE_DIMENSION_NOT_SUPPLIED", "SOURCE_NOT_SUPPLIED"})
        output.write_bytes(b"PRESERVE")
        invalid = self.work / "invalid.json"
        invalid.write_bytes(b'{"project":"x","project":"y"}')
        rejected = self.run_design(invalid, output)
        self.assertEqual(rejected.returncode, 2)
        self.assertEqual(json.loads(rejected.stdout)["error"], "DUPLICATE_JSON_KEY")
        self.assertEqual(output.read_bytes(), b"PRESERVE")
        duplicate = self.run_helper("design", "--input", str(missing), "--input", str(missing),
                                    "--output", str(output))
        self.assertEqual(duplicate.returncode, 2)
        self.assertEqual(output.read_bytes(), b"PRESERVE")
        abbreviated = self.run_helper("design", "--in", str(missing), "--output", str(output))
        self.assertEqual(abbreviated.returncode, 2)
        self.assertEqual(output.read_bytes(), b"PRESERVE")
        global_abbreviated = self.run_helper("--sta", str(self.work / "state.json"), "design",
                                             "--input", str(missing), "--output", str(output))
        self.assertEqual(global_abbreviated.returncode, 2)
        self.assertEqual(output.read_bytes(), b"PRESERVE")
        self.assertFalse(list(self.work.glob(".qa-master-*")))

    def test_tc_imd_009_direct_campaign_mode_remains_unchanged(self):
        source = self.target / "examples" / "design-methods.json"
        direct = self.work / "direct.json"
        installed = self.work / "installed.json"
        direct_report = write_campaign(source, direct)
        result = self.run_design(source, installed)
        self.assertEqual(result.returncode, 0, result.stderr)
        installed_report = json.loads(installed.read_text(encoding="utf-8"))
        self.assertNotIn("installed_design", direct_report)
        self.assertEqual(direct_report, {key: value for key, value in installed_report.items()
                                         if key != "installed_design"})


if __name__ == "__main__":
    unittest.main()
