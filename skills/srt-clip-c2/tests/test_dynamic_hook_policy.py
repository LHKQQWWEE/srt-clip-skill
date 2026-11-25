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
        self.assertIn("承接须依据当前原话动态延续或增强观看动力", policy)
        for bridge in ("情绪感染", "视觉/动作期待", "种草兴趣", "具体购买收益"):
            self.assertIn(bridge, policy)
        self.assertNotIn("共情入口优先", policy)
        self.assertNotIn("优先层级", policy)

    def test_joint_opening_uses_two_windows_and_reference_only_timing(self) -> None:
        policy = read("references/editorial-policy.md")
        contract = read("references/runtime-contract.md")
        self.assertIn("联合编排为一个连续开头单元", policy)
        self.assertIn("前 2 秒能否吸引注意", policy)
        self.assertIn("前 5 秒能否把观看兴趣连续承接下去", policy)
        self.assertIn("默认以 1.2 倍速", policy)
        self.assertIn("原素材累计 2.4 秒", policy)
        self.assertIn("原素材累计 6 秒", policy)
        self.assertIn("不是选段资格线或硬剪辑点", policy)
        self.assertIn("不得为对齐时间硬截完整原话", policy)
        self.assertIn("前 2 秒吸引力", contract)
        self.assertIn("前 5 秒连续吸引力", contract)
        self.assertIn("不得硬截完整原话", contract)

    def test_full_product_pool_precedes_joint_hook_comparison(self) -> None:
        policy = read("references/editorial-policy.md")
        contract = read("references/runtime-contract.md")
        self.assertLess(policy.index("完整读取目标商品全部有效窗口"), policy.index("联合编排为一个连续开头单元"))
        self.assertIn("全部有效卖点信息池", policy)
        self.assertIn("跨主题比较", policy)
        self.assertIn("真实原话", policy)
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
        self.assertIn("真实喜爱", policy)
        self.assertIn("动作展示", policy)
        self.assertIn("视觉好奇", policy)

    def test_active_rule_surfaces_remove_previous_fixed_hook_hierarchy(self) -> None:
        surfaces = (
            "SKILL.md", "README.md", "START-HERE.md", "ENVIRONMENT.md",
            "agents/openai.yaml", "C2-Universal-Portable.md",
            "references/editorial-policy.md", "references/runtime-contract.md",
            "references/ai-first-constitution.md", "references/highlight-selection.md",
            "references/final-check.md", "references/long-context-mode.md",
            "references/update-protocol.md", "references/runtime-current.md",
            "references/execution-summary.json", "tests/quality-rubric.md",
            "tests/dynamic-hook-regression-0.4.29.md",
            "tests/test_runtime_contract.py", "tests/test_rule_integrity.py",
        )
        stale_phrases = (
            "共情入口优先", "按共情优先顺序", "共情优先层级",
            "比较顺序为：有原话依据的真实顾客困扰",
            "开头尽早在前三秒形成吸引力", "不得为凑足前三秒而硬截",
        )
        for relative in surfaces:
            content = read(relative)
            for phrase in stale_phrases:
                with self.subTest(file=relative, phrase=phrase):
                    self.assertNotIn(phrase, content)

    def test_optional_selection_schema_does_not_create_type_or_timing_gate(self) -> None:
        schema = json.loads(read("scripts/selection.schema.json"))
        opening = schema["properties"]["opening_choice"]
        self.assertNotIn("priority", opening["properties"])
        self.assertNotIn("score", opening["properties"])
        self.assertIn("No fixed hook type, order, weight, or score", opening["description"])
        self.assertIn("never hard cuts", opening["description"])
        self.assertIn("not a workflow dependency", opening["description"])

    def test_regression_matrix_covers_joint_windows_and_adaptive_bridges(self) -> None:
        matrix = read("tests/dynamic-hook-regression-0.4.29.md")
        for term in ("前 2 秒", "前 5 秒", "1.2 倍速", "2.4 秒", "6 秒", "不得硬切", "承接动力"):
            self.assertIn(term, matrix)
        for term in ("场景 A", "场景 B", "场景 C", "场景 D", "场景 E", "不固定类型", "不能确认动作"):
            self.assertIn(term, matrix)
        self.assertIn("文本判断不声称平台实际完播或转化提升", matrix)

    def test_versions_summary_runtime_and_mirror_agree(self) -> None:
        plugin_root = ROOT.parent.parent
        plugin = json.loads((plugin_root / "plugin.json").read_text(encoding="utf-8"))
        core_version = (plugin_root / "VERSION").read_text(encoding="utf-8").strip()
        skill_version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        manifest = json.loads(read("references/runtime-manifest.json"))
        summary = json.loads(read("references/execution-summary.json"))
        self.assertEqual(core_version, "0.4.7")
        self.assertEqual(skill_version, "0.4.29")
        self.assertEqual(plugin["version"], "0.4.29")
        self.assertEqual(manifest["core_version"], core_version)
        self.assertEqual(manifest["skill_version"], skill_version)
        self.assertEqual(summary["core_version"], core_version)
        self.assertEqual(summary["skill_version"], skill_version)
        self.assertIn("前 2 秒", summary["summary"])
        self.assertIn("前 5 秒", summary["summary"])
        plugin_text = (plugin_root / "plugin.json").read_text(encoding="utf-8")
        self.assertIn("前2秒吸引力", plugin_text)
        self.assertIn("前5秒连续吸引力", plugin_text)
        for phrase in ("共情入口优先", "按共情优先顺序", "共情优先层级"):
            self.assertNotIn(phrase, plugin_text)
        for relative, digest in manifest["source_hashes"].items():
            self.assertEqual(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(), digest)
        runtime_digest = hashlib.sha256((ROOT / "references/runtime-current.md").read_bytes()).hexdigest()
        self.assertEqual(runtime_digest, manifest["runtime_sha256"])
        mirrored = plugin_root / ".agents/skills/srt-clip-c2"
        for path in ROOT.rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts:
                other = mirrored / path.relative_to(ROOT)
                self.assertTrue(other.is_file(), str(other))
                self.assertEqual(path.read_bytes(), other.read_bytes(), str(path.relative_to(ROOT)))


if __name__ == "__main__":
    unittest.main()
