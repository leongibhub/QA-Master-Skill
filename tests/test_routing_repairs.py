"""TASK-115/116: bounded intent grammar and actual catalog reachability."""
import tempfile
import unittest
from pathlib import Path
from qa_master.intent import plan_task
from qa_master.skill_registry import discover_vendor_skills, select_vendor_skills
from qa_master.application import CampaignApplicationService


class RoutingRepairTests(unittest.TestCase):
    def test_negative_stages_bilingual(self):
        for prompt, expected in [
            ('不提交bug，只生成测试报告', ['report']),
            ('不要提交缺陷，只评审用例', ['case_review']),
            ('不回归，只写测试报告', ['report']),
            ('do not submit bugs, only test report', ['report']),
            ('no regression, just test report', ['report']),
            ('do not run tests, only test cases', ['design']),
            ('never execute tests; test plan and test report', ['test_plan', 'report']),
        ]:
            with self.subTest(prompt=prompt):
                result = plan_task(prompt)
                self.assertEqual(result['stages'], expected)
                self.assertTrue(result['no_execution'])
                self.assertTrue(result['no_external_writes'])

    def test_combined_plan_and_cases(self):
        self.assertEqual(plan_task('编写测试计划和用例')['stages'], ['test_plan', 'design'])
        self.assertTrue(plan_task('编写测试计划和用例')['no_execution'])

    def test_execution_and_write_scopes_are_independent(self):
        for prompt in ('执行测试，不要提交缺陷', '运行测试但不提交bug', 'run tests, do not submit bugs'):
            result = plan_task(prompt)
            self.assertEqual(result['stages'], ['execution'])
            self.assertFalse(result['no_execution'])
            self.assertTrue(result['no_external_writes'])
        result = plan_task('执行测试并提交bug然后回归')
        self.assertEqual(result['stages'], ['execution', 'regression'])
        self.assertFalse(result['no_external_writes'])

    def test_full_and_specialist_end_to_end_are_distinct(self):
        result = plan_task('全流程，不执行测试')
        self.assertNotIn('execution', result['stages'])
        self.assertNotIn('regression', result['stages'])
        self.assertTrue(result['no_execution'])
        result = plan_task('full workflow, no regression')
        self.assertIn('execution', result['stages'])
        self.assertNotIn('regression', result['stages'])
        for prompt in ('Playwright end to end testing', 'end-to-end-testing'):
            self.assertNotIn('execution', plan_task(prompt)['stages'])
            self.assertEqual(plan_task(prompt)['scope'], 'limited')

    def test_catalog_canonical_names_reachable(self):
        # Real package catalog, not an invented stub: each canonical leaf routes.
        for name in {item['name'] for item in discover_vendor_skills()['skills']}:
            with self.subTest(name=name):
                selected = select_vendor_skills(prompt='Use ' + name)['selected']
                self.assertEqual({item['name'] for item in selected}, {name})
                self.assertEqual({item['language'] for item in selected}, {'en'})

    def test_curated_specialist_terms_and_locale(self):
        for prompt, names, lang in [
            ('property-based testing', {'property-based-testing'}, 'en'),
            ('属性测试', {'property-based-testing'}, 'zh'),
            ('chaos engineering', {'chaos-testing'}, 'en'),
            ('混沌测试', {'chaos-testing'}, 'zh'),
            ('RAG testing', {'rag-quality-testing', 'rag-retrieval-testing'}, 'en'),
            ('用Playwright设计测试', {'ui-test-playwright'}, 'zh'),
        ]:
            result = select_vendor_skills(prompt=prompt)
            with self.subTest(prompt=prompt):
                self.assertEqual({item['name'] for item in result['selected']}, names)
                self.assertEqual({item['language'] for item in result['selected']}, {lang})
                self.assertEqual(result['execution'], 'NOT_EXECUTED')
        self.assertIn('AMBIGUOUS_SPECIALIST_REQUEST', [g['code'] for g in select_vendor_skills(prompt='RAG testing')['gaps']])

    def test_denied_and_unknown_specialists_are_not_guessed(self):
        self.assertEqual(select_vendor_skills(prompt='do not use property-based-testing')['selected'], [])
        for prompt in ('不要使用Playwright', '不要使用 Playwright，只做 API 测试',
                       '不运行 RAG 测试，只写测试报告', 'do not use Playwright'):
            self.assertEqual(select_vendor_skills(prompt=prompt)['selected'], [])
            self.assertTrue(plan_task(prompt)['no_execution'])
        self.assertEqual({s['name'] for s in select_vendor_skills(prompt='piano property-based-testing')['selected']}, {'property-based-testing'})
        result = select_vendor_skills(names=['nonexistent-test-skill'])
        self.assertEqual(result['selected'], [])
        self.assertIn('REQUESTED_VENDOR_SKILL_UNAVAILABLE', [g['code'] for g in result['gaps']])

    def test_application_projects_specialist_and_preserves_scope(self):
        with tempfile.TemporaryDirectory() as folder:
            service = CampaignApplicationService.initialize(Path(folder) / 'state.json', 'routing')
            result = service.mutate('plan', prompt='只使用属性测试设计，不执行测试')
            self.assertTrue(result['no_execution'])
            self.assertIn('property-based-testing', {i['name'] for i in result['vendor_skills']['selected']})
            result = service.mutate('plan', prompt='执行测试')
            self.assertTrue(result['no_execution'])
            self.assertFalse(service.status()['execution_authorized'])


if __name__ == '__main__':
    unittest.main()
