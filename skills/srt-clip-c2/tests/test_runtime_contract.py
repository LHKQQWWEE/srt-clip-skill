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
        self.assertIn("候选识别只评估开头本身", editorial)
        self.assertIn("开放式观看动力优先级", editorial)
        self.assertIn("候选池纳入其中全部合格候选", editorial)
        self.assertIn("只有完全不存在合格的第一优先级候选时", editorial)
        self.assertIn("候选展示不设数量上限", editorial)
        self.assertIn("主体内容可合理复用", editorial)
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
        self.assertIn("容量复核", final_check)

    def test_duration_and_original_cta_contract(self):
        policy = read("references/clip-selection-policy.md")
        editorial = read("references/editorial-policy.md")
        self.assertIn("写出正文前建立本条成片的时长预算", policy)
        self.assertIn("首稿必须以已完成容量优化的选段为基础", policy)
        self.assertIn("预计成片时长 = 原始选段累计时长 ÷ 1.2", policy)
        self.assertIn("90 秒是有效信息密度目标", policy)
        self.assertIn("超过 100 秒须启动专项优化并逐条复核", policy)
        self.assertIn("促单独立分类", editorial)
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
        self.assertIn("duration_review", schema["properties"])
        self.assertIn("content_blocks", schema["properties"])
        self.assertNotIn("multi_video_opportunity", schema["properties"])
        self.assertNotIn("checkpoint_status", schema["properties"])
        self.assertNotIn("candidate_comparison", schema["properties"])
        self.assertEqual(schema["properties"]["roles"]["items"]["properties"]["role"]["enum"], ["独立卖点", "证据", "条件", "必要衔接", "适用促单原话"])
        self.assertEqual(schema["properties"]["flags"]["items"]["properties"]["type"]["enum"], ["fact_pending", "risk_hint", "key_limit"])


if __name__ == "__main__":
    unittest.main()
