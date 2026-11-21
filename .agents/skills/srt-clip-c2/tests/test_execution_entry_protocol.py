import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = next(path for path in ROOT.parents if (path / "plugin.json").is_file())


class ExecutionEntryProtocolTests(unittest.TestCase):
    def test_all_entry_surfaces_require_a_fresh_complete_read(self):
        manifest = json.loads((PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8"))
        codex_manifest = json.loads((PLUGIN_ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        prompt = manifest["extensions"]["com.openai"]["interface"]["defaultPrompt"]
        codex_prompt = codex_manifest["interface"]["defaultPrompt"]
        launcher = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
        portable = (ROOT / "C2-Universal-Portable.md").read_text(encoding="utf-8")

        self.assertEqual(prompt, codex_prompt)
        self.assertIn(prompt, launcher)
        self.assertIn(prompt, portable)
        for phrase in [
            "每次触发",
            "SKILL.md 全文",
            "同一对话每次触发都必须重新确认",
            "若任一必读文件缺失、截断或未完整取得",
            "不得凭记忆输出正式成片",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, prompt)

    def test_every_required_reference_is_present_in_the_active_skill(self):
        manifest = json.loads((PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8"))
        prompt = manifest["extensions"]["com.openai"]["interface"]["defaultPrompt"]
        paths = re.findall(r"references/[a-z0-9-]+\.md", prompt)
        self.assertEqual(len(paths), 6)
        for relative in paths:
            with self.subTest(path=relative):
                self.assertTrue((ROOT / relative).is_file(), relative)

    def test_package_version_and_core_version_are_separate_and_aligned(self):
        manifest = json.loads((PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8"))
        codex_manifest = json.loads((PLUGIN_ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual((PLUGIN_ROOT / "VERSION").read_text(encoding="utf-8").strip(), "0.4.6")
        self.assertEqual(manifest["version"], "0.4.18")
        self.assertEqual(codex_manifest["version"], manifest["version"])


if __name__ == "__main__":
    unittest.main()
