import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class PurchaseDecisionPolicyTests(unittest.TestCase):
    def test_complete_inventory_precedes_opening_and_plan_generation(self):
        contract = read("references/runtime-contract.md")
        self.assertLess(contract.index("建立完整信息池"), contract.index("按共情优先层级比较开头"))
        self.assertLess(contract.index("建立完整信息池"), contract.index("单条/多方案数量"))

    def test_each_plan_starts_from_the_same_pool_and_does_not_use_union_coverage(self):
        policy = read("references/clip-selection-policy.md")
        self.assertIn("每条独立覆盖完整有效卖点", policy)
        self.assertIn("不得把卖点拆到两条、只靠并集覆盖", policy)
        self.assertIn("超长预设", policy)

    def test_point_granularity_keeps_examples_grouped_and_facts_distinct(self):
        editorial = read("references/editorial-policy.md")
        self.assertIn("不把同一购买意义下的一组例子机械拆成多个卖点", editorial)
        self.assertIn("不同具体事实过度合并", editorial)

    def test_default_dual_plan_runs_without_theme_pause(self):
        policy = read("references/clip-selection-policy.md")
        contract = read("references/runtime-contract.md")
        self.assertIn("默认直接生成两条", policy)
        self.assertIn("不得暂停等待用户选择", policy)
        self.assertIn("单条", policy)
        self.assertNotIn("暂停生成正式成片", contract)

    def test_full_cut_competition_is_removed(self):
        editorial = read("references/editorial-policy.md")
        self.assertIn("不比较、评分或排名完整成片", editorial)

    def test_low_value_does_not_mean_weak_increment_or_fixed_category(self):
        policy = read("references/clip-selection-policy.md")
        self.assertIn("不得固定某些卖点永远低价值", policy)
        self.assertIn("低价值但有效信息", policy)
        self.assertIn("不等于弱增量", policy)

    def test_fixed_five_parts_and_one_ai_remain(self):
        contract = read("references/runtime-contract.md")
        self.assertIn("一个 AI", contract)
        self.assertIn("固定五部分交付", contract)
        self.assertIn("不新增 Agent", contract)


if __name__ == "__main__":
    unittest.main()
