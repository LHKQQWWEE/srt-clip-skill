import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class RuntimeContractTests(unittest.TestCase):
    def test_machine_and_ai_boundaries_keep_semantics_with_ai(self):
        final_check = read("references/final-check.md")
        self.assertIn("机器不判断", final_check)
        self.assertIn("AI 的语义判断", final_check)
        self.assertIn("risk_hint", final_check)
        self.assertIn("信息池完整性", final_check)

    def test_opening_compares_dynamic_hook_candidates_only(self):
        editorial = read("references/editorial-policy.md")
        self.assertIn("动态顾客心理驱动钩子机制", editorial)
        self.assertIn("开头比较只覆盖开头本身", editorial)
        self.assertIn("开放式观看动力优先级", editorial)
        self.assertIn("存在合格的第一优先级开头候选，必须从这些候选中动态择优", editorial)
        self.assertIn("只有不存在合格的第一优先级候选时，才从其他有效钩子候选中择优", editorial)
        self.assertIn("多方案", editorial)
        self.assertIn("不比较、评分或排名完整成片", editorial)

    def test_pool_is_complete_before_plan_count_and_generation(self):
        contract = read("references/runtime-contract.md")
        self.assertLess(contract.index("建立完整信息池"), contract.index("开头候选等待关口"))
        self.assertLess(contract.index("等待用户选择商品"), contract.index("确认后才为所选商品生成开头候选"))
        self.assertIn("用户最多选择 3 个", contract)

    def test_final_check_covers_actual_output_plans(self):
        final_check = read("references/final-check.md")
        self.assertIn("只对实际写出的成片执行终检", final_check)
        self.assertIn("方案数量", final_check)
        self.assertIn("超长例外", final_check)

    def test_duration_and_original_cta_contract(self):
        policy = read("references/clip-selection-policy.md")
        editorial = read("references/editorial-policy.md")
        self.assertIn("先完成全部有效卖点的完整编排，再计算时长", policy)
        self.assertIn("120 秒不是目标，也不是硬上限", policy)
        self.assertIn("明显超过 120 秒", policy)
        self.assertIn("原文存在适用且合规的促单话术时，必须保留", editorial)
        self.assertIn("原文没有促单时，禁止编造、改写或补充", editorial)

    def test_five_part_output_and_single_ai_remain(self):
        contract = read("references/runtime-contract.md")
        self.assertIn("一个 AI", contract)
        self.assertIn("固定五部分交付", contract)
        self.assertIn("不重写整份五部分", contract)

    def test_schema_describes_one_record_per_generated_plan(self):
        schema = json.loads(read("scripts/selection.schema.json"))
        self.assertIn("one actual user-selected final cut", schema["description"])
        self.assertIn("Routine SRT execution never calls this JSON schema or Python tools", schema["description"])
        self.assertIn("opening_choice", schema["properties"])
        self.assertIn("plan_core", schema["properties"])
        self.assertIn("duration_mode", schema["properties"])
        self.assertIn("omitted_selling_points", schema["properties"])
        self.assertNotIn("multi_video_opportunity", schema["properties"])
        self.assertNotIn("checkpoint_status", schema["properties"])
        self.assertNotIn("candidate_comparison", schema["properties"])
        self.assertEqual(schema["properties"]["roles"]["items"]["properties"]["role"]["enum"], ["独立卖点", "证据", "条件", "必要衔接", "适用促单原话"])
        self.assertEqual(schema["properties"]["flags"]["items"]["properties"]["type"]["enum"], ["fact_pending", "risk_hint", "key_limit"])


if __name__ == "__main__":
    unittest.main()
