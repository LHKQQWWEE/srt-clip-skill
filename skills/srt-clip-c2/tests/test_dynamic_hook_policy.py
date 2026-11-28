from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def text_sha256(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


class DynamicHookPolicyTests(unittest.TestCase):
    def test_priority_defines_candidate_pool_without_selecting_a_winner(self) -> None:
        policy = read("references/editorial-policy.md")
        self.assertIn("动态顾客心理驱动钩子机制", policy)
        self.assertIn("陌生潜在买家", policy)
        self.assertIn("继续观看欲望", policy)
        self.assertIn("开放式观看动力优先级", policy)
        self.assertIn("候选池纳入其中全部合格候选", policy)
        self.assertIn("只有完全不存在合格的第一优先级候选时", policy)
        self.assertIn("不用于给候选排出一个胜者", policy)
        self.assertIn("池内所有达到质量门槛且实质不同的候选都必须展示", policy)
        self.assertIn("候选展示不设数量上限", policy)
        self.assertIn("用户最多选择三个", policy)

    def test_open_ended_types_and_joint_timing_windows_remain(self) -> None:
        policy = read("references/editorial-policy.md")
        contract = read("references/runtime-contract.md")
        for dimension in ("情绪感染", "审美种草", "视觉好奇", "动作展示", "穿搭种草", "反差惊喜", "情感共鸣", "上身效果", "场景代入", "悬念期待", "质感种草", "设计吸引", "体验感染", "需求唤醒"):
            self.assertIn(dimension, policy)
        self.assertIn("联合编排为一个连续开头单元", policy)
        self.assertIn("前 2 秒能否吸引注意", policy)
        self.assertIn("前 5 秒能否把观看兴趣连续承接下去", policy)
        self.assertIn("沿用全片估时的 1.2 倍速", policy)
        self.assertIn("原素材累计 2.4 秒", policy)
        self.assertIn("原素材累计 6 秒", policy)
        self.assertIn("不得为对齐时间硬截完整原话", policy)
        self.assertIn("优先级只确定候选资格范围", contract)
        self.assertIn("候选展示不限量", contract)

    def test_complete_product_pool_precedes_candidate_qualification(self) -> None:
        policy = read("references/editorial-policy.md")
        contract = read("references/runtime-contract.md")
        self.assertLess(policy.index("完整读取目标商品全部有效窗口"), policy.index("才识别开头候选"))
        self.assertLess(contract.index("建立完整信息池"), contract.index("开头候选等待关口"))
        self.assertIn("不比较、评分或排名完整成片", policy)
        self.assertIn("每条方案继续覆盖全部有效卖点", policy)

    def test_truth_and_srt_visual_limits_remain_hard_boundaries(self) -> None:
        policy = read("references/editorial-policy.md")
        for phrase in ("商品归属", "正式合规", "自然语义", "后文兑现", "仅凭 SRT", "不能确认实际画面", "不能确认主播的真实语气、表情或情绪表现"):
            self.assertIn(phrase, policy)

    def test_opening_does_not_reduce_coverage_or_create_a_source_cta(self) -> None:
        policy = read("references/editorial-policy.md")
        selection = read("references/clip-selection-policy.md")
        self.assertIn("每条方案继续覆盖全部有效卖点", policy)
        self.assertIn("references/promotion-policy.md", policy)
        self.assertIn("每条成片先完整覆盖信息池内全部有效卖点", selection)

    def test_schema_describes_user_choice_and_uncapped_candidates(self) -> None:
        schema = json.loads(read("scripts/selection.schema.json"))
        opening = schema["properties"]["opening_choice"]
        self.assertIn("exact real opening selected by the user", opening["description"])
        self.assertIn("show every distinct qualified first-priority candidate", opening["description"])
        self.assertIn("does not rank a winner or select for the user", opening["description"])
        self.assertIn("Candidate display has no count limit", opening["description"])
        self.assertIn("up to three", opening["description"])
        self.assertIn("each selected opening starts its own independent complete cut", opening["description"])

    def test_current_regression_matrix_covers_all_required_selection_edges(self) -> None:
        policy = read("references/clip-selection-policy.md")
        for term in ("不设候选识别数或展示数上限", "不得预选", "用户最多选择 3 个候选", "对应用户所选开头原话开始", "每条成片独立划分和编排内容板块", "每条成片先完整覆盖", "不新增第六部分"):
            self.assertIn(term, policy)

    def test_versions_manifest_hashes_and_mirror_agree(self) -> None:
        plugin_root = ROOT.parent.parent
        plugin = json.loads((plugin_root / "plugin.json").read_text(encoding="utf-8"))
        core_version = (plugin_root / "VERSION").read_text(encoding="utf-8").strip()
        skill_version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        manifest = json.loads(read("references/runtime-manifest.json"))
        summary = json.loads(read("references/execution-summary.json"))
        self.assertEqual(core_version, "0.4.7")
        self.assertEqual(skill_version, "0.4.51")
        self.assertEqual(plugin["version"], "0.4.51")
        self.assertEqual(manifest["core_version"], core_version)
        self.assertEqual(manifest["skill_version"], skill_version)
        self.assertEqual(summary["core_version"], core_version)
        self.assertEqual(summary["skill_version"], skill_version)
        self.assertIn("候选展示不限量", summary["summary"])
        self.assertIn("对应用户所选开头原话开始", summary["summary"])
        for relative, digest in manifest["source_hashes"].items():
            self.assertEqual(text_sha256(ROOT / relative), digest)
        self.assertEqual(text_sha256(ROOT / "references/runtime-current.md"), manifest["runtime_sha256"])
        mirrored = plugin_root / ".agents/skills/srt-clip-c2"
        for path in ROOT.rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
                other = mirrored / path.relative_to(ROOT)
                self.assertTrue(other.is_file(), str(other))
                self.assertEqual(path.read_bytes(), other.read_bytes(), str(path.relative_to(ROOT)))


if __name__ == "__main__":
    unittest.main()
