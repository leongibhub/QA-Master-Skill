import tempfile, unittest
from pathlib import Path
from qa_master.generator import design,coverage_plan
from qa_master.code_intel import inventory_python
from qa_master.api_intel import draft_openapi
class DesignTests(unittest.TestCase):
 def setUp(self):self.req={'id':'R1','text':'上传文档','acceptance':'列表显示指定文件','source':'PRD-v1','test_data':'a.pdf'}
 def test_one_positive(self):self.assertEqual(len(design([self.req])['cases']),1)
 def test_draft_status(self):self.assertEqual(design([self.req])['status'],'DRAFT_UNAPPROVED')
 def test_no_criterion(self):self.assertEqual(len(design([{'id':'R1','text':'上传'}])['cases']),0)
 def test_negative_requires_oracle(self):
  x=dict(self.req,invalid_input='bad');self.assertEqual(len(design([x])['cases']),1)
 def test_negative_generated_with_expected(self):
  x=dict(self.req,invalid_input='bad',invalid_expected='HTTP 400');self.assertEqual(len(design([x])['cases']),2)
 def test_source_trace(self):self.assertEqual(design([self.req])['cases'][0]['trace'],['R1'])
 def test_unknown_dimension(self):self.assertEqual(len(design([dict(self.req,dimension='unknown')])['cases']),0)
 def test_coverage_not_false_pass(self):self.assertEqual(coverage_plan([self.req])['api']['status'],'UNASSESSED')
 def test_case_review(self):self.assertTrue(design([self.req])['review']['pass'])
class CodeTests(unittest.TestCase):
 def test_python_functions(self):
  with tempfile.TemporaryDirectory() as d:
   Path(d,'x.py').write_text('def hello(v):\n if v:\n  raise ValueError()\n return 1\n')
   r=inventory_python(d);self.assertEqual(r['functions'][0]['branch_points'],1)
 def test_unapproved_code(self):
  with tempfile.TemporaryDirectory() as d:
   Path(d,'x.py').write_text('def a(): pass')
   self.assertEqual(inventory_python(d)['functions'][0]['requirement_approval'],'NOT_APPROVED')
 def test_syntax_failure_not_silent(self):
  with tempfile.TemporaryDirectory() as d:
   Path(d,'bad.py').write_text('def (')
   self.assertEqual(len(inventory_python(d)['parse_problems']),1)
 def test_file_limit(self):
  with tempfile.TemporaryDirectory() as d:
   Path(d,'a.py').write_text('pass')
   with self.assertRaises(ValueError):inventory_python(d,max_files=0)
class OpenAPITests(unittest.TestCase):
 def test_simple_endpoint(self):self.assertEqual(len(draft_openapi({'paths':{'/health':{'get':{'responses':{'200':{}}}}}})['cases']),1)
 def test_no_success_contract_is_gap(self):self.assertEqual(len(draft_openapi({'paths':{'/x':{'post':{'responses':{'400':{}}}}}})['gaps']),1)
 def test_openapi_required(self):
  with self.assertRaises(ValueError):draft_openapi({})
 def test_not_executed(self):self.assertEqual(draft_openapi({'paths':{'/a':{'get':{'responses':{'200':{}}}}}})['cases'][0]['execution'],'NOT_RUN')
