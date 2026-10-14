import unittest
from dataclasses import replace
from qa_master.ci_attestation import ExpectedRun,AttestationError,assess_ci_job
SHA='a'*40
class FakeGitLab:
 def project(self,id):return {'id':1}
 def job(self,p,j):return {'id':2,'status':'success','pipeline':{'id':3},'commit':{'id':SHA},'environment':{'name':'staging'}}
 def pipeline(self,p,i):return {'id':3,'sha':SHA,'ref':'main','status':'success','ref_protected':True}
class CITests(unittest.TestCase):
 def setUp(self):self.e=ExpectedRun(1,2,3,SHA,'main','staging');self.reader=FakeGitLab()
 def test_valid(self):self.assertTrue(assess_ci_job(self.reader,self.e)['metadata_matches'])
 def test_not_artifact_authenticated(self):self.assertFalse(assess_ci_job(self.reader,self.e)['artifact_authenticated'])
 def test_wrong_sha(self):self.assertIn('PIPELINE_COMMIT_MISMATCH',assess_ci_job(self.reader,replace(self.e,commit_sha='b'*40))['reasons'])
 def test_short_sha_denied(self):
  with self.assertRaises(AttestationError):assess_ci_job(self.reader,replace(self.e,commit_sha='abc'))
 def test_id(self):
  with self.assertRaises(AttestationError):assess_ci_job(self.reader,replace(self.e,job_id=0))
 def test_wrong_env(self):self.assertIn('ENVIRONMENT_MISMATCH',assess_ci_job(self.reader,replace(self.e,environment='prod'))['reasons'])
 def test_unprotected(self):
  class R(FakeGitLab):
   def pipeline(self,p,i):return dict(super().pipeline(p,i),ref_protected=False)
  self.assertIn('PROTECTED_REF_NOT_CONFIRMED',assess_ci_job(R(),self.e)['reasons'])
 def test_allow_unprotected_opt_in(self):
  class R(FakeGitLab):
   def pipeline(self,p,i):return dict(super().pipeline(p,i),ref_protected=False)
  self.assertTrue(assess_ci_job(R(),self.e,protected_ref_required=False)['metadata_matches'])
 def test_failed_job(self):
  class R(FakeGitLab):
   def job(self,p,j):return dict(super().job(p,j),status='failed')
  self.assertIn('JOB_NOT_SUCCESS',assess_ci_job(R(),self.e)['reasons'])
 def test_wrong_pipeline(self):
  class R(FakeGitLab):
   def job(self,p,j):return dict(super().job(p,j),pipeline={'id':9})
  self.assertIn('JOB_PIPELINE_MISMATCH',assess_ci_job(R(),self.e)['reasons'])
 def test_project_mismatch(self):
  class R(FakeGitLab):
   def project(self,p):return {'id':2}
  with self.assertRaises(AttestationError):assess_ci_job(R(),self.e)
 def test_pipeline_not_success(self):
  class R(FakeGitLab):
   def pipeline(self,p,i):return dict(super().pipeline(p,i),status='pending')
  self.assertIn('PIPELINE_NOT_SUCCESS',assess_ci_job(R(),self.e)['reasons'])
