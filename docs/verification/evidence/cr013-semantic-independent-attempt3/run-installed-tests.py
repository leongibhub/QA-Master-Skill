import importlib.util,sys,unittest
from pathlib import Path
import qa_master
assert 'site-packages' in qa_master.__file__,qa_master.__file__
spec=importlib.util.spec_from_file_location('installed_semantic_independent','D:/QA-Master-PR2/tests/test_semantic_quality_independent.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(module))
print('PACKAGE_SOURCE='+qa_master.__file__)
sys.exit(not result.wasSuccessful())
