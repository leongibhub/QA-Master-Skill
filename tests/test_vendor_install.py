"""TASK-113: standalone vendor delivery, inventory and resource safety."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from qa_master.codex_skill import install_skill, skill_bundle, _vendor_files, SkillInstallError


class VendorInstallTests(unittest.TestCase):
    def test_complete_inventory_installed_and_discovered_outside_checkout(self):
        bundle = skill_bundle()
        prefix = 'scripts/qa_master/skills/'
        inventory = json.loads(bundle[prefix + 'vendor-files.json'])['files']
        self.assertEqual(len(inventory), 5820)
        self.assertTrue(any(name.endswith('.yaml') for name in inventory))
        self.assertTrue(any(name.endswith('.csv') for name in inventory))
        self.assertIn('vendor/awesome-qa-skills/LICENSE', inventory)
        self.assertEqual(sorted(inventory), sorted(name[len(prefix):] for name in bundle
                                                  if name.startswith(prefix + 'vendor/')))
        # Freeze one package-resource snapshot across install/readback/idempotence.
        # Concurrent development must not turn this into a different-version update.
        with patch('qa_master.codex_skill.skill_bundle', return_value=bundle), \
                tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / 'installed'
            install_skill(target)
            for name in inventory:
                self.assertEqual((target / prefix / name).read_bytes(), bundle[prefix + name])
            script = target / 'scripts' / 'qa.py'
            proc = subprocess.run([sys.executable, '-I', str(script), 'skills'], cwd=root,
                                  text=True, capture_output=True, timeout=60)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            result = json.loads(proc.stdout)
            self.assertEqual(result['vendor']['count'], 330)
            self.assertEqual(result['vendor']['languages'], {'en': 165, 'zh': 165})
            # Exercise routing from the installed module without repo imports.
            code = ('import sys,json;sys.path.insert(0,sys.argv[1]);'
                    'from qa_master.skill_registry import select_vendor_skills;'
                    'print(json.dumps(select_vendor_skills(["design"])))')
            proc = subprocess.run([sys.executable, '-I', '-c', code, str(target / 'scripts')],
                                  cwd=root, text=True, capture_output=True, timeout=60)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            routed = json.loads(proc.stdout)
            self.assertGreater(routed['count'], 0)
            for item in routed['selected']:
                path = Path(item['path']).resolve(strict=True)
                self.assertTrue(path.is_relative_to(target.resolve()))
            self.assertEqual(install_skill(target)['status'], 'UNCHANGED')

    def test_inventory_excludes_unlisted_build_artifacts(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            vendor = root / 'skills' / 'vendor' / 'test'
            vendor.mkdir(parents=True)
            (vendor / 'LICENSE').write_bytes(b'license')
            (vendor / 'untracked.json').write_bytes(b'junk')
            inventory = root / 'skills' / 'vendor-files.json'
            inventory.write_text(json.dumps({'schema_version': 1, 'files': ['vendor/test/LICENSE']}))
            files = dict(_vendor_files(root))
            self.assertEqual(set(files), {'vendor/test/LICENSE', 'vendor-files.json'})
            self.assertEqual(files['vendor/test/LICENSE'], b'license')
            for name in ['vendor/test/../../escape', 'vendor/test/C:evil', 'vendor/test//LICENSE']:
                inventory.write_text(json.dumps({'schema_version': 1, 'files': [name]}))
                with self.assertRaises(SkillInstallError):
                    dict(_vendor_files(root))

    def test_inventory_rejects_linked_resource_before_read(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            vendor = root / 'skills' / 'vendor' / 'test'
            vendor.mkdir(parents=True)
            (vendor / 'LICENSE').write_bytes(b'license')
            (root / 'skills' / 'vendor-files.json').write_text(json.dumps(
                {'schema_version': 1, 'files': ['vendor/test/LICENSE']}))
            with patch('qa_master.codex_skill._linked', side_effect=lambda p: p == vendor):
                with self.assertRaisesRegex(SkillInstallError, 'SKILL_RESOURCE_LINK_FORBIDDEN'):
                    dict(_vendor_files(root))


if __name__ == '__main__':
    unittest.main()
