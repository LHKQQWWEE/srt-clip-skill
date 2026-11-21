from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = next(p for p in ROOT.parents if (p / "plugin.json").is_file())

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class C2UniversalIntegrityTests(unittest.TestCase):
    def test_skill_frontmatter_and_version(self):
        version = (PLUGIN_ROOT / "VERSION").read_text(encoding="utf-8").strip()
        text = read("SKILL.md")
        self.assertEqual(version, "0.4.6")  # Release number advances only after acceptance.
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
                self.assertNotIn("0.4.0", text)
                self.assertNotIn("0.4.1", text)

    def test_core_files_and_knowledge_packs_exist(self):
        for path in [
            "references/editorial-policy.md",
            "references/highlight-selection.md",
            "references/product-knowledge-registry.md",
            "references/global-rules.md",
            "references/final-check.md",
            "references/long-context-mode.md",
            "product-knowledge-packs/womens-fashion.md",
            "product-knowledge-packs/shoes.md",
            "product-knowledge-packs/scarves.md",
            "C2-Universal-Portable.md",
            "START-HERE.md",
        ]:
            self.assertTrue((ROOT / path).is_file(), path)

    def test_no_old_category_routing_files_remain(self):
        if (ROOT / "categories").exists():
            self.assertFalse(any(p.is_file() for p in (ROOT / "categories").rglob("*")))
        self.assertFalse((ROOT / "references/category-registry.md").exists())
        for p in [ROOT / "SKILL.md", ROOT / "references/product-knowledge-registry.md"]:
            text = p.read_text(encoding="utf-8")
            self.assertNotIn("categories/", text)
            self.assertNotIn("category-registry.md", text)

    def test_distribution_contains_only_current_release_record(self):
        acceptance_files = sorted(p.name for p in (ROOT / "tests").glob("release-*-acceptance.md"))
        self.assertEqual(set(acceptance_files), {"release-0.4.6-acceptance.md"})
        self.assertFalse((PLUGIN_ROOT / "docs" / "history").exists())
        self.assertFalse((ROOT / "references" / "qianchuan-offline.md").exists())
        self.assertFalse((ROOT / "tests" / "test_early_purchase_opportunity.py").exists())
        self.assertNotIn("docs/history", read("SKILL.md"))
        archive = PLUGIN_ROOT / "archive"
        if archive.exists():
            self.assertFalse(any(p.is_file() for p in archive.rglob("*")), str(archive))

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
        adapter = (PLUGIN_ROOT / "docs/platform-adapter-interface.md").read_text(encoding="utf-8")
        self.assertIn("1.2 倍速", skill)
        self.assertIn("45 秒是一般成片的合理下限参考", selection)
        self.assertIn("不设固定时长上限", selection)
        self.assertIn("短时长例外", selection)
        self.assertIn("取消 120 秒硬上限", skill)
        self.assertNotIn("45–120 秒", selection)
        self.assertIn("按购买价值与节奏动态确定时长", adapter)
        self.assertNotIn("45–120秒规则", adapter)
        self.assertIn("固定五部分", skill)

    def test_duplicate_highlight_policy_and_semantic_value(self):
        selection = read("references/highlight-selection.md")
        self.assertIn("泛夸赞", selection)
        self.assertIn("已被更强信息充分覆盖", selection)
        self.assertIn("单条正式方案必须覆盖全部已确认有效独立卖点", selection)
        self.assertIn("每条多视频方案也都必须覆盖同一完整卖点池", selection)
        self.assertIn("逐条复评", selection)

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
        for token in ["八项固定审查", "三条一票否决", "动态结构", "知识包"]:
            self.assertIn(token, protocol)
        self.assertIn("update-protocol.md", skill)
        self.assertIn("不增加日常剪辑流程", protocol)

    def test_portable_embeds_all_active_instruction_sources(self):
        portable = read("C2-Universal-Portable.md")
        for path in [
            "SKILL.md",
            "references/ai-first-constitution.md",
            "references/editorial-policy.md",
            "references/highlight-selection.md",
            "references/product-knowledge-registry.md",
            "references/global-rules.md",
            "references/final-check.md",
            "references/long-context-mode.md",
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
        for phrase in ["SKILL.md", "当前唯一生效", "每次触发", "完整取得", "不得凭记忆输出正式成片"]:
            self.assertIn(phrase, prompt)
        self.assertIn("references/runtime-manifest.json", prompt)
        self.assertIn("manifest.required_files", prompt)
        runtime_manifest = json.loads(read("references/runtime-manifest.json"))
        for path in runtime_manifest["required_files"]:
            self.assertTrue((ROOT / path).is_file(), path)
        long_description = manifest["extensions"]["com.openai"]["interface"]["longDescription"]
        self.assertIn("全部有效独立购买信息", long_description)
        self.assertIn("固定五部分交付", long_description)
        for detailed_rule in ["显气色", "45秒", "多条互补"]:
            self.assertNotIn(detailed_rule, prompt)

    def test_launcher_metadata_uses_current_version_and_roles(self):
        version = (PLUGIN_ROOT / "VERSION").read_text(encoding="utf-8").strip()
        start = read("START-HERE.md")
        launcher = read("agents/openai.yaml")
        for text in [start, launcher]:
            self.assertIn(version, text)
            self.assertIn("SKILL.md", text)
            self.assertNotIn("0.3.20", text)
            self.assertNotIn("0.4.0", text)
            self.assertNotIn("0.4.1", text)
        self.assertIn("当前唯一执行版本", start)
        self.assertIn("逻辑职责", start)
        self.assertIn("每次触发", launcher)
        manifest = json.loads((PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8"))
        self.assertIn("一个 AI", manifest["extensions"]["com.openai"]["interface"]["longDescription"])

    def test_plugin_manifests_match_version(self):
        version = (PLUGIN_ROOT / "VERSION").read_text(encoding="utf-8").strip()
        manifest = json.loads((PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8"))
        codex_manifest = json.loads((PLUGIN_ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        package_version = manifest["version"]
        self.assertEqual(manifest["name"], "srt-clip-c2")
        self.assertEqual(codex_manifest["version"], package_version)
        self.assertIn(f"SRT Clip C2 Universal {version}", read("SKILL.md"))
        self.assertIn(version, manifest["extensions"]["com.openai"]["interface"]["displayName"])
        self.assertIn(version, codex_manifest["interface"]["displayName"])
        self.assertEqual(manifest["extensions"]["com.openai"]["interface"]["defaultPrompt"],
                         codex_manifest["interface"]["defaultPrompt"])

    def test_user_designated_prohibited_terms_are_unconditional_and_scoped(self):
        rules = read("references/global-rules.md")
        section = rules.split("## 正式禁用词库", 1)[1].split("\n## ", 1)[0]
        terms = set(re.findall(r"^\s*-\s+`([^`]+)`", section, flags=re.MULTILINE))
        self.assertEqual(terms, {"羊毛", "皮草", "羊绒", "特殊动物绒", "全金纺半高领"})
        for phrase in ["## 正式禁用词库", "`羊毛`", "匹配证明不能豁免此词", "`羊绒`：", "直接匹配字面词及其组合", "防静电不是正式禁词", "只排除实际命中的完整字幕序号"]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, rules)
        self.assertNotIn("条件性正式拦截", rules)
        self.assertNotIn("证明匹配时，本条不触发正式拦截", rules)
        self.assertIn("只排除命中的完整字幕序号", rules)

    def test_superseded_historical_compliance_notes_are_not_distributed(self):
        rules = read("references/global-rules.md")
        self.assertNotIn("历史审核背景", rules)
        self.assertNotIn("有匹配证明即可保留羊毛宣传", rules)
        self.assertFalse((ROOT / "references/qianchuan-offline.md").exists())


if __name__ == "__main__":
    unittest.main()
