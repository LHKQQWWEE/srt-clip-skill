import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGRESSION_CASES = (
    ("#1466–1474", "主动品质介绍归主体"),
    ("#1205–1210", "参数核对候选，冲突未解不得标为已核实"),
    ("#1215–1217", "具体身形选码是促单候选"),
    ("#1233–1236 与 #1264–1265", "重复核对竞争，不拼接问答"),
    ("#1751–1756", "保留150斤顾客的独立条件"),
    ("#1799–1801", "保留另一顾客的独立条件并核对商品/转写"),
    ("#600–601 与 #1215–1217", "一般尺码建议与具体身形条件均保留"),
    ("#1889–1892 与 #1907–1909", "结合颜色纠结上下文识别购买选择"),
    ("#725–726", "有效行动收尾候选"),
    ("#1519–1524", "护理顾虑候选，洗护事实须核验"),
    ("#1364–1368", "温度顾虑候选，不扩展未经证实承诺"),
    ("#277–278", "二维码、鸭绒及星级溯源主张待核"),
    ("#774–776", "吊牌及二维码溯源主张待核"),
    ("#1110–1115", "购买行动候选与标签主张分开核验，保留转写疑点"),
    ("#1286–1290", "吊牌、真伪及溯源主张待核"),
)


class PurchasePromptNeutralityTests(unittest.TestCase):
    def test_plugin_versions_are_current(self):
        plugin = ROOT.parents[1]
        self.assertEqual((plugin / "VERSION").read_text().strip(), "0.4.7")
        self.assertEqual(json.loads((plugin / "plugin.json").read_text(encoding="utf-8"))["version"], "0.4.51")
        self.assertEqual((ROOT / "VERSION").read_text(encoding="utf-8").strip(), "0.4.51")

    def test_classification_uses_full_context_and_function_not_keywords(self):
        policy = (ROOT / "references" / "promotion-policy.md").read_text(encoding="utf-8")
        self.assertIn("按话术在完整上下文中实际帮助观众完成的任务分类", policy)
        self.assertIn("主播主动介绍、展示或解释商品价值", policy)
        self.assertIn("普通搭配展示或审美种草默认仍属主体", policy)
        self.assertIn("正在解决顾客的颜色/搭配选择", policy)
        self.assertIn("示例只说明判断方式，不构成固定、穷尽的促单类别清单", policy)

    def test_units_preserve_context_customers_skus_and_conditions(self):
        policy = (ROOT / "references" / "promotion-policy.md").read_text(encoding="utf-8")
        self.assertIn("保留理解决策所需的完整问答、回应、前提、范围、例外", policy)
        self.assertIn("不拼接不同顾客的问答，不混合不同商品或款式", policy)
        self.assertIn("每个单元内部原则上保持原始对话顺序", policy)
        self.assertIn("未解决的事实冲突不得作为已核实参数", policy)

    def test_candidates_compete_without_dropping_independent_value(self):
        policy = (ROOT / "references" / "promotion-policy.md").read_text(encoding="utf-8")
        self.assertIn("全量识别候选", policy)
        self.assertIn("只有在同一商品/款式及相同决策信息下", policy)
        self.assertIn("不同顾客的不同身形", policy)
        self.assertIn("一般尺码建议与具体身形指导", policy)
        self.assertIn("重复参数核对", policy)
        self.assertIn("最小完整组合", policy)
        self.assertIn("候选被识别不等于必须入片", policy)

    def test_close_checks_required_cases_and_source_truth(self):
        policy = (ROOT / "references" / "promotion-policy.md").read_text(encoding="utf-8")
        self.assertEqual(len(REGRESSION_CASES), 15)
        self.assertTrue(all(case and expected for case, expected in REGRESSION_CASES))
        self.assertIn("事实冲突", policy)
        self.assertIn("二维码", policy)
        self.assertIn("护理", policy)
        self.assertIn("促单绝不豁免正式禁词", policy)

    def test_promotion_has_no_fixed_category_count_or_duration_cap(self):
        policy = (ROOT / "references/promotion-policy.md").read_text(encoding="utf-8")
        self.assertIn("候选类别数量和促单板块时长均不设固定上限", policy)
        self.assertIn("不新增促单秒数上限、固定候选数量、固定类别数量", policy)
        schema = json.loads((ROOT / "scripts/selection.schema.json").read_text(encoding="utf-8"))
        self.assertNotIn("cta_type", schema["properties"]["roles"]["items"]["properties"])

    def test_existing_output_duration_and_runtime_boundaries_remain(self):
        clip = (ROOT / "references/clip-selection-policy.md").read_text(encoding="utf-8")
        contract = (ROOT / "references/runtime-contract.md").read_text(encoding="utf-8")
        self.assertIn("预计成片时长 = 原始选段累计时长 ÷ 1.2", clip)
        self.assertIn("90 秒是有效信息密度目标", clip)
        self.assertIn("100 秒可作为可接受参考", clip)
        self.assertIn("固定五部分交付", contract)
        self.assertIn("日常执行不调用 Python、脚本或外部工具", contract)


if __name__ == "__main__":
    unittest.main()
