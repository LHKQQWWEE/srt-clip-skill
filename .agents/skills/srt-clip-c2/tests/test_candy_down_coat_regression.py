import json
import unittest
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "candy-down-coat-2166-regression.json"


class CandyDownCoatRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_five_historical_sequence_lists_recalculate_from_real_source_durations(self):
        self.assertEqual(self.fixture["source"]["cue_count"], 2166)
        self.assertEqual(self.fixture["source"]["sha256"], "BB2E80D50950B0360A33C9F7EBAA36C31B4AF94AD980A6E2DABA8803C273ECF5")
        expected = {
            "A114": (114, "170.870", "142.3916666666666666666666667"),
            "E114": (114, "170.870", "142.3916666666666666666666667"),
            "A70": (70, "104.970", "87.475"),
            "E69": (69, "104.370", "86.975"),
            "C74": (74, "113.910", "94.925"),
        }
        durations = self.fixture["selected_cue_durations_seconds"]
        for name, (count, raw_expected, playback_expected) in expected.items():
            with self.subTest(selection=name):
                row = self.fixture["selection_sets"][name]
                ids = [str(cue_id) for cue_id in row["sequence_ids"]]
                self.assertEqual(row["cue_count"], count)
                self.assertEqual(len(ids), count)
                self.assertEqual(len(set(ids)), count)
                self.assertTrue(set(ids) <= set(durations))
                raw = sum((Decimal(durations[cue_id]) for cue_id in ids), Decimal(0))
                playback = raw / Decimal("1.2")
                self.assertEqual(format(raw, "f"), raw_expected)
                self.assertEqual(format(playback, "f"), playback_expected)

    def test_third_version_conflicting_duration_claim_is_resolved_from_its_74_ids(self):
        row = self.fixture["selection_sets"]["C74"]
        raw = sum((Decimal(self.fixture["selected_cue_durations_seconds"][str(cue_id)]) for cue_id in row["sequence_ids"]), Decimal(0))
        playback = raw / Decimal("1.2")
        self.assertNotEqual(raw, Decimal("113.37"))
        self.assertEqual(raw, Decimal("113.910"))
        self.assertEqual(playback, Decimal("94.925"))
        self.assertEqual(playback.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), Decimal("94.93"))

    def test_c_version_keeps_distinct_purchase_conditions_and_supporting_details(self):
        selected = set(self.fixture["selection_sets"]["C74"]["sequence_ids"])
        for case, cue_ids in self.fixture["coverage_cases"].items():
            with self.subTest(case=case):
                self.assertTrue(set(cue_ids) <= selected)
        text = self.fixture["critical_cue_texts"]
        self.assertIn("黄黑皮", text["674"])
        self.assertIn("选蓝色", text["674"])
        self.assertIn("更没有心理负担", text["676"])
        self.assertIn("黄黑皮素颜", text["1295"])
        self.assertIn("买这个粉色", text["1296"])
        self.assertIn("更立体", text["1716"])
        self.assertIn("压下去", text["1614"])
        self.assertIn("容易回来", text["1615"])
        self.assertIn("普通九零白鸭绒", text["1210"])


if __name__ == "__main__":
    unittest.main()
