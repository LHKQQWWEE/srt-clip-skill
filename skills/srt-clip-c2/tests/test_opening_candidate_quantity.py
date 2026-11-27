from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = (ROOT / "references" / "clip-selection-policy.md").read_text(encoding="utf-8")
CONTRACT = (ROOT / "references" / "runtime-contract.md").read_text(encoding="utf-8")
FINAL_CHECK = (ROOT / "references" / "final-check.md").read_text(encoding="utf-8")
EDITORIAL = (ROOT / "references" / "editorial-policy.md").read_text(encoding="utf-8")
CONSTITUTION = (ROOT / "references" / "ai-first-constitution.md").read_text(encoding="utf-8")

FIELDS = ("方案名称", "开头原话", "原始 SRT 序号", "预估时长")


def display_qualified_candidates(candidates):
    # Render all distinct candidates already marked as quality-qualified.
    return list(candidates)


def cuts_for_selection(candidates):
    # The user selection cap is separate from the uncapped display list.
    if len(candidates) > 3:
        raise ValueError("用户最多选择 3 个开头")
    return list(candidates)


def render_clips(selected_openers, bodies, required_points):
    """Build test outputs keyed to the user's exact opener and audit each independently."""
    if len(selected_openers) > 3:
        raise ValueError("用户最多选择 3 个开头")
    clips = []
    for opener in selected_openers:
        body = bodies[opener["id"]]
        clips.append({
            "opening_id": opener["id"],
            "opening_text": opener["开头原话"],
            "cues": [opener, *body],
            "blocks": ["opening", *[item["block"] for item in body]],
        })
    for clip, opener in zip(clips, selected_openers):
        if clip["cues"][0]["id"] != opener["id"] or clip["cues"][0]["开头原话"] != opener["开头原话"]:
            raise AssertionError("成片未从对应用户所选开头开始")
        if not required_points.issubset({point for item in clip["cues"] for point in item.get("points", set())}):
            raise AssertionError("单条成片未覆盖全部有效卖点")
    return clips


class OpeningCandidateQuantityTests(unittest.TestCase):
    def test_policy_explicitly_separates_uncapped_display_from_selection_cap(self):
        self.assertIn("所有达到现有质量门槛", POLICY)
        self.assertIn("不设候选识别数或展示数上限", POLICY)
        self.assertIn("彼此实质不同", POLICY)
        self.assertIn("同一开头的轻微改写或实质相同表达不得包装成多个候选", POLICY)
        self.assertIn("用户最多选择 3 个候选", POLICY)
        self.assertIn("不得静默截断或代选", POLICY)
        self.assertIn("遗漏任何达到现有质量门槛的候选", FINAL_CHECK)
        self.assertIn("不设识别或展示数量上限", CONSTITUTION)
        self.assertIn("用户最多选择三个", CONSTITUTION)
        self.assertIn("展示全部合格且彼此实质不同的候选", EDITORIAL)
        self.assertIn("候选展示不设数量上限", EDITORIAL)

    def test_all_qualified_candidate_count_cases(self):
        for count in (0, 1, 3, 5, 10):
            with self.subTest(candidate_count=count):
                candidates = [
                    {
                        "id": index,
                        "方案名称": f"方案 {index + 1}",
                        "开头原话": f"合格且互不重复的原话 {index + 1}",
                        "原始 SRT 序号": str(index + 1),
                        "预估时长": "3 秒",
                        "quality_pass": True,
                    }
                    for index in range(count)
                ]
                qualified = [candidate for candidate in candidates if candidate["quality_pass"]]
                displayed = display_qualified_candidates(qualified)
                self.assertEqual(len(displayed), count)
                self.assertEqual([item["id"] for item in displayed], list(range(count)))
                for item in displayed:
                    self.assertEqual(tuple(field for field in FIELDS if field in item), FIELDS)

    def test_user_selection_limit_is_three_and_selected_count_maps_to_cuts(self):
        candidates = [{"id": index, "独立完整成片": True} for index in range(10)]
        for count in (1, 3):
            with self.subTest(selected_count=count):
                cuts = cuts_for_selection(candidates[:count])
                self.assertEqual(len(cuts), count)
                self.assertTrue(all(cut["独立完整成片"] for cut in cuts))
        with self.assertRaisesRegex(ValueError, "最多选择 3 个"):
            cuts_for_selection(candidates[:4])
        self.assertIn("每个已选开头分别生成一条完整成片", POLICY)
        self.assertIn("每条成片先完整覆盖", POLICY)

    def test_each_cut_starts_with_exact_selected_opener_and_has_full_coverage(self):
        openers = [
            {"id": "A", "开头原话": "这件上身特别利落", "points": {"fit"}},
            {"id": "B", "开头原话": "这块面料很有垂感", "points": {"fabric"}},
        ]
        bodies = {
            "A": [
                {"id": "A2", "block": "fit-proof", "points": {"fit-proof"}},
                {"id": "A3", "block": "fabric", "points": {"fabric"}},
                {"id": "A4", "block": "fabric-proof", "points": {"fabric-proof"}},
            ],
            "B": [
                {"id": "B2", "block": "fabric-proof", "points": {"fabric-proof"}},
                {"id": "B3", "block": "fit", "points": {"fit"}},
                {"id": "B4", "block": "fit-proof", "points": {"fit-proof"}},
            ],
        }
        required = {"fit", "fit-proof", "fabric", "fabric-proof"}
        clips = render_clips(openers, bodies, required)
        self.assertEqual(len(clips), len(openers))
        for clip, opener in zip(clips, openers):
            self.assertEqual(clip["cues"][0]["id"], opener["id"])
            self.assertEqual(clip["cues"][0]["开头原话"], opener["开头原话"])
            self.assertEqual({point for cue in clip["cues"] for point in cue.get("points", set())}, required)
        self.assertNotEqual(clips[0]["blocks"], clips[1]["blocks"])

    def test_fixed_fields_and_open_hook_rules_remain(self):
        self.assertIn("每个候选只显示四项", POLICY)
        for field in FIELDS:
            self.assertIn(field, POLICY)
        self.assertIn("开放式观看动力优先级", EDITORIAL)
        self.assertIn("前 2 秒", EDITORIAL)
        self.assertIn("前 5 秒", EDITORIAL)
        self.assertIn("候选池纳入其中全部合格候选", EDITORIAL)


if __name__ == "__main__":
    unittest.main()
