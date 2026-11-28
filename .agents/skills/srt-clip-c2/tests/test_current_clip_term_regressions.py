import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
FINAL_CHECK = (ROOT / "references" / "final-check.md").read_text(encoding="utf-8")
GLOBAL_RULES = (ROOT / "references" / "global-rules.md").read_text(encoding="utf-8")
GUARD = ROOT / "scripts" / "prohibited_term_guard.py"


class SpecialUpgrade046Tests(unittest.TestCase):
    def run_guard(self, source, *extra_args):
        with tempfile.TemporaryDirectory() as directory:
            source_path = Path(directory) / "input.txt"
            source_path.write_text(source, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(GUARD), str(source_path), *extra_args],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

    def test_user_selected_openings_and_capacity_review_are_explicit(self):
        policy = (ROOT / "references" / "clip-selection-policy.md").read_text(encoding="utf-8")
        contract = (ROOT / "references" / "runtime-contract.md").read_text(encoding="utf-8")
        self.assertIn("不设候选识别数或展示数上限", policy)
        self.assertIn("用户最多选择 3 个候选", policy)
        self.assertIn("每个已选开头分别生成一条完整成片", policy)
        self.assertIn("每条成片先完整覆盖", policy)
        self.assertIn("超过 100 秒须逐条复核", policy)
        self.assertIn("用户选择商品", contract)

    def test_duration_is_approximate_and_final_audit_is_selected_only(self):
        highlight = (ROOT / "references" / "highlight-selection.md").read_text(encoding="utf-8")
        policy = (ROOT / "references" / "clip-selection-policy.md").read_text(encoding="utf-8")
        self.assertIn("90 秒是有效信息密度目标", policy)
        self.assertIn("写出正文前完成首次容量规划", policy)
        self.assertIn("首稿必须以已完成容量优化的选段为基础", policy)
        self.assertIn("只对实际写出的成片执行终检", FINAL_CHECK)
        self.assertIn("同一根因最多三轮", FINAL_CHECK)

    def test_formal_wool_and_cashmere_terms_do_not_expand_to_static_control(self):
        self.assertTrue("## 正式禁用词库" in GLOBAL_RULES, "formal list heading is missing")
        self.assertTrue("羊毛" in GLOBAL_RULES, "user-authorized wool term is missing")
        self.assertTrue("| `羊绒` | direct |" in GLOBAL_RULES, "user-authorized cashmere term is missing")
        self.assertTrue("字面词匹配，包括组合和比例表达" in GLOBAL_RULES, "cashmere match scope must be explicit")
        self.assertTrue("防静电不是正式禁词" in GLOBAL_RULES, "static-control claims must stay outside the ban")

    def test_guard_normalizes_spacing_and_punctuation_but_keeps_related_cues(self):
        result = self.run_guard(
            "1 1.0 这件羊毛混纺\n"
            "2 1.0 这件绵 羊-毛混纺\n"
            "3 1.0 这个面料可以防静电\n"
            "4 1.0 羊绒花纱围巾\n"
            "5 1.0 特殊纤维防起静电\n"
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["source_rows"], 5)
        self.assertEqual([hit["cue_id"] for hit in report["direct_hits"]], ["1", "2", "4"])
        self.assertEqual(report["excluded_full_cue_ids"], ["1", "2", "4"])
        self.assertEqual(report["status"], "SCAN_COMPLETE")

    def test_selected_cue_and_final_copy_are_hard_blocked_on_a_direct_hit(self):
        with tempfile.TemporaryDirectory() as directory:
            source_path = Path(directory) / "input.txt"
            final_path = Path(directory) / "final.txt"
            source_path.write_text("1 1.0 防静电\n2 1.0 99%绵羊毛\n", encoding="utf-8")
            final_path.write_text("标题：99%绵羊毛大衣\n", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(GUARD),
                    str(source_path),
                    "--selected-ids",
                    "1,2",
                    "--final-text",
                    str(final_path),
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
        self.assertEqual(result.returncode, 1)
        report = json.loads(result.stdout)
        self.assertEqual(report["selected_hit_ids"], ["2"])
        self.assertTrue(report["final_text_hits"])
        self.assertEqual(report["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
