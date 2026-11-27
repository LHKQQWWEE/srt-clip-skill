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
        self.assertIn("每条常规时长方案须独立覆盖", policy)
        self.assertIn("超长预设", policy)
        self.assertIn("逐项说明被省略的有效信息", policy)

    def test_dynamic_opening_and_customer_value_remain(self):
        editorial = read("references/editorial-policy.md")
        self.assertIn("动态顾客心理驱动钩子机制", editorial)
        self.assertIn("普遍但具体、可信且有支撑的购买结果仍可胜出", editorial)
        self.assertIn("颜色、搭配、材质或外观表达不按关键词禁用或排除", editorial)

    def test_under_limit_preserves_valid_points_but_overlong_is_dynamic(self):
        policy = read("references/clip-selection-policy.md")
        self.assertIn("预计不超过 120 秒时，必须保留该方案全部有效卖点", policy)
        self.assertIn("只在确有必要时筛除", policy)
        self.assertIn("不得固定某些卖点永远低价值", policy)
        self.assertIn("略超 120 秒", policy)

    def test_repetition_policy_competes_on_approximate_expression_tasks(self):
        editorial = read("references/editorial-policy.md")
        self.assertIn("大致重复表达", editorial)
        self.assertIn("没有新增独立事实、证据、体验、条件、场景、选择帮助或必要承接", editorial)
        self.assertIn("情绪感染力、自然度、种草效果和当前上下文适配", editorial)
        self.assertIn("不是字幕文本去重、关键词匹配或主题去重", editorial)

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

    def test_selected_opening_count_drives_independent_complete_cuts(self):
        policy = read("references/clip-selection-policy.md")
        contract = read("references/runtime-contract.md")
        self.assertIn("每个已选开头分别生成一条完整成片", policy)
        self.assertIn("每条常规时长方案须独立覆盖", policy)
        self.assertNotIn("暂停生成正式成片", contract)


if __name__ == "__main__":
    unittest.main()
