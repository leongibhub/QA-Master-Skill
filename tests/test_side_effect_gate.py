import unittest
from qa_master.workflow import Workflow
class SideEffectGateTests(unittest.TestCase):
 def ready_plan(self):
  w=Workflow('project')
  w.request(['test_plan'])
  w.answer('source','spec')
  w.complete('requirements','req')
  w.complete('review','review')
  w.approve('requirements','r1','project')
  w.complete('baseline','baseline')
  w.complete('design','cases')
  w.approve('cases','c1','project')
  w.complete('case_review','review-cases')
  for k in ('jira_project','plan_name','cycle_name'):w.answer(k,k)
  w.approve('test_plan','old','project')
  return w
 def test_legacy_completion_denied(self):
  w=self.ready_plan()
  with self.assertRaises(PermissionError):w.complete('test_plan','created')
 def test_legacy_approval_denied_by_exact(self):
  w=self.ready_plan()
  self.assertEqual(w.evaluate_exact('test_plan',{'test_plan':{'cases':['A']}},{'test_plan':'project'}),'WAITING_APPROVAL')
 def test_exact_completion(self):
  w=self.ready_plan()
  doc={'cases':['A']}
  w.approve_exact('test_plan','project',doc,'approver')
  w.complete_exact('test_plan','dry-run-result',{'test_plan':doc},{'test_plan':'project'})
  self.assertEqual(w.steps['test_plan'].status,'DONE')
 def test_modified_artifact_denied(self):
  w=self.ready_plan()
  w.approve_exact('test_plan','project',{'cases':['A']},'approver')
  with self.assertRaises(PermissionError):
   w.complete_exact('test_plan','result',{'test_plan':{'cases':['B']}},{'test_plan':'project'})
 def test_no_evidence_denied(self):
  w=self.ready_plan();doc={'cases':['A']}
  w.approve_exact('test_plan','project',doc,'approver')
  with self.assertRaises(ValueError):w.complete_exact('test_plan','',{'test_plan':doc},{'test_plan':'project'})
