import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DurationAndPurchaseInformationPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.duration_policy = (ROOT / "references" / "clip-selection-policy.md").read_text(encoding="utf-8")
        cls.editorial_policy = (ROOT / "references" / "editorial-policy.md").read_text(encoding="utf-8")
        cls.final_check = (ROOT / "references" / "final-check.md").read_text(encoding="utf-8")

    def test_first_draft_uses_the_90_second_target_and_explicit_review_tiers(self):
        for phrase in (
            "90–95 秒为优先区间",
            "95–100 秒进入复核",
            "超过 100 秒启动专项优化",
            "120 秒原始时长对应 100 秒播放复核线",
            "写出正文前建立本条成片的时长预算",
            "必要内容仍超过 100 秒时，逐项说明保留依据",
        ):
            with self.subTest(phrase=phrase):
                self.assertTrue(phrase in self.duration_policy, f"Missing duration policy phrase: {phrase}")

    def test_purchase_information_competition_preserves_distinct_value_within_a_theme(self):
        for phrase in (
            "购买信息单元",
            "不得按主题粗暴去重",
            "新增事实、证据、体验、条件、场景或选择帮助",
            "有效候选删除追溯",
            "不同肤色、妆容条件分别保留",
            "同主题内的信息单元逐项比较",
        ):
            with self.subTest(phrase=phrase):
                self.assertTrue(phrase in self.editorial_policy, f"Missing purchase information phrase: {phrase}")

    def test_final_review_checks_deleted_candidates_and_full_information_coverage(self):
        self.assertTrue("有效候选删除追溯" in self.final_check, "Missing deletion trace in final review")
        self.assertTrue("独立信息覆盖复核" in self.final_check, "Missing independent coverage review")
        self.assertTrue("每条成片分别核对" in self.final_check, "Missing per-cut coverage review")

    def test_five_part_text_only_delivery_remains_frozen(self):
        contract = (ROOT / "references" / "runtime-contract.md").read_text(encoding="utf-8")
        self.assertIn("固定五部分交付", contract)
        self.assertIn("只交付纯文本，不引入画面辅助", contract)
        self.assertIn("不添加第六部分", contract)


if __name__ == "__main__":
    unittest.main()
