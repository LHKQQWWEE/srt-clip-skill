import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class PurchaseReasonPolicyTests(unittest.TestCase):
    def test_complete_reason_keeps_evidence_and_conditions(self):
        policy = read("references/clip-selection-policy.md")
        self.assertIn("完整购买理由须让顾客理解具体结果、用途或待解决问题", policy)
        self.assertIn("保留成立所需的证据、适配条件和限制", policy)
        self.assertIn("行动口号不单独构成购买理由", policy)

    def test_every_plan_is_independent_and_long_form_omissions_are_visible(self):
        policy = read("references/clip-selection-policy.md")
        self.assertIn("每条独立覆盖完整有效卖点", policy)
        self.assertIn("超长预设", policy)
        self.assertIn("逐项说明被省略的有效信息", policy)

    def test_empathy_first_opening_and_customer_value_remain(self):
        editorial = read("references/editorial-policy.md")
        self.assertIn("共情入口优先", editorial)
        self.assertIn("具体可信", editorial)
        self.assertIn("颜色、搭配、材质或外观表达不按关键词禁用或排除", editorial)

    def test_under_limit_preserves_valid_points_but_overlong_is_dynamic(self):
        policy = read("references/clip-selection-policy.md")
        self.assertIn("预计不超过 120 秒时，必须保留该方案全部有效卖点", policy)
        self.assertIn("只在确有必要时筛除", policy)
        self.assertIn("不得固定某些卖点永远低价值", policy)
        self.assertIn("略超 120 秒", policy)

    def test_repetition_policy_still_uses_semantic_increments(self):
        editorial = read("references/editorial-policy.md")
        self.assertIn("先判同事实", editorial)
        self.assertIn("新增信息", editorial)
        self.assertIn("说服增量", editorial)

    def test_global_bans_remain_scoped_and_category_neutral(self):
        rules = read("references/global-rules.md")
        self.assertIn("羊毛", rules)
        self.assertIn("羊绒", rules)
        self.assertIn("防静电不是正式禁词", rules)

    def test_only_one_hundred_twenty_seconds_is_the_duration_boundary(self):
        policy = read("references/clip-selection-policy.md")
        final_check = read("references/final-check.md")
        self.assertIn("120 秒不是目标，也不是硬上限", policy)
        self.assertIn("明显超过 120 秒", policy)
        self.assertIn("不硬截时长", policy)
        for text in (policy, final_check):
            for unsupported in ("45 秒", "45秒", "130 秒", "130秒"):
                self.assertNotIn(unsupported, text)

    def test_default_dual_plan_has_no_pause(self):
        policy = read("references/clip-selection-policy.md")
        contract = read("references/runtime-contract.md")
        self.assertIn("默认直接生成两条", policy)
        self.assertIn("不得暂停等待用户选择", policy)
        self.assertNotIn("暂停生成正式成片", contract)


if __name__ == "__main__":
    unittest.main()
