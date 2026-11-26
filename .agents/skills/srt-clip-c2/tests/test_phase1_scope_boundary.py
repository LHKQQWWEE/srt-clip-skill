import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT.parents[1]
MIRROR = PLUGIN_ROOT / ".agents" / "skills" / ROOT.name


class PhaseOneScopeBoundaryTests(unittest.TestCase):
    def test_deferred_block_ordering_is_absent_from_active_rules(self):
        paths = (
            ROOT / "SKILL.md",
            ROOT / "ENVIRONMENT.md",
            ROOT / "references" / "ai-first-constitution.md",
            ROOT / "references" / "clip-selection-policy.md",
            ROOT / "references" / "editorial-policy.md",
            ROOT / "references" / "final-check.md",
            ROOT / "references" / "long-context-mode.md",
            ROOT / "references" / "runtime-contract.md",
            ROOT / "references" / "runtime-current.md",
            ROOT / "C2-Universal-Portable.md",
            MIRROR / "references" / "editorial-policy.md",
            MIRROR / "references" / "final-check.md",
            MIRROR / "references" / "runtime-current.md",
        )
        forbidden = (
            "## 开放式内容板块动态编排",
            "## 板块编排专项终检",
            "独立动态划分和重排内容板块",
            "每条独立动态编排板块",
        )
        for path in paths:
            text = path.read_text(encoding="utf-8")
            for phrase in forbidden:
                with self.subTest(path=path, phrase=phrase):
                    self.assertNotIn(phrase, text)

    def test_phase_one_keeps_dynamic_body_order_and_candidate_limit(self):
        policy = (ROOT / "references" / "clip-selection-policy.md").read_text(encoding="utf-8")
        self.assertIn("不设候选识别数或展示数上限", policy)
        self.assertIn("用户最多选择 3 个候选", policy)
        self.assertIn("每条独立重新编排正文并动态重排", policy)
        self.assertIn("每条常规时长方案须独立覆盖", policy)
        self.assertIn("不新增第六部分", policy)

    def test_development_governance_stays_out_of_daily_runtime(self):
        governance = (ROOT / "references" / "update-protocol.md").read_text(encoding="utf-8")
        runtime = (ROOT / "references" / "runtime-current.md").read_text(encoding="utf-8")
        portable = (ROOT / "C2-Universal-Portable.md").read_text(encoding="utf-8")
        self.assertIn("自动判断 L1/L2/L3", governance)
        self.assertIn("一次性同步、发布", governance)
        for marker in ("自动判断 L1/L2/L3", "本协议仅在开发", "一次性同步、发布"):
            self.assertNotIn(marker, runtime)
            self.assertNotIn(marker, portable)

    def test_mirror_sync_removes_stale_files(self):
        script = ROOT / "scripts" / "sync_skill_mirror.py"
        spec = importlib.util.spec_from_file_location("sync_skill_mirror", script)
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
