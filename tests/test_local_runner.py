import tempfile,unittest
from pathlib import Path
from qa_master.local_runner import RunPermit,run_local
class LocalRunnerTests(unittest.TestCase):
 def run_case(self,code):
  with tempfile.TemporaryDirectory() as d,tempfile.TemporaryDirectory() as evidence:
   base=str(Path(d).resolve())
   Path(d,'test_dummy.py').write_text(code)
   argv=['python','-m','unittest','discover']
   permit=RunPermit('demo',tuple(argv),base,'reviewer','v1')
   return run_local('demo',argv,base,'v1',permit,evidence)
 def test_success(self):
  r=self.run_case('import unittest\nclass T(unittest.TestCase):\n def test_a(self):self.assertTrue(True)\n')
  self.assertEqual(r['process_status'],'PROCESS_SUCCEEDED')
 def test_failure(self):
  r=self.run_case('import unittest\nclass T(unittest.TestCase):\n def test_a(self):self.assertTrue(False)\n')
  self.assertEqual(r['process_status'],'PROCESS_FAILED')
 def test_no_business_pass(self):self.assertEqual(self.run_case('')['business_result'],'NOT_ASSESSED')
 def test_command_scope(self):
  with tempfile.TemporaryDirectory() as d:
   p=RunPermit('demo',('python','-m','unittest'),str(Path(d).resolve()),'reviewer','v1')
   with self.assertRaises(PermissionError):run_local('demo',['python','-m','pytest'],d,'v1',p,d+'-e')
 def test_shell_denied(self):
  with tempfile.TemporaryDirectory() as d:
   p=RunPermit('demo',('bash','-c','true'),str(Path(d).resolve()),'reviewer','v1')
   with self.assertRaises(PermissionError):run_local('demo',['bash','-c','true'],d,'v1',p,d+'-e')
 def test_arbitrary_python_denied(self):
  with tempfile.TemporaryDirectory() as d:
   p=RunPermit('demo',('python','-c','print(1)'),str(Path(d).resolve()),'reviewer','v1')
   with self.assertRaises(PermissionError):run_local('demo',['python','-c','print(1)'],d,'v1',p,d+'-e')
 def test_requires_approver(self):
  with tempfile.TemporaryDirectory() as d:
   p=RunPermit('demo',('python','-m','unittest'),str(Path(d).resolve()),'','v1')
   with self.assertRaises(PermissionError):p.verify('demo',['python','-m','unittest'],str(Path(d).resolve()),'v1')
 def test_timeout_limit(self):
  with tempfile.TemporaryDirectory() as d:
   p=RunPermit('demo',('python','-m','unittest'),str(Path(d).resolve()),'a','v1')
   with self.assertRaises(ValueError):run_local('demo',['python','-m','unittest'],d,'v1',p,d+'-e',timeout=0)
 def test_version_scope(self):
  with tempfile.TemporaryDirectory() as d:
   p=RunPermit('demo',('python','-m','unittest'),str(Path(d).resolve()),'a','v1')
   with self.assertRaises(PermissionError):p.verify('demo',['python','-m','unittest'],str(Path(d).resolve()),'v2')
