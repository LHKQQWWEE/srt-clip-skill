import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENTRY = (ROOT / "SKILL.md").read_text(encoding="utf-8")
ADVISORY = (ROOT / "references" / "commerce-advisory.md").read_text(encoding="utf-8")
PLUGIN = json.loads((ROOT.parents[1] / "plugin.json").read_text(encoding="utf-8"))
PROMPT = PLUGIN["extensions"]["com.openai"]["interface"]["defaultPrompt"]


class CommerceAdvisoryPolicyTests(unittest.TestCase):
    def test_advisory_mode_is_discoverable_and_separate_from_srt_delivery(self):
        self.assertIn("抖音电商增长/带货建议", ENTRY)
        self.assertIn("先读 references/commerce-advisory.md", ENTRY)
        self.assertIn("纯 SRT 文案仍按 C2 既有流程和固定五部分格式交付", ENTRY)

    def test_advice_distinguishes_evidence_and_gives_actionable_measurement(self):
        for phrase in ("已知事实", "推断", "待核实", "可观察指标", "一个最关键的问题"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, ADVISORY)
        self.assertIn("不保证结果", ADVISORY)
        self.assertIn("可直接使用的内容", ADVISORY)

    def test_current_platform_research_is_not_blocked_by_the_srt_tool_boundary(self):
        start_here = (ROOT / "START-HERE.md").read_text(encoding="utf-8")
        self.assertIn("仅限日常 SRT", ENTRY)
        self.assertIn("平台规则", ADVISORY)
        self.assertIn("官方权威来源", ADVISORY)
        self.assertIn("仅限日常 SRT", start_here)

    def test_major_workflow_plan_waits_before_creating_full_deliverable(self):
        self.assertIn("重要既有工作流作重大调整", ADVISORY)
        self.assertIn("停下等待用户确认", ADVISORY)
        self.assertIn("不预写完整新话术、SOP", ADVISORY)
        self.assertIn("仍是确认前实施", ADVISORY)

    def test_plugin_prompt_exposes_the_advisory_mode(self):
        self.assertIn("Skill 0.4.47", PROMPT)
        self.assertIn("重大工作流调整先给方案并等确认", PROMPT)
        self.assertIn("全部达到现有质量门槛且彼此实质不同", PROMPT)

    def test_plugin_launcher_scopes_tools_and_shows_the_90_second_review(self):
        plugin_start = (ROOT.parents[1] / "START-HERE.md").read_text(encoding="utf-8")
        self.assertIn("工具边界仅限日常 SRT", plugin_start)
        self.assertIn("电商咨询涉及最新平台规则时，可按需核对官方权威来源", plugin_start)
        self.assertIn("超过 90 秒比较", plugin_start)


if __name__ == "__main__":
    unittest.main()
