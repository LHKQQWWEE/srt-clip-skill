import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import release_gate


class ReleaseGateSemanticTests(unittest.TestCase):
    def test_release_target_matches_skill_version(self):
        self.assertEqual(release_gate.EXPECTED_SKILL, (ROOT / "VERSION").read_text(encoding="utf-8").strip())

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
        current = "不得按固定成交模板排列正文；正文根据真实购买信息动态组织。"
        self.assertEqual(release_gate.semantic_conflicts(current), [])

    def test_unrelated_negation_does_not_hide_a_retired_candidate_cap(self):
        stale = "候选最多展示" + "3" + "个。不得改写原话。"
        self.assertEqual(
            [item[1] for item in release_gate.semantic_conflicts(stale)],
            ["candidate_display_cap"],
        )

    def test_detects_retired_duration_and_closing_activity_rules_in_plain_chinese(self):
        samples = (
            ("旧口径要求超过" + "两分钟" + "之后才可以删减。", "duration_cap"),
            ("福利仍在活动期，所以" +
             "可以留在最后。", "closing_activity_exception"),
            ("Skill / Plugin 0.4." + "44", "stale_version"),
        )
        for text, expected in samples:
            with self.subTest(expected=expected):
                self.assertEqual([item[1] for item in release_gate.semantic_conflicts(text)], [expected])

    def test_allows_current_rule_that_explicitly_rejects_activity_exceptions(self):
        current = "活动有效期或活动素材需求不构成例外。"
        self.assertEqual(release_gate.semantic_conflicts(current), [])

    def test_stale_runtime_policy_markers_are_blocked(self):
        stale_markers = ("0.4." + "43", "old-" + "dictionary", "第三" + "阶段")
        for marker in stale_markers:
            with self.subTest(marker=marker), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                reference = root / "skills" / "srt-clip-c2" / "references" / "global-rules.md"
                reference.parent.mkdir(parents=True)
                reference.write_text("retired marker: " + marker, encoding="utf-8")
                with patch.object(release_gate, "PLUGIN_ROOT", root):
                    with self.assertRaisesRegex(ValueError, "stale"):
                        release_gate.assert_no_historical_package_files()

    def test_semantic_scan_excludes_gitignored_superpowers_work_notes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".superpowers" / "sdd").mkdir(parents=True)
            note = root / ".superpowers" / "sdd" / "old-note.md"
            note.write_text("local working note", encoding="utf-8")
            readme = root / "README.md"
            readme.write_text("release source", encoding="utf-8")
            with patch.object(release_gate, "PLUGIN_ROOT", root):
                paths = release_gate.semantic_surface_paths()
            self.assertIn(readme, paths)
            self.assertNotIn(note, paths)

    def test_empty_acceptance_directory_is_not_historical_content(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs" / "acceptance").mkdir(parents=True)
            with patch.object(release_gate, "PLUGIN_ROOT", root):
                release_gate.assert_no_historical_package_files()

    def test_stale_phase_plan_is_blocked_from_current_release_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan = root / "docs" / "superpowers" / "plans" / "2026-11-27-c2-phase3.md"
            plan.parent.mkdir(parents=True)
            plan.write_text("Target Skill 0.4." + "44; old duration policy.", encoding="utf-8")
            with patch.object(release_gate, "PLUGIN_ROOT", root):
                with self.assertRaisesRegex(ValueError, "historical"):
                    release_gate.assert_no_historical_package_files()

    def test_current_changelog_rejects_old_version_history(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "CHANGELOG.md").write_text(
                "# Current release\n\n## Skill / Plugin 0.4.48\n\nCurrent.\n\n## Skill / Plugin 0.4." + "46\n\nOld.\n",
                encoding="utf-8",
            )
            with patch.object(release_gate, "PLUGIN_ROOT", root):
                with self.assertRaisesRegex(ValueError, "historical"):
                    release_gate.assert_no_historical_package_files()


if __name__ == "__main__":
    unittest.main()
