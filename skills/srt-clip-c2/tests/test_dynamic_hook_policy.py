from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


class DynamicHookPolicyTests(unittest.TestCase):
    def test_policy_uses_customer_motivation_without_fixed_hook_hierarchy(self) -> None:
        policy = read("references/editorial-policy.md")
        self.assertIn("动态顾客心理驱动钩子机制", policy)
        self.assertIn("陌生潜在买家", policy)
        self.assertIn("继续观看欲望", policy)
        self.assertIn("与商品相关的购买兴趣", policy)
        for dimension in ("情绪感染", "视觉引导", "好奇期待", "审美种草", "场景代入", "共情", "需求与收益", "自然原生感"):
            self.assertIn(dimension, policy)
        self.assertIn("不设置固定钩子类型优先级", policy)
        self.assertIn("权重、分数或额外语义轮次", policy)
        self.assertIn("不预设种草或共情优先", policy)
        self.assertNotIn("共情入口优先", policy)
        self.assertNotIn("优先层级", policy)

    def test_full_product_pool_precedes_local_hook_comparison(self) -> None:
        policy = read("references/editorial-policy.md")
        contract = read("references/runtime-contract.md")
        self.assertLess(policy.index("完整读取目标商品"), policy.index("比较开头"))
        self.assertIn("全部有效卖点信息池", policy)
        self.assertIn("跨主题比较", policy)
        self.assertIn("真实原话", policy)
        self.assertIn("必要紧邻承接", policy)
        self.assertIn("不比较、评分或排名完整成片", policy)
        self.assertLess(contract.index("3. 在同一次语义分析"), contract.index("4. 信息池完成后"))

    def test_truth_and_srt_visual_limits_remain_hard_boundaries(self) -> None:
        policy = read("references/editorial-policy.md")
        self.assertIn("商品归属", policy)
        self.assertIn("正式合规", policy)
        self.assertIn("自然语义", policy)
        self.assertIn("后文兑现", policy)
        self.assertIn("仅凭 SRT", policy)
        self.assertIn("不能确认实际画面", policy)
        self.assertIn("不能确认主播的真实语气、表情或情绪表现", policy)

    def test_opening_is_an_entry_not_a_reason_to_drop_body_or_source_cta(self) -> None:
        policy = read("references/editorial-policy.md")
        selection = read("references/clip-selection-policy.md")
        self.assertIn("每条方案继续覆盖全部有效卖点", policy)
        self.assertIn("原文保留适用且合规的促单", policy)
        self.assertIn("常规时长方案须覆盖信息池全部有效卖点", selection)
        self.assertIn("开头尽早在前三秒形成吸引力", policy)
        self.assertIn("不得为凑足前三秒而硬截", policy)
        self.assertIn("真实喜爱", policy)
        self.assertIn("动作展示", policy)
        self.assertIn("视觉好奇", policy)

    def test_active_rule_surfaces_no_longer_teach_fixed_hook_hierarchy(self) -> None:
        surfaces = (
            "SKILL.md", "README.md", "START-HERE.md", "ENVIRONMENT.md",
            "agents/openai.yaml", "C2-Universal-Portable.md",
            "references/editorial-policy.md", "references/runtime-contract.md",
            "references/ai-first-constitution.md", "references/highlight-selection.md",
            "references/final-check.md", "references/long-context-mode.md",
            "references/update-protocol.md", "references/runtime-current.md",
            "references/execution-summary.json", "tests/quality-rubric.md",
            "tests/dynamic-hook-regression-0.4.28.md",
            "tests/test_runtime_contract.py", "tests/test_rule_integrity.py",
        )
        stale_phrases = ("共情入口优先", "按共情优先顺序", "共情优先层级", "比较顺序为：有原话依据的真实顾客困扰")
        for relative in surfaces:
            content = read(relative)
            for phrase in stale_phrases:
                with self.subTest(file=relative, phrase=phrase):
                    if phrase in content:
                        self.fail(f"{relative} contains obsolete rule phrase: {phrase}")

    def test_optional_selection_schema_does_not_force_a_hook_type(self) -> None:
        schema = json.loads(read("scripts/selection.schema.json"))
        opening = schema["properties"]["opening_choice"]
        self.assertNotIn("priority", opening["properties"])
        self.assertIn("No fixed hook category, priority, weight, or score", opening["description"])

    def test_regression_matrix_covers_other_categories_and_rational_hooks(self) -> None:
        matrix = read("tests/dynamic-hook-regression-0.4.28.md")
        for term in ("马甲", "鞋类", "家居收纳", "强理性钩子", "SRT"):
            self.assertIn(term, matrix)
        self.assertIn("不固化", matrix)
        self.assertIn("只凭字幕不能认定", matrix)

    def test_versions_summary_and_generated_runtime_agree(self) -> None:
        plugin_root = ROOT.parent.parent
        plugin = json.loads((plugin_root / "plugin.json").read_text(encoding="utf-8"))
        core_version = (plugin_root / "VERSION").read_text(encoding="utf-8").strip()
        skill_version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        manifest = json.loads(read("references/runtime-manifest.json"))
        summary = json.loads(read("references/execution-summary.json"))
        self.assertEqual(core_version, "0.4.7")
        self.assertEqual(skill_version, "0.4.28")
        self.assertEqual(plugin["version"], "0.4.28")
        self.assertEqual(manifest["core_version"], core_version)
        self.assertEqual(manifest["skill_version"], skill_version)
        self.assertEqual(summary["core_version"], core_version)
        self.assertEqual(summary["skill_version"], skill_version)
        self.assertIn("动态顾客心理驱动钩子机制", summary["summary"])
        plugin_text = (plugin_root / "plugin.json").read_text(encoding="utf-8")
        self.assertIn("动态顾客心理驱动钩子机制", plugin_text)
        for phrase in ("共情入口优先", "按共情优先顺序", "共情优先层级"):
            self.assertNotIn(phrase, plugin_text)
        for relative, digest in manifest["source_hashes"].items():
            self.assertEqual(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(), digest)
        runtime_digest = hashlib.sha256((ROOT / "references/runtime-current.md").read_bytes()).hexdigest()
        self.assertEqual(runtime_digest, manifest["runtime_sha256"])


if __name__ == "__main__":
    unittest.main()
