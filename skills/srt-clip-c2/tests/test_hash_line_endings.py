from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY_TOOL = ROOT / "scripts" / "execution_summary.py"
PLUGIN = next(parent for parent in ROOT.parents if (parent / "plugin.json").is_file())
sys.path.insert(0, str(ROOT / "scripts"))
import build_runtime


class TextHashLineEndingTests(unittest.TestCase):
    def test_build_hash_treats_crlf_and_lf_as_the_same_text(self):
        self.assertEqual(
            build_runtime.sha256("规则行\n下一行\n".encode("utf-8")),
            build_runtime.sha256("规则行\r\n下一行\r\n".encode("utf-8")),
        )

    def test_refreshed_summary_stays_valid_after_checkout_line_endings_change(self):
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            root = temp / "plugin" / "skills" / "srt-clip-c2"
            root.parent.mkdir(parents=True)
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            plugin_root = root.parents[1]
            shutil.copy2(PLUGIN / "plugin.json", plugin_root / "plugin.json")
            shutil.copytree(PLUGIN / ".codex-plugin", plugin_root / ".codex-plugin")
            summary = temp / "execution-summary.json"
            body = temp / "summary-body.txt"
            body.write_text("测试摘要", encoding="utf-8")
            refresh = subprocess.run(
                [sys.executable, str(SUMMARY_TOOL), "refresh", "--skill-root", str(root), "--summary", str(summary), "--body", str(body)],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(refresh.returncode, 0, refresh.stderr + refresh.stdout)

            manifest_path = root / "references" / "runtime-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            text_paths = {"VERSION", "SKILL.md", manifest["runtime_file"], "references/runtime-manifest.json", *manifest["source_hashes"]}
            for relative in text_paths:
                path = root / relative
                path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n"))

            validate = subprocess.run(
                [sys.executable, str(SUMMARY_TOOL), "validate", "--skill-root", str(root), "--summary", str(summary)],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(validate.returncode, 0, validate.stderr + validate.stdout)
            self.assertEqual(json.loads(validate.stdout)["state"], "valid")


if __name__ == "__main__":
    unittest.main()
