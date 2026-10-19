import tempfile
import unittest
import hashlib
import json
from pathlib import Path

from qa_master.skill_registry import (
    discover_vendor_skills,
    select_vendor_skills,
    vendor_skill_root,
)


class VendorSkillsTests(unittest.TestCase):
    def test_vendor_source_provenance_binds_bilingual_snapshot(self):
        root = vendor_skill_root()
        metadata = json.loads((root / "SOURCE_PROVENANCE.json").read_text(encoding="utf-8"))
        self.assertEqual(metadata["schema_version"], 1)
        self.assertEqual(metadata["source_repository"],
                         "https://github.com/naodeng/awesome-qa-skills")
        self.assertEqual(metadata["source_commit"], "547fbcd9c417ab8afbde1cd9f18b40ecbae0333b")
        self.assertEqual(metadata["upstream_commit_time"], "2026-10-19T01:50:43Z")
        self.assertEqual(metadata["upstream_tree_git_sha1"],
                         "694cf0b677cb90cee101e7806657537b016c356c")
        self.assertEqual(metadata["license_path"], "LICENSE")
        self.assertEqual(metadata["verification_status"], "VERIFIED")
        self.assertRegex(metadata["retrieved_at"], r"^\d{4}-\d{2}-\d{2}$")
        self.assertEqual(metadata["snapshot"]["included_paths"], ["skills/en", "skills/zh"])
        files = sorted(
            path for language in ("en", "zh") for path in (root / language).rglob("*")
            if path.is_file()
        )
        manifest = b"".join(
            f"{path.relative_to(root).as_posix()}|"
            f"{hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest()}\n".encode("utf-8")
            for path in files
        )
        self.assertEqual(metadata["snapshot"]["file_count"], len(files))
        self.assertEqual(metadata["snapshot"]["sha256"], hashlib.sha256(manifest).hexdigest())

    def test_playwright_runner_keeps_json_report_contract_bilingually(self):
        root = vendor_skill_root()
        for language in ("en", "zh"):
            script = root / language / "testing-types" / "ui-test-playwright" / "scripts" / "run-tests.sh"
            content = script.read_text(encoding="utf-8")
            self.assertIn('PLAYWRIGHT_JSON_OUTPUT_FILE="$REPORT_JSON"', content)
            self.assertIn("--reporter=list,html,json", content)

    def test_vendor_catalog_is_discovered_bilingually(self):
        result = discover_vendor_skills()
        self.assertEqual(result["status"], "DISCOVERED")
        self.assertGreaterEqual(result["count"], 300)  # 165 skill names x (en + zh)
        self.assertEqual(result["gaps"], [])
        names = {skill["name"] for skill in result["skills"]}
        self.assertIn("api-testing", names)
        self.assertIn("requirements-analysis", names)
        self.assertEqual({skill["language"] for skill in result["skills"]}, {"en", "zh"})

    def test_vendor_root_is_resolvable(self):
        self.assertTrue(str(vendor_skill_root()))

    def test_vendor_routing_maps_stages_to_skills(self):
        result = select_vendor_skills(stages=["requirements", "design"])
        self.assertEqual(result["execution"], "NOT_EXECUTED")
        selected_names = {skill["name"] for skill in result["selected"]}
        self.assertIn("requirements-analysis", selected_names)
        self.assertIn("test-case-writing", selected_names)
        # Every wanted name resolves to both language leaves.
        for name in result["wanted"]:
            matching = [s for s in result["selected"] if s["name"] == name]
            self.assertEqual({s["language"] for s in matching}, {"en", "zh"})

    def test_vendor_routing_skips_names_owned_by_bundled_guides(self):
        # 'regression-testing' is mapped by core but absent from the vendor
        # catalog; it must be skipped rather than reported as an error.
        result = select_vendor_skills(stages=["regression"])
        self.assertIn("regression-testing", result["wanted"])
        self.assertEqual([s for s in result["selected"] if s["name"] == "regression-testing"], [])

    def test_vendor_routing_by_dimension(self):
        result = select_vendor_skills(dimensions=["security"])
        self.assertIn("security-testing", {s["name"] for s in result["selected"]})

    def test_vendor_metadata_parsed_from_frontmatter(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill_dir = root / "en" / "testing-types" / "demo-skill"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                "---\nname: demo-skill\ndescription: demo description\n---\n# Demo\n",
                encoding="utf-8",
            )
            result = discover_vendor_skills(root)
        self.assertEqual([s["name"] for s in result["skills"]], ["demo-skill"])
        self.assertEqual(result["skills"][0]["language"], "en")
        self.assertEqual(result["skills"][0]["category"], "testing-types")

    def test_vendor_missing_skill_file_reported_as_gap(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill_dir = root / "zh" / "skill-engineering" / "broken"
            skill_dir.mkdir(parents=True)
            result = discover_vendor_skills(root)
        self.assertEqual(result["skills"], [])
        self.assertIn("VENDOR_SKILL_UNREADABLE", [gap["code"] for gap in result["gaps"]])


if __name__ == "__main__":
    unittest.main()
