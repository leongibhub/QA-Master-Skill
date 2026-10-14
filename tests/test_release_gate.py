import unittest
from qa_master.release_gate import assess_release
C=[{'id':'A'},{'id':'B'}]
R=[{'case_id':'A','status':'PASS','evidence':'artifact://a'}, {'case_id':'B','status':'PASS','evidence':'artifact://b'}]
class ReleaseGateTests(unittest.TestCase):
 def check(self,cases=C,runs=R,defects=(),approved=('A','B'),**kwargs):
  return assess_release(cases,runs,list(defects) if defects is not None else None,approved_case_ids=approved,**kwargs)
 def test_clean_requires_human(self):self.assertEqual(self.check().decision,'READY_FOR_HUMAN_REVIEW')
 def test_evidence_coverage(self):self.assertEqual(self.check().evidence_coverage,1.0)
 def test_no_cases_blocks(self):self.assertEqual(self.check(cases=[],runs=[]).decision,'BLOCKED')
 def test_missing_run(self):self.assertIn('NOT_RUN:B',self.check(runs=R[:1]).reasons)
 def test_missing_evidence(self):self.assertIn('MISSING_EVIDENCE:A',self.check(runs=[dict(R[0],evidence=''),R[1]]).reasons)
 def test_failed(self):self.assertIn('FAIL:B',self.check(runs=[R[0],dict(R[1],status='FAIL')]).reasons)
 def test_blocked(self):self.assertIn('BLOCKED:B',self.check(runs=[R[0],dict(R[1],status='BLOCKED')]).reasons)
 def test_running(self):self.assertIn('RUNNING:B',self.check(runs=[R[0],dict(R[1],status='RUNNING')]).reasons)
 def test_unknown_defects(self):self.assertIn('DEFECT_STATUS_UNKNOWN',self.check(defects=None).reasons)
 def test_open_defects(self):self.assertIn('OPEN_DEFECT:J-1',self.check(defects=[{'id':'J-1','status':'OPEN'}]).reasons)
 def test_approved_cases(self):self.assertIn('CASE_NOT_APPROVED:B',self.check(approved=('A',)).reasons)
 def test_skipped_needs_waiver(self):self.assertIn('UNAPPROVED_SKIP:B',self.check(runs=[R[0],dict(R[1],status='SKIPPED')]).reasons)
 def test_waiver(self):
  w={'B':{'reason':'not applicable','approved_by':'lead','scope':'v1'}}
  self.assertEqual(self.check(runs=[R[0],dict(R[1],status='SKIPPED')],waivers=w).decision,'READY_FOR_HUMAN_REVIEW')
 def test_duplicate_run(self):
  with self.assertRaises(ValueError):self.check(runs=R+[R[0]])
 def test_orphan_run(self):
  with self.assertRaises(ValueError):self.check(runs=R+[{'case_id':'C','status':'PASS'}])
 def test_duplicate_case(self):
  with self.assertRaises(ValueError):self.check(cases=C+C)
 def test_bad_status(self):
  with self.assertRaises(ValueError):self.check(runs=[dict(R[0],status='NONSENSE'),R[1]])
 def test_cannot_auto_authorize(self):self.assertTrue(self.check().approval_required)
 def test_all_skipped_cannot_release(self):
  skipped=[dict(x,status='SKIPPED') for x in R]
  waivers={x['case_id']:{'reason':'deferred','approved_by':'lead','scope':'v1'} for x in skipped}
  self.assertIn('NO_EVIDENCED_PASS',self.check(runs=skipped,waivers=waivers).reasons)
 def test_none_passed_cannot_release(self):
  self.assertIn('NO_EVIDENCED_PASS',self.check(runs=[dict(R[0],status='FAIL'),dict(R[1],status='BLOCKED')]).reasons)
