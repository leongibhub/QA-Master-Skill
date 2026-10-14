import unittest
from qa_master.quality import analyze_requirements,review_cases,execution_report
class RequirementsTests(unittest.TestCase):
 def test_missing_source(self):self.assertIn('NO_PROVENANCE',[x['code'] for x in analyze_requirements([{'id':'R1','text':'提交文档','acceptance':'保存成功'}])['findings']])
 def test_vague(self):self.assertIn('AMBIGUOUS',[x['code'] for x in analyze_requirements([{'id':'R1','text':'要快速响应','source':'doc','acceptance':'快'}])['findings']])
 def test_code_requires_confirmation(self):self.assertIn('CODE_UNCONFIRMED',[x['code'] for x in analyze_requirements([{'id':'R1','text':'实现','source':'sha1','origin':'code','acceptance':'result'}])['findings']])
 def test_duplicate_ids(self):self.assertIn('DUPLICATE_REQUIREMENT_ID',[x['code'] for x in analyze_requirements([{'id':'X','text':'a'},{'id':'X','text':'b'}])['findings']])
 def test_review_never_approves(self):self.assertEqual(analyze_requirements([])['approval'],'PENDING_HUMAN')
class CaseTests(unittest.TestCase):
 def setUp(self):self.case={'id':'TC-1','title':'上传合法文件','priority':'P1','trace':['R1'],'dimension':'functional','preconditions':'已登录','data':'test.pdf','steps':['上传文件','查看状态'],'expected':'页面显示上传成功且文件列表出现 test.pdf'}
 def test_complete(self):self.assertTrue(review_cases([self.case],{'R1'})['pass'])
 def test_missing_fields(self):
  c=self.case.copy();c.pop('expected');self.assertIn('MISSING_FIELD',[x['code'] for x in review_cases([c])['issues']])
 def test_weak_oracle(self):
  c=self.case.copy();c['expected']='系统正常';self.assertFalse(review_cases([c])['pass'])
 def test_duplicate_ids(self):self.assertIn('DUPLICATE_ID',[x['code'] for x in review_cases([self.case,self.case])['issues']])
 def test_trace_gap(self):self.assertIn('UNCOVERED_REQUIREMENT',[x['code'] for x in review_cases([self.case],{'R1','R2'})['issues']])
 def test_unapproved_trace(self):self.assertIn('UNAPPROVED_TRACE',[x['code'] for x in review_cases([self.case],{'R2'})['issues']])
 def test_no_trace(self):
  c=self.case.copy();c['trace']=[];self.assertFalse(review_cases([c])['pass'])
 def test_human_review_pending(self):self.assertEqual(review_cases([self.case])['human_final_decision'],'PENDING')
class ReportTests(unittest.TestCase):
 def test_no_run(self):self.assertEqual(execution_report([])['status'],'NOT_EXECUTED')
 def test_pass_without_evidence_not_pass(self):self.assertEqual(execution_report([{'status':'PASS'}])['counts']['PASS'],0)
 def test_pass_with_evidence(self):self.assertEqual(execution_report([{'status':'PASS','evidence':'artifact://1'}])['counts']['PASS'],1)
 def test_unknown_defects_not_zero(self):self.assertIsNone(execution_report([])['defect_count'])
 def test_report_does_not_release(self):self.assertFalse(execution_report([{'status':'PASS','evidence':'x'}])['release_approved'])
