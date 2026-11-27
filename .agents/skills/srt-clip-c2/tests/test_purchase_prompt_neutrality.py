import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class PurchasePromptNeutralityTests(unittest.TestCase):
 def test_plugin_versions_are_current(self):
  plugin=ROOT.parents[1]; self.assertEqual((plugin/"VERSION").read_text().strip(),"0.4.7"); self.assertEqual(json.loads((plugin/"plugin.json").read_text(encoding="utf-8"))["version"],"0.4.47")
 def test_source_cta_is_preserved_and_never_invented(self):
  e=(ROOT/"references/editorial-policy.md").read_text(encoding="utf-8"); h=(ROOT/"references/highlight-selection.md").read_text(encoding="utf-8")
  self.assertIn("原文存在适用且合规的促单时，完整保留原话",e); self.assertIn("原文没有促单时，禁止编造、改写或补充",e); self.assertIn("适用且合规时完整保留",h)
 def test_compliant_cta_is_a_complete_last_board_with_original_internal_order(self):
  e=(ROOT/"references/editorial-policy.md").read_text(encoding="utf-8"); p=(ROOT/"references/clip-selection-policy.md").read_text(encoding="utf-8")
  self.assertIn("最后的独立促单板块",e); self.assertIn("板块内维持原文顺序",e); self.assertIn("不得跨商品移用话术",e)
 def test_duration_is_only_an_estimate(self):
  p=(ROOT/"references/clip-selection-policy.md").read_text(encoding="utf-8"); f=(ROOT/"references/final-check.md").read_text(encoding="utf-8")
  self.assertIn("预计",p); self.assertIn("90 秒是有效信息密度目标",p); self.assertIn("超过 100 秒须逐条复核",p)
  for phrase in ("45 秒","45秒"): self.assertNotIn(phrase,p)
 def test_no_extra_semantic_stage_or_tool_gate(self):
  c=(ROOT/"references/runtime-contract.md").read_text(encoding="utf-8"); self.assertIn("一个 AI",c); self.assertIn("不新增 Agent",c); self.assertIn("日常执行不调用 Python、脚本或外部工具",c)
if __name__=="__main__": unittest.main()
