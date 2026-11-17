from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PurchaseReasonPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.selection = (ROOT / "references/highlight-selection.md").read_text(encoding="utf-8")
        cls.editorial = (ROOT / "references/editorial-policy.md").read_text(encoding="utf-8")
        cls.qianchuan = (ROOT / "references/qianchuan-offline.md").read_text(encoding="utf-8")
        cls.categories = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (ROOT / "categories").glob("*.md")
        )
        cls.women = (ROOT / "categories/womens-fashion.md").read_text(encoding="utf-8")

    def test_hook_value_gets_minimal_sufficient_support(self):
        self.assertTrue("最小充分承接" in self.selection, "opening support must be minimal and sufficient")
        self.assertTrue("开头核心价值" in self.selection, "opening value must have an explicit payoff")

    def test_first_conversion_follows_a_valid_purchase_reason(self):
        self.assertTrue("购买理由成立后" in self.selection, "conversion must follow a formed reason to buy")
        self.assertTrue("最早合理的成交机会" in self.selection, "conversion should use the earliest reasonable opportunity")

    def test_selection_continues_after_first_conversion(self):
        self.assertTrue("成交之后继续" in self.selection, "selection must continue after a CTA")
        self.assertTrue("独立购买价值" in self.selection, "independent purchase reasons must remain eligible")

    def test_conversion_nodes_have_no_fixed_count_or_position(self):
        self.assertTrue("不设置固定成交次数" in self.selection, "CTA count and placement must remain dynamic")
        self.assertTrue("不强制逼单" in self.editorial, "the ending must not require a CTA")
        self.assertTrue("新增转化价值" in self.selection, "repeated CTAs need a distinct conversion purpose")

    def test_dynamic_transaction_information_is_excluded_by_default(self):
        for phrase in ["动态交易信息", "具体商品价格", "库存", "默认排除"]:
            with self.subTest(phrase=phrase):
                self.assertTrue(phrase in self.editorial, "dynamic transaction information must be excluded globally")
        self.assertFalse("已核实的价格优惠" in self.selection, "verified promotions must not become normal clip candidates")

    def test_mixed_transaction_and_product_cue_keeps_only_an_exact_complete_clause(self):
        self.assertTrue("原始连续表达" in self.editorial, "mixed cues may retain only a source-contiguous clause")
        self.assertTrue("完整原话子句" in self.editorial, "mixed cues must retain a complete source clause, not a fragment")
        self.assertTrue("不保留残句" in self.editorial, "mixed cues must reject leftover fragments")
        self.assertTrue("不得改字、补词或拼接不连续片段" in self.editorial, "mixed cue handling must preserve original wording")
        for path in ["womens-fashion.md", "shoes.md", "scarves.md"]:
            category = (ROOT / "categories" / path).read_text(encoding="utf-8")
            with self.subTest(category=path):
                self.assertIn("完整原话子句", category, "category summaries must use the shared exact-clause boundary")

    def test_category_modules_do_not_restore_dynamic_trade_or_fixed_cta_rules(self):
        self.assertFalse("用户要保留且当前信息已核实" in self.categories, "a category rule must not restore a user-verifiable promo exception")
        self.assertFalse("强制收尾" in self.categories, "a category rule must not require CTA endings")

    def test_update_does_not_add_a_daily_execution_stage(self):
        self.assertTrue("一次分析" in self.skill, "semantic decisions remain in the existing one-pass flow")
        self.assertFalse("第七步：" in self.skill, "the update must not add a daily execution stage")


    def test_stranger_first_without_banning_existing_fans(self):
        self.assertIn("陌生顾客", self.skill)
        self.assertIn("老粉兼顾", self.skill)
        self.assertIn("不是禁止", self.editorial)

    def test_hook_has_no_fixed_type_ranking(self):
        self.assertIn("不设固定类型排序", self.skill)
        self.assertIn("差异性是重要加分项，不是硬门槛", self.skill)
        for token in ["顾客相关性", "即时收益", "具体与可信度", "后续承接"]:
            self.assertIn(token, self.skill)

    def test_color_is_downranked_not_banned(self):
        self.assertIn("纯颜色介绍", self.women)
        self.assertIn("不是关键词黑名单", self.women)
        self.assertIn("颜色若直接带来明确顾客结果", self.skill)

    def test_first_conversion_follows_valid_reason_and_stranger_fit(self):
        self.assertIn("购买理由成立后", self.selection)
        self.assertIn("最早合理", self.selection)
        self.assertIn("对陌生顾客", self.selection)
        self.assertIn("老粉、老顾客、复购限定成交话术默认降级", self.selection)

    def test_weak_cta_cannot_displace_independent_value(self):
        self.assertIn("弱成交话术不得挤占独立有效卖点", self.skill)
        order = [
            "真正语义重复的信息",
            "没有信息增量的重复夸赞或情绪强化",
            "重复或弱成交话术",
            "购买决策价值较低的内容",
            "已由更强片段充分覆盖的次级信息",
            "舍弃部分独立有效卖点",
        ]
        positions = [self.selection.index(x) for x in order]
        self.assertEqual(positions, sorted(positions))

    def test_single_plan_quality_precedes_coverage_density(self):
        self.assertIn("单条最优，多条互补", self.selection)
        self.assertIn("覆盖不是塞满", self.selection)
        self.assertIn("120秒是硬上限，不是目标时长", self.selection)
        self.assertIn("进入候选不等于必须无条件进入最终成片", self.skill)

    def test_multi_output_requires_complementary_decision_value(self):
        self.assertIn("Single Analysis, Complementary Multi Output", self.skill)
        self.assertIn("每增加一条正式方案都应带来新的购买决策价值", self.skill)
        self.assertIn("不能只更换第一句而让主体长期高度同质", self.skill)
        self.assertIn("单条质量 > 多条价值差异 > 形式上的低重复", self.selection)

    def test_core_reasons_may_repeat_across_plans(self):
        self.assertIn("不是整个多方案任务的累计上限", self.selection)
        self.assertIn("核心购买理由若对不同方案都不可替代", self.selection)
        self.assertIn("核心购买理由和必要承接可以共享", self.editorial)

    def test_multi_plan_summary_is_lightweight_not_a_new_ledger(self):
        self.assertIn("简短的整体覆盖摘要", self.skill)
        self.assertIn("不输出机械覆盖率百分比", self.skill)
        self.assertIn("不为生成摘要另建卖点台账或新增模型轮次", self.skill)

    def test_requested_multi_count_is_not_a_low_quality_quota(self):
        self.assertIn("以请求数量为目标", self.skill)
        self.assertIn("只交付可支撑的高质量方案数", self.selection)
        self.assertIn("说明素材限制", self.selection)

if __name__ == "__main__":
    unittest.main()
