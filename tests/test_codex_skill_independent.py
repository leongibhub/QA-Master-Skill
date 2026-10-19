"""Independent black-box verification of the packaged Codex skill installer.

These cases deliberately avoid reusing the developer test helpers.  They exercise
the public installer and the installed helper from disposable project locations.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from zipfile import ZipFile

from qa_master.codex_skill import MANIFEST, SkillInstallError, install_skill, skill_bundle


class IndependentCodexSkillInstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="qa-master-pr2-independent-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.target = self.root / "project" / ".agents" / "skills" / "qa-master"

    def _run_installed_helper(self, *args):
        other_project = self.root / "unrelated project"
        other_project.mkdir(exist_ok=True)
        return subprocess.run(
            [sys.executable, "-I", str(self.target / "scripts" / "qa.py"), *args],
            cwd=other_project,
            text=True,
            capture_output=True,
            timeout=20,
            check=False,
        )

    def _tree_bytes(self):
        return {
            path.relative_to(self.target).as_posix(): path.read_bytes()
            for path in self.target.rglob("*") if path.is_file()
        }

    def test_install_is_self_contained_and_reports_planning_only(self):
        result = install_skill(self.target)
        self.assertEqual(result["status"], "INSTALLED")
        self.assertEqual(result["execution"], "NOT_EXECUTED")
        response = self._run_installed_helper("skills")
        self.assertEqual(response.returncode, 0, response.stderr)
        discovered = json.loads(response.stdout)
        self.assertEqual(discovered["status"], "DISCOVERED")
        self.assertEqual(discovered["gaps"], [])
        self.assertEqual(len(discovered["guides"]), 6)
        target_root = self.target.resolve(strict=True)
        for guide in discovered["guides"]:
            guide_path = Path(guide["path"]).resolve(strict=True)
            self.assertTrue(guide_path.is_relative_to(target_root))
        init = self._run_installed_helper("init", "independent")
        self.assertEqual(init.returncode, 0, init.stderr)
        plan = self._run_installed_helper("plan", "评审需求并生成测试用例，不执行测试")
        self.assertEqual(plan.returncode, 0, plan.stderr)
        planned = json.loads(plan.stdout)
        self.assertTrue(planned["no_execution"])
        self.assertEqual(planned["professional_guidance"]["execution"], "NOT_EXECUTED")

    def test_managed_update_replaces_bundle_and_keeps_complete_backup(self):
        install_skill(self.target)
        original = self._tree_bytes()
        changed_bundle = skill_bundle()
        changed_bundle["SKILL.md"] += b"\nIndependent update marker.\n"
        with patch("qa_master.codex_skill.skill_bundle", return_value=changed_bundle):
            with self.assertRaisesRegex(SkillInstallError, "SKILL_UPDATE_REQUIRED"):
                install_skill(self.target)
            result = install_skill(self.target, update=True)
        self.assertEqual(result["status"], "UPDATED")
        self.assertTrue(Path(result["backup"]).is_file())
        recovery = Path(result["recovery_directory"])
        self.assertTrue(recovery.is_dir())
        self.assertTrue(recovery.is_relative_to(self.target.parent.parent / ".qa-master-recovery"))
        # Vendored guidance may contain nested entries; updates must retain
        # exactly the managed entries without a sibling/staging backup Skill.
        expected_entries = {self.target / name for name in changed_bundle
                            if Path(name).name == "SKILL.md"}
        self.assertEqual(set(self.target.parent.rglob("SKILL.md")), expected_entries)
        self.assertEqual(list(self.target.parent.glob("*/SKILL.md")), [self.target / "SKILL.md"])
        self.assertEqual((self.target / "SKILL.md").read_bytes(), changed_bundle["SKILL.md"])
        import zipfile
        with zipfile.ZipFile(result["backup"]) as archive:
            self.assertEqual(set(archive.namelist()), set(original))
            for name, expected in original.items():
                self.assertEqual(archive.read(name), expected)

    def test_failed_publication_rolls_back_exact_original_directory(self):
        install_skill(self.target)
        original = self._tree_bytes()
        changed_bundle = skill_bundle()
        changed_bundle["SKILL.md"] += b"\nIndependent rollback marker.\n"
        original_rename = os.rename

        def fail_staged_publication(source, destination):
            source_path = Path(source)
            if source_path.name == "qa-master" and source_path.parent.name.startswith(".qa-master-stage-"):
                raise OSError("independent synthetic publication failure")
            return original_rename(source, destination)

        with patch("qa_master.codex_skill.skill_bundle", return_value=changed_bundle), \
             patch("qa_master.codex_skill.os.rename", side_effect=fail_staged_publication):
            with self.assertRaises(OSError):
                install_skill(self.target, update=True)
        self.assertEqual(self._tree_bytes(), original)
        self.assertEqual(install_skill(self.target)["status"], "UNCHANGED")

    def test_target_symlink_is_refused_without_following_it(self):
        outside = self.root / "outside"
        outside.mkdir()
        marker = outside / "marker.txt"
        marker.write_text("must remain", encoding="utf-8")
        self.target.parent.mkdir(parents=True)
        try:
            self.target.symlink_to(outside, target_is_directory=True)
        except OSError as error:
            self.skipTest(f"symlink creation unavailable: {error}")
        with self.assertRaisesRegex(SkillInstallError, "SKILL_TARGET_CONFLICT"):
            install_skill(self.target)
        self.assertEqual(marker.read_text(encoding="utf-8"), "must remain")
        self.target.unlink()

    def test_nested_symlink_is_refused_without_following_it(self):
        outside = self.root / "outside"
        outside.mkdir()
        marker = outside / "marker.txt"
        marker.write_text("must remain", encoding="utf-8")
        install_skill(self.target)
        nested = self.target / "unmanaged-link"
        try:
            nested.symlink_to(outside, target_is_directory=True)
        except OSError as error:
            self.skipTest(f"symlink creation unavailable: {error}")
        with self.assertRaisesRegex(SkillInstallError, "SKILL_TARGET_MODIFIED"):
            install_skill(self.target, update=True)
        self.assertEqual(marker.read_text(encoding="utf-8"), "must remain")

    def test_manifest_covers_every_installed_managed_file(self):
        install_skill(self.target)
        manifest = json.loads((self.target / MANIFEST).read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema_version"], 1)
        actual = {
            path.relative_to(self.target).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in self.target.rglob("*")
            if path.is_file() and path.name != MANIFEST
        }
        self.assertEqual(manifest["files"], actual)

    def test_update_rejects_edit_in_the_verify_to_publish_window(self):
        install_skill(self.target)
        changed_bundle = skill_bundle()
        changed_bundle["SKILL.md"] += b"\nIndependent concurrent-update marker.\n"
        original_existing = __import__("qa_master.codex_skill", fromlist=["_existing"])._existing
        calls = 0

        def edit_after_last_verification(target):
            nonlocal calls
            observed = original_existing(target)
            calls += 1
            if calls == 2:
                (self.target / "SKILL.md").write_text("concurrent user edit", encoding="utf-8")
            return observed

        with patch("qa_master.codex_skill.skill_bundle", return_value=changed_bundle), \
             patch("qa_master.codex_skill._existing", side_effect=edit_after_last_verification):
            with self.assertRaisesRegex(SkillInstallError, "SKILL_TARGET_MODIFIED"):
                install_skill(self.target, update=True)
        self.assertEqual((self.target / "SKILL.md").read_text(encoding="utf-8"), "concurrent user edit")

    def test_update_rejects_user_file_hidden_under_pycache(self):
        install_skill(self.target)
        user_file = self.target / "scripts" / "qa_master" / "__pycache__" / "user-notes.txt"
        user_file.parent.mkdir()
        user_file.write_text("user-owned data", encoding="utf-8")
        changed_bundle = skill_bundle()
        changed_bundle["SKILL.md"] += b"\nIndependent pycache-update marker.\n"
        with patch("qa_master.codex_skill.skill_bundle", return_value=changed_bundle):
            with self.assertRaisesRegex(SkillInstallError, "SKILL_TARGET_MODIFIED"):
                install_skill(self.target, update=True)
        self.assertEqual(user_file.read_text(encoding="utf-8"), "user-owned data")

    def test_double_publication_and_rollback_failure_retains_recovery_directory(self):
        install_skill(self.target)
        original = self._tree_bytes()
        changed_bundle = skill_bundle()
        changed_bundle["SKILL.md"] += b"\nIndependent double-failure marker.\n"
        original_rename = os.rename

        def fail_publication_and_recovery(source, destination):
            source_path = Path(source)
            destination_path = Path(destination)
            if source_path.name == "qa-master" and source_path.parent.name.startswith(".qa-master-stage-"):
                raise OSError("independent staged publication failure")
            if source_path.name.startswith("qa-master.previous-") and destination_path == self.target:
                raise OSError("independent rollback publication failure")
            return original_rename(source, destination)

        with patch("qa_master.codex_skill.skill_bundle", return_value=changed_bundle), \
             patch("qa_master.codex_skill.os.rename", side_effect=fail_publication_and_recovery):
            with self.assertRaisesRegex(SkillInstallError, "SKILL_INSTALL_RECOVERY_REQUIRED:") as caught:
                install_skill(self.target, update=True)
        recovery = [Path(str(caught.exception).split(":", 1)[1])]
        self.assertFalse(self.target.exists(), "a recovery-required install must not claim publication")
        self.assertEqual(len(recovery), 1)
        self.assertTrue(recovery[0].is_relative_to(self.target.parent.parent / ".qa-master-recovery"))
        recovered_tree = {
            path.relative_to(recovery[0]).as_posix(): path.read_bytes()
            for path in recovery[0].rglob("*") if path.is_file()
        }
        self.assertEqual(recovered_tree, original)

    def test_post_detach_edit_during_archive_is_rejected_and_restored(self):
        install_skill(self.target)
        changed_bundle = skill_bundle()
        changed_bundle["SKILL.md"] += b"\nIndependent archive-race marker.\n"
        original_writestr = ZipFile.writestr
        edited = False

        def edit_after_skill_is_archived(archive, *args, **kwargs):
            nonlocal edited
            result = original_writestr(archive, *args, **kwargs)
            name = str(args[0]).replace("\\", "/") if args else ""
            if name == "SKILL.md" and not edited:
                recovery = list((self.target.parent.parent / ".qa-master-recovery").glob("qa-master.previous-*"))
                self.assertEqual(len(recovery), 1)
                (recovery[0] / "SKILL.md").write_text("late open-writer edit", encoding="utf-8")
                edited = True
            return result

        with patch("qa_master.codex_skill.skill_bundle", return_value=changed_bundle), \
             patch.object(ZipFile, "writestr", autospec=True, side_effect=edit_after_skill_is_archived):
            with self.assertRaisesRegex(SkillInstallError, "SKILL_TARGET_MODIFIED"):
                install_skill(self.target, update=True)
        self.assertTrue(edited)
        self.assertEqual((self.target / "SKILL.md").read_text(encoding="utf-8"), "late open-writer edit")

    @unittest.skipUnless(os.name == "nt", "Windows junction test")
    def test_windows_junction_target_is_refused_without_mutating_destination(self):
        outside = self.root / "junction destination"
        outside.mkdir()
        marker = outside / "marker.txt"
        marker.write_text("must remain", encoding="utf-8")
        self.target.parent.mkdir(parents=True)
        created = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(self.target), str(outside)],
            text=True,
            capture_output=True,
            timeout=15,
            check=False,
        )
        if created.returncode != 0:
            self.skipTest(f"junction creation unavailable: {created.stderr or created.stdout}")
        with self.assertRaisesRegex(SkillInstallError, "SKILL_TARGET_CONFLICT"):
            install_skill(self.target)
        self.assertEqual(marker.read_text(encoding="utf-8"), "must remain")


if __name__ == "__main__":
    unittest.main()
