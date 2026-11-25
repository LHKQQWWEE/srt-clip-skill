from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = (ROOT / "references" / "editorial-policy.md").read_text(encoding="utf-8")
FINAL_CHECK = (ROOT / "references" / "final-check.md").read_text(encoding="utf-8")
RUNTIME = (ROOT / "references" / "runtime-current.md").read_text(encoding="utf-8")
PORTABLE = (ROOT / "C2-Universal-Portable.md").read_text(encoding="utf-8")
GOVERNANCE = (ROOT / "references" / "update-protocol.md").read_text(encoding="utf-8")
FIXTURE = json.loads((ROOT / "tests" / "fixtures" / "block-ordering-supplement.json").read_text(encoding="utf-8"))


class ContentBlockPolicyTests(unittest.TestCase):
    def test_open_blocks_and_complete_block_order_are_in_runtime(self):
        for phrase in (
            "开放式内容板块动态编排",
            "板块类型和数量开放",
            "只允许移动完整板块",
            "禁止跨板块混编",
            "独立评估所有板块",
            "不得预设板块数量、优先级、排序",
        ):
            self.assertIn(phrase, POLICY)
            self.assertIn(phrase, RUNTIME)
            self.assertIn(phrase, PORTABLE)
        self.assertIn("板块编排专项终检", FINAL_CHECK)
        self.assertIn("过渡自然", FINAL_CHECK)

    def test_test_plans_cover_each_cue_once_and_move_whole_boards(self):
        cue_ids = set(FIXTURE["cues"])
        story = FIXTURE["required_subsequence"]["cue_ids"]
        orders = []
        for plan in FIXTURE["plans"]:
            board_names = [block["board"] for block in plan["blocks"]]
            self.assertEqual(len(board_names), len(set(board_names)))
            self.assertTrue(set(plan["hook_cue_ids"]).issubset(set(plan["blocks"][0]["cue_ids"])))
            flattened = [cue for block in plan["blocks"] for cue in block["cue_ids"]]
            self.assertCountEqual(flattened, cue_ids)
            self.assertEqual(len(flattened), len(set(flattened)))
            story_block = next(block for block in plan["blocks"] if block["board"] == "revision-story")
            self.assertEqual(story_block["cue_ids"], story)
            orders.append(board_names)
        self.assertNotEqual(orders[0], orders[1])

    def test_synthetic_supplement_is_explicitly_nonproduction(self):
        self.assertIn("Synthetic development-only", FIXTURE["purpose"])
        self.assertIn("Do not use", FIXTURE["purpose"])

    def test_permanent_governance_is_not_in_daily_runtime_or_portable(self):
        for marker in ("自动判断 L1/L2/L3", "本协议仅在开发", "一次性同步、发布"):
            self.assertIn(marker, GOVERNANCE)
            self.assertNotIn(marker, RUNTIME)
            self.assertNotIn(marker, PORTABLE)

    def test_mirror_sync_replaces_stale_files_from_canonical_tree(self):
        spec = importlib.util.spec_from_file_location("sync_skill_mirror", ROOT / "scripts" / "sync_skill_mirror.py")
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "canonical"
            mirror = Path(tmp) / "mirror"
            source.mkdir()
            mirror.mkdir()
            (source / "current.md").write_text("canonical", encoding="utf-8")
            (mirror / "old.md").write_text("stale", encoding="utf-8")
            count = module.sync_mirror(source, mirror)
            self.assertEqual(count, 1)
            self.assertEqual((mirror / "current.md").read_text(encoding="utf-8"), "canonical")
            self.assertFalse((mirror / "old.md").exists())


if __name__ == "__main__":
    unittest.main()
