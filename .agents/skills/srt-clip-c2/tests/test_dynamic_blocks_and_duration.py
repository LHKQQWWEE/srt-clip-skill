import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DynamicBlocksAndDurationTests(unittest.TestCase):
    def test_duration_policy_has_90_second_target_and_preserves_raw_120_second_mapping(self):
        policy = (ROOT / "references" / "clip-selection-policy.md").read_text(encoding="utf-8")
        self.assertIn("90 秒是有效信息密度目标", policy)
        self.assertIn("90–95 秒为优先区间", policy)
        self.assertIn("95–100 秒进入复核", policy)
        self.assertIn("超过 100 秒启动专项优化", policy)
        self.assertIn("95–100 秒进入复核", policy)
        self.assertIn("120 秒原始时长对应 100 秒播放复核线", policy)
        self.assertIn("超过 100 秒", policy)
        self.assertIn("超过 90 秒时", policy)
        self.assertIn("不得自动截断", policy)
        self.assertIn("完整覆盖", policy)
        self.assertIn("低价值完整板块", policy)
        self.assertIsNone(re.search(r"(?:成片|播放)(?:时长)?目标.{0,15}120\s*秒|120\s*秒.{0,15}(?:成片目标|播放目标)", policy))

    def test_first_pass_duration_optimization_happens_before_copy_is_written(self):
        policy = (ROOT / "references" / "clip-selection-policy.md").read_text(encoding="utf-8")
        for phrase in (
            "写出正文前建立本条成片的时长预算",
            "首稿必须以已完成容量优化的选段为基础",
            "不得等待用户指出过长后才开始压缩",
            "大致重复表达先竞争",
            "所有独立有效卖点",
        ):
            self.assertIn(phrase, policy)

    def test_hook_attention_reference_uses_the_same_speed_as_full_clip_estimate(self):
        policy = (ROOT / "references" / "clip-selection-policy.md").read_text(encoding="utf-8")
        contract = (ROOT / "references" / "runtime-contract.md").read_text(encoding="utf-8")
        editorial = (ROOT / "references" / "editorial-policy.md").read_text(encoding="utf-8")
        for text in (policy, contract):
            self.assertIn("预计成片时长 = 原始选段累计时长 ÷ 1.2", text)
        self.assertIn("沿用全片估时的 1.2 倍速", editorial)
        self.assertIn("前 2 秒约对应原素材累计 2.4 秒", editorial)
        self.assertIn("前 5 秒约对应原素材累计 6 秒", editorial)

    def test_reference_surfaces_keep_the_same_two_duration_review_stages(self):
        policy = (ROOT / "references" / "clip-selection-policy.md").read_text(encoding="utf-8")
        editorial = (ROOT / "references" / "editorial-policy.md").read_text(encoding="utf-8")
        highlight = (ROOT / "references" / "highlight-selection.md").read_text(encoding="utf-8")
        for surface in (editorial, highlight):
            self.assertIn("超过 90 秒", surface)
            self.assertIn("超过 100 秒", surface)
        self.assertIn("完整覆盖所有有效卖点", policy)
        self.assertIn("95–100 秒进入复核", policy)
        self.assertIn("超过 100 秒启动专项优化", policy)

    def test_content_boards_are_open_and_dynamically_ordered_as_units(self):
        policy = (ROOT / "references" / "clip-selection-policy.md").read_text(encoding="utf-8")
        self.assertIn("分类开放", policy)
        self.assertIn("调整板块内的原话顺序", policy)
        self.assertIn("整块动态排列板块之间的顺序", policy)
        self.assertIn("不得交叉穿插", policy)
        self.assertIn("每条成片独立确定顺序", policy)

    def test_promotion_is_separate_and_ends_with_a_compliant_original_quote(self):
        editorial = (ROOT / "references" / "editorial-policy.md").read_text(encoding="utf-8")
        policy = (ROOT / "references" / "clip-selection-policy.md").read_text(encoding="utf-8")
        self.assertIn("直接行动型", editorial)
        self.assertIn("种草/推荐/购买信心强化型", editorial)
        self.assertIn("不计入卖点支持集合", editorial)
        self.assertIn("不参与卖点价值排序", editorial)
        self.assertIn("最后的独立促单板块", editorial)
        self.assertIn("来源可核验且明确对应当前商品/SKU 的真实商品标价", editorial)
        self.assertIn("促单不豁免绝对化宣传", editorial)
        self.assertNotIn("活动素材且确认活动", editorial)
        self.assertNotIn("活动例外", editorial)
        self.assertIn("结尾促单默认排除", policy)

    def test_schema_records_open_boards_promotion_and_per_plan_duration_review(self):
        schema = json.loads((ROOT / "scripts" / "selection.schema.json").read_text(encoding="utf-8"))
        self.assertIn("content_blocks", schema["required"])
        self.assertIn("content_blocks", schema["properties"])
        self.assertIn("duration_review", schema["properties"])
        self.assertIn("stage", schema["properties"]["duration_review"]["required"])
        speed = schema["properties"]["full_clip_playback_speed"]
        self.assertEqual(speed["default"], 1.2)
        self.assertEqual(speed["const"], 1.2)
        role = schema["properties"]["roles"]["items"]["properties"]
        self.assertIn("cta_type", role)
        self.assertIn("transaction_info", role)

    def test_duration_schema_requires_the_matching_review_stage_from_95_seconds(self):
        schema = json.loads((ROOT / "scripts" / "selection.schema.json").read_text(encoding="utf-8"))
        review = schema["properties"]["duration_review"]
        self.assertEqual(
            review["properties"]["stage"]["enum"],
            ["review_95_to_100", "special_optimization_over_100"],
        )
        self.assertTrue(any("minimum" in rule.get("if", {}).get("properties", {}).get("estimated_duration_seconds", {}) for rule in schema["allOf"]))


if __name__ == "__main__":
    unittest.main()
