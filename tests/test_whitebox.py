import unittest
from qa_master.whitebox import inspect_python,review_readiness
class WhiteboxTests(unittest.TestCase):
 def test_if(self):self.assertEqual(inspect_python('def f(x):\n if x: pass','a.py')['candidates'][0]['scenarios'],['condition_true','condition_false'])
 def test_raise(self):self.assertEqual(inspect_python('def f():\n raise ValueError()','a.py')['candidates'][0]['kind'],'Raise')
 def test_while(self):self.assertEqual(inspect_python('def f(x):\n while x: break','a.py')['candidates'][0]['scenarios'][0],'zero_iterations')
 def test_try(self):self.assertIn('handled_exception_path',inspect_python('def f():\n try: pass\n except: pass','a.py')['candidates'][0]['scenarios'])
 def test_no_oracle(self):self.assertIsNone(inspect_python('def f(x):\n if x: pass','a.py')['candidates'][0]['expected'])
 def test_commit(self):self.assertEqual(inspect_python('def f(x):\n if x: pass','a.py',commit_sha='abc')['candidates'][0]['source']['commit'],'abc')
 def test_parse_error(self):self.assertEqual(inspect_python('def (','a.py')['status'],'PARSE_ERROR')
 def test_traversal(self):
  with self.assertRaises(ValueError):inspect_python('pass','../a.py')
 def test_absolute(self):
  with self.assertRaises(ValueError):inspect_python('pass','/a.py')
 def test_nonpython(self):
  with self.assertRaises(ValueError):inspect_python('pass','a.js')
 def test_nested_not_duplicated(self):self.assertEqual(len(inspect_python('def a():\n def b(x):\n  if x: pass','a.py')['candidates']),1)
 def test_stable_ids(self):
  s='def f(x):\n if x: pass'
  self.assertEqual(inspect_python(s,'a.py')['candidates'][0]['id'],inspect_python(s,'a.py')['candidates'][0]['id'])
 def test_coverage_not_measured(self):self.assertEqual(inspect_python('def f(x):\n if x: pass','a.py')['candidates'][0]['branch_coverage'],'NOT_MEASURED')
 def test_not_ready(self):self.assertFalse(review_readiness(inspect_python('def f(x):\n if x: pass','a.py'))['ready'])
 def test_no_auto_approval(self):self.assertFalse(inspect_python('pass','a.py')['approved'])
