import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class WorkflowRevision047Tests(unittest.TestCase):
    def test_opening_only_comparison_is_empathy_first(self):
        editorial = read("references/editorial-policy.md")
        self.assertIn("共情入口优先", editorial)
        self.assertIn("只比较开头本身", editorial)
        self.assertIn("不比较、评分或排名完整成片", editorial)
        self.assertNotIn("不做六维评分", editorial)

    def test_complete_pool_precedes_direct_dual_plan(self):
        contract = read("references/runtime-contract.md")
        policy = read("references/clip-selection-policy.md")
        self.assertLess(contract.index("建立完整信息池"), contract.index("按共情优先层级比较开头"))
        self.assertLess(contract.index("建立完整信息池"), contract.index("单条/多方案数量"))
        self.assertIn("默认直接生成两条", policy)
        self.assertIn("不得暂停等待用户选择", policy)

    def test_each_plan_starts_from_complete_pool_and_superlong_is_explicit(self):
        policy = read("references/clip-selection-policy.md")
        self.assertIn("每条独立覆盖完整有效卖点", policy)
        self.assertIn("不得把卖点拆到两条、只靠并集覆盖", policy)
        self.assertIn("明显超过 120 秒", policy)
        self.assertIn("逐项说明被省略的有效信息", policy)

    def test_original_eligible_purchase_prompt_is_required_but_never_invented(self):
        editorial = read("references/editorial-policy.md")
        self.assertIn("原文存在适用且合规的促单话术时，必须保留", editorial)
        self.assertIn("原文没有促单时，禁止编造、改写或补充", editorial)
        self.assertIn("不得跨商品移用话术", editorial)

    def test_duration_is_calculated_after_complete_arrangement(self):
        policy = read("references/clip-selection-policy.md")
        check = read("references/final-check.md")
        self.assertIn("先完成全部有效卖点的完整编排，再计算时长", policy)
        self.assertIn("120 秒不是目标，也不是硬上限", policy)
        self.assertIn("略超 120 秒", policy)
        self.assertIn("未明显超过 120 秒时是否保留全部有效信息", check)
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
        self.assertEqual(manifest["skill_version"], "0.4.27")
        self.assertTrue(manifest["source_map"])
        self.assertEqual(hashlib.sha256(runtime.read_bytes()).hexdigest(), manifest["runtime_sha256"])
        for relative, digest in manifest["source_hashes"].items():
            self.assertEqual(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(), digest, relative)

    def test_fixed_five_parts_and_single_ai_architecture_remain(self):
        contract = read("references/runtime-contract.md")
        for phrase in ("一个 AI", "固定五部分交付", "不新增 Agent"):
            self.assertIn(phrase, contract)

    def test_real_srt_regression_report_is_present(self):
        report = read("tests/real-source-regression-0.4.7.md")
        self.assertIn("SRT", report)
        self.assertIn("字幕序号", report)
        self.assertIn("未做音画核验", report)


if __name__ == "__main__":
    unittest.main()
