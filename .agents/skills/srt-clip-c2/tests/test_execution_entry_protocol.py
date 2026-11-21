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
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertEqual(prompt, codex_prompt)
        self.assertIn(prompt, launcher)
        self.assertIn(prompt, portable)
        self.assertIn("每次运行前强制完整读取", skill)
        self.assertIn("完整读取本文件全文", skill)
        self.assertIn("任一必读文件缺失或截断", skill)
        self.assertLess(skill.index("每次运行前强制完整读取"), skill.index("## 1. 唯一入口与版本优先级"))
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
        runtime_manifest = json.loads((ROOT / "references/runtime-manifest.json").read_text(encoding="utf-8"))
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        read_contract = skill.split("## 1. 唯一入口与版本优先级", 1)[0]
        paths = set(re.findall(r"`(references/[a-z0-9-]+\.md)`", read_contract))
        self.assertFalse(paths, "the entry must not duplicate the manifest's required file list")
        self.assertIn("required_files", read_contract)
        self.assertTrue(runtime_manifest["required_files"])
        for relative in runtime_manifest["required_files"]:
            with self.subTest(path=relative):
                self.assertTrue((ROOT / relative).is_file(), relative)

    def test_package_version_and_core_version_are_separate_and_aligned(self):
        manifest = json.loads((PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8"))
        codex_manifest = json.loads((PLUGIN_ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual((PLUGIN_ROOT / "VERSION").read_text(encoding="utf-8").strip(), "0.4.6")
        self.assertEqual(manifest["version"], "0.4.23")
        self.assertEqual(codex_manifest["version"], manifest["version"])


if __name__ == "__main__":
    unittest.main()
