import tempfile, unittest
from pathlib import Path
from qa_master.workflow import Workflow

class WorkflowTests(unittest.TestCase):
 def setup_workflow(self):
  w=Workflow('demo');w.request(['execution']);return w
 def test_dependencies(self):
  self.assertEqual(set(self.setup_workflow().steps),{'requirements','review','baseline','design','case_review','test_plan','execution'})
 def test_missing_input(self):self.assertEqual(self.setup_workflow().evaluate('requirements'),'WAITING_INPUT')
 def test_explicit_none(self):
  w=self.setup_workflow();w.answer('source','没有');self.assertEqual(w.evaluate('requirements'),'BLOCKED')
 def test_input_present(self):
  w=self.setup_workflow();w.answer('source','doc');self.assertEqual(w.evaluate('requirements'),'READY')
 def test_cannot_skip(self):
  with self.assertRaises(PermissionError):self.setup_workflow().complete('execution','run1')
 def test_no_evidence(self):
  w=self.setup_workflow();w.answer('source','doc')
  with self.assertRaises(ValueError):w.complete('requirements','')
 def test_approval_needed(self):
  w=self.setup_workflow();w.answer('source','doc');w.complete('requirements','req');w.complete('review','review')
  self.assertEqual(w.evaluate('baseline'),'WAITING_APPROVAL')
 def test_scope_needed(self):
  with self.assertRaises(ValueError):self.setup_workflow().approve('requirements','v1','')
 def test_unknown_approval(self):
  with self.assertRaises(ValueError):self.setup_workflow().approve('unknown','v1','demo')
 def test_side_effect_blocked(self):self.assertEqual(self.setup_workflow().evaluate('execution'),'PENDING')
 def test_full_preflight(self):
  w=self.setup_workflow();w.answer('source','doc');w.complete('requirements','req');w.complete('review','review')
  w.approve('requirements','r1','demo');w.complete('baseline','base')
  w.answer('plan_name','plan-val')
  self.assertEqual(w.evaluate('test_plan'),'WAITING_APPROVAL')
  w.approve('test_plan','p1','demo')
  self.assertEqual(w.evaluate('test_plan'),'READY')
  w.complete('test_plan','plan')
  w.complete('design','draft')
  w.approve('cases','c1','demo');w.complete('case_review','cases')
  for k in ('build_ref','environment','jira_project','cycle_name'):w.answer(k,k+'-val')
  self.assertEqual(w.evaluate('execution'),'WAITING_APPROVAL')
  w.approve('execution','sha1','demo-lab');self.assertEqual(w.evaluate('execution'),'READY')
 def test_downstream_invalidation(self):
  w=self.setup_workflow()
  for k in ('requirements','review','baseline','design','case_review'):w.steps[k].status='DONE'
  w.approve('cases','v1','demo');affected=w.invalidate('review')
  self.assertIn('execution',affected);self.assertNotIn('cases',w.approvals);self.assertEqual(w.steps['requirements'].status,'DONE')
 def test_save_load(self):
  w=self.setup_workflow();w.answer('source','没有')
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'w.json';w.save(p);self.assertEqual(Workflow.load(p).evaluate('requirements'),'BLOCKED')
 def test_stage_only(self):
  w=Workflow('demo');w.request(['design']);self.assertNotIn('execution',w.steps)
 def test_report_dependency(self):
  w=Workflow('demo');w.request(['report']);self.assertEqual(w.steps['report'].depends_on,['execution'])
