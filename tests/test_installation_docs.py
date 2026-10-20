"""CR-031: Windows install paths are actionable without inventing host evidence."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class InstallationDocumentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        cls.guide = (ROOT / 'docs' / 'GETTING_STARTED.md').read_text(encoding='utf-8')

    def test_windows_branches_cover_existing_and_managed_python(self):
        for text in (self.readme, self.guide):
            self.assertIn('仅克隆', text)
            self.assertIn('py -3 -m qa_master install-codex --user', text)
            self.assertIn('不依赖', text)
            self.assertIn('winget install --id=astral-sh.uv -e', text)
            self.assertIn('uv tool install --force --python 3.13 .', text)
            self.assertIn('uv tool update-shell', text)
            self.assertIn('uv tool run --from . --python 3.13 qa-master', text)
            self.assertNotIn('py -3 -m venv', text)
            self.assertNotIn('Activate.ps1', text)

        self.assertIn('py -3 -m pip install --user .', self.readme)
        self.assertIn('py -3 -m pip install --user .', self.guide)

    def test_documented_windows_host_matrix_has_global_and_project_targets(self):
        for text in (self.readme, self.guide):
            self.assertIn('py -3 -m qa_master install-codex --user', text)
            self.assertIn('%USERPROFILE%\\.agents\\skills\\qa-master', text)
            self.assertIn('py -3 -m qa_master install-codex --project "<项目绝对路径>"', text)
            self.assertIn('%USERPROFILE%\\.claude\\skills\\qa-master', text)
            self.assertIn('<项目绝对路径>\\.claude\\skills\\qa-master', text)
            self.assertIn('%USERPROFILE%\\.trae-cn\\skills\\qa-master', text)
            self.assertIn('<项目绝对路径>\\.trae\\skills\\qa-master', text)

    def test_boundaries_verification_and_non_windows_instructions_are_retained(self):
        for text in (self.readme, self.guide):
            self.assertIn('DeepSeek', text)
            self.assertIn('API Token', text)
            self.assertIn('NOT_EXECUTED', text)
            self.assertIn('py -3 -I', text)
            self.assertIn('uv run --no-project --python 3.13 python', text)
            self.assertIn('330', text)
            self.assertIn('165', text)
            self.assertIn('hardlink', text)
            self.assertIn('--link-mode=copy', text)
            self.assertIn('Linux / macOS', text)
            self.assertIn('python3 -m qa_master install-codex --user', text)


if __name__ == '__main__':
    unittest.main()
