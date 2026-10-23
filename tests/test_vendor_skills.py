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
        self.assertEqual(metadata["schema_version"], 2)
        self.assertEqual(metadata["source_repository"],
                         "https://github.com/naodeng/awesome-qa-skills")
        self.assertEqual(metadata["source_commit"], "547fbcd9c417ab8afbde1cd9f18b40ecbae0333b")
        self.assertEqual(metadata["upstream_commit_time"], "2026-10-19T01:50:43Z")
        self.assertEqual(metadata["upstream_tree_git_sha1"],
                         "694cf0b677cb90cee101e7806657537b016c356c")
        self.assertEqual(metadata["license_path"], "LICENSE")
        self.assertEqual(metadata["verification_status"], "OBSERVED")
        self.assertNotIn("independent_verification_status", metadata)
        self.assertEqual(metadata["independent_verification_status_at_freeze"], "PENDING")
        verification = metadata["independent_verification"]
        self.assertEqual(verification["status"], "VERIFIED")
        self.assertEqual(verification["subject_commit"],
                         "523ec344112f03ea350e1fa13c16d5ddc755277e")
        self.assertEqual(verification["source_commit"], metadata["source_commit"])
        self.assertEqual(verification["snapshot_sha256"], metadata["snapshot"]["sha256"])
        self.assertEqual(len(verification["reports"]), 2)
        for report in verification["reports"]:
            expected_url = ("https://github.com/leongibhub/QA-Master-Skill/blob/"
                            f"{verification['evidence_commit']}/{report['path']}")
            self.assertEqual(report["url"], expected_url)
            report_bytes = (Path(__file__).resolve().parents[1] / report["path"]).read_bytes()
            report_text = report_bytes.decode("utf-8")
            self.assertIn(report["artifact_id"], report_text)
            self.assertIn(verification["subject_commit"], report_text)
            self.assertIn(verification["snapshot_sha256"], report_text)
            self.assertEqual(report["sha256"], hashlib.sha256(
                report_bytes.replace(b"\r\n", b"\n")).hexdigest())
        self.assertRegex(metadata["retrieved_at"], r"^\d{4}-\d{2}-\d{2}$")
        self.assertEqual(metadata["snapshot"]["included_paths"], ["skills/en", "skills/zh"])
        def relative_path(path):
            return path.relative_to(root).as_posix()

        files = sorted(
            (path for language in ("en", "zh") for path in (root / language).rglob("*")
            if path.is_file()),
            key=lambda path: relative_path(path).encode("utf-8"),
        )
        snapshot = metadata["snapshot"]
        text_extensions = set(snapshot["text_extensions"])
        binary_extensions = set(snapshot["binary_extensions"])

        def canonical_bytes(path):
            content = path.read_bytes()
            if path.suffix.lower() in text_extensions or path.name in text_extensions:
                content.decode("utf-8", errors="strict")
                return content.replace(b"\r\n", b"\n")
            self.assertIn(path.suffix.lower(), binary_extensions,
                          f"undeclared vendor file extension: {path}")
            return content

        observed_extensions = {path.name if path.name in text_extensions else path.suffix.lower()
                               for path in files}
        self.assertEqual(observed_extensions, text_extensions | binary_extensions)
        self.assertFalse(text_extensions & binary_extensions)
        self.assertIn("UTF-8 bytewise relative POSIX path order", snapshot["algorithm"])
        self.assertEqual(
            sorted(["zh/Z.md", "en/a.md", "en/A.md", "en/é.md"],
                   key=lambda path: path.encode("utf-8")),
            ["en/A.md", "en/a.md", "en/é.md", "zh/Z.md"],
        )
        manifest = b"".join(
            f"{relative_path(path)}|"
            f"{hashlib.sha256(canonical_bytes(path)).hexdigest()}\n".encode("utf-8")
            for path in files
        )
        self.assertEqual(snapshot["file_count"], len(files))
        self.assertEqual(snapshot["sha256"], hashlib.sha256(manifest).hexdigest())
        with tempfile.TemporaryDirectory() as directory:
            invalid_text = Path(directory) / "invalid.md"
            invalid_text.write_bytes(b"\xff")
            with self.assertRaises(UnicodeDecodeError):
                canonical_bytes(invalid_text)
            unknown_extension = Path(directory) / "unknown.extension"
            unknown_extension.write_bytes(b"text")
            with self.assertRaises(AssertionError):
                canonical_bytes(unknown_extension)
            binary_file = Path(directory) / "binary.docx"
            binary_file.write_bytes(b"\xff\r\n")
            self.assertEqual(canonical_bytes(binary_file), b"\xff\r\n")

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
