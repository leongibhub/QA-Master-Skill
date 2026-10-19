import unittest
from qa_master.intent import plan_task
class IntentTests(unittest.TestCase):
 def test_empty(self):
  with self.assertRaises(ValueError):plan_task('')
 def test_no_input(self):self.assertEqual(len(plan_task('帮我测试')['questions']),1)
 def test_requirements_only(self):
  r=plan_task('先评审需求，生成测试用例',{'requirements':'doc'})
  self.assertEqual(r['stages'],['review','design']);self.assertTrue(r['no_execution'])
 def test_negated_execution(self):self.assertNotIn('execution',plan_task('只生成用例，不执行测试')['stages'])
 def test_full_flow(self):
  r=plan_task('从头到尾完成完整质量闭环',{'requirements':'doc'})
  self.assertIn('execution',r['stages']);self.assertEqual(r['scope'],'full')
 def test_full_but_developing(self):
  r=plan_task('从头到尾做全流程，开发还没完成',{'requirements':'doc'})
  self.assertTrue(r['no_execution']);self.assertNotIn('execution',r['stages']);self.assertTrue(r['uncertainty'])
 def test_gitlab_question(self):self.assertIn('正式需求',plan_task('生成用例',{'gitlab':'repo'})['questions'][0])
 def test_gitlab_confirmed_none(self):self.assertEqual(plan_task('生成用例',{'gitlab':'repo','requirements_status':'CONFIRMED_NONE'})['questions'],[])
 def test_web_only(self):self.assertEqual(plan_task('整理需求',{'web_url':'https://example.test'})['questions'],[])
 def test_regression(self):self.assertEqual(plan_task('只做回归测试',{'requirements':'doc'})['stages'],['regression'])
 def test_report(self):self.assertEqual(plan_task('只生成测试报告',{'requirements':'doc'})['stages'],['report'])
 def test_no_external_write(self):self.assertTrue(plan_task('只生成用例，不导入SynapseRT')['no_external_writes'])
 def test_development(self):self.assertEqual(plan_task('开发中先写用例',{'requirements':'doc'})['phase'],'development')
 def test_normal_execution(self):self.assertIn('execution',plan_task('开始执行测试',{'requirements':'doc'})['stages'])
 def test_no_eager_expansion(self):self.assertNotIn('execution',plan_task('写测试用例',{'requirements':'doc'})['stages'])
 def test_test_plan(self):self.assertEqual(plan_task('只写测试计划',{'requirements':'doc'})['stages'],['test_plan'])
 def test_case_review(self):self.assertEqual(plan_task('只做用例评审',{'requirements':'doc'})['stages'],['case_review'])
 def test_bug_and_regression(self):self.assertEqual(plan_task('执行测试并提交bug然后回归',{'requirements':'doc'})['stages'],['execution','regression'])
 def test_combined_modules(self):self.assertEqual(plan_task('需求评审和测试计划和测试用例编写',{'requirements':'doc'})['stages'],['review','design','test_plan'])
