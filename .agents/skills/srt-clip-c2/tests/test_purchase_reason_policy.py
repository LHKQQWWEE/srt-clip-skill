from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PurchaseReasonPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.editorial = (ROOT / "references/editorial-policy.md").read_text(encoding="utf-8")
        cls.selection = (ROOT / "references/highlight-selection.md").read_text(encoding="utf-8")
        cls.global_rules = (ROOT / "references/global-rules.md").read_text(encoding="utf-8")
        cls.categories = "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "categories").glob("*.md"))

    def test_universal_core_owns_structure(self):
        self.assertIn("购买决策编辑器", self.skill)
        self.assertIn("结构权威", self.skill)
        self.assertIn("Universal Core", self.editorial)
        self.assertIn("类目模块只保留", self.skill)

    def test_stranger_first_screen_value_and_strong_candidate_priority(self):
        for phrase in ["陌生顾客首屏价值测试", "顾客收益 > 具体可信", "强候选", "弱候选", "差异性只加分"]:
            self.assertIn(phrase, self.editorial)
        self.assertIn("老粉、老顾客、复购用户限定内容默认不代表陌生顾客", self.editorial)

    def test_color_is_not_banned_but_requires_customer_value(self):
        self.assertIn("颜色、搭配、材质或外观表达不按关键词禁用", self.editorial)
        self.assertIn("显气色、不沉闷、显瘦", self.editorial)

    def test_first_purchase_closure_uses_reason_then_low_resistance(self):
        for phrase in ["第一次购买决策闭环", "购买理由尚未成立前", "低阻力", "弱逼单"]:
            self.assertIn(phrase, self.editorial)

    def test_first_close_does_not_end_high_value_selection(self):
        self.assertIn("成交后继续覆盖尚未利用的高决策价值独立亮点", self.selection)
        self.assertIn("高决策价值", self.selection)

    def test_value_tiers_and_information_density(self):
        for phrase in ["高决策价值", "中决策价值", "弱增量", "单位时间购买决策价值", "信息密度"]:
            self.assertIn(phrase, self.selection)
        self.assertIn("不设机械覆盖率", self.selection)
        self.assertIn("不得无理由遗漏", self.selection)

    def test_high_value_coverage_has_real_reasons_for_omission(self):
        for phrase in ["合规/事实问题", "归属不明", "真实重复", "正式时长硬限制"]:
            self.assertIn(phrase, self.selection)

    def test_midsection_is_a_decision_chain(self):
        self.assertIn("购买决策链", self.editorial)
        self.assertIn("而不是卖点类别堆叠", self.editorial)
        self.assertIn("每个片段都应承担至少一种", self.editorial)

    def test_multi_output_requires_complementary_decision_paths(self):
        self.assertIn("购买决策路径", self.selection)
        self.assertIn("只换开头", self.selection)
        self.assertIn("实质互补", self.selection)
        self.assertIn("核心理由、必要证明", self.selection)

    def test_duration_floor_ceiling_and_no_padding(self):
        for phrase in ["45–120 秒", "45–90 秒", "90–120 秒", "禁止为凑 45 秒", "短候选，非正式成片"]:
            self.assertIn(phrase, self.selection)

    def test_duration_trim_order_puts_weak_cta_before_independent_high_value(self):
        order = [
            "真正语义重复",
            "无信息增量的重复夸赞",
            "弱/重复成交话术",
            "弱增量和低决策价值内容",
            "已被更强信息充分覆盖",
            "独立高决策价值理由只可在 120 秒硬上限",
        ]
        positions = [self.selection.index(term) for term in order]
        self.assertEqual(positions, sorted(positions))

    def test_dynamic_transaction_info_is_excluded_and_no_extra_clause_rule(self):
        for phrase in ["具体商品价格", "全片默认排除", "原话逐字保留", "不润色、改写、补词或拼接不连续片段"]:
            self.assertIn(phrase, self.editorial)
        self.assertIn("日常切片排除规则见 `references/editorial-policy.md`", self.global_rules)
        self.assertNotIn("用户要保留且当前信息已核实", self.selection)

    def test_categories_only_add_specialist_judgments(self):
        for phrase in ["陌生顾客首屏价值测试", "第一次购买决策闭环", "单位时间购买决策价值", "45–120 秒", "120 秒上限", "单条最优、多条互补"]:
            self.assertNotIn(phrase, self.categories)
        for phrase in ["羊毛/羊绒", "鞋底结构", "围法"]:
            self.assertIn(phrase, self.categories)

    def test_third_part_has_only_a_concise_reason_summary(self):
        self.assertIn("核心购买理由、关键补充理由、重要未采用内容及原因", self.skill)
        self.assertNotIn("逐版列出亮点覆盖清单", self.skill)
        self.assertIn("不输出完整卖点目录、机械覆盖率", self.skill)

    def test_no_extra_daily_analysis_stage_or_ledger(self):
        self.assertIn("一次分析", self.skill)
        self.assertNotIn("第六步：", self.skill)


if __name__ == "__main__":
    unittest.main()
