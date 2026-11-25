import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import release_gate


class ReleaseGateSemanticTests(unittest.TestCase):
    def test_flags_retired_semantic_variants(self):
        from_codes = lambda codes: "".join(chr(value) for value in codes)
        stale_share = from_codes([22810, 24320, 22836, 20801, 35768, 20849, 20139, 21516, 19968, 26368, 20339, 38057, 23376])
        stale_cap = from_codes([20505, 36873, 26368, 22810, 23637, 31034, 19977, 20010])
        stale_auto_pick = "AI " + from_codes([40664, 35748, 36873, 25321, 24320, 22836])
        stale_fixed_order = from_codes([20869, 23481, 32467, 26500, 24517, 39035, 25353, 22266, 23450, 27169, 26495])
        for sample, label in (
            (stale_share, "hook_reuse"),
            (stale_cap, "candidate_display_cap"),
            (stale_auto_pick, "automatic_user_choice"),
            (stale_fixed_order, "fixed_block_order"),
        ):
            with self.subTest(label=label):
                self.assertEqual([item[1] for item in release_gate.semantic_conflicts(sample)], [label])

    def test_allows_current_user_cap_and_body_reuse_rules(self):
        current = "用户最多选择 3 个候选。主体内容可合理复用，但每条成片仍从对应用户所选开头开始。"
        self.assertEqual(release_gate.semantic_conflicts(current), [])

    def test_allows_negated_fixed_template_prohibition(self):
        current = "不得按固定模板排列内容板块；板块类型和数量由当前素材决定。"
        self.assertEqual(release_gate.semantic_conflicts(current), [])


if __name__ == "__main__":
    unittest.main()
