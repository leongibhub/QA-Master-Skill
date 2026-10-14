import unittest
from qa_master.coverage_design import design_matrix
BASE={'id':'R1','text':'上传文件','dimension':'functional','acceptance':'列表出现指定文件','approved':True,'source':'PRD'}
class CoverageDesignTests(unittest.TestCase):
 def test_positive_case(self):self.assertEqual(len(design_matrix([BASE])['cases']),1)
 def test_approved_still_draft(self):self.assertEqual(design_matrix([BASE])['status'],'DRAFT_UNAPPROVED')
 def test_trace(self):self.assertEqual(design_matrix([BASE])['cases'][0]['trace'],['R1'])
 def test_no_approval(self):self.assertIn('REQUIREMENT_NOT_APPROVED',[x['code'] for x in design_matrix([dict(BASE,approved=False)])['gaps']])
 def test_no_oracle(self):self.assertEqual(len(design_matrix([dict(BASE,acceptance=None)])['cases']),0)
 def test_nonfunctional_no_threshold(self):self.assertIn('THRESHOLD_UNCONFIRMED',[x['code'] for x in design_matrix([dict(BASE,dimension='performance')])['gaps']])
 def test_nonfunctional_oracle_threshold(self):
  r=dict(BASE,dimension='performance',thresholds={'performance':{'p95_ms':500}})
  self.assertEqual(len(design_matrix([r])['cases']),1)
 def test_multiple_dimensions(self):
  r=dict(BASE,dimensions=['functional','api'],oracles={'api':'HTTP 201 且返回文件标识'})
  self.assertEqual(len(design_matrix([r])['cases']),2)
 def test_unknown_dimension(self):self.assertIn('INVALID_DIMENSION',[x['code'] for x in design_matrix([dict(BASE,dimension='fantasy')])['gaps']])
 def test_duplicate_id(self):self.assertIn('INVALID_OR_DUPLICATE_ID',[x['code'] for x in design_matrix([BASE,BASE])['gaps']])
 def test_na_requires_reason(self):self.assertEqual(design_matrix([],applicable={'api':{'status':'N/A'}})['coverage']['api']['status'],'UNASSESSED')
 def test_na_with_reason(self):self.assertEqual(design_matrix([],applicable={'api':{'status':'N/A','reason':'无API'}})['coverage']['api']['status'],'N/A')
 def test_unassessed(self):self.assertEqual(design_matrix([])['coverage']['security']['status'],'UNASSESSED')
 def test_no_implicit_pass(self):self.assertNotIn('PASS',[x['status'] for x in design_matrix([BASE])['coverage'].values()])
 def test_human_pending(self):self.assertEqual(design_matrix([BASE])['human_final_decision'],'PENDING')
