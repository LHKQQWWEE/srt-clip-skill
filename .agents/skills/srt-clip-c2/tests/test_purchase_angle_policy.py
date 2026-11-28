import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class PurchaseAnglePolicyTests(unittest.TestCase):
    def test_current_package_and_core_versions(self):
        plugin = ROOT.parents[1]
        manifest = json.loads(read("references/runtime-manifest.json"))
        self.assertEqual((plugin / "VERSION").read_text(encoding="utf-8").strip(), "0.4.7")
        self.assertEqual(json.loads((plugin / "plugin.json").read_text(encoding="utf-8"))["version"], "0.4.50")
        self.assertEqual(manifest["skill_version"], "0.4.50")

    def test_opening_choice_uses_dynamic_customer_motivation(self):
        editorial = read("references/editorial-policy.md")
        self.assertIn("动态顾客心理驱动钩子机制", editorial)
        self.assertIn("陌生潜在买家", editorial)
        self.assertIn("继续观看欲望", editorial)
        self.assertIn("与商品相关的购买兴趣", editorial)
        self.assertIn("不比较、评分或排名完整成片", editorial)
        self.assertIn("开放式观看动力优先级", editorial)
        self.assertIn("候选池纳入其中全部合格候选", editorial)
        self.assertIn("只有完全不存在合格的第一优先级候选时", editorial)
        self.assertIn("第一优先级内部不设固定类型清单、顺序、权重或分数", editorial)
        self.assertIn("不替用户选定开头", editorial)
        self.assertIn("每条成片必须以对应的用户所选开头原话开始", editorial)
        self.assertIn("主体内容可合理复用", editorial)

    def test_opening_is_grounded_and_not_fabricated_as_customer_feedback(self):
        editorial = read("references/editorial-policy.md")
        self.assertIn("顾客反馈", editorial)
        self.assertIn("原话支撑", editorial)
        self.assertIn("主播设问", editorial)

    def test_complete_pool_precedes_user_selected_opening_generation(self):
        contract = read("references/runtime-contract.md")
        policy = read("references/clip-selection-policy.md")
        self.assertLess(contract.index("建立完整信息池"), contract.index("开头候选等待关口"))
        self.assertLess(contract.index("先只呈现商品身份"), contract.index("确认前不得生成开头候选"))
        self.assertIn("用户最多选择 3 个候选", policy)
        self.assertIn("只为用户选中的开头生成成片", policy)

    def test_each_plan_is_independent_and_capacity_review_is_explicit(self):
        policy = read("references/clip-selection-policy.md")
        self.assertIn("每条成片先完整覆盖", policy)
        self.assertIn("方案之间不互相补足", policy)
        self.assertIn("超过 100 秒须启动专项优化并逐条复核", policy)
        self.assertIn("省略的完整板块", policy)

    def test_fixed_output_and_prohibited_terms_are_preserved(self):
        runtime = read("references/runtime-current.md")
        global_rules = read("references/global-rules.md")
        for title in ("一、文件解析结果", "二、商品识别", "三、最佳成片方案", "四、作品标题与话题", "五、原始 SRT 序号"):
            self.assertIn(title, runtime)
        for term in ("羊毛", "皮草", "羊绒", "特殊动物绒", "全金纺半高领"):
            self.assertIn(term, global_rules)


if __name__ == "__main__":
    unittest.main()
