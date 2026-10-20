"""TASK-113: build a clean wheel and verify every inventoried vendor byte."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile


class VendorWheelTests(unittest.TestCase):
    def test_clean_wheel_preserves_complete_vendor_inventory(self):
        source = Path(__file__).resolve().parents[1]
        inventory_path = source / 'qa_master' / 'skills' / 'vendor-files.json'
        inventory = json.loads(inventory_path.read_text(encoding='utf-8'))['files']
        self.assertTrue(inventory)
        self.assertTrue(any(Path(name).name == '.gitignore' for name in inventory))
        with tempfile.TemporaryDirectory(prefix='qa-master-wheel-') as temp:
            clean = Path(temp)
            shutil.copy2(source / 'pyproject.toml', clean / 'pyproject.toml')
            shutil.copytree(source / 'qa_master', clean / 'qa_master',
                            ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            # Never reuse checkout build/ or egg-info/SOURCES.txt: stale manifests
            # could mask an incomplete package-data declaration.
            proc = subprocess.run(
                [sys.executable, '-c',
                 'from setuptools.build_meta import build_wheel; build_wheel("dist")'],
                cwd=clean, capture_output=True, text=True, encoding='utf-8',
                errors='replace', timeout=600)
            self.assertEqual(proc.returncode, 0, (proc.stdout + proc.stderr)[-8000:])
            wheels = list((clean / 'dist').glob('*.whl'))
            self.assertEqual(len(wheels), 1)
            with ZipFile(wheels[0]) as wheel:
                names = wheel.namelist()
                self.assertEqual(len(names), len(set(names)))
                self.assertEqual(wheel.read('qa_master/skills/vendor-files.json'),
                                 inventory_path.read_bytes())
                missing = sorted('qa_master/skills/' + name for name in inventory
                                 if 'qa_master/skills/' + name not in names)
                self.assertEqual(missing, [], 'Inventoried resources missing from wheel')
                expected = {'qa_master/skills/' + name for name in inventory}
                actual = {name for name in names
                          if name.startswith('qa_master/skills/vendor/') and not name.endswith('/')}
                self.assertEqual(actual, expected, 'Wheel vendor inventory must match exactly')
                for name in inventory:
                    with self.subTest(resource=name):
                        self.assertEqual(wheel.read('qa_master/skills/' + name),
                                         (source / 'qa_master' / 'skills' / name).read_bytes())


if __name__ == '__main__':
    unittest.main()
