import tempfile,unittest
from pathlib import Path
from qa_master.workflow import Workflow

class WorkflowExactApprovalTests(unittest.TestCase):
 def ready_baseline(self):
  w=Workflow('project-x');w.request(['baseline'])
  w.answer('source','spec-v1');w.complete('requirements','req.json')
  w.complete('review','review.json')
  return w
 def test_exact_approval(self):
  w=self.ready_baseline();artifact={'requirements':['R1']}
  w.approve_exact('requirements','project-x/release-a',artifact,'reviewer')
  self.assertEqual(w.evaluate_exact('baseline',{'requirements':artifact},{'requirements':'project-x/release-a'}),'READY')
  w.complete_exact('baseline','baseline.json',{'requirements':artifact},{'requirements':'project-x/release-a'})
  self.assertEqual(w.steps['baseline'].status,'DONE')
 def test_changed_document_blocks(self):
  w=self.ready_baseline();w.approve_exact('requirements','release-a',{'requirements':['R1']},'reviewer')
  self.assertEqual(w.evaluate_exact('baseline',{'requirements':{'requirements':['R2']}},{'requirements':'release-a'}),'WAITING_APPROVAL')
 def test_legacy_approval_fails_closed(self):
  w=self.ready_baseline();w.approve('requirements','v1','release-a')
  self.assertEqual(w.evaluate_exact('baseline',{'requirements':{'v':1}},{'requirements':'release-a'}),'WAITING_APPROVAL')
 def test_recovery_rechecks(self):
  w=self.ready_baseline();artifact={'requirements':['R1']}
  w.approve_exact('requirements','release-a',artifact,'reviewer')
  with tempfile.TemporaryDirectory() as d:
   path=Path(d)/'state.json';w.save(path);recovered=Workflow.load(path)
   self.assertEqual(recovered.evaluate_exact('baseline',{'requirements':artifact},{'requirements':'release-a'}),'READY')
   self.assertEqual(recovered.evaluate_exact('baseline',{'requirements':{'requirements':['R2']}},{'requirements':'release-a'}),'WAITING_APPROVAL')
 def test_denied_completion(self):
  w=self.ready_baseline();w.approve_exact('requirements','release-a',{'x':1},'reviewer')
  with self.assertRaises(PermissionError):w.complete_exact('baseline','ref',{'requirements':{'x':2}},{'requirements':'release-a'})
