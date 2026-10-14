import tempfile, unittest
from pathlib import Path
from qa_master.core import Campaign,DIMENSIONS,save,load
class CoreTests(unittest.TestCase):
 def test_empty_prompts_for_input(self):
  self.assertEqual(Campaign('x').next_action('design')['state'],'NEEDS_INPUT')
 def test_gitlab_asks_for_requirements(self):
  c=Campaign('x');c.set_answer('gitlab','group/repo');self.assertIn('需求',c.next_action('design')['question'])
 def test_none_not_reasked(self):
  c=Campaign('x');c.set_answer('gitlab','group/repo');c.set_answer('requirements','没有');self.assertEqual(c.next_action('design')['state'],'READY')
 def test_no_code_design_possible(self):
  c=Campaign('x');c.set_answer('requirements','spec.md');self.assertEqual(c.next_action('design')['state'],'READY')
 def test_execution_approval_gate(self):
  c=Campaign('x');c.set_answer('requirements','spec.md');self.assertEqual(c.next_action('execution')['state'],'WAITING_APPROVAL')
 def test_wait_for_build(self):
  c=Campaign('x');c.set_answer('requirements','spec.md');c.approve('requirements','r1');c.approve('cases','c1');self.assertEqual(c.next_action('execution')['state'],'WAITING_FOR_BUILD')
 def test_execution_full_preflight(self):
  c=Campaign('x');c.set_answer('requirements','x');c.approve('requirements','r1');c.approve('cases','c1')
  for k in ['build','environment','jira_project','plan_name','cycle_name','bug_assignee']:c.set_answer(k,'test')
  self.assertEqual(c.next_action('execution')['state'],'WAITING_APPROVAL');c.approve('execution','run1');self.assertEqual(c.next_action('execution')['state'],'READY')
 def test_invalidation(self):
  c=Campaign('x');[c.approve(k,'v1') for k in ('requirements','cases','execution','report')];c.invalidate('code');self.assertEqual(set(c.approvals),{'requirements'})
 def test_limited_scope(self):
  c=Campaign('x');p=c.plan('只生成测试用例，不执行测试');self.assertIn('design',p['intent']);self.assertNotIn('execution',p['intent'])
 def test_full_pipeline(self):
  c=Campaign('x');p=c.plan('从头到尾完整测试');self.assertIn('execution',p['intent']);self.assertIn('report',p['intent'])
 def test_coverage_all(self):
  c=Campaign('x');entries={d:{'status':'COVERED','cases':['TC1']} for d in DIMENSIONS};self.assertTrue(c.coverage(entries)['pass'])
 def test_na_needs_reason(self):
  c=Campaign('x');entries={d:{'status':'N/A','reason':'not applicable'} for d in DIMENSIONS};entries['api']={'status':'N/A'};self.assertFalse(c.coverage(entries)['pass'])
 def test_serialization(self):
  c=Campaign('x');c.set_answer('requirements','没有')
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'state.json';save(c,p);self.assertEqual(load(p).status('requirements'),'CONFIRMED_NONE')
if __name__=='__main__':unittest.main()

class ExtendedTests(unittest.TestCase):
 def test_read_only_report(self):
  c=Campaign('x');self.assertNotIn('execution',c.plan('只写测试报告')['intent'])
 def test_no_run_explicit(self):
  c=Campaign('x');self.assertNotIn('execution',c.plan('只评审需求，不执行测试')['intent'])
 def test_web_only_discovery(self):
  c=Campaign('x');c.set_answer('web_url','https://example.test');self.assertEqual(c.next_action('design')['state'],'READY')
 def test_requires_environment(self):
  c=Campaign('x');c.set_answer('requirements','x');c.approve('requirements','r1');c.approve('cases','c1');c.set_answer('build','v1');self.assertEqual(c.next_action('execution')['state'],'WAITING_ENVIRONMENT')
 def test_unknown_approval_rejected(self):
  with self.assertRaises(ValueError):Campaign('x').approve('danger','x')
 def test_requirement_invalidation(self):
  c=Campaign('x');[c.approve(k,'v1') for k in ('requirements','cases','execution','report')];c.invalidate('requirements');self.assertEqual(c.approvals,{})
 def test_coverage_missing(self):
  self.assertFalse(Campaign('x').coverage({})['pass'])
 def test_refuse_missing_version(self):
  with self.assertRaises(ValueError):Campaign('x').approve('cases','')
