import tempfile,unittest
from pathlib import Path
from qa_master.approval import artifact_digest
from qa_master.workflow import VerifiedCompletionReceipt, Workflow

def synthetic_receipt_verifier(receipt,binding):
 # Test-only host fixture. It is not a production approval or authenticated receipt.
 if not (receipt=='synthetic-test-receipt' and binding['project']=='project' and
         binding['step']=='execution' and binding['result_ref']=='dry-run-result'):
  return None
 return VerifiedCompletionReceipt('fixture-dry-run','synthetic-test-host',
  '2026-10-14T00:00:00Z','2026-10-14T01:00:00Z',artifact_digest(binding),'dry-run-result')

class SideEffectGateTests(unittest.TestCase):
 def ready_execution(self):
  w=Workflow('project')
  w.request(['execution'])
  w.answer('source','spec')
  w.complete('requirements','req')
  w.complete('review','review')
  w.approve('requirements','r1','project')
  w.complete('baseline','baseline')
  w.answer('plan_name','plan')
  w.approve('test_plan','t1','project')
  w.complete('test_plan','plan')
  w.complete('design','cases')
  w.approve('cases','c1','project')
  w.complete('case_review','review-cases')
  for k in ('build_ref','environment','jira_project','cycle_name'):w.answer(k,k)
  w.approve('execution','old','project')
  return w
 def test_legacy_completion_denied(self):
  w=self.ready_execution()
  with self.assertRaises(PermissionError):w.complete('execution','executed')
 def test_legacy_approval_denied_by_exact(self):
  w=self.ready_execution()
  self.assertEqual(w.evaluate_exact('execution',{'execution':{'cases':['A']}},{'execution':'project'}),'WAITING_APPROVAL')
 def test_exact_completion(self):
  w=self.ready_execution()
  doc={'cases':['A']}
  w.approve_exact('execution','project',doc,'approver')
  w.complete_exact('execution','dry-run-result',{'execution':doc},{'execution':'project'},
                   receipt='synthetic-test-receipt',verifier=synthetic_receipt_verifier)
  self.assertEqual(w.steps['execution'].status,'DONE')
 def test_modified_artifact_denied(self):
  w=self.ready_execution()
  w.approve_exact('execution','project',{'cases':['A']},'approver')
  with self.assertRaises(PermissionError):
   w.complete_exact('execution','result',{'execution':{'cases':['B']}},{'execution':'project'})
 def test_completed_execution_becomes_stale_when_artifact_changes(self):
  w=self.ready_execution();doc={'cases':['A']}
  w.approve_exact('execution','project',doc,'approver')
  w.complete_exact('execution','dry-run-result',{'execution':doc},{'execution':'project'},
                   receipt='synthetic-test-receipt',verifier=synthetic_receipt_verifier)
  self.assertEqual(w.evaluate_exact('execution',{'execution':{'cases':['B']}},{'execution':'project'}),'STALE')
  self.assertEqual(w.steps['execution'].status,'PENDING')
  self.assertNotIn('execution',w.approvals)
 def test_no_evidence_denied(self):
  w=self.ready_execution();doc={'cases':['A']}
  w.approve_exact('execution','project',doc,'approver')
  with self.assertRaises(ValueError):w.complete_exact('execution','',{'execution':doc},{'execution':'project'})
 def test_boolean_verifier_result_is_denied(self):
  w=self.ready_execution();doc={'cases':['A']}
  w.approve_exact('execution','project',doc,'approver')
  with self.assertRaises(PermissionError):
   w.complete_exact('execution','dry-run-result',{'execution':doc},{'execution':'project'},
                    receipt='synthetic-test-receipt',verifier=lambda receipt,binding:True)
 def test_receipt_with_wrong_binding_hash_is_denied(self):
  w=self.ready_execution();doc={'cases':['A']}
  w.approve_exact('execution','project',doc,'approver')
  def wrong_hash(receipt,binding):
   return VerifiedCompletionReceipt('fixture-bad','synthetic-test-host','2026-10-14T00:00:00Z',
    '2026-10-14T01:00:00Z','0'*64,'dry-run-result')
  with self.assertRaises(PermissionError):
   w.complete_exact('execution','dry-run-result',{'execution':doc},{'execution':'project'},
                    receipt='synthetic-test-receipt',verifier=wrong_hash)
 def test_verified_receipt_survives_save_reload(self):
  w=self.ready_execution();doc={'cases':['A']}
  w.approve_exact('execution','project',doc,'approver')
  w.complete_exact('execution','dry-run-result',{'execution':doc},{'execution':'project'},
                   receipt='synthetic-test-receipt',verifier=synthetic_receipt_verifier)
  with tempfile.TemporaryDirectory() as directory:
   path=Path(directory)/'workflow.json';w.save(path);reloaded=Workflow.load(path)
   stored=reloaded.steps['execution'].execution_receipt
   self.assertEqual(stored['receipt_id'],'fixture-dry-run')
   self.assertEqual(stored['evidence_ref'],'dry-run-result')
   self.assertEqual(reloaded.evaluate_exact('execution',{'execution':doc},{'execution':'project'}),'DONE')
