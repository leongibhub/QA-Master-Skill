"""CR-029: README catalogue is a complete, navigable view of bundled skills."""

from collections import Counter
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "qa_master" / "skills" / "vendor" / "awesome-qa-skills"
LINK = re.compile(
    r"qa_master/skills/vendor/awesome-qa-skills/"
    r"(?P<language>zh|en)/"
    r"(?P<category>testing-workflows|testing-types|skill-engineering)/"
    r"(?P<name>[a-z0-9-]+)/SKILL\.md"
)
MARKDOWN_LINK = re.compile(r"\[[^]]+\]\((?P<target>[^)#]+)(?:#[^)]*)?\)")


def _records(text: str) -> list[tuple[str, str, str]]:
    return [
        (match.group("category"), match.group("name"), match.group("language"))
        for match in LINK.finditer(text)
    ]


def _section(text: str, start: str, end: str) -> str:
    start_at = text.index(start)
    end_at = text.index(end, start_at)
    return text[start_at:end_at]


def _bundled_records() -> set[tuple[str, str, str]]:
    records = set()
    for language in ("zh", "en"):
        for category in ("testing-workflows", "testing-types", "skill-engineering"):
            for skill_file in (VENDOR / language / category).glob("*/SKILL.md"):
                records.add((category, skill_file.parent.name, language))
    return records


class ReadmeCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.readme = (ROOT / "README.md").read_text(encoding="utf-8")
        cls.path_catalog = (ROOT / "docs" / "SKILL_CATALOG.md").read_text(encoding="utf-8")
        cls.expected = _bundled_records()

    def test_readme_complete_catalog_lists_each_bundled_skill_once_per_language(self):
        complete = _section(self.readme, "## 完整技能目录", "## 文档导航")
        listed = _records(complete)

        self.assertEqual(len(self.expected), 330)
        self.assertEqual(set(listed), self.expected)
        self.assertTrue(all(count == 1 for count in Counter(listed).values()))
        self.assertEqual(len({name for _, name, language in listed if language == "zh"}), 165)
        self.assertEqual(len({name for _, name, language in listed if language == "en"}), 165)

    def test_readme_catalog_keeps_workflow_layer_and_type_layer_counts(self):
        workflow = _section(self.readme, "### 跨阶段工作流", "### 四层能力体系与研发测试阶段")
        core = _section(self.readme, "#### Core QA Skills — 基础质量能力",
                        "#### Engineering QA Skills — 质量工程能力")
        engineering = _section(self.readme, "#### Engineering QA Skills — 质量工程能力",
                               "#### Production Quality Skills — 生产质量能力")
        production = _section(self.readme, "#### Production Quality Skills — 生产质量能力",
                              "#### AI Native QA Skills — AI 原生质量能力")
        ai_native = _section(self.readme, "#### AI Native QA Skills — AI 原生质量能力",
                             "### Skill Engineering（横向治理）")
        skill_engineering = _section(self.readme, "### Skill Engineering（横向治理）",
                                     "## 文档导航")

        expected = {
            "testing-workflows": (workflow, 10),
            "core": (core, 28),
            "engineering": (engineering, 100),
            "production": (production, 4),
            "ai-native": (ai_native, 18),
            "skill-engineering": (skill_engineering, 5),
        }
        for layer, (content, count) in expected.items():
            records = _records(content)
            zh_names = [name for _, name, language in records if language == "zh"]
            en_names = [name for _, name, language in records if language == "en"]
            self.assertEqual(len(zh_names), count, layer)
            self.assertEqual(len(en_names), count, layer)
            self.assertEqual(set(zh_names), set(en_names), layer)

        self.assertEqual({category for category, _, _ in _records(workflow)}, {"testing-workflows"})
        self.assertEqual({category for category, _, _ in _records(skill_engineering)},
                         {"skill-engineering"})
        for content in (core, engineering, production, ai_native):
            self.assertEqual({category for category, _, _ in _records(content)}, {"testing-types"})

    def test_stable_catalog_matches_readme_and_all_bilingual_targets_resolve(self):
        listed = _records(self.path_catalog)
        self.assertEqual(set(listed), self.expected)
        self.assertTrue(all(count == 1 for count in Counter(listed).values()))
        self.assertIn("## 测试工作流（10 项）", self.path_catalog)
        self.assertIn("## 测试类型（150 项）", self.path_catalog)
        self.assertIn("## 技能工程（5 项）", self.path_catalog)

        for document, content in ((ROOT / "README.md", self.readme),
                                  (ROOT / "docs" / "SKILL_CATALOG.md", self.path_catalog)):
            for link in MARKDOWN_LINK.finditer(content):
                target = link.group("target")
                if "qa_master/skills/vendor/awesome-qa-skills/" in target:
                    self.assertTrue((document.parent / target).resolve().is_file(),
                                    f"broken link in {document.name}: {target}")

    def test_readme_preserves_single_entry_and_evidence_boundaries(self):
        self.assertIn("单独做一个阶段、组合多个阶段或规划完整流程，都使用同一个入口。", self.readme)
        self.assertEqual(self.readme.count("<项目>/.agents/skills/qa-master/SKILL.md"), 1)
        boundary = _section(self.readme, "## 当前交付边界", "## 参与开发")
        self.assertIn("安装成功、指南被选中或单元测试通过，也不能代替具体项目的验收。", boundary)


if __name__ == "__main__":
    unittest.main()
