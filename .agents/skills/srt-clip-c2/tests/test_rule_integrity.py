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

    def test_core_files_exist(self):
        for path in [
            "references/editorial-policy.md",
            "references/highlight-selection.md",
            "references/category-registry.md",
            "references/global-rules.md",
            "references/final-check.md",
            "references/long-context-mode.md",
            "references/qianchuan-offline.md",
            "categories/womens-fashion.md",
            "categories/shoes.md",
            "categories/scarves.md",
            "C2-Universal-Portable.md",
            "START-HERE.md",
        ]:
            self.assertTrue((ROOT / path).is_file(), path)

    def test_distribution_contains_only_current_release_record(self):
        acceptance_files = sorted(p.name for p in (ROOT / "tests").glob("release-*-acceptance.md"))
        self.assertEqual(acceptance_files, ["release-0.3.20-acceptance.md"])
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

    def test_duplicate_highlight_policy(self):
        selection = read("references/highlight-selection.md")
        self.assertIn("重复夸赞", selection)
        self.assertIn("已被更强信息充分覆盖", selection)

    def test_purchase_information_priority_and_semantic_dedup(self):
        selection = read("references/highlight-selection.md")
        editorial = read("references/editorial-policy.md")
        for token in ["高决策价值", "中决策价值", "弱增量", "机械覆盖率", "单位时间购买决策价值"]:
            self.assertIn(token, selection)
        self.assertIn("主题顺序只决定怎么排，不决定理由留不留", editorial)
        self.assertNotIn("先建立高价值候选集", editorial)

    def test_no_extra_semantic_stages(self):
        long_mode = read("references/long-context-mode.md")
        skill = read("SKILL.md")
        self.assertIn("不另设主题分析、卖点池", long_mode)
        self.assertIn("不是新增第二轮筛选", long_mode)
        self.assertNotIn("反向漏检（Reverse Coverage Check）", long_mode)
        self.assertNotIn("第六步：", skill)

    def test_ai_first_constitution(self):
        skill = read("SKILL.md")
        constitution = read("references/ai-first-constitution.md")
        self.assertIn("AI 主导", skill)
        self.assertIn("最高架构约束", constitution)
        self.assertIn("工具不可用", constitution)
        self.assertIn("购买决策编辑器", skill)

    def test_update_protocol_governance_only(self):
        protocol = read("references/update-protocol.md")
        skill = read("SKILL.md")
        portable = read("C2-Universal-Portable.md")
        for token in ["六项固定审查", "三条一票否决", "质量不退步", "环境零强制"]:
            self.assertIn(token, protocol)
        self.assertIn("不增加每次使用", protocol)
        self.assertIn("references/update-protocol.md", skill)
        self.assertIn("update-protocol.md", portable)
        self.assertIn("固定五部分", skill)

    def test_long_context_position_fairness(self):
        long_mode = read("references/long-context-mode.md")
        self.assertIn("前后位置公平", long_mode)
        self.assertIn("后段", long_mode)
        self.assertIn("同一组语义标准", long_mode)
        self.assertIn("不是新增第二轮筛选", long_mode)
        self.assertNotIn("必须调用 Python", long_mode)

    def test_no_hard_tool_dependency_language(self):
        active = "\n".join([
            read("SKILL.md"),
            read("references/ai-first-constitution.md"),
            read("references/long-context-mode.md"),
        ])
        for forbidden in ["Python 不可用则无法交付", "必须运行脚本后才能", "未运行程序不得交付"]:
            self.assertNotIn(forbidden, active)

    def test_global_cue_exclusion_contract(self):
        skill = read("SKILL.md")
        global_rules = read("references/global-rules.md")
        editorial = read("references/editorial-policy.md")
        self.assertIn("原始字幕编号", skill)
        self.assertIn("审核截图", skill)
        self.assertIn("语义", global_rules)
        self.assertIn("完整原始字幕序号", editorial)
        self.assertNotIn("命中时按完整句删除", global_rules)

    def test_universal_topic_policy(self):
        core = read("SKILL.md")
        global_rules = read("references/global-rules.md")
        fashion = read("categories/womens-fashion.md")
        self.assertIn("类目模块可指定最多两个类目固定话题", core)
        self.assertIn("不是 Universal 全局固定话题", global_rules)
        self.assertIn("#穿搭", fashion)
        self.assertIn("#时尚营销", fashion)

    def test_plugin_prompts_route_to_current_skill_without_business_duplicates(self):
        root_manifest = json.loads((PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8"))
        codex_manifest = json.loads((PLUGIN_ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        root_prompt = root_manifest["extensions"]["com.openai"]["interface"]["defaultPrompt"]
        codex_prompt = codex_manifest["interface"]["defaultPrompt"]
        self.assertEqual(root_prompt, codex_prompt)
        for phrase in ["0.3.20", "当前", "SKILL.md", "引用文件", "旧版副本"]:
            self.assertIn(phrase, root_prompt)
        for duplicate in ["第一次刷到", "购买决策闭环", "45–120", "多条互补"]:
            self.assertNotIn(duplicate, root_prompt)

    def test_launcher_metadata_uses_current_version_and_routes(self):
        version = (PLUGIN_ROOT / "VERSION").read_text(encoding="utf-8").strip()
        start = read("START-HERE.md")
        launcher = read("agents/openai.yaml")
        for text in [start, launcher]:
            self.assertIn(version, text)
            self.assertIn("SKILL.md", text)
            self.assertNotIn("0.3.19", text)
        self.assertIn("当前唯一执行版本", start)
        self.assertIn("不要读取或混用旧版副本", launcher)

    def test_plugin_manifests_match_version(self):
        version = (PLUGIN_ROOT / "VERSION").read_text(encoding="utf-8").strip()
        manifest = json.loads((PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8"))
        codex_manifest = json.loads((PLUGIN_ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "srt-clip-c2")
        self.assertEqual(manifest["version"], version)
        self.assertEqual(codex_manifest["version"], version)
        self.assertIn(version, manifest["extensions"]["com.openai"]["interface"]["displayName"])
        self.assertIn(version, codex_manifest["interface"]["displayName"])


if __name__ == "__main__":
    unittest.main()
