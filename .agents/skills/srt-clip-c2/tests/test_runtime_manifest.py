import hashlib,json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"references/runtime-manifest.json"
class RuntimeManifestTests(unittest.TestCase):
 def setUp(self): self.m=json.loads(MANIFEST.read_text(encoding="utf-8")); self.entry=(ROOT/"SKILL.md").read_text(encoding="utf-8")
 def test_entry_loads_compiled_runtime_without_manifest_requirement(self):
  self.assertIn("runtime-current.md",self.entry); self.assertIn("runtime-manifest.json",self.entry); self.assertEqual(self.m["required_files"],["references/runtime-current.md"]); self.assertTrue((ROOT/self.m["runtime_file"]).is_file())
 def test_source_hashes_runtime_hash_and_source_map_are_current(self):
  self.assertEqual(self.m["core_version"],"0.4.7"); self.assertEqual(self.m["skill_version"],"0.4.27"); self.assertTrue(self.m["source_map"]); self.assertEqual(hashlib.sha256((ROOT/self.m["runtime_file"]).read_bytes()).hexdigest(),self.m["runtime_sha256"])
  for p,d in self.m["source_hashes"].items(): self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),d,p)
 def test_conditional_paths_resolve(self):
  for item in self.m["conditional_files"]: self.assertTrue(list(ROOT.glob(item["path"])),item["path"])
 def test_runtime_build_check(self):
  r=subprocess.run([sys.executable,str(ROOT/"scripts/build_runtime.py"),"--check"],capture_output=True,text=True,encoding="utf-8"); self.assertEqual(r.returncode,0,r.stdout+r.stderr)
if __name__=="__main__": unittest.main()
