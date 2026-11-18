from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = next(p for p in ROOT.parents if (p / "plugin.json").is_file())


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class EarlyPurchaseOpportunityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = read("SKILL.md")
        cls.editorial = read("references/editorial-policy.md")
        cls.selection = read("references/highlight-selection.md")
        cls.audit = read("references/final-check.md")
        cls.global_rules = read("references/global-rules.md")
        cls.portable = read("C2-Universal-Portable.md")

    def test_attention_decay_and_minimum_sufficient_unit_are_explicit(self):
        for phrase in ["注意力衰减", "最小充分购买单元", "最早合理成交机会"]:
            self.assertIn(phrase, self.editorial)
            self.assertIn(phrase, self.portable)

    def test_first_reason_gets_earliest_contextually_valid_opportunity(self):
        for phrase in ["第一个完整购买理由", "最早合理成交机会", "前置依赖", "颜色", "对象"]:
            self.assertIn(phrase, self.editorial)
        self.assertIn("上下文", self.audit)

    def test_complete_reason_is_more_than_an_attribute_or_action_prompt(self):
        for phrase in ["具体的顾客结果", "足够依据", "必要条件", "孤立商品属性", "宽泛适配词"]:
            self.assertIn(phrase, self.editorial)
        self.assertIn("完整购买理由", self.audit)

    def test_moved_action_preserves_its_local_context(self):
        for phrase in ["完整语义、前置依赖和原有局部语境", "价格/活动说明", "上架/链接状态", "不为保住 CTA"]:
            self.assertIn(phrase, self.editorial)
        self.assertIn("不把该行动句单独前移", self.audit)

    def test_later_independent_reasons_allow_dynamic_reassessment(self):
        for phrase in ["新的独立购买理由", "再次判断", "不以增加劝买密度为目标"]:
            self.assertIn(phrase, self.editorial)
        for forbidden in ["固定成交次数", "固定成交位置", "固定软逼单+强逼单"]:
            self.assertNotIn(forbidden, self.editorial)

    def test_back_half_cannot_carry_first_persuasion(self):
        for phrase in ["后半段", "第一次说服", "购买理由"]:
            self.assertIn(phrase, self.editorial)
        self.assertIn("第一次说服", self.audit)

    def test_auditor_uses_nonmechanical_truncation_pressure_test(self):
        for phrase in ["非机械", "截断压力测试", "前段", "前中段", "中段", "累计前缀", "不把三个区段当成固定三点清单"]:
            self.assertIn(phrase, self.audit)
        self.assertIn("累计语义前缀", self.skill)
        self.assertIn("不把这些区段当成固定三点清单", self.skill)
        for fixed_template in ["15秒", "30%", "固定时间点"]:
            self.assertNotIn(fixed_template, self.audit)

    def test_core_version_and_plugin_package_version_are_aligned(self):
        core_version = (PLUGIN_ROOT / "VERSION").read_text(encoding="utf-8").strip()
        package = json.loads((PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8"))
        manifest = json.loads((PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(core_version, "0.4.2")
        self.assertIn(f"SRT Clip C2 Universal {core_version}", self.skill)
        self.assertEqual(package["version"], "0.4.8")
        self.assertEqual(manifest["version"], "0.4.8")

    def test_trade_information_exclusions_and_existing_output_contract_remain(self):
        for phrase in ["动态价格", "优惠", "库存", "限时", "直播专属福利"]:
            self.assertIn(phrase, self.editorial)
        self.assertIn("固定五部分交付", self.skill)
        self.assertIn("原话逐字保留", self.editorial)
        self.assertIn("不得无理由遗漏", self.selection)


if __name__ == "__main__":
    unittest.main()
