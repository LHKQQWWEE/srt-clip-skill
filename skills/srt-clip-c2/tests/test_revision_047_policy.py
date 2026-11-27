from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "references" / "clip-selection-policy.md"
SUMMARY_TOOL = ROOT / "scripts" / "execution_summary.py"


def read(path: str) -> str:
    target = ROOT / path
    if not target.is_file():
        raise AssertionError(f"required current rule file is missing: {path}")
    return target.read_text(encoding="utf-8")


class Revision047PolicyTests(unittest.TestCase):
    def test_duration_and_opening_choice_rules_have_one_source(self):
        self.assertTrue(POLICY.is_file(), "the new canonical clip-selection policy is missing")
        policy = POLICY.read_text(encoding="utf-8")
        contract = read("references/runtime-contract.md")
        editorial = read("references/editorial-policy.md")
        highlight = read("references/highlight-selection.md")
        final_check = read("references/final-check.md")
        self.assertIn("唯一规则来源", policy)
        self.assertIn("90 秒是有效信息密度目标", policy)
        self.assertIn("先完成全部有效卖点的完整编排，再计算时长", policy)
        self.assertIn("超过 100 秒须逐条复核", policy)
        self.assertIn("不得自动截断", policy)
        self.assertIn("不得固定某些卖点永远低价值", policy)
        self.assertIn("所有达到现有质量门槛且彼此实质不同", policy)
        self.assertIn("不设候选识别数或展示数上限", policy)
        self.assertIn("用户最多选择 3 个候选", policy)
        self.assertIn("每个候选只显示四项", policy)
        self.assertIn("不得预选", policy)
        self.assertIn("每个已选开头分别生成一条完整成片", policy)
        self.assertIn("每条成片先完整覆盖", policy)
        self.assertIn("不得凑数", policy)
        self.assertIn("单条", policy)
        self.assertIn("按推荐版", policy)
        self.assertIn("references/clip-selection-policy.md", contract)
        self.assertIn("references/clip-selection-policy.md", editorial)
        self.assertIn("references/clip-selection-policy.md", highlight)
        self.assertIn("references/clip-selection-policy.md", final_check)
        for text in (contract, editorial, highlight, final_check):
            self.assertNotIn("暂停生成正式成片", text)
            self.assertNotIn("每次调用都重新完整读取", text)

    def test_entry_uses_summary_as_optional_context_and_reads_runtime_on_mismatch(self):
        entry = read("SKILL.md")
        self.assertIn("execution-summary.json", entry)
        self.assertIn("Skill 版本", entry)
        self.assertIn("规则文件 SHA-256", entry)
        self.assertIn("摘要有效时直接复用", entry)
        self.assertIn("首次运行", entry)
        self.assertIn("版本不匹配", entry)
        self.assertIn("缓存丢失", entry)
        self.assertNotIn("每次触发时，在处理素材前完整读取本文件和 `references/runtime-current.md`", entry)


class ExecutionSummaryTests(unittest.TestCase):
    def run_summary(self, *args: str) -> tuple[int, dict[str, object]]:
        self.assertTrue(SUMMARY_TOOL.is_file(), "persistent execution-summary tool is missing")
        result = subprocess.run(
            [sys.executable, str(SUMMARY_TOOL), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            self.fail(f"summary command must emit JSON status: {exc}; stderr={result.stderr}")
        return result.returncode, payload

    def test_missing_summary_requires_full_rule_read_even_if_cache_exists(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "skill"
            copy_skill(root)
            cache = Path(temp) / "optional-cache.json"
            cache.write_text("{}", encoding="utf-8")
            code, result = self.run_summary("validate", "--skill-root", str(root), "--summary", str(Path(temp) / "missing.json"), "--cache", str(cache))
            self.assertEqual(code, 2)
            self.assertEqual(result["state"], "missing")
            self.assertTrue(result["requires_full_read"])

    def test_refresh_creates_persistent_versioned_summary_and_later_reuses_it(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "skill"
            copy_skill(root)
            summary = Path(temp) / "persistent" / "execution-summary.json"
            body = Path(temp) / "body.txt"
            body.write_text("简明摘要内容", encoding="utf-8")
            code, created = self.run_summary("refresh", "--skill-root", str(root), "--summary", str(summary), "--body", str(body))
            self.assertEqual(code, 0)
            self.assertTrue(summary.is_file())
            data = json.loads(summary.read_text(encoding="utf-8"))
            self.assertEqual(data["skill_version"], "0.4.45")
            self.assertEqual(data["core_version"], "0.4.7")
            self.assertTrue(data["rule_hashes"])
            code, status = self.run_summary("validate", "--skill-root", str(root), "--summary", str(summary))
            self.assertEqual(code, 0)
            self.assertEqual(status["state"], "valid")
            self.assertFalse(status["requires_full_read"])

    def test_skill_version_change_invalidates_summary(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "skill"
            copy_skill(root)
            summary = Path(temp) / "execution-summary.json"
            create_summary(root, summary, Path(temp))
            manifest_path = root / "references" / "runtime-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["skill_version"] = "0.4.28"
            manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            code, status = self.run_summary("validate", "--skill-root", str(root), "--summary", str(summary))
            self.assertEqual(code, 2)
            self.assertTrue(status["requires_full_read"])
            self.assertIn(status["state"], {"version_mismatch", "manifest_stale"})

    def test_rule_file_change_invalidates_summary(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "skill"
            copy_skill(root)
            summary = Path(temp) / "execution-summary.json"
            create_summary(root, summary, Path(temp))
            rule = root / "references" / "editorial-policy.md"
            rule.write_text(rule.read_text(encoding="utf-8") + "\n规则变更。\n", encoding="utf-8")
            code, status = self.run_summary("validate", "--skill-root", str(root), "--summary", str(summary))
            self.assertEqual(code, 2)
            self.assertTrue(status["requires_full_read"])

    def test_lost_optional_cache_falls_back_to_valid_persistent_summary(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "skill"
            copy_skill(root)
            summary = Path(temp) / "execution-summary.json"
            create_summary(root, summary, Path(temp))
            code, status = self.run_summary("validate", "--skill-root", str(root), "--summary", str(summary), "--cache", str(Path(temp) / "deleted-cache.json"))
            self.assertEqual(code, 0)
            self.assertEqual(status["state"], "valid")
            self.assertFalse(status["requires_full_read"])
            self.assertEqual(status["cache_state"], "missing")


def copy_skill(target: Path) -> None:
    import shutil
    shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))


def create_summary(root: Path, summary: Path, temp: Path) -> None:
    body = temp / "summary-body.txt"
    body.write_text("摘要文本", encoding="utf-8")
    code, _ = ExecutionSummaryTests().run_summary("refresh", "--skill-root", str(root), "--summary", str(summary), "--body", str(body))
    if code != 0:
        raise AssertionError("test setup could not create an execution summary")


if __name__ == "__main__":
    unittest.main()
