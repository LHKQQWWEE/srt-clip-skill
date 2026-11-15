from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT
PLUGIN_ROOT = ROOT.parents[1]

class C2UniversalIntegrityTests(unittest.TestCase):
    def test_skill_frontmatter_and_version(self):
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: srt-clip-c2\n"))
        self.assertIn("SRT Clip C2 Universal 0.3.1", text)
        front = text.split("---", 2)[1]
        for trigger in ["srt文案", "srt切片文案", "str文案", "C2完整精简版"]:
            self.assertIn(trigger, front)
        self.assertNotIn("“切片文案”", front)

    def test_core_files_exist(self):
        for path in [
            "references/editorial-policy.md",
            "references/highlight-selection.md",
            "references/category-registry.md",
            "references/global-rules.md",
            "references/final-check.md",
            "references/qianchuan-offline.md",
            "categories/womens-fashion.md",
            "C2-Universal-Portable.md",
            "START-HERE.md",
        ]:
            self.assertTrue((SKILL_DIR / path).is_file(), path)

    def test_no_old_mandatory_workflow_in_active_rules(self):
        active = [
            (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8"),
            (SKILL_DIR / "references/highlight-selection.md").read_text(encoding="utf-8"),
            (SKILL_DIR / "references/final-check.md").read_text(encoding="utf-8"),
        ]
        combined = "\n".join(active)
        for old in ["workflow_gate.py", "multi_plan.py", "check_highlights.py", "highlights.json", "workflow.json"]:
            self.assertNotIn(old, combined)

    def test_duration_and_output_rules(self):
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("1.2", text)
        self.assertIn("120 秒", text)
        self.assertIn("固定五部分", text)

    def test_offline_compliance_trigger(self):
        text = (SKILL_DIR / "references/qianchuan-offline.md").read_text(encoding="utf-8")
        self.assertIn("更新违禁词", text)

    def test_benchmark_has_ten_cases_and_no_raw_transcripts(self):
        text = (SKILL_DIR / "tests/benchmark-cases.md").read_text(encoding="utf-8")
        self.assertEqual(len(re.findall(r"\| B\d{2} \|", text)), 10)
        self.assertIn("不包含任何原始SRT行", text)

    def test_duplicate_highlight_policy(self):
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        detail = (SKILL_DIR / "references/highlight-selection.md").read_text(encoding="utf-8")
        self.assertIn("最多保留两处", text)
        self.assertIn("先保不同卖点覆盖，再删重复强化", detail)

    def test_plugin_manifest(self):
        manifest = json.loads((PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "srt-clip-c2")
        self.assertEqual(manifest["version"], "0.3.1")
        self.assertEqual(manifest["extensions"]["com.openai"]["interface"]["shortDescription"], "AI主导，跨平台带货剪辑")

if __name__ == "__main__":
    unittest.main()
