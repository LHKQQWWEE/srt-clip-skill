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

    def test_every_plan_is_independent_and_capacity_omissions_are_visible(self):
        policy = read("references/clip-selection-policy.md")
        self.assertIn("每条成片先完整覆盖", policy)
        self.assertIn("超过 100 秒须启动专项优化并逐条复核", policy)
        self.assertIn("逐项注明省略的完整板块", policy)

    def test_dynamic_opening_and_customer_value_remain(self):
        editorial = read("references/editorial-policy.md")
        self.assertIn("动态顾客心理驱动钩子机制", editorial)
        self.assertIn("普遍但具体、可信且有支撑的购买结果仍可胜出", editorial)
        self.assertIn("颜色、搭配、材质或外观表达不按关键词禁用或排除", editorial)

    def test_full_point_coverage_precedes_dynamic_board_review(self):
        policy = read("references/clip-selection-policy.md")
        self.assertIn("完整覆盖所有有效卖点", policy)
        self.assertIn("仅可整块省略没有尚未覆盖的独立有效卖点", policy)
        self.assertIn("不得固定某些卖点永远低价值", policy)
        self.assertIn("不得自动截断", policy)

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

    def test_90_second_target_and_100_second_reference_are_not_a_hard_cap(self):
        policy = read("references/clip-selection-policy.md")
        final_check = read("references/final-check.md")
        self.assertIn("90 秒是有效信息密度目标", policy)
        self.assertIn("95–100 秒进入复核", policy)
        self.assertIn("不形成容量上限", policy)
        for text in (policy, final_check):
            for unsupported in ("45 秒", "45秒", "130 秒", "130秒"):
                self.assertNotIn(unsupported, text)

    def test_selected_opening_count_drives_independent_complete_cuts(self):
        policy = read("references/clip-selection-policy.md")
        contract = read("references/runtime-contract.md")
        self.assertIn("每个已选开头分别生成一条完整成片", policy)
        self.assertIn("每条成片先完整覆盖", policy)
        self.assertNotIn("暂停生成正式成片", contract)


if __name__ == "__main__":
    unittest.main()
