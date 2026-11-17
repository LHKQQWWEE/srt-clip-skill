from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = next(p for p in ROOT.parents if (p / "plugin.json").is_file())

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class C2UniversalIntegrityTests(unittest.TestCase):
    def test_skill_frontmatter_and_version(self):
        version = (PLUGIN_ROOT / "VERSION").read_text(encoding="utf-8").strip()
        text = read("SKILL.md")
        self.assertEqual(version, "0.4.0")
        self.assertTrue(text.startswith("---\nname: srt-clip-c2\n"))
        self.assertIn(f"SRT Clip C2 Universal {version}", text)
        front = text.split("---", 2)[1]
        for trigger in ["srt文案", "srt切片文案", "str文案", "C2完整精简版"]:
            self.assertIn(trigger, front)
        self.assertNotIn("“切片文案”", front)

    def test_one_current_version_on_loadable_entries(self):
        version = (PLUGIN_ROOT / "VERSION").read_text(encoding="utf-8").strip()
        entries = [
            read("SKILL.md"),
            read("README.md"),
            read("START-HERE.md"),
            read("ENVIRONMENT.md"),
            read("C2-Universal-Portable.md"),
            read("agents/openai.yaml"),
            (PLUGIN_ROOT / "README.md").read_text(encoding="utf-8"),
            (PLUGIN_ROOT / "START-HERE.md").read_text(encoding="utf-8"),
            (PLUGIN_ROOT / "docs/platform-adapter-interface.md").read_text(encoding="utf-8"),
        ]
        for index, text in enumerate(entries):
            with self.subTest(entry=index):
                self.assertIn(version, text)
                self.assertNotIn("0.3.19", text)
                self.assertNotIn("0.3.20", text)

    def test_core_files_and_knowledge_packs_exist(self):
        for path in [
            "references/editorial-policy.md",
            "references/highlight-selection.md",
            "references/product-knowledge-registry.md",
            "references/global-rules.md",
            "references/final-check.md",
            "references/long-context-mode.md",
            "references/qianchuan-offline.md",
            "product-knowledge-packs/womens-fashion.md",
            "product-knowledge-packs/shoes.md",
            "product-knowledge-packs/scarves.md",
            "C2-Universal-Portable.md",
            "START-HERE.md",
        ]:
            self.assertTrue((ROOT / path).is_file(), path)

    def test_no_old_category_routing_files_remain(self):
        self.assertFalse((ROOT / "categories").exists())
        self.assertFalse((ROOT / "references/category-registry.md").exists())
        for p in [ROOT / "SKILL.md", ROOT / "references/product-knowledge-registry.md"]:
            text = p.read_text(encoding="utf-8")
            self.assertNotIn("categories/", text)
            self.assertNotIn("category-registry.md", text)

    def test_distribution_contains_only_current_release_record(self):
        acceptance_files = sorted(p.name for p in (ROOT / "tests").glob("release-*-acceptance.md"))
        self.assertEqual(acceptance_files, ["release-0.4.0-acceptance.md"])
        for directory in [PLUGIN_ROOT / "archive", PLUGIN_ROOT / "docs" / "history"]:
            if directory.exists():
                self.assertFalse(any(p.is_file() for p in directory.rglob("*")), str(directory))

    def test_no_old_mandatory_workflow_in_active_rules(self):
        active = "\n".join([
            read("SKILL.md"),
            read("references/highlight-selection.md"),
            read("references/final-check.md"),
            read("references/long-context-mode.md"),
        ])
        for old in ["workflow_gate.py", "multi_plan.py", "check_highlights.py", "highlights.json", "workflow.json"]:
            self.assertNotIn(old, active)

    def test_duration_and_output_rules(self):
        skill = read("SKILL.md")
        selection = read("references/highlight-selection.md")
        self.assertIn("1.2 倍速", skill)
        for phrase in ["45–120 秒", "45–90 秒", "90–120 秒"]:
            self.assertIn(phrase, selection)
        self.assertIn("120 秒", skill)
        self.assertIn("固定五部分", skill)

    def test_duplicate_highlight_policy_and_semantic_value(self):
        selection = read("references/highlight-selection.md")
        self.assertIn("重复夸赞", selection)
        self.assertIn("已被更强信息充分覆盖", selection)
        self.assertIn("独立高决策价值理由", selection)

    def test_ai_first_organization_and_dynamic_structure(self):
        skill = read("SKILL.md")
        constitution = read("references/ai-first-constitution.md")
        self.assertIn("一个 AI、一次语义分析、一次终检", skill)
        self.assertIn("Chief Decision Editor", skill)
        self.assertIn("AI-First Constitution", constitution)
        self.assertIn("产品知识包只提供属性事实提醒", constitution)
        self.assertIn("不按品类预设", skill)

    def test_update_protocol_is_development_only(self):
        protocol = read("references/update-protocol.md")
        skill = read("SKILL.md")
        for token in ["六项固定审查", "三条一票否决", "动态结构", "知识包"]:
            self.assertIn(token, protocol)
        self.assertIn("update-protocol.md", skill)
        self.assertIn("不增加日常剪辑流程", protocol)

    def test_portable_embeds_all_active_instruction_sources(self):
        portable = read("C2-Universal-Portable.md")
        for path in [
            "SKILL.md",
            "references/editorial-policy.md",
            "references/highlight-selection.md",
            "references/product-knowledge-registry.md",
            "references/global-rules.md",
            "references/final-check.md",
            "product-knowledge-packs/womens-fashion.md",
            "product-knowledge-packs/shoes.md",
            "product-knowledge-packs/scarves.md",
        ]:
            self.assertIn(read(path).strip(), portable, path)

    def test_plugin_prompts_route_to_current_skill(self):
        manifest = json.loads((PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8"))
        codex_manifest = json.loads((PLUGIN_ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        prompt = manifest["extensions"]["com.openai"]["interface"]["defaultPrompt"]
        codex_prompt = codex_manifest["interface"]["defaultPrompt"]
        self.assertEqual(prompt, codex_prompt)
        for phrase in ["0.4.0", "SKILL.md", "当前", "动态购买决策结构"]:
            self.assertIn(phrase, prompt)
        for detailed_rule in ["显气色", "第一次购买机会", "45–120 秒", "多条互补"]:
            self.assertNotIn(detailed_rule, prompt)

    def test_launcher_metadata_uses_current_version_and_roles(self):
        version = (PLUGIN_ROOT / "VERSION").read_text(encoding="utf-8").strip()
        start = read("START-HERE.md")
        launcher = read("agents/openai.yaml")
        for text in [start, launcher]:
            self.assertIn(version, text)
            self.assertIn("SKILL.md", text)
            self.assertNotIn("0.3.20", text)
        self.assertIn("当前唯一执行版本", start)
        self.assertIn("逻辑职责", start)
        self.assertIn("同一AI", launcher)

    def test_plugin_manifests_match_version(self):
        version = (PLUGIN_ROOT / "VERSION").read_text(encoding="utf-8").strip()
        manifest = json.loads((PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8"))
        codex_manifest = json.loads((PLUGIN_ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "srt-clip-c2")
        self.assertEqual(manifest["version"], version)
        self.assertEqual(codex_manifest["version"], version)
        self.assertIn(version, manifest["extensions"]["com.openai"]["interface"]["displayName"])
        self.assertIn(version, codex_manifest["interface"]["displayName"])
        self.assertEqual(manifest["extensions"]["com.openai"]["interface"]["defaultPrompt"],
                         codex_manifest["interface"]["defaultPrompt"])


if __name__ == "__main__":
    unittest.main()
