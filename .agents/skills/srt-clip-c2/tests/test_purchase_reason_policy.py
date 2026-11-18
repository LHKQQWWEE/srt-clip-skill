from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class PurchaseReasonPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = read("SKILL.md")
        cls.editorial = read("references/editorial-policy.md")
        cls.selection = read("references/highlight-selection.md")
        cls.global_rules = read("references/global-rules.md")
        cls.packs = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (ROOT / "product-knowledge-packs").glob("*.md")
        )

    def test_universal_core_owns_dynamic_structure(self):
        self.assertIn("商品购买决策架构师", self.skill)
        self.assertIn("动态决定内容路径", self.skill)
        self.assertIn("Universal Core", self.editorial)
        self.assertIn("不规定结构", self.packs)

    def test_stranger_first_screen_value_and_strong_candidate_priority(self):
        for phrase in ["陌生顾客首屏价值测试", "顾客收益", "强候选", "弱候选", "差异性只加分"]:
            self.assertIn(phrase, self.editorial)
        self.assertIn("老粉、老顾客、复购用户限定内容默认不代表陌生顾客", self.editorial)

    def test_color_is_not_banned_but_requires_customer_value(self):
        self.assertIn("颜色、搭配、材质或外观表达不按关键词禁用", self.editorial)
        self.assertIn("显气色、不沉闷、显瘦", self.editorial)

    def test_purchase_opportunity_requires_a_reason_and_is_flexible(self):
        for phrase in ["购买理由尚未成立前", "低阻力", "弱逼单", "可按依赖关系重排，也可在素材不支持时省略某一环节"]:
            self.assertIn(phrase, self.editorial)

    def test_first_purchase_opportunity_does_not_end_high_value_selection(self):
        self.assertIn("尚未利用的独立高决策价值理由", self.selection)
        self.assertIn("首次购买机会", self.selection)

    def test_value_tiers_and_information_density(self):
        for phrase in ["高决策价值", "中决策价值", "弱增量", "单位时间购买决策价值", "信息密度"]:
            self.assertIn(phrase, self.selection)
        self.assertIn("不设机械覆盖率", self.selection)
        self.assertIn("不得无理由遗漏", self.selection)

    def test_duration_has_general_floor_no_ceiling_and_short_exception(self):
        for phrase in ["45 秒是一般成片的合理下限参考", "不设固定时长上限", "取消 120 秒硬上限", "短时长例外", "质量合格", "不得为达到某个时长"]:
            self.assertIn(phrase, self.selection)
        self.assertNotIn("45–120 秒", self.selection)
        self.assertNotIn("120 秒硬上限确实无法满足", self.selection)

    def test_important_reason_coverage_is_qualitative(self):
        for phrase in ["定性覆盖判断", "改变是否购买", "不设机械覆盖率", "不得为追求 100% 覆盖", "真实原因"]:
            self.assertIn(phrase, self.selection)
        self.assertNotIn("覆盖百分比", self.selection.split("## 时长下限与动态取舍", 1)[1])

    def test_trim_order_prioritizes_low_value_without_a_ceiling_gate(self):
        order = [
            "机械性重复与过度性重复",
            "无明显信息增量或说服增量的夸赞/情绪强化",
            "弱/重复成交话术",
            "弱增量和低决策价值内容",
            "已被更强信息充分覆盖",
        ]
        positions = [self.selection.index(term) for term in order]
        self.assertEqual(positions, sorted(positions))

    def test_global_bans_remain_scoped_and_category_neutral(self):
        self.assertIn("全商品通用的用户剪辑禁用库", self.global_rules)
        self.assertIn("历史审核案例与默认取舍（非永久禁词）", self.global_rules)
        self.assertIn("全羊毛", self.global_rules)
        self.assertIn("对应质检证明条件", self.global_rules)
        self.assertIn("不同成分比例", self.global_rules)
        self.assertIn("动态生成", self.global_rules)

    def test_multi_output_defaults_to_one_and_proactively_prompts(self):
        for phrase in ["默认只生成一条最佳成片", "主动提示", "用户要求后", "不默认同时输出多版完整脚本", "不得把 120 秒当成拆分门槛", "独立成片"]:
            self.assertIn(phrase, self.selection)
        for phrase in ["购买决策路径", "只换开头", "实质差异", "核心理由、必要证明"]:
            self.assertIn(phrase, self.selection)

    def test_no_extra_semantic_stage_or_tool_gate(self):
        self.assertIn("一次语义分析", self.skill)
        self.assertIn("不是新增的多阶段工作流", self.skill)
        self.assertNotIn("第六步：", self.skill)
        self.assertIn("Python、脚本、联网、API、JSON 台账", self.skill)


if __name__ == "__main__":
    unittest.main()
