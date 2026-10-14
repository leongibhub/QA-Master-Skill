import unittest
from qa_master.reverse_requirements import eligible,analyze_source,inspect_repository
class TestReverseRequirements(unittest.TestCase):
 def test_python_allowed(self):self.assertTrue(eligible('app/foo.py'))
 def test_secret_excluded(self):self.assertFalse(eligible('.env.py'))
 def test_path_traversal(self):self.assertFalse(eligible('../a.py'))
 def test_vendor_excluded(self):self.assertFalse(eligible('node_modules/a.py'))
 def test_absolute_path(self):self.assertFalse(eligible('/a.py'))
 def test_branch_hint(self):self.assertEqual(analyze_source('a.py','def f(x):\n if x: return 1')['risk_hints'] if isinstance(analyze_source('a.py','def f(x):\n if x: return 1'),dict) else analyze_source('a.py','def f(x):\n if x: return 1')[0]['risk_hints'],['BRANCHES'])
 def test_unapproved(self):self.assertEqual(analyze_source('a.py','def f():pass')[0]['status'],'NEEDS_HUMAN_CONFIRMATION')
 def test_unknown_oracle(self):self.assertIsNone(analyze_source('a.py','def f():pass')[0]['acceptance'])
 def test_source_ref(self):self.assertEqual(analyze_source('a.py','def f():pass',ref='sha1')[0]['source']['ref'],'sha1')
 def test_js_not_analyzed(self):self.assertEqual(analyze_source('a.js','function f() {}'),[])
 def test_syntax_error(self):self.assertEqual(analyze_source('a.py','def ('),[])
 def test_stable_id(self):self.assertEqual(analyze_source('a.py','def f():pass')[0]['id'],analyze_source('a.py','def f():pass')[0]['id'])
 def reader(self):
  class Reader:
   def project(self,project):return {'id':1}
   def tree(self,project,ref):return [{'path':'src/a.py','type':'blob'},{'path':'.env.py','type':'blob'}]
   def file(self,project,path,ref):return {'content':'def login(x):\n if x: return True','blob_id':'sha'}
  return Reader()
 def test_repo_candidates(self):self.assertEqual(len(inspect_repository(self.reader(),1)['candidates']),1)
 def test_secret_skipped(self):self.assertEqual(inspect_repository(self.reader(),1)['scanned_files'],['src/a.py'])
 def test_not_approved(self):self.assertEqual(inspect_repository(self.reader(),1)['approval'],'PENDING_HUMAN')
 def test_bad_limit(self):
  with self.assertRaises(ValueError):inspect_repository(self.reader(),1,max_files=0)
 def test_read_failure(self):
  class Broken:
   def project(self,p):return {}
   def tree(self,p,r):return [{'path':'a.py','type':'blob'}]
   def file(self,*args):raise TimeoutError()
  self.assertEqual(inspect_repository(Broken(),1)['gaps'][0]['kind'],'READ_FAILED')
