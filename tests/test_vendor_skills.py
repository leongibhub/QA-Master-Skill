import tempfile
import unittest
from pathlib import Path

from qa_master.skill_registry import (
    discover_vendor_skills,
    select_vendor_skills,
    vendor_skill_root,
)


class VendorSkillsTests(unittest.TestCase):
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
