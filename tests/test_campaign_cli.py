import json,subprocess,sys,tempfile,unittest
from pathlib import Path
from qa_master.campaign_cli import prepare_campaign,write_campaign
class CampaignCLIIntegration(unittest.TestCase):
 def setUp(self):
  self.bundle={'project':'demo','requirements':[
   {'id':'REQ-1','text':'上传','source':'PRD-1','approved':True,'dimension':'functional','acceptance':'文件进入列表'},
   {'id':'REQ-2','text':'API 上传','source':'PRD-1','approved':True,'dimension':'api','acceptance':'201 和文件标识'}]}
 def test_integration(self):
  x=prepare_campaign(self.bundle)
  self.assertEqual(len(x['test_cases']),2)
  self.assertTrue(x['case_review']['pass'])
  self.assertFalse(x['formal_baseline_approved'])
  self.assertEqual(x['workflow']['execution'],'NOT_AUTHORIZED')
 def test_digest(self):self.assertEqual(prepare_campaign(self.bundle)['input_sha256'],prepare_campaign(self.bundle)['input_sha256'])
 def test_missing_oracle(self):
  del self.bundle['requirements'][0]['acceptance']
  r=prepare_campaign(self.bundle)
  self.assertEqual(len(r['test_cases']),1)
  self.assertIn('ORACLE_MISSING',[x['code'] for x in r['unresolved']['design_gaps']])
 def test_code_approval(self):
  self.bundle['requirements'][0].update(origin='code',approved=False)
  self.assertIn('CODE_UNCONFIRMED',[x['code'] for x in prepare_campaign(self.bundle)['requirement_review']['findings']])
 def test_invalid(self):
  for obj in ([],{}, {'project':'X','requirements':{}}, {'project':'X','requirements':['bad']}):
   with self.subTest(obj=obj),self.assertRaises(ValueError):prepare_campaign(obj)
 def test_file_doesnt_overwrite_input(self):
  with tempfile.TemporaryDirectory() as d:
   src=Path(d)/'input.json';out=Path(d)/'output.json'
   src.write_text(json.dumps(self.bundle,ensure_ascii=False),encoding='utf-8')
   write_campaign(src,out)
   self.assertEqual(json.loads(out.read_text(encoding='utf-8'))['project'],'demo')
   with self.assertRaises(ValueError):write_campaign(src,src)
 def test_real_cli_process(self):
  with tempfile.TemporaryDirectory() as d:
   src=Path(d)/'input.json';out=Path(d)/'output.json'
   src.write_text(json.dumps(self.bundle,ensure_ascii=False),encoding='utf-8')
   p=subprocess.run([sys.executable,'-m','qa_master.campaign_cli','--input',str(src),'--output',str(out)],capture_output=True,text=True)
   self.assertEqual(p.returncode,0,p.stderr)
   self.assertEqual(json.loads(out.read_text(encoding='utf-8'))['workflow']['synapsert'],'NOT_WRITTEN')
 def test_performance_without_threshold(self):
  r=dict(self.bundle['requirements'][0],dimension='performance')
  report=prepare_campaign({'project':'demo','requirements':[r]})
  self.assertEqual(report['test_cases'],[])
  self.assertIn('THRESHOLD_UNCONFIRMED',[x['code'] for x in report['unresolved']['design_gaps']])
