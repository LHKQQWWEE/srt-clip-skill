from decimal import Decimal
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import srt_tools
import test_repetition_semantics as prior_cases

# Human-reviewed test source: broad appearance praise competes, while each
# separately useful fit, construction, wearing, and outfit detail remains.
CUES = {
    500: (Decimal("5.0"), "这个针织衫真的特别好看"),
    501: (Decimal("5.0"), "我真的太喜欢这个款了"),
    502: (Decimal("5.0"), "你们看上身效果真的特别漂亮"),
    503: (Decimal("5.0"), "这个款式真的太美了"),
    510: (Decimal("7.25"), "腰线收得高，能修饰胯宽"),
    511: (Decimal("7.25"), "大腿有点肉穿上也不紧"),
    512: (Decimal("7.25"), "面料摸起来很柔软"),
    513: (Decimal("7.25"), "内侧有一层薄磨毛"),
    514: (Decimal("7.25"), "面料有弹性，抬手不扯"),
    515: (Decimal("7.25"), "穿上不显得厚重"),
    516: (Decimal("7.25"), "领口罗纹收边"),
    517: (Decimal("7.25"), "袖口走线收得干净"),
    518: (Decimal("7.25"), "衣摆盖过胯部"),
    519: (Decimal("7.25"), "搭配西装裤适合通勤"),
    520: (Decimal("7.25"), "搭配牛仔裤周末也合适"),
    521: (Decimal("7.25"), "肩线往里收，视觉上更显腰"),
    522: (Decimal("7.25"), "后背有一道竖向分割线"),
    523: (Decimal("7.25"), "坐下后腰部没有明显拉扯感"),
    524: (Decimal("7.25"), "短款外套叠穿时下摆不会堆在腰部"),
    525: (Decimal("7.25"), "转身时后背活动没有明显牵扯"),
}
DENSITY_KEEP = {502, *range(510, 524)}
COMPLETE_KEEP = DENSITY_KEEP | {524, 525}
SOURCE = "\n".join(f"{cue_id} {duration} {text}" for cue_id, (duration, text) in CUES.items())


class Phase3DuplicateControlTests(unittest.TestCase):
    def test_differently_worded_generic_praise_competes_for_one_best_line(self):
        praise_ids = {500, 501, 502, 503}
        self.assertEqual(DENSITY_KEEP & praise_ids, {502})

    def test_same_topic_different_buying_reasons_and_experiences_survive(self):
        self.assertTrue(set(range(510, 524)).issubset(DENSITY_KEEP))
        self.assertEqual(DENSITY_KEEP & {510, 511, 521}, {510, 511, 521})
        self.assertEqual(DENSITY_KEEP & {512, 513, 514, 515}, {512, 513, 514, 515})
        self.assertEqual(DENSITY_KEEP & {519, 520}, {519, 520})

    def test_removed_praise_frees_room_for_unique_information_near_90_seconds(self):
        kept_seconds = sum((CUES[i][0] for i in DENSITY_KEEP), Decimal("0"))
        unfiltered_seconds = sum((CUES[i][0] for i in DENSITY_KEEP | {500, 501, 503}), Decimal("0"))
        self.assertEqual(kept_seconds / Decimal("1.2"), Decimal("88.75"))
        self.assertEqual(unfiltered_seconds / Decimal("1.2"), Decimal("101.25"))

    def test_useful_information_can_continue_past_90_seconds_without_hard_cut(self):
        kept_seconds = sum((CUES[i][0] for i in COMPLETE_KEEP), Decimal("0"))
        self.assertGreater(kept_seconds / Decimal("1.2"), Decimal("90"))
        self.assertIn(524, COMPLETE_KEEP)
        self.assertIn(525, COMPLETE_KEEP)

    def test_selected_source_text_ids_and_durations_remain_verifiable(self):
        report = srt_tools.parse_source(SOURCE)
        source = {int(cue.cue_id): cue for cue in report.cues}
        self.assertEqual(set(source), set(CUES))
        for cue_id in COMPLETE_KEEP:
            self.assertEqual(source[cue_id].original_text, CUES[cue_id][1])
            self.assertEqual(source[cue_id].duration_ms, CUES[cue_id][0] * Decimal("1000"))
        ordered_selected = [source[i] for i in sorted(COMPLETE_KEEP)]
        self.assertEqual([cue.source_order for cue in ordered_selected], sorted(cue.source_order for cue in ordered_selected))

    def test_previous_human_reviewed_praise_pair_now_keeps_only_one(self):
        self.assertEqual(set(prior_cases.PANTS_SELECTED) & {497, 498}, {498})

    def test_active_duration_policy_names_90_second_reference_not_hard_cut(self):
        policy = (ROOT / "references" / "clip-selection-policy.md").read_text(encoding="utf-8")
        self.assertIn("90 秒", policy)
        self.assertIn("信息密度参考目标", policy)
        self.assertIn("不是硬截断条件", policy)


if __name__ == "__main__":
    unittest.main()
