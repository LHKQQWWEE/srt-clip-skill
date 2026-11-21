import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "references" / "runtime-manifest.json"


class RuntimeManifestTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(MANIFEST_PATH.is_file(), "runtime manifest must exist")
        self.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        self.entry = (ROOT / "SKILL.md").read_text(encoding="utf-8")

    def test_manifest_paths_match_entry_without_a_fixed_count(self):
        required = set(self.manifest["required_files"])
        read_contract = self.entry.split("## 1. 唯一入口与版本优先级", 1)[0]

        self.assertEqual(self.manifest["entry_file"], "SKILL.md")
        self.assertIn("required_files", read_contract)
        self.assertIn("runtime-manifest.json", read_contract)
        self.assertFalse(re.search(r"`references/[a-z0-9-]+\.md`", read_contract))
        for path in required:
            self.assertTrue(path.startswith("references/"))
        self.assertNotIn("len(paths) ==", self.entry)

    def test_every_required_and_conditional_path_resolves(self):
        required = self.manifest["required_files"]
        conditional = self.manifest["conditional_files"]

        self.assertEqual(len(required), len(set(required)))
        self.assertFalse(set(required) & {item["path"] for item in conditional if "*" not in item["path"]})
        for relative in [self.manifest["entry_file"], *required]:
            with self.subTest(path=relative):
                self.assertTrue((ROOT / relative).is_file(), relative)
        for item in conditional:
            with self.subTest(path=item["path"]):
                matches = list(ROOT.glob(item["path"]))
                self.assertTrue(matches, item["path"])

    def test_load_contract_names_batch_read_and_range_gate(self):
        text = self.entry.split("## 1. 唯一入口与版本优先级", 1)[0]
        self.assertIn("runtime-manifest.json", text)
        self.assertIn("并发", text)
        self.assertIn("首尾", text)
        self.assertIn("截断", text)
        self.assertIn("不得进入素材语义分析", text)


if __name__ == "__main__":
    unittest.main()
