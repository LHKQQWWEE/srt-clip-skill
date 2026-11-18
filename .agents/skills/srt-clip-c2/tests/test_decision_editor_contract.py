from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DecisionEditorContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.editorial = (ROOT / "references/editorial-policy.md").read_text(encoding="utf-8")
        cls.selection = (ROOT / "references/highlight-selection.md").read_text(encoding="utf-8")
        cls.long_context = (ROOT / "references/long-context-mode.md").read_text(encoding="utf-8")
        cls.final_check = (ROOT / "references/final-check.md").read_text(encoding="utf-8")
        cls.rubric = (ROOT / "tests/quality-rubric.md").read_text(encoding="utf-8")
        cls.categories = "\n".join(
            path.read_text(encoding="utf-8") for path in (ROOT / "categories").glob("*.md")
        )

    def test_skill_has_one_purchase_decision_editor_identity(self):
        self.assertIn("带货短视频购买决策编辑器", self.skill)
        self.assertIn("结构权威", self.editorial)

    def test_stranger_first_screen_test_overrules_weaker_opening(self):
        self.assertIn("陌生顾客首屏价值测试", self.editorial)
        self.assertIn("强候选", self.editorial)
        self.assertIn("弱候选", self.editorial)
        self.assertIn("顾客收益", self.editorial)

    def test_first_purchase_loop_prefers_natural_low_resistance_close(self):
        self.assertIn("第一次购买决策闭环", self.editorial)
        self.assertIn("低阻力", self.editorial)
        self.assertIn("购买理由成立", self.editorial)
        self.assertIn("弱逼单", self.editorial)

    def test_first_close_does_not_end_high_value_selection(self):
        self.assertIn("成交后继续", self.selection)
        self.assertIn("高决策价值", self.selection)
        self.assertIn("独立亮点", self.selection)

    def test_value_tiers_are_dynamic_and_do_not_use_coverage_percentages(self):
        for tier in ["高决策价值", "中决策价值", "弱增量"]:
            self.assertIn(tier, self.selection)
        self.assertIn("机械覆盖率", self.selection)
        self.assertIn("不得无理由遗漏", self.selection)

    def test_formal_duration_floor_ceiling_and_extension_rules(self):
        for token in ["45–120 秒", "45–90 秒", "90–120 秒", "禁止为凑 45 秒"]:
            self.assertIn(token, self.selection)
        self.assertIn("短候选", self.selection)
        self.assertIn("信息不足", self.selection)

    def test_information_density_is_judged_per_segment(self):
        self.assertIn("单位时间购买决策价值", self.selection)
        self.assertIn("信息密度", self.selection)
        self.assertIn("新增购买理由", self.selection)

    def test_midsection_is_a_decision_chain_not_a_category_stack(self):
        self.assertIn("购买决策链", self.editorial)
        self.assertIn("引出顾客接下来会问的问题", self.editorial)
        self.assertIn("不是卖点类别堆叠", self.editorial)

    def test_multi_output_requires_complementary_decision_paths(self):
        self.assertIn("购买决策路径", self.selection)
        self.assertIn("只换开头", self.selection)
        self.assertIn("实质互补", self.selection)

    def test_long_context_gives_late_strong_candidates_fair_competition(self):
        self.assertIn("前后位置公平", self.long_context)
        self.assertIn("后段", self.long_context)
        self.assertIn("同一组语义标准", self.long_context)
        self.assertIn("不是新增第二轮筛选", self.long_context)

    def test_category_modules_do_not_redefine_universal_structure(self):
        for token in ["陌生顾客首屏价值测试", "第一次购买决策闭环", "不超过 120 秒", "1.2 倍速"]:
            self.assertNotIn(token, self.categories)
        self.assertIn("羊毛", self.categories)
        self.assertIn("鞋底", self.categories)
        self.assertIn("围法", self.categories)

    def test_part_three_uses_concise_reason_summary(self):
        self.assertIn("核心购买理由", self.skill)
        self.assertIn("关键补充理由", self.skill)
        self.assertIn("重要未采用内容及原因", self.skill)
        self.assertNotIn("逐版列出亮点覆盖清单", self.skill)

    def test_final_check_names_new_hard_failures(self):
        for phrase in [
            "弱开头压过强结果开头",
            "购买理由未成立就弱逼单",
            "素材充分却低于45秒",
            "为凑时长灌水",
            "高决策价值亮点无理由遗漏",
            "多条仅换开头但购买路径同质",
        ]:
            self.assertIn(phrase, self.final_check)

    def test_quality_rubric_reweights_purchase_decision_quality(self):
        self.assertIn("购买决策链", self.rubric)
        self.assertIn("单位时间购买决策价值", self.rubric)
        self.assertIn("第一次购买决策闭环", self.rubric)
        self.assertIn("正式成片45–120秒", self.rubric)


if __name__ == "__main__":
    unittest.main()
