import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = next(path for path in ROOT.parents if (path / "plugin.json").is_file())


class ExecutionEntryProtocolTests(unittest.TestCase):
    def test_all_entry_surfaces_route_to_the_compiled_runtime(self):
        plugin = json.loads((PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8"))
        codex = json.loads((PLUGIN_ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        prompt = plugin["extensions"]["com.openai"]["interface"]["defaultPrompt"]
        codex_prompt = codex["interface"]["defaultPrompt"]
        launcher = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
        portable = (ROOT / "C2-Universal-Portable.md").read_text(encoding="utf-8")
        entry = (ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertEqual(prompt, codex_prompt)
        self.assertIn(prompt, launcher)
        self.assertIn(prompt, portable)
        for phrase in ["每次运行前强制完整读取", "references/runtime-current.md", "正常任务不得再逐份加载"]:
            self.assertIn(phrase, entry)
        self.assertIn("不得开始语义分析", entry)
        self.assertIn("每次调用重新读取当前版本", entry)
        self.assertNotIn("manifest.required_files", prompt)
        for phrase in ["每次调用", "完整重读", "runtime-current.md", "不得使用历史摘要", "固定五部分交付"]:
            self.assertIn(phrase, prompt)

    def test_manifest_maps_all_sources_to_one_runtime_file(self):
        manifest = json.loads((ROOT / "references/runtime-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["entry_file"], "SKILL.md")
        self.assertEqual(manifest["runtime_file"], "references/runtime-current.md")
        self.assertEqual(manifest["required_files"], [manifest["runtime_file"]])
        self.assertTrue(manifest["source_files"])
        self.assertEqual(set(manifest["source_files"]), set(manifest["source_hashes"]))
        for item in manifest["source_map"]:
            self.assertIn(item["source"], manifest["source_files"])
            self.assertGreaterEqual(item["runtime_line"], 1)
        self.assertTrue((ROOT / manifest["runtime_file"]).is_file())

    def test_conditional_material_is_not_part_of_the_always_loaded_runtime(self):
        manifest = json.loads((ROOT / "references/runtime-manifest.json").read_text(encoding="utf-8"))
        runtime = (ROOT / manifest["runtime_file"]).read_text(encoding="utf-8")
        for item in manifest["conditional_files"]:
            if "*" not in item["path"]:
                self.assertNotIn(item["path"], manifest["required_files"])
        self.assertNotIn("# Long Context Mode", runtime)
        for pack in (ROOT / "product-knowledge-packs").glob("*.md"):
            self.assertNotIn(pack.read_text(encoding="utf-8").strip(), runtime)

    def test_package_and_core_versions_remain_separate(self):
        plugin = json.loads((PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8"))
        codex = json.loads((PLUGIN_ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual((PLUGIN_ROOT / "VERSION").read_text(encoding="utf-8").strip(), "0.4.6")
        self.assertEqual(plugin["version"], "0.4.24")
        self.assertEqual(codex["version"], plugin["version"])


if __name__ == "__main__":
    unittest.main()
