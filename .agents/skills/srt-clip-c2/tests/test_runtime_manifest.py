from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "references" / "runtime-manifest.json"


def text_sha256(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


class RuntimeManifestTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.entry = (ROOT / "SKILL.md").read_text(encoding="utf-8")

    def test_entry_loads_compiled_runtime_without_manifest_requirement(self):
        self.assertIn("runtime-current.md", self.entry)
        self.assertIn("runtime-manifest.json", self.entry)
        self.assertEqual(self.manifest["required_files"], ["references/runtime-current.md"])
        self.assertTrue((ROOT / self.manifest["runtime_file"]).is_file())

    def test_source_hashes_runtime_hash_and_source_map_are_current(self):
        self.assertEqual(self.manifest["core_version"], "0.4.7")
        self.assertEqual(self.manifest["skill_version"], "0.4.49")
        self.assertTrue(self.manifest["source_map"])
        self.assertEqual(text_sha256(ROOT / self.manifest["runtime_file"]), self.manifest["runtime_sha256"])
        for path, digest in self.manifest["source_hashes"].items():
            self.assertEqual(text_sha256(ROOT / path), digest, path)

    def test_summary_binds_long_context_and_runtime_prompts(self):
        self.assertIn("references/long-context-mode.md", self.manifest["summary_files"])
        self.assertIn("references/commerce-advisory.md", self.manifest["summary_files"])
        self.assertIn("agents/openai.yaml", self.manifest["summary_files"])
        self.assertIn("product-knowledge-packs/*.md", self.manifest["summary_files"])
        self.assertIn("../../plugin.json", self.manifest["optional_summary_files"])
        self.assertIn("../../.codex-plugin/plugin.json", self.manifest["optional_summary_files"])
        for relative in ("references/long-context-mode.md", "agents/openai.yaml"):
            self.assertIn(relative, self.manifest["source_hashes"])

    def test_conditional_paths_resolve(self):
        for item in self.manifest["conditional_files"]:
            self.assertTrue(list(ROOT.glob(item["path"])), item["path"])

    def test_runtime_build_check(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/build_runtime.py"), "--check"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
