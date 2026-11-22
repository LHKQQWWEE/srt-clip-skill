import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class PurchasePromptNeutralityTests(unittest.TestCase):
 def test_plugin_versions_are_current(self):
  plugin=ROOT.parents[1]; self.assertEqual((plugin/"VERSION").read_text().strip(),"0.4.6"); self.assertEqual(json.loads((plugin/"plugin.json").read_text(encoding="utf-8"))["version"],"0.4.26")
 def test_source_cta_is_preserved_and_never_invented(self):
  e=(ROOT/"references/editorial-policy.md").read_text(encoding="utf-8"); h=(ROOT/"references/highlight-selection.md").read_text(encoding="utf-8")
  self.assertIn("原文存在适用且合规的促单话术时，必须保留",e); self.assertIn("原文没有促单时，禁止编造、改写或补充",e); self.assertIn("完整原话",h)
 def test_no_forced_early_or_rewritten_cta(self):
  e=(ROOT/"references/editorial-policy.md").read_text(encoding="utf-8"); self.assertIn("不得为开头或时长要求提前移动、拆写原话",e); self.assertIn("不得跨商品移用话术",e)
 def test_duration_is_only_an_estimate(self):
  h=(ROOT/"references/highlight-selection.md").read_text(encoding="utf-8"); f=(ROOT/"references/final-check.md").read_text(encoding="utf-8")
  for text in (h,f): self.assertIn("约数",text); self.assertIn("不参与",text); self.assertIn("拆条",text)
  for phrase in ("45 秒","45秒","120 秒","120秒","130 秒","130秒"): self.assertNotIn(phrase,h)
 def test_no_extra_semantic_stage_or_tool_gate(self):
  c=(ROOT/"references/runtime-contract.md").read_text(encoding="utf-8"); self.assertIn("一个 AI",c); self.assertIn("不新增 Agent",c); self.assertIn("工具不可用时继续处理可靠可读文本",c)
if __name__=="__main__": unittest.main()
