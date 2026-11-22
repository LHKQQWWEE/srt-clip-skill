import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p): return (ROOT/p).read_text(encoding="utf-8")
class ResponsibilityArchitectureTests(unittest.TestCase):
 def test_one_ai_and_existing_logical_responsibilities_remain(self):
  c=read("references/runtime-contract.md"); self.assertIn("一个 AI",c); self.assertIn("一次语义分析",c); self.assertIn("一次终检",c)
  for role in ("Chief Decision Editor","Product Purchase-Decision Architect","Product Facts & Boundaries Officer","Purchase-Decision Editor","Final Quality Auditor"): self.assertIn(role,c)
  self.assertIn("不新增 Agent",c)
 def test_architecture_keeps_dynamic_structure_and_empathy_first_opening(self):
  e=read("references/editorial-policy.md"); self.assertIn("动态构建路径",e); self.assertIn("共情优先",e); self.assertNotIn("通过覆盖资格后，按六维评分比较完整候选",e)
 def test_full_pool_gate_and_individual_coverage(self):
  c=read("references/runtime-contract.md"); e=read("references/editorial-policy.md"); self.assertLess(c.index("建立完整卖点池"),c.index("检测多视频机会")); self.assertIn("每一条实际选中的成片",e); self.assertIn("不重复识别",c)
 def test_source_words_and_final_audit_scope(self):
  e=read("references/editorial-policy.md"); f=read("references/final-check.md"); self.assertIn("原话逐字保留",e); self.assertIn("仅为用户已选定且实际写出的成片",f); self.assertIn("不终检未选主题",f)
 def test_global_rules_and_factual_veto_are_not_overridable(self):
  c=read("references/runtime-contract.md"); g=read("references/global-rules.md"); self.assertIn("商品事实与全局硬规则优先",c); self.assertIn("正式禁用词库",g)
 def test_prohibited_term_owner_and_user_authorization_boundary(self):
  g=read("references/global-rules.md"); self.assertIn("用户明确指定",g); self.assertIn("未授权",g); self.assertIn("正式禁词",g)
 def test_unregistered_category_does_not_block_processing(self):
  r=read("references/product-knowledge-registry.md"); self.assertIn("未注册类别仍可按 Universal Core 正常处理",r)
if __name__=="__main__": unittest.main()
