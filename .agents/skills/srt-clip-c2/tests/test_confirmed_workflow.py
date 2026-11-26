import dataclasses
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
import srt_tools


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class ConfirmedWorkflowPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = read("references/runtime-contract.md")
        cls.policy = read("references/clip-selection-policy.md")
        cls.audit = read("references/final-check.md")
        cls.entry = read("SKILL.md")
        cls.runtime = read("references/runtime-current.md")

    def test_01_multiple_products_pause_before_opening_candidates(self):
        self.assertIn("归类为主商品、独立讲解商品、搭配辅助或归属待定", self.contract)
        self.assertIn("等待用户选择商品", self.contract)
        self.assertIn("确认后才为所选商品生成开头候选", self.contract)
        self.assertIn("确认前不得生成开头候选", self.contract)

    def test_02_opening_candidates_have_only_four_fields_and_no_default(self):
        for field in ("方案名称", "开头原话", "原始 SRT 序号", "预估时长"):
            self.assertIn(field, self.policy)
        self.assertIn("用户最多选择 3 个候选", self.policy)
        self.assertIn("不得预选", self.policy)
        self.assertIn("不得凑数", self.policy)
        self.assertIn("只为用户选中的开头生成成片", self.policy)

    def test_03_each_selected_opening_has_its_own_complete_dynamic_cut(self):
        self.assertIn("每个已选开头分别生成一条完整成片", self.policy)
        self.assertIn("每条独立重新编排正文并动态重排", self.policy)
        self.assertIn("信息池内全部有效卖点", self.policy)
        self.assertIn("120 秒不是目标，也不是硬上限", self.policy)
        self.assertIn("明显超过 120 秒", self.policy)

    def test_04_text_only_context_tracks_event_lifecycle(self):
        for state in ("待回应", "延迟回应", "已回应", "删除但保留必要铺垫", "无法确定"):
            self.assertIn(state, self.contract)
        self.assertIn("仅凭可靠字幕文本即可执行", self.contract)
        self.assertIn("不要求视频或图片", self.contract)
        self.assertIn("动作与结果", self.contract)

    def test_05_daily_entry_has_no_python_or_script_dependency(self):
        for path, text in (("SKILL.md", self.entry), ("runtime-contract", self.contract), ("runtime-current", self.runtime)):
            with self.subTest(path=path):
                self.assertNotIn("python scripts/", text.lower())
                self.assertNotIn("python -m", text.lower())
                self.assertNotIn(".py`", text.lower())
        self.assertIn("不调用 Python、脚本或外部工具", self.contract)

    def test_06_sequence_accuracy_is_a_hard_gate_and_five_parts_are_frozen(self):
        for phrase in (
            "不可变原始映射",
            "原话、时长",
            "逐条核对",
            "最终序号输出必须与所选原始序号逐项完全一致",
            "任一不一致即 FAIL",
        ):
            self.assertIn(phrase, self.audit)
        self.assertIn("固定五部分交付", self.contract)
        self.assertIn("不添加第六部分", self.contract)


class ImmutableSequenceGateTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(callable(getattr(srt_tools, "verify_final_output", None)))
        self.source_text = (
            "1\n00:00:00,000 --> 00:00:01,000\n真实开头原话\n\n"
            "2\n00:00:01,500 --> 00:00:02,500\n商品点甲\n\n"
            "3\n00:00:02,500 --> 00:00:06,000\n商品点甲的必要证据\n\n"
            "5\n00:00:10,000 --> 00:00:14,000\n商品点乙"
        )
        self.source = srt_tools.parse_source(self.source_text)
        self.selection = {
            "verification_mode": "script",
            "source_sha256": self.source.source_sha256,
            "selected_ids": ["1", "2", "3", "5"],
            "selling_points": [
                {"id": "P1", "support_ids": ["2"], "necessary_evidence_ids": ["3"], "required_condition_ids": []},
                {"id": "P2", "support_ids": ["5"], "necessary_evidence_ids": [], "required_condition_ids": []},
            ],
            "roles": [
                {"cue_id": "1", "role": "必要衔接"},
                {"cue_id": "2", "role": "独立卖点"},
                {"cue_id": "3", "role": "证据"},
                {"cue_id": "5", "role": "独立卖点"},
            ],
            "flags": [],
        }

    def test_immutable_cue_records_bind_id_text_and_exact_duration(self):
        self.assertIsInstance(self.source.cues, tuple)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            self.source.cues[0].original_text = "错误替换"
        exported = srt_tools.preprocess_text(self.source_text, formal_terms=[])
        self.assertEqual(
            [(row["id"], row["original_text"], row["duration_ms_exact"]) for row in exported["source_map"]],
            [("1", "真实开头原话", "1000"), ("2", "商品点甲", "1000"), ("3", "商品点甲的必要证据", "3500"), ("5", "商品点乙", "4000")],
        )

    def test_final_body_and_fifth_part_sequence_match_source_exactly(self):
        assembly = srt_tools.assemble_selection(self.source, self.selection, formal_terms=[])
        result = srt_tools.verify_final_output(
            self.source,
            self.selection,
            assembly,
            final_text="\n".join(cue.original_text for cue in self.source.cues),
            final_sequence="1,2,3,5",
        )
        self.assertEqual(result["status"], "PASS")

    def test_any_text_or_final_sequence_mismatch_fails(self):
        assembly = srt_tools.assemble_selection(self.source, self.selection, formal_terms=[])
        wrong_text = srt_tools.verify_final_output(
            self.source, self.selection, assembly, "\n错误替换\n".join(c.original_text for c in self.source.cues), "1,2,3,5"
        )
        wrong_sequence = srt_tools.verify_final_output(
            self.source, self.selection, assembly, assembly["body_text"], "1,3,2,5"
        )
        self.assertEqual(wrong_text["status"], "FAIL")
        self.assertEqual(wrong_sequence["status"], "FAIL")

    def test_two_independent_selections_keep_independent_bodies_and_durations(self):
        first = srt_tools.assemble_selection(self.source, self.selection, formal_terms=[])
        other = dict(
            self.selection,
            selected_ids=["1", "5", "2", "3"],
            roles=[self.selection["roles"][0], self.selection["roles"][3], self.selection["roles"][1], self.selection["roles"][2]],
        )
        second = srt_tools.assemble_selection(self.source, other, formal_terms=[])
        self.assertEqual(first["body_text"], "真实开头原话\n商品点甲\n商品点甲的必要证据\n商品点乙")
        self.assertEqual(second["body_text"], "真实开头原话\n商品点乙\n商品点甲\n商品点甲的必要证据")
        self.assertNotEqual(first["source_duration_ms"], second["source_duration_ms"])
        self.assertEqual(first["fifth_part_sequence"], "1,2,3,5")
        self.assertEqual(second["fifth_part_sequence"], "1,5,2,3")


if __name__ == "__main__":
    unittest.main()
