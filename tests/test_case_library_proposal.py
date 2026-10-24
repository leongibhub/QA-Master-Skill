"""Developer unit tests for CR-036 / TASK-148 case-library proposals."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from qa_master.design_methods import design_methods


EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "design-methods.json"


def _row(candidate):
    return {"candidate_id": candidate["id"], "method_data": copy.deepcopy(candidate["method_data"]),
            "requirement_ids": list(candidate["trace"]), "source_ref_ids": [item["id"] for item in candidate["source_refs"]],
            "oracle_ref_ids": [item["id"] for item in candidate["oracle_refs"]]}


def _library(bundle, *, gaps=None):
    return {"schema_version": 1, "design_input_sha256": design_methods(bundle)["input_sha256"], "cases": [
        {"id": "CASE-PROPOSAL", "title": "Authored prose", "preconditions": "ready", "steps": ["act"],
         "expected": "observe", "scenarios": [_row(item) for item in design_methods(bundle)["candidates"]]}], "gaps": gaps or []}


class CaseLibraryProposalTeachingTests(unittest.TestCase):
    def test_public_proposal_api_exists(self):
        from qa_master.case_library_proposal import propose_method_case_library

        self.assertTrue(callable(propose_method_case_library))


class CaseLibraryProposalTests(unittest.TestCase):
    def setUp(self):
        self.before = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        self.library = _library(self.before)

    def test_unchanged_library_is_a_non_applied_carry_proposal(self):
        from qa_master.case_library_proposal import propose_method_case_library

        report = propose_method_case_library(self.before, self.before, self.library)
        self.assertEqual((report["status"], report["execution"], report["application_state"]),
                         ("DRAFT_UNAPPROVED", "NOT_EXECUTED", "NOT_APPLIED"))
        self.assertEqual(report["case_decisions"][0]["decision"], "CARRY_PROPOSED")
        self.assertEqual(report["proposed_case_library_sha256"], report["post_proposal_audit"]["case_library_sha256"])

    def test_context_change_rebinds_and_preserves_prose(self):
        from qa_master.case_library_proposal import propose_method_case_library

        after = copy.deepcopy(self.before)
        after["design_models"]["source_refs"][0]["sha256"] = "a" * 64
        report = propose_method_case_library(self.before, after, self.library)
        self.assertEqual(report["case_decisions"][0]["decision"], "REBIND_PROPOSED_REVIEW_REQUIRED")
        self.assertEqual(report["proposed_case_library"]["cases"][0]["title"], "Authored prose")

    def test_gap_is_held_without_copying_its_business_reason(self):
        from qa_master.case_library_proposal import propose_method_case_library

        candidate = design_methods(self.before)["candidates"][0]
        report = propose_method_case_library(self.before, self.before, _library(self.before, gaps=[{"candidate_id": candidate["id"], "reason_code": "OTHER"}]))
        self.assertEqual(report["held_gaps"][0]["decision"], "HELD_GAP_REVIEW_REQUIRED")
        self.assertNotIn("OTHER", report["held_gaps"][0]["reason_codes"])

    def test_eight_held_gaps_keep_canonical_projection_order_not_digest_order(self):
        from qa_master.case_library_proposal import propose_method_case_library

        candidates = design_methods(self.before)["candidates"]
        gaps = ([{"candidate_id": candidates[1]["id"], "reason_code": code} for code in
                 ("OTHER", "SOURCE_MISSING", "ORACLE_MISSING", "SETUP_MISSING", "OBSERVABLE_MISSING", "CLEANUP_MISSING")] +
                [{"candidate_id": candidates[0]["id"], "reason_code": "OTHER"},
                 {"candidate_id": candidates[0]["id"], "reason_code": "SOURCE_MISSING"}])
        report = propose_method_case_library(self.before, self.before, _library(self.before, gaps=gaps))
        canonical = lambda item: json.dumps({"candidate_id": item["candidate_id"], "reason_code": item["reason_code"]},
                                            ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        expected = sorted(gaps, key=canonical)
        self.assertEqual([item["original_gap"] for item in report["held_gaps"]], expected)
        self.assertNotEqual([item["gap_sha256"] for item in report["held_gaps"]],
                            sorted(item["gap_sha256"] for item in report["held_gaps"]))

    def test_writer_uses_compact_json_and_never_overwrites(self):
        from qa_master.case_library_proposal import CaseLibraryProposalError, write_method_case_library_proposal

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); before, after, cases, output = (root / name for name in ("before.json", "after.json", "cases.json", "proposal.json"))
            before.write_text(json.dumps(self.before), encoding="utf-8"); after.write_text(json.dumps(self.before), encoding="utf-8")
            cases.write_text(json.dumps(self.library), encoding="utf-8")
            write_method_case_library_proposal(before, after, cases, output)
            self.assertTrue(output.read_bytes().endswith(b"\n"))
            with self.assertRaises(CaseLibraryProposalError) as caught:
                write_method_case_library_proposal(before, after, cases, output)
            self.assertEqual(caught.exception.code, "OUTPUT_EXISTS")

    def test_mixed_case_hold_carries_full_case_reason_to_matching_followups(self):
        from qa_master.case_library_proposal import propose_method_case_library

        after = copy.deepcopy(self.before)
        after["design_models"]["models"][0]["spec"]["upper"]["value"] = "101"
        report = propose_method_case_library(self.before, after, self.library)
        self.assertEqual(report["case_decisions"][0]["decision"], "HELD_REMOVAL")
        self.assertTrue(all("CASE_PARTIAL_REBIND_FORBIDDEN" in row["reason_codes"] for row in report["row_decisions"]))
        matched = [item for item in report["missing_vector_followups"] if "CASE_HELD" in item["reason_codes"]]
        self.assertTrue(matched)
        self.assertTrue(all("CASE_PARTIAL_REBIND_FORBIDDEN" in item["reason_codes"] for item in matched))

    def test_inconsistent_fresh_impact_action_rejects_instead_of_reclassifying(self):
        from qa_master.case_library_proposal import CaseLibraryProposalError, propose_method_case_library
        from qa_master.method_impact import analyze_method_impact

        inconsistent = analyze_method_impact(self.before, self.before, self.library)
        inconsistent["case_row_actions"][0]["after_candidate_id"] = None
        with patch("qa_master.case_library_proposal.analyze_method_impact", return_value=inconsistent):
            with self.assertRaises(CaseLibraryProposalError) as caught:
                propose_method_case_library(self.before, self.before, self.library)
        self.assertEqual(caught.exception.code, "PROPOSAL_INVARIANT_FAILED")

    def test_inconsistent_post_audit_candidate_set_rejects(self):
        from qa_master.case_conformance import audit_method_cases
        from qa_master.case_library_proposal import CaseLibraryProposalError, propose_method_case_library

        def forged_post(*args):
            report = audit_method_cases(*args)
            report["candidates"][0]["id"] = "FORGED"
            return report

        with patch("qa_master.case_library_proposal.audit_method_cases", side_effect=forged_post):
            with self.assertRaises(CaseLibraryProposalError) as caught:
                propose_method_case_library(self.before, self.before, self.library)
        self.assertEqual(caught.exception.code, "PROPOSAL_INVARIANT_FAILED")


if __name__ == "__main__":
    unittest.main()
