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
        self.assertEqual(json.loads((plugin / "plugin.json").read_text(encoding="utf-8"))["version"], "0.4.27")
        self.assertEqual(manifest["skill_version"], "0.4.27")

    def test_empathy_priority_is_only_for_opening_comparison(self):
        editorial = read("references/editorial-policy.md")
        self.assertIn("共情入口优先", editorial)
        self.assertIn("只比较开头本身", editorial)
        self.assertIn("不比较、评分或排名完整成片", editorial)
        self.assertNotIn("通过覆盖资格后，按六维评分比较完整候选", editorial)

    def test_opening_is_grounded_and_not_fabricated_as_customer_feedback(self):
        editorial = read("references/editorial-policy.md")
        self.assertIn("顾客反馈", editorial)
        self.assertIn("原话支撑", editorial)
        self.assertIn("主播提出的设问", editorial)

    def test_complete_pool_precedes_direct_plan_generation(self):
        contract = read("references/runtime-contract.md")
        policy = read("references/clip-selection-policy.md")
        self.assertLess(contract.index("建立完整信息池"), contract.index("按共情优先层级比较开头"))
        self.assertLess(contract.index("建立完整信息池"), contract.index("单条/多方案数量"))
        self.assertIn("默认直接生成两条", policy)
        self.assertIn("不得暂停等待用户选择", policy)
        self.assertIn("按推荐版", policy)

    def test_each_plan_is_independent_and_long_form_is_explicit(self):
        policy = read("references/clip-selection-policy.md")
        self.assertIn("每条独立覆盖完整有效卖点", policy)
        self.assertIn("不得把卖点拆到两条、只靠并集覆盖", policy)
        self.assertIn("超长预设", policy)
        self.assertIn("省略的有效信息", policy)

    def test_fixed_output_and_prohibited_terms_are_preserved(self):
        runtime = read("references/runtime-current.md")
        global_rules = read("references/global-rules.md")
        for title in ("一、文件解析结果", "二、商品识别", "三、最佳成片方案", "四、作品标题与话题", "五、原始 SRT 序号"):
            self.assertIn(title, runtime)
        for term in ("羊毛", "皮草", "羊绒", "特殊动物绒", "全金纺半高领"):
            self.assertIn(term, global_rules)


if __name__ == "__main__":
    unittest.main()
