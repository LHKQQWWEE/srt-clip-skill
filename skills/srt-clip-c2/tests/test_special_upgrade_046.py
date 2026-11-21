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

    def test_every_multi_video_plan_covers_the_full_point_pool_and_waits_for_choice(self):
        self.assertTrue("每条多视频方案也都必须覆盖同一完整卖点池" in SKILL, "per-video coverage rule is missing")
        self.assertTrue("用户选择数量及主题后，再正式生成" in SKILL, "multi-video generation is not gated on user choice")
        self.assertTrue("多条方案并集" in SKILL, "collective coverage must remain documented as a second invariant")
        self.assertFalse("多条最终方案并集覆盖全部有效卖点" in SKILL, "collective coverage cannot replace per-video coverage")
        self.assertTrue("每条视频" in FINAL_CHECK, "final audit must check each delivered video")

    def test_duration_is_not_a_completion_gate_and_failed_acceptance_repairs(self):
        self.assertTrue("时长不作为任务完成条件" in SKILL, "duration must not terminate the task")
        self.assertTrue("PASS / FAIL / BLOCKED" in FINAL_CHECK, "acceptance states are missing")
        self.assertTrue("同一根因最多进行三轮" in FINAL_CHECK, "repair loop must have a bounded limit")
        self.assertTrue("重新运行导致失败的测试" in FINAL_CHECK, "repair must rerun the failing check")

    def test_formal_wool_and_cashmere_terms_do_not_expand_to_static_control(self):
        self.assertTrue("## 正式禁用词库" in GLOBAL_RULES, "formal list heading is missing")
        self.assertTrue("羊毛" in GLOBAL_RULES, "user-authorized wool term is missing")
        self.assertTrue("`羊绒`：" in GLOBAL_RULES, "user-authorized cashmere term is missing")
        self.assertTrue("直接匹配字面词及其组合" in GLOBAL_RULES, "cashmere match scope must be explicit")
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
