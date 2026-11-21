from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class PurchaseReasonPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = read("references/runtime-current.md")
        cls.editorial = read("references/editorial-policy.md")
        cls.selection = read("references/highlight-selection.md")
        cls.global_rules = read("references/global-rules.md")
        cls.packs = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (ROOT / "product-knowledge-packs").glob("*.md")
        )

    def test_universal_core_owns_dynamic_structure(self):
        self.assertIn("Product Purchase-Decision Architect（商品购买决策架构师）", self.skill)
        self.assertIn("内容结构根据本商品", self.skill)
        self.assertIn("Universal Core", self.editorial)
        self.assertIn("不规定结构", self.packs)

    def test_stranger_first_screen_value_and_strong_candidate_priority(self):
        for phrase in ["陌生顾客首屏价值测试", "顾客收益", "强候选", "弱候选", "差异性只加分"]:
            self.assertIn(phrase, self.editorial)
        self.assertIn("老粉、老顾客、复购用户限定内容默认不代表陌生顾客", self.editorial)

    def test_color_is_not_banned_but_requires_customer_value(self):
        self.assertIn("颜色、搭配、材质或外观表达不按关键词禁用", self.editorial)
        self.assertIn("显气色、不沉闷、显瘦", self.editorial)

    def test_complete_reason_still_has_evidence_and_conditions_without_forcing_cta(self):
        for phrase in ["具体结果/用途/待解决问题", "足够原话依据与必要条件", "孤立属性", "购买推动是可选项", "强制提前安排购买机会"]:
            self.assertIn(phrase, self.editorial)

    def test_all_points_are_reassessed_for_each_angle(self):
        for phrase in ["完整目标商品窗口中识别出的全部有效独立购买信息", "逐项判断每个卖点对本条角度的作用", "同一卖点在不同成片中可以有不同价值等级"]:
            self.assertIn(phrase, self.selection)

    def test_value_tiers_and_information_density(self):
        for phrase in ["高决策价值", "中决策价值", "弱增量", "单位时间购买决策价值", "信息密度"]:
            self.assertIn(phrase, self.selection)
        self.assertIn("单条正式方案必须覆盖全部已确认有效独立卖点", self.selection)
        self.assertIn("每条多视频方案也都必须覆盖同一完整卖点池", self.selection)

    def test_duration_has_general_floor_no_ceiling_and_short_exception(self):
        for phrase in ["45 秒是一般成片的合理下限参考", "不设固定时长上限", "取消 120 秒硬上限", "短时长例外", "质量合格", "不得为达到某个时长"]:
            self.assertIn(phrase, self.selection)
        self.assertNotIn("45–120 秒", self.selection)
        self.assertNotIn("120 秒硬上限确实无法满足", self.selection)

    def test_important_reason_coverage_is_mandatory(self):
        for phrase in ["全部有效独立购买信息", "逐条复评", "单条正式方案必须覆盖全部已确认有效独立卖点", "每条多视频方案也都必须覆盖同一完整卖点池"]:
            self.assertIn(phrase, self.selection)
        self.assertNotIn("单条成片尽可能完整覆盖", self.selection)
        self.assertNotIn("多条整体尽可能覆盖", self.selection)

    def test_trim_order_prioritizes_low_value_without_a_ceiling_gate(self):
        duration_section = self.selection.split("## 时长下限与动态取舍", 1)[-1].split("## 停止条件", 1)[0]
        order = [
            "机械性重复",
            "过度性重复",
            "弱增量",
            "泛夸赞",
            "普通过渡",
            "弱 CTA",
            "同一卖点的过多证明",
        ]
        positions = [duration_section.index(term) for term in order]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("不得删除有效独立卖点", duration_section)

    def test_global_bans_remain_scoped_and_category_neutral(self):
        self.assertIn("全商品通用的用户剪辑禁用库", self.global_rules)
        self.assertIn("## 正式禁用词库", self.global_rules)
        self.assertIn("`羊毛`", self.global_rules)
        self.assertIn("匹配证明不能豁免此词", self.global_rules)
        self.assertIn("`羊绒`：", self.global_rules)
        self.assertIn("直接匹配字面词及其组合", self.global_rules)
        self.assertIn("防静电不是正式禁词", self.global_rules)
        self.assertIn("动态生成", self.global_rules)

    def test_multi_output_is_differentiated_and_each_video_covers_fully(self):
        for phrase in ["明确要求多条时，每条都交付完整、可独立成立的方案", "核心购买角度", "差异化组合", "每条方案必须各自覆盖全部有效独立卖点", "禁止机械 Top N", "不得把 120 秒作为删减或拆条门槛", "独立成立"]:
            self.assertIn(phrase, self.selection)
        for phrase in ["核心购买角度", "不得只更换开头", "实质差异", "保留必要证据和条件"]:
            self.assertIn(phrase, self.selection)

    def test_cta_is_optional_and_not_a_timing_gate(self):
        self.assertIn("购买推动是可选项", self.editorial)
        self.assertIn("不强制提前安排购买机会", self.editorial)
        self.assertIn("不因 CTA 较晚或某条成片没有 CTA 而判定失败", self.editorial)

    def test_no_extra_semantic_stage_or_tool_gate(self):
        self.assertIn("一次语义分析", self.skill)
        self.assertIn("不创建多个模型、串行 Agent", self.skill)
        self.assertNotIn("第六步：", self.skill)
        self.assertIn("不允许把某个 Python 版本、脚本、API、联网能力", self.skill)


if __name__ == "__main__":
    unittest.main()
