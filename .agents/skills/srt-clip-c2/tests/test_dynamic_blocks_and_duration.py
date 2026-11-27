import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DynamicBlocksAndDurationTests(unittest.TestCase):
    def test_duration_policy_has_target_tolerance_and_review_without_old_threshold(self):
        policy = (ROOT / "references" / "clip-selection-policy.md").read_text(encoding="utf-8")
        self.assertIn("90 秒是有效信息密度目标", policy)
        self.assertIn("默认按 1.2 倍速估算", policy)
        self.assertIn("100 秒可作为可接受参考", policy)
        self.assertIn("超过 100 秒", policy)
        self.assertIn("超过 90 秒时", policy)
        self.assertIn("不得自动截断", policy)
        self.assertIn("完整覆盖", policy)
        self.assertIn("低价值完整板块", policy)
        self.assertIsNone(re.search(r"\b120\s*秒", policy))

    def test_reference_surfaces_keep_the_same_two_duration_review_stages(self):
        policy = (ROOT / "references" / "clip-selection-policy.md").read_text(encoding="utf-8")
        editorial = (ROOT / "references" / "editorial-policy.md").read_text(encoding="utf-8")
        highlight = (ROOT / "references" / "highlight-selection.md").read_text(encoding="utf-8")
        for surface in (editorial, highlight):
            self.assertIn("超过 90 秒", surface)
            self.assertIn("超过 100 秒", surface)
        self.assertIn("完整覆盖所有有效卖点", policy)

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
        role = schema["properties"]["roles"]["items"]["properties"]
        self.assertIn("cta_type", role)
        self.assertIn("transaction_info", role)


if __name__ == "__main__":
    unittest.main()
