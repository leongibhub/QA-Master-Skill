"""Independent CR-028 behavioral checks; no business-system execution."""
import itertools
import json
from pathlib import Path
import tempfile
import unittest

from qa_master.application import CampaignApplicationService
from qa_master.design_methods import design_methods
from qa_master.intent import plan_task
from qa_master.skill_registry import discover_vendor_skills, select_vendor_skills


class ContinuationIndependentTests(unittest.TestCase):
    def test_negative_scope_survives_persistence(self):
        scenarios = {
            "不提交bug，只生成测试报告": ["report"],
            "不要提交缺陷，只评审用例": ["case_review"],
            "不回归，只写测试报告": ["report"],
            "Do not run tests; only write test reports": ["report"],
            "不要运行测试，只写测试计划": ["test_plan"],
        }
        for prompt, stages in scenarios.items():
            with self.subTest(prompt=prompt), tempfile.TemporaryDirectory() as tmp:
                plan = plan_task(prompt)
                self.assertEqual(plan["stages"], stages)
                self.assertTrue(plan["no_execution"])
                service = CampaignApplicationService.initialize(Path(tmp) / "state.json", "independent")
                service.mutate("plan", prompt=prompt)
                saved = CampaignApplicationService.load(service.path).document["task_contract"]
                self.assertEqual(saved["stages"], stages)
                self.assertTrue(saved["no_execution"])
                self.assertTrue(saved["no_external_writes"])
                self.assertEqual(saved["capabilities"], {"execute": False, "external_write": False})

    def test_explicit_execution_remains_a_planning_request(self):
        plan = plan_task("执行测试并提交bug然后回归")
        self.assertEqual(plan["stages"], ["execution", "regression"])
        self.assertFalse(plan["no_execution"])

    def test_every_canonical_skill_is_reachable_in_both_languages(self):
        catalog = discover_vendor_skills()
        names = {item["name"] for item in catalog["skills"]}
        self.assertEqual(len(names), 165)
        self.assertEqual(catalog["count"], 330)
        self.assertEqual(catalog["gaps"], [])
        for name, language in itertools.product(sorted(names), ("en", "zh")):
            with self.subTest(name=name, language=language):
                selected = select_vendor_skills(prompt=name, language=language)
                self.assertIn((name, language), {(s["name"], s["language"]) for s in selected["selected"]})
                self.assertEqual(selected["execution"], "NOT_EXECUTED")
                self.assertEqual(selected["status"], "PLANNING_ONLY")

    def test_curated_and_ambiguous_requests_are_visible(self):
        for prompt, name in (("属性测试", "property-based-testing"),
                             ("混沌工程", "chaos-testing"),
                             ("Playwright end-to-end tests", "ui-test-playwright")):
            with self.subTest(prompt=prompt):
                result = select_vendor_skills(prompt=prompt)
                self.assertIn(name, {s["name"] for s in result["selected"]})
                self.assertTrue(plan_task(prompt)["no_execution"])
        result = select_vendor_skills(prompt="RAG testing")
        self.assertIn("AMBIGUOUS_SPECIALIST_REQUEST", {g["code"] for g in result["gaps"]})
        self.assertEqual(result["execution"], "NOT_EXECUTED")
        self.assertNotIn("chaos-testing", {s["name"] for s in select_vendor_skills(prompt="不要混沌测试，只评审用例")["selected"]})

    def test_coverage_counts_distinct_interactions_not_rows(self):
        parameters = [{"id": "browser", "values": ["a", "b", "c"]},
                      {"id": "role", "values": ["reader", "writer"]},
                      {"id": "locale", "values": ["en", "zh"]},
                      {"id": "mode", "values": ["online", "offline"]}]
        for strength, oracle in itertools.product((2, 3), ("O", None)):
            with self.subTest(strength=strength, oracle=oracle):
                bundle = {"project": "independent", "requirements": [{"id": "REQ-1", "priority": "P1"}],
                          "design_models": {"schema_version": 1,
                              "source_refs": [{"id": "S", "kind": "requirement", "locator": "docs/r"}],
                              "oracle_refs": [{"id": "O", "kind": "outcome", "locator": "docs/o"}],
                              "models": [{"id": "M", "method": "combinatorial", "title": "M", "dimension": "functional",
                                  "requirement_ids": ["REQ-1"], "source_refs": ["S"],
                                  "spec": {"parameters": parameters, "strength": strength, "oracle_ref": oracle}}]}}
                result = design_methods(bundle)
                required = set()
                for group in itertools.combinations(parameters, strength):
                    for values in itertools.product(*(p["values"] for p in group)):
                        required.add(tuple(sorted(zip((p["id"] for p in group), values))))
                observed = set()
                for case in result["candidates"]:
                    assignment = case["method_data"]["assignment"]
                    observed.update(tuple(sorted((k, assignment[k]) for k in group))
                                    for group in itertools.combinations(assignment, strength))
                    self.assertEqual(case["validation_action"], "NOT_EXECUTED")
                coverage = result["model_results"][0]["coverage"]
                self.assertEqual(coverage["denominator"], len(required))
                self.assertEqual(coverage["candidate_ready"], len(observed & required))
                if oracle:
                    self.assertEqual(observed, required)
                    self.assertEqual(coverage["oracle_missing"], 0)
                else:
                    self.assertEqual(result["candidates"], [])
                    self.assertEqual(coverage["oracle_missing"], len(required))


if __name__ == "__main__":
    unittest.main()
