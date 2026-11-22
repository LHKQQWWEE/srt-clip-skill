import hashlib
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PLUGIN=next(p for p in ROOT.parents if (p/"plugin.json").is_file())
def read(path): return (ROOT/path).read_text(encoding="utf-8")
class C2UniversalIntegrityTests(unittest.TestCase):
 def test_core_files_and_current_knowledge_packs_exist(self):
  for path in ("SKILL.md","references/runtime-manifest.json","references/runtime-current.md","references/runtime-contract.md","references/global-rules.md","references/editorial-policy.md","references/highlight-selection.md","references/final-check.md","scripts/srt_tools.py","scripts/selection.schema.json"):
   self.assertTrue((ROOT/path).is_file(),path)
  for path in ("product-knowledge-packs/womens-fashion.md","product-knowledge-packs/shoes.md","product-knowledge-packs/scarves.md"): self.assertTrue((ROOT/path).is_file(),path)
 def test_core_and_plugin_versions_are_aligned(self):
  a=json.loads((PLUGIN/"plugin.json").read_text(encoding="utf-8")); b=json.loads((PLUGIN/".codex-plugin/plugin.json").read_text(encoding="utf-8")); m=json.loads((ROOT/"references/runtime-manifest.json").read_text(encoding="utf-8"))
  self.assertEqual((PLUGIN/"VERSION").read_text().strip(),"0.4.6"); self.assertEqual(a["version"],"0.4.26"); self.assertEqual(b["version"],a["version"]); self.assertEqual(m["core_version"],"0.4.6")
  self.assertIn("0.4.26",read("C2-Universal-Portable.md"))
 def test_plugin_identity_entry_and_connection_metadata_remain(self):
  a=json.loads((PLUGIN/"plugin.json").read_text(encoding="utf-8")); b=json.loads((PLUGIN/".codex-plugin/plugin.json").read_text(encoding="utf-8"))
  self.assertEqual(a["name"],"srt-clip-c2"); self.assertEqual(b["name"],a["name"]); self.assertEqual(a["skills"],"./skills"); self.assertEqual(b["skills"],"./skills")
  self.assertEqual(a["extensions"]["com.openai"]["interface"]["defaultPrompt"],b["interface"]["defaultPrompt"]); self.assertEqual(a["extensions"]["com.openai"]["interface"]["defaultPrompt"],read("agents/openai.yaml").split("default_prompt: ",1)[1].strip().strip('"'))
 def test_ai_first_dynamic_structure_and_no_full_cut_competition(self):
  c=read("references/runtime-contract.md"); e=read("references/editorial-policy.md"); h=read("references/highlight-selection.md")
  self.assertIn("AI-First",c); self.assertIn("一个 AI",c); self.assertIn("共情优先",e); self.assertIn("只比较开头",e); self.assertIn("不开启完整成片候选的资格评分",e); self.assertNotIn("通过覆盖资格后，比较完整候选路径",e)
 def test_multi_video_gate_and_per_video_coverage(self):
  c=read("references/runtime-contract.md"); e=read("references/editorial-policy.md"); self.assertLess(c.index("建立完整卖点池"),c.index("检测多视频机会")); self.assertIn("暂停生成正式成片",c); self.assertIn("不重复识别",c); self.assertIn("每一条实际选中的成片",e); self.assertIn("方案并集不能补足",e)
 def test_original_cta_and_duration_contract(self):
  e=read("references/editorial-policy.md"); h=read("references/highlight-selection.md"); f=read("references/final-check.md")
  self.assertIn("原文存在适用且合规的促单话术时，必须保留",e); self.assertIn("原文没有促单时，禁止编造、改写或补充",e); self.assertIn("预计成片时长只作约数参考",h); self.assertIn("不参与质量验收",h); self.assertIn("不触发拆条",h)
  for text in (e,h,f):
   for threshold in ("45 秒","45秒","120 秒","120秒","130 秒","130秒"): self.assertNotIn(threshold,text)
 def test_final_audit_is_selected_only_and_output_stays_fixed(self):
  f=read("references/final-check.md"); c=read("references/runtime-contract.md"); self.assertIn("仅为用户已选定且实际写出的成片",f)
  for title in ("一、文件解析结果","二、商品识别","三、最佳成片方案","四、作品标题与话题","五、原始 SRT 序号"): self.assertIn(title,c)
 def test_runtime_bundle_hashes_and_source_map_are_current(self):
  m=json.loads(read("references/runtime-manifest.json")); self.assertTrue(m["source_map"]); self.assertEqual(hashlib.sha256((ROOT/m["runtime_file"]).read_bytes()).hexdigest(),m["runtime_sha256"])
  for source,digest in m["source_hashes"].items(): self.assertEqual(hashlib.sha256((ROOT/source).read_bytes()).hexdigest(),digest,source)
 def test_exact_formal_term_scope_remains_single_source(self):
  g=read("references/global-rules.md"); self.assertIn("羊毛",g); self.assertIn("皮草",g); self.assertIn("羊绒",g); self.assertIn("特殊动物绒",g); self.assertIn("全金纺半高领",g); self.assertIn("防静电不是正式禁词",g)
  self.assertIn("不得扩大到未授权",g); self.assertIn("只排除",g)
 def test_portable_is_generated_from_current_sources(self):
  import sys
  sys.path.insert(0,str(ROOT/"scripts")); import build_portable
  self.assertEqual((ROOT/"C2-Universal-Portable.md").read_text(encoding="utf-8"),build_portable.build())
 def test_update_protocol_and_tests_are_not_runtime_load_requirements(self):
  m=json.loads(read("references/runtime-manifest.json")); self.assertNotIn("references/update-protocol.md",m["source_files"]); self.assertNotIn("references/update-protocol.md",m["required_files"])
  self.assertFalse(list((PLUGIN/"docs/history/releases").glob("*.md")) if (PLUGIN/"docs/history/releases").exists() else [])
if __name__=="__main__": unittest.main()
