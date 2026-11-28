import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def text_sha256(path):
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


class CurrentWorkflowIntegrityTests(unittest.TestCase):
    def test_opening_only_comparison_uses_dynamic_customer_motivation(self):
        editorial = read("references/editorial-policy.md")
        self.assertIn("动态顾客心理驱动钩子机制", editorial)
        self.assertIn("候选识别只评估开头本身", editorial)
        self.assertIn("开放式观看动力优先级", editorial)
        self.assertIn("候选池纳入其中全部合格候选", editorial)
        self.assertIn("第一优先级内部不设固定类型清单、顺序、权重或分数", editorial)
        self.assertIn("不比较、评分或排名完整成片", editorial)

    def test_complete_pool_precedes_user_selected_opening_generation(self):
        contract = read("references/runtime-contract.md")
        policy = read("references/clip-selection-policy.md")
        self.assertLess(contract.index("建立完整信息池"), contract.index("开头候选等待关口"))
        self.assertLess(contract.index("先只呈现商品身份"), contract.index("确认前不得生成开头候选"))
        self.assertIn("每个已选开头分别生成一条完整成片", policy)
        self.assertIn("所有达到现有质量门槛且彼此实质不同", policy)
        self.assertIn("用户最多选择 3 个候选", policy)

    def test_each_plan_starts_from_complete_pool_and_capacity_review_is_explicit(self):
        policy = read("references/clip-selection-policy.md")
        self.assertIn("每条成片先完整覆盖", policy)
        self.assertIn("方案之间不互相补足", policy)
        self.assertIn("超过 100 秒须逐条复核", policy)
        self.assertIn("逐项注明省略的完整板块", policy)

    def test_promotion_policy_preserves_complete_units_and_never_invents(self):
        policy = read("references/promotion-policy.md")
        self.assertIn("完整上下文", policy)
        self.assertIn("不拼接不同顾客的问答，不混合不同商品或款式", policy)
        self.assertIn("最小完整组合", policy)
        self.assertIn("没有时不编造、改写或补充购买口号", policy)

    def test_duration_is_planned_after_full_pool_and_before_first_copy(self):
        policy = read("references/clip-selection-policy.md")
        check = read("references/final-check.md")
        self.assertIn("先建立完整信息池", policy)
        self.assertIn("写出正文前完成首次容量规划", policy)
        self.assertNotIn("先完成全部有效卖点的完整编排，再计算时长", policy)
        self.assertIn("90 秒是有效信息密度目标", policy)
        self.assertIn("100 秒可作为可接受参考", policy)
        self.assertIn("超过 100 秒须逐条复核", policy)
        self.assertIn("90 秒为目标", check)
        self.assertIn("超过 90 秒比较", check)
        for path in (policy, check):
            for unsupported in ("45 秒", "45秒", "130 秒", "130秒"):
                self.assertNotIn(unsupported, path)

    def test_only_actual_emitted_plans_receive_final_audit(self):
        check = read("references/final-check.md")
        self.assertIn("只对实际写出的成片执行终检", check)
        self.assertNotIn("应暂停等待选择", check)

    def test_runtime_manifest_hashes_and_versions_are_current(self):
        manifest = json.loads(read("references/runtime-manifest.json"))
        runtime = ROOT / manifest["runtime_file"]
        self.assertEqual(manifest["core_version"], "0.4.7")
        self.assertEqual(manifest["skill_version"], "0.4.51")
        self.assertTrue(manifest["source_map"])
        self.assertEqual(text_sha256(runtime), manifest["runtime_sha256"])
        for relative, digest in manifest["source_hashes"].items():
            self.assertEqual(text_sha256(ROOT / relative), digest, relative)

    def test_fixed_five_parts_and_single_ai_architecture_remain(self):
        contract = read("references/runtime-contract.md")
        for phrase in ("一个 AI", "固定五部分交付", "不新增 Agent"):
            self.assertIn(phrase, contract)

if __name__ == "__main__":
    unittest.main()
