import unittest
from qa_master.approval import artifact_digest,approve_artifact,check_approval,approval_record,ArtifactApproval
class ApprovalTests(unittest.TestCase):
 def setUp(self):
  self.artifact={'requirements':[{'id':'R1','acceptance':'HTTP 201'}]}
  self.a=approve_artifact(kind='cases',project='demo',scope='release-1',artifact=self.artifact,reviewer='tester')
 def test_digest_stable_order(self):
  self.assertEqual(artifact_digest({'a':1,'b':2}),artifact_digest({'b':2,'a':1}))
 def test_digest_changes_with_content(self):
  self.assertNotEqual(artifact_digest({'a':1}),artifact_digest({'a':2}))
 def test_authorized(self):self.assertTrue(check_approval(approval_record(self.a),kind='cases',project='demo',scope='release-1',artifact=self.artifact))
 def test_changed_artifact_denied(self):
  self.artifact['requirements'][0]['acceptance']='HTTP 200'
  self.assertFalse(check_approval(approval_record(self.a),kind='cases',project='demo',scope='release-1',artifact=self.artifact))
 def test_different_project_denied(self):
  self.assertFalse(check_approval(approval_record(self.a),kind='cases',project='another',scope='release-1',artifact=self.artifact))
 def test_different_scope_denied(self):
  self.assertFalse(check_approval(approval_record(self.a),kind='cases',project='demo',scope='release-2',artifact=self.artifact))
 def test_different_action_denied(self):
  self.assertFalse(check_approval(approval_record(self.a),kind='execution',project='demo',scope='release-1',artifact=self.artifact))
 def test_missing_record_denied(self):
  self.assertFalse(check_approval({},kind='cases',project='demo',scope='release-1',artifact=self.artifact))
 def test_forged_hash_denied(self):
  r=approval_record(self.a);r['artifact_sha256']='0'*64
  self.assertFalse(check_approval(r,kind='cases',project='demo',scope='release-1',artifact=self.artifact))
 def test_bad_hash_rejected(self):
  with self.assertRaises(ValueError):ArtifactApproval('cases','demo','scope','abc','human')
 def test_not_approved_rejected(self):
  with self.assertRaises(ValueError):ArtifactApproval('cases','demo','scope','0'*64,'human','REJECTED')
 def test_no_reviewer_rejected(self):
  with self.assertRaises(ValueError):approve_artifact(kind='cases',project='demo',scope='scope',artifact={},reviewer='')
