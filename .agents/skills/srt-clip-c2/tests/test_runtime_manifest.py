import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "references" / "runtime-manifest.json"


class RuntimeManifestTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        self.runtime = (ROOT / self.manifest["runtime_file"]).read_text(encoding="utf-8")

    def test_runtime_is_the_single_required_load(self):
        entry = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertEqual(self.manifest["required_files"], [self.manifest["runtime_file"]])
        self.assertIn(self.manifest["runtime_file"], entry)
        self.assertIn("正常任务不得再逐份加载其开发源文件或读取 `references/runtime-manifest.json`", entry)
        self.assertIn("manifest 只供构建和完整性测试使用", entry)

    def test_source_hashes_and_runtime_hash_are_current(self):
        for relative, expected in self.manifest["source_hashes"].items():
            self.assertEqual(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(), expected, relative)
        actual = hashlib.sha256(self.runtime.encode("utf-8")).hexdigest()
        self.assertEqual(actual, self.manifest["runtime_sha256"])

    def test_source_map_is_unique_complete_and_points_to_verbatim_lines(self):
        source_map = self.manifest["source_map"]
        ids = [item["rule_id"] for item in source_map]
        self.assertEqual(len(ids), len(set(ids)))
        mapped = {}
        runtime_lines = self.runtime.splitlines()
        for item in source_map:
            source_lines = (ROOT / item["source"]).read_text(encoding="utf-8").splitlines()
            expected = source_lines[item["source_line"] - 1]
            self.assertEqual(runtime_lines[item["runtime_line"] - 1], expected, item["rule_id"])
            mapped.setdefault(item["source"], set()).add(item["source_line"])
        self.assertEqual(set(mapped), set(self.manifest["source_files"]))
        for source in self.manifest["source_files"]:
            source_lines = (ROOT / source).read_text(encoding="utf-8").splitlines()
            nonempty = {i for i, line in enumerate(source_lines, start=1) if line.strip()}
            self.assertEqual(mapped[source], nonempty, source)

    def test_compiler_rebuild_is_idempotent(self):
        script = ROOT / "scripts" / "build_runtime.py"
        result = subprocess.run([sys.executable, str(script), "--check"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_conditional_paths_resolve_without_becoming_required_loads(self):
        required = set(self.manifest["required_files"])
        for item in self.manifest["conditional_files"]:
            self.assertNotIn(item["path"], required)
            self.assertTrue(list(ROOT.glob(item["path"])), item["path"])


if __name__ == "__main__":
    unittest.main()
