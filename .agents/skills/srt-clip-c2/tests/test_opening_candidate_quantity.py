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
        self.assertNotIn("最多三个且无预选", FINAL_CHECK)
        self.assertNotIn("候选最多三个", POLICY)
        self.assertNotIn("最多 3 个真实、合格的开头候选", POLICY)

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
        self.assertIn("每条常规时长方案须独立覆盖", POLICY)

    def test_fixed_fields_and_open_hook_rules_remain(self):
        self.assertIn("每个候选只显示四项", POLICY)
        for field in FIELDS:
            self.assertIn(field, POLICY)
        self.assertIn("开放式观看动力优先级", EDITORIAL)
        self.assertIn("前 2 秒", EDITORIAL)
        self.assertIn("前 5 秒", EDITORIAL)
        self.assertIn("存在合格的第一优先级开头候选，必须从这些候选中动态择优", EDITORIAL)


if __name__ == "__main__":
    unittest.main()
