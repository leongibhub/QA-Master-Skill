"""CR-030: concise Windows host-install instructions remain truthful."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class InstallationDocumentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        cls.guide = (ROOT / 'docs' / 'GETTING_STARTED.md').read_text(encoding='utf-8')

    def test_windows_primary_path_uses_uv_without_manual_venv(self):
        quickstart = self.readme[self.readme.index('## 快速开始'):self.readme.index('## 按你需要的范围工作')]
        self.assertIn('uv tool install --force --python 3.13 .', quickstart)
        self.assertNotIn('py -3 -m venv', quickstart)
        self.assertNotIn('Activate.ps1', quickstart)

    def test_documented_host_choices_and_safe_claude_boundary(self):
        for text in (self.readme, self.guide):
            self.assertIn('qa-master install-codex --user', text)
            self.assertIn('$HOME\\.agents\\skills\\qa-master', text)
            self.assertIn('qa-master install-codex --target "$HOME\\.claude\\skills\\qa-master"', text)
            self.assertIn('$HOME\\.claude\\skills\\qa-master', text)
            self.assertIn('DeepSeek', text)
            self.assertIn('不读取', text)
            self.assertIn('API Token', text)
        self.assertIn('已写入的文件和本地助手自检证明的是安装交付', self.readme)
        self.assertIn('qa-master install-codex --project "<项目绝对路径>"', self.guide)
        self.assertIn('qa-master install-codex --target "<项目绝对路径>\\.claude\\skills\\qa-master"', self.guide)
        self.assertIn('$HOME/.claude/skills/qa-master', self.guide)

    def test_documented_verification_restart_prompt_and_update_boundary(self):
        for text in (self.readme, self.guide):
            self.assertIn('Test-Path', text)
            self.assertIn('py -3 -I', text)
            self.assertIn('330', text)
            self.assertIn('165', text)
            self.assertIn('/qa-master', text)
            self.assertIn('--link-mode=copy', text)
            self.assertIn('hardlink', text)


if __name__ == '__main__':
    unittest.main()
