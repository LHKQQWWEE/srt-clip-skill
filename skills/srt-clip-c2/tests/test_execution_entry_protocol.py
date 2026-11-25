import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = next(parent for parent in ROOT.parents if (parent / "plugin.json").is_file())


class EntryProtocolTests(unittest.TestCase):
    def test_entries_preserve_identity_and_use_the_summary_protocol(self):
        plugin = json.loads((PLUGIN / "plugin.json").read_text(encoding="utf-8"))
        companion = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        prompt = plugin["extensions"]["com.openai"]["interface"]["defaultPrompt"]
        self.assertEqual(prompt, companion["interface"]["defaultPrompt"])
        self.assertEqual(plugin["name"], "srt-clip-c2")
        self.assertEqual(plugin["skills"], "./skills")
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        portable = (ROOT / "C2-Universal-Portable.md").read_text(encoding="utf-8")
        self.assertIn("execution-summary.json", skill)
        self.assertIn("clip-selection-policy.md", skill)
        self.assertIn("clip-selection-policy.md", prompt)
        self.assertIn("摘要有效时直接复用", skill)
        self.assertIn("至多 3 个开头候选", prompt)
        self.assertIn("不预选、不凑数", prompt)
        self.assertNotIn("每次调用 C2", prompt)
        self.assertIn(prompt, portable)

    def test_manifest_declares_runtime_summary_and_resolved_paths(self):
        manifest = json.loads((ROOT / "references/runtime-manifest.json").read_text(encoding="utf-8"))
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertEqual(manifest["entry_file"], "SKILL.md")
        self.assertEqual(manifest["required_files"], ["references/runtime-current.md"])
        self.assertEqual(manifest["summary_file"], "references/execution-summary.json")
        self.assertIn("runtime-manifest.json", skill)
        self.assertIn("规则文件 SHA-256", skill)
        for name in [manifest["entry_file"], *manifest["required_files"], manifest["summary_file"]]:
            self.assertTrue((ROOT / name).is_file(), name)
        for item in manifest["conditional_files"]:
            self.assertTrue(list(ROOT.glob(item["path"])), item["path"])

    def test_core_skill_and_plugin_versions_are_aligned(self):
        plugin = json.loads((PLUGIN / "plugin.json").read_text(encoding="utf-8"))
        companion = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        manifest = json.loads((ROOT / "references/runtime-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual((PLUGIN / "VERSION").read_text(encoding="utf-8").strip(), "0.4.7")
        self.assertEqual((ROOT / "VERSION").read_text(encoding="utf-8").strip(), "0.4.36")
        self.assertEqual(plugin["version"], "0.4.36")
        self.assertEqual(companion["version"], plugin["version"])
        self.assertEqual(manifest["core_version"], "0.4.7")
        self.assertEqual(manifest["skill_version"], "0.4.36")


if __name__ == "__main__":
    unittest.main()
