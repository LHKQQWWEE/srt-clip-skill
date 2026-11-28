import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DurationAndPurchaseInformationPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.duration_policy = (ROOT / "references" / "clip-selection-policy.md").read_text(encoding="utf-8")
        cls.promotion_policy = (ROOT / "references" / "promotion-policy.md").read_text(encoding="utf-8")
        cls.final_check = (ROOT / "references" / "final-check.md").read_text(encoding="utf-8")

    def test_duration_uses_installed_90_second_target_without_new_fixed_tiers(self):
        self.assertIn("全片统一按 1.2 倍速估算", self.duration_policy)
        self.assertIn("90 秒是有效信息密度目标", self.duration_policy)
        self.assertIn("100 秒可作为可接受参考", self.duration_policy)
        for phrase in ("90–95 秒为优先区间", "95–100 秒进入复核", "120 秒原始时长对应"):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, self.duration_policy)

    def test_purchase_information_competition_preserves_distinct_value(self):
        for phrase in (
            "一个真实、完整的购买决策或顾虑回应作为语义单元",
            "不拼接不同顾客的问答，不混合不同商品或款式",
            "候选被识别不等于必须入片",
            "最小完整组合",
            "不同顾客条件和独立购买信息是否保留",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.promotion_policy)

    def test_omitted_independent_candidates_keep_a_traceable_reason(self):
        self.assertIn("未选理由", self.promotion_policy)
        self.assertIn("对应保留原话或仍待覆盖的信息", self.promotion_policy)
        self.assertIn("独立候选未入片时是否记录", self.final_check)

    def test_promotion_keeps_the_existing_ad_boundary_and_delivery_format(self):
        self.assertIn("现有广告合规规则", self.promotion_policy)
        self.assertIn("固定五部分", self.promotion_policy)
        self.assertIn("促单分析只整合在第三部分", self.promotion_policy)


if __name__ == "__main__":
    unittest.main()
