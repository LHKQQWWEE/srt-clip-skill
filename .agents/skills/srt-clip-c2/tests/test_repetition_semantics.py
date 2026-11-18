from decimal import Decimal, ROUND_HALF_UP
import unittest


# Human-reviewed semantic gold cases from the 0.4.0 shoe transcript and a
# second product window. This fixture guards the intended editorial decisions;
# it is not a text-similarity algorithm and does not claim to automate AI judgment.
SHOE = {
    17: ("1.24", "就鞋型很好"),
    19: ("1.62", "这双鞋你穿上"),
    20: ("1.34", "你不会觉得"),
    21: ("3.16", "你不会觉得你是穿了一双毛的鞋子"),
    22: ("1.90", "它任何毛不钻出来"),
    23: ("1.46", "然后它不发抛"),
    24: ("1.04", "什么意思呢"),
    25: ("1.44", "就是它不发胖"),
    26: ("1.97", "就跟单的鞋子一样"),
    27: ("1.70", "是瘦窄型的"),
    48: ("1.06", "它就是很显贵"),
    34: ("1.839", "这个颜色会更好搭配"),
    35: ("1.621", "这个颜色不用穿搭"),
    36: ("0.90", "就是更好搭配"),
    37: ("0.68", "你穿什么"),
    38: ("2.28", "穿深色这双鞋子都可以的啊"),
    102: ("0.82", "不偏大"),
    103: ("0.94", "正码正拍"),
    104: ("0.84", "正码正拍"),
    105: ("1.60", "我觉得半马脚可以拍小"),
    106: ("1.44", "半码脚可以拍小"),
    140: ("2.34", "正码就我穿36，我是瘦脚"),
    141: ("2.35", "然后穿这个鞋会有一点松量的"),
    142: ("1.36", "会有一点点松亮"),
    143: ("1.40", "因为里面的毛踩踩"),
    144: ("2.16", "你穿久了肯定会稍微有点瘪的嘛"),
    145: ("1.24", "嗯，我现在穿久了"),
    146: ("2.28", "但你穿上袜子就完全刚刚好"),
    147: ("3.04", "所以你们胖脚、肉脚、宽脚的也是正码正拍"),
    148: ("1.63", "正码正拍啊"),
    149: ("2.07", "瘦脚的半马脚可以拍小"),
}

PANTS = {
    497: ("1.40", "对，显高显瘦"),
    498: ("0.92", "真显高显瘦"),
    499: ("1.72", "因为我们都做高腰的啊"),
    500: ("0.88", "其实都做高腰"),
    501: ("1.88", "上身比例的高腰裤"),
    502: ("1.48", "比例感很好"),
    503: ("2.76", "且这个位置做的很服帖"),
    504: ("2.68", "这块位置他做的特别的服帖"),
    506: ("2.78", "梨形穿S，嗯"),
    507: ("2.44", "呃，胯窄的选XS"),
}

SHOE_SELECTED = [19, 21, 22, 25, 26, 27, 48, 34, 35, 37, 38,
                 102, 103, 106, 140, 141, 143, 144, 145, 146, 147]
PANTS_SELECTED = [497, 498, 499, 501, 502, 504, 506, 507]


def estimate(selected, cues):
    raw = sum(Decimal(cues[i][0]) for i in selected)
    accelerated = (raw / Decimal("1.2")).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)
    return raw, accelerated


class RepetitionSemanticRegressionTests(unittest.TestCase):
    def test_incomplete_restart_is_removed_but_complete_sentence_survives(self):
        self.assertEqual(SHOE[20][1], "你不会觉得")
        self.assertEqual(SHOE[21][1], "你不会觉得你是穿了一双毛的鞋子")
        self.assertNotIn(20, SHOE_SELECTED)
        self.assertIn(21, SHOE_SELECTED)

    def test_progressive_explanation_and_analogy_are_not_collapsed(self):
        # 25 clarifies the bulky-look concern, 26 gives a familiar comparison,
        # and 27 names the resulting silhouette; these are not word-match repeats.
        for cue_id in (25, 26, 27):
            self.assertIn(cue_id, SHOE_SELECTED)
        self.assertNotIn(23, SHOE_SELECTED)  # unclear ASR wording, not needed for the complete benefit
        self.assertNotIn(24, SHOE_SELECTED)  # question/repair setup is unnecessary once 23 is omitted

    def test_effective_emphasis_can_survive_without_new_fact(self):
        # The pants clip retains the intensified restatement for memory and conviction.
        self.assertEqual(PANTS[497][1], "对，显高显瘦")
        self.assertEqual(PANTS[498][1], "真显高显瘦")
        self.assertIn(497, PANTS_SELECTED)
        self.assertIn(498, PANTS_SELECTED)

    def test_overstatement_is_trimmed_without_losing_distinct_reason(self):
        # 35 adds a practical styling framing; 36 simply restates easier-to-match.
        self.assertIn(34, SHOE_SELECTED)
        self.assertIn(35, SHOE_SELECTED)
        self.assertNotIn(36, SHOE_SELECTED)
        # 103 contains the fit advice; 104 repeats it verbatim.
        self.assertIn(103, SHOE_SELECTED)
        self.assertNotIn(104, SHOE_SELECTED)
        # 141/142 and 147/148: retain the complete useful version, trim the no-gain echo.
        self.assertIn(141, SHOE_SELECTED)
        self.assertNotIn(142, SHOE_SELECTED)
        self.assertIn(147, SHOE_SELECTED)
        self.assertNotIn(148, SHOE_SELECTED)

    def test_independent_fit_reasons_and_conditions_survive(self):
        for cue_id in (102, 103, 106, 140, 141, 143, 144, 145, 146, 147):
            self.assertIn(cue_id, SHOE_SELECTED)
        self.assertNotIn(105, SHOE_SELECTED)  # partial, misrecognized restart before corrected line 106
        self.assertNotIn(149, SHOE_SELECTED)  # suspected ASR error; 106 already states the clear advice

    def test_human_reviewed_clips_are_not_padded_to_duration_floor(self):
        shoe_raw, shoe_1_2x = estimate(SHOE_SELECTED, SHOE)
        pants_raw, pants_1_2x = estimate(PANTS_SELECTED, PANTS)
        self.assertEqual(shoe_raw, Decimal("37.280"))
        self.assertEqual(shoe_1_2x, Decimal("31.067"))
        self.assertEqual(pants_raw, Decimal("15.30"))
        self.assertEqual(pants_1_2x, Decimal("12.750"))
        self.assertLess(shoe_1_2x, Decimal("45"))
        self.assertLess(pants_1_2x, Decimal("45"))
        # Semantic QA must label both as short candidates rather than retain weak
        # repeats simply to cross the formal 45-second floor.

    def test_duplicate_decisions_are_defined_in_active_rules(self):
        from pathlib import Path
        root = Path(__file__).resolve().parents[1]
        editorial = (root / "references/editorial-policy.md").read_text(encoding="utf-8")
        selection = (root / "references/highlight-selection.md").read_text(encoding="utf-8")
        final_check = (root / "references/final-check.md").read_text(encoding="utf-8")
        for category in ("机械性重复", "强调性重复", "递进性重复", "过度性重复"):
            self.assertIn(category, editorial)
            self.assertIn(category, selection)
        self.assertIn("词面相似度", selection)
        self.assertIn("说服增量", selection)
        self.assertIn("挤占更重要的独立购买理由", final_check)


if __name__ == "__main__":
    unittest.main()
