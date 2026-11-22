import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PLUGIN=next(p for p in ROOT.parents if (p/"plugin.json").is_file())
class EntryProtocolTests(unittest.TestCase):
 def test_entries_preserve_identity_and_daily_runtime_loading(self):
  p=json.loads((PLUGIN/"plugin.json").read_text(encoding="utf-8")); c=json.loads((PLUGIN/".codex-plugin/plugin.json").read_text(encoding="utf-8"))
  prompt=p["extensions"]["com.openai"]["interface"]["defaultPrompt"]
  self.assertEqual(prompt,c["interface"]["defaultPrompt"]); self.assertEqual(p["name"],"srt-clip-c2"); self.assertEqual(p["skills"],"./skills")
  skill=(ROOT/"SKILL.md").read_text(encoding="utf-8"); portable=(ROOT/"C2-Universal-Portable.md").read_text(encoding="utf-8")
  self.assertIn("runtime-current.md",skill); self.assertIn("runtime-manifest.json",skill)
  self.assertIn("runtime-current.md",prompt); self.assertIn("唯一日常业务规则正文",prompt)
  self.assertIn("不要读取仅用于构建和测试的 runtime-manifest.json",prompt)
  self.assertNotIn("required_files",prompt)
  self.assertIn(prompt,portable)
 def test_manifest_paths_are_build_and_test_metadata(self):
  m=json.loads((ROOT/"references/runtime-manifest.json").read_text(encoding="utf-8")); skill=(ROOT/"SKILL.md").read_text(encoding="utf-8")
  self.assertEqual(m["entry_file"],"SKILL.md"); self.assertEqual(m["required_files"],["references/runtime-current.md"])
  self.assertIn("runtime-manifest.json",skill); self.assertIn("不得再逐份加载",skill)
  for name in [m["entry_file"],*m["required_files"]]: self.assertTrue((ROOT/name).is_file(),name)
  for item in m["conditional_files"]: self.assertTrue(list(ROOT.glob(item["path"])),item["path"])
 def test_package_and_core_versions_are_separate(self):
  p=json.loads((PLUGIN/"plugin.json").read_text(encoding="utf-8")); c=json.loads((PLUGIN/".codex-plugin/plugin.json").read_text(encoding="utf-8"))
  self.assertEqual((PLUGIN/"VERSION").read_text(encoding="utf-8").strip(),"0.4.6")
  self.assertEqual(p["version"],"0.4.26"); self.assertEqual(c["version"],p["version"])
if __name__=="__main__": unittest.main()
