from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT
PLUGIN_ROOT = next(p for p in ROOT.parents if (p / "plugin.json").is_file())

class C2UniversalIntegrityTests(unittest.TestCase):
    def test_skill_frontmatter_and_version(self):
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: srt-clip-c2\n"))
        self.assertIn("SRT Clip C2 Universal " + (PLUGIN_ROOT / "VERSION").read_text(encoding="utf-8").strip(), text)
        front = text.split("---", 2)[1]
        for trigger in ["srt文案", "srt切片文案", "str文案", "C2完整精简版"]:
            self.assertIn(trigger, front)
        self.assertNotIn("“切片文案”", front)

    def test_core_files_exist(self):
        for path in [
            "references/editorial-policy.md",
            "references/highlight-selection.md",
            "references/category-registry.md",
            "references/global-rules.md",
            "references/final-check.md",
            "references/qianchuan-offline.md",
            "categories/womens-fashion.md",
            "C2-Universal-Portable.md",
            "START-HERE.md",
        ]:
            self.assertTrue((SKILL_DIR / path).is_file(), path)

    def test_no_old_mandatory_workflow_in_active_rules(self):
        active = [
            (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8"),
            (SKILL_DIR / "references/highlight-selection.md").read_text(encoding="utf-8"),
            (SKILL_DIR / "references/final-check.md").read_text(encoding="utf-8"),
        ]
        combined = "\n".join(active)
        for old in ["workflow_gate.py", "multi_plan.py", "check_highlights.py", "highlights.json", "workflow.json"]:
            self.assertNotIn(old, combined)

    def test_duration_and_output_rules(self):
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("1.2", text)
        self.assertIn("120 秒", text)
        self.assertIn("固定五部分", text)

    def test_offline_compliance_trigger(self):
        text = (SKILL_DIR / "references/qianchuan-offline.md").read_text(encoding="utf-8")
        self.assertIn("审核截图", text)
        self.assertIn("明确指定词句", text)
        self.assertIn("日常离线使用", text)

    def test_benchmark_has_ten_cases_and_no_raw_transcripts(self):
        text = (SKILL_DIR / "tests/benchmark-cases.md").read_text(encoding="utf-8")
        self.assertEqual(len(re.findall(r"\| B\d{2} \|", text)), 10)
        self.assertIn("不包含任何原始 SRT 行", text)

    def test_duplicate_highlight_policy(self):
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        detail = (SKILL_DIR / "references/highlight-selection.md").read_text(encoding="utf-8")
        self.assertIn("最多保留两处", text)
        self.assertIn("已由更强片段充分覆盖", detail)

    def test_purchase_information_priority_and_semantic_dedup(self):
        selection = (SKILL_DIR / "references/highlight-selection.md").read_text(encoding="utf-8")
        editorial = (SKILL_DIR / "references/editorial-policy.md").read_text(encoding="utf-8")
        for token in ["卖点决定“留不留”，结构决定“怎么排”", "购买决策信息", "真正语义重复", "同类别的不同事实", "真实反差"]:
            self.assertIn(token, selection)
        self.assertIn("主题先后只影响编排，不决定卖点去留", editorial)
        self.assertNotIn("一个商品主题通常先讲清楚", editorial)

    def test_no_extra_semantic_stages(self):
        long_mode = (SKILL_DIR / "references/long-context-mode.md").read_text(encoding="utf-8")
        self.assertIn("不另设主题分析、卖点池建立、遗漏扫描", long_mode)
        self.assertNotIn("单一卖点池", long_mode)
        self.assertNotIn("反向漏检（Reverse Coverage Check）", long_mode)
        self.assertNotIn("先建立高价值候选集", long_mode)

    def test_duration_trim_order(self):
        selection = (SKILL_DIR / "references/highlight-selection.md").read_text(encoding="utf-8")
        order = ["真正语义重复的信息", "没有信息增量的重复夸赞", "购买决策价值较低的内容", "已由更强片段充分覆盖", "舍弃部分独立有效卖点"]
        positions = [selection.index(term) for term in order]
        self.assertEqual(positions, sorted(positions))

    def test_ai_first_constitution(self):
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        constitution = (SKILL_DIR / "references/ai-first-constitution.md").read_text(encoding="utf-8")
        self.assertIn("AI-First Constitution", text)
        self.assertIn("最高架构约束", constitution)
        self.assertIn("不能替代这些语义决策", text)
        self.assertIn("工具不可用", constitution)

    def test_update_protocol_governance_only(self):
        protocol = (SKILL_DIR / "references/update-protocol.md").read_text(encoding="utf-8")
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        portable = (SKILL_DIR / "C2-Universal-Portable.md").read_text(encoding="utf-8")
        for token in ["六项固定审查", "三条一票否决", "质量不退步", "环境零强制", "仅约束未来版本"]:
            if token == "仅约束未来版本":
                self.assertIn("不增加每次使用", protocol)
            else:
                self.assertIn(token, protocol)
        self.assertIn("references/update-protocol.md", skill)
        self.assertIn("## 附录｜固定版本更新协议", portable)
        self.assertIn("固定五部分交付", skill)

    def test_long_context_mode(self):
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        long_mode = (SKILL_DIR / "references/long-context-mode.md").read_text(encoding="utf-8")
        self.assertIn("Long Context Mode", text)
        self.assertIn("2000条", long_mode)
        self.assertIn("多方案共享同一次", long_mode)
        self.assertNotIn("反向漏检（Reverse Coverage Check）", long_mode)
        self.assertNotIn("必须调用 Python", long_mode)

    def test_no_hard_tool_dependency_language(self):
        active = "\n".join([
            (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8"),
            (SKILL_DIR / "references/ai-first-constitution.md").read_text(encoding="utf-8"),
            (SKILL_DIR / "references/long-context-mode.md").read_text(encoding="utf-8"),
        ])
        forbidden = ["Python 不可用则无法交付", "必须运行脚本后才能", "未运行程序不得交付"]
        for token in forbidden:
            self.assertNotIn(token, active)

    def test_global_cue_exclusion_contract(self):
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        global_rules = (SKILL_DIR / "references/global-rules.md").read_text(encoding="utf-8")
        women = (SKILL_DIR / "categories/womens-fashion.md").read_text(encoding="utf-8")
        for content in [skill, global_rules, women]:
            self.assertIn("原始字幕序号", content)
        self.assertIn("审核截图", skill)
        self.assertIn("语义", global_rules)
        self.assertNotIn("只删除含违规内容的句子", women)
        self.assertNotIn("命中时按完整句删除", global_rules)

    def test_universal_topic_policy(self):
        core = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        global_rules = (SKILL_DIR / "references/global-rules.md").read_text(encoding="utf-8")
        fashion = (SKILL_DIR / "categories/womens-fashion.md").read_text(encoding="utf-8")
        self.assertIn("通用核心不得强制加入其他类目的话题", core)
        self.assertIn("不是 Universal 全局固定话题", global_rules)
        self.assertIn("#穿搭", fashion)
        self.assertIn("#时尚营销", fashion)

    def test_publisher_default_prompt_compatibility(self):
        manifest = json.loads((PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8"))
        prompt = manifest["extensions"]["com.openai"]["interface"]["defaultPrompt"]
        self.assertIn("C2 Universal 0.3.11", prompt)
        self.assertIn("Long Context Mode", prompt)
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("发布兼容字段", skill)

    def test_plugin_manifest(self):
        manifest = json.loads((PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "srt-clip-c2")
        self.assertEqual(manifest["version"], (PLUGIN_ROOT / "VERSION").read_text(encoding="utf-8").strip())
        self.assertEqual(manifest["extensions"]["com.openai"]["interface"]["shortDescription"], "AI主导，跨平台带货剪辑")

if __name__ == "__main__":
    unittest.main()
