import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p): return (ROOT/p).read_text(encoding="utf-8")
class PurchaseAnglePolicyTests(unittest.TestCase):
 def test_current_package_and_core_versions(self):
  plugin=ROOT.parents[1]; self.assertEqual((plugin/"VERSION").read_text().strip(),"0.4.6"); self.assertEqual(json.loads((plugin/"plugin.json").read_text(encoding="utf-8"))["version"],"0.4.26")
 def test_empathy_priority_is_only_for_opening_comparison(self):
  e=read("references/editorial-policy.md"); self.assertIn("共情入口优先",e); self.assertIn("只比较开头本身",e); self.assertNotIn("通过覆盖资格后，按六维评分比较完整候选",e); self.assertNotIn("完整候选路径",e)
 def test_opening_is_grounded_and_not_fabricated_as_customer_feedback(self):
  e=read("references/editorial-policy.md"); self.assertIn("顾客反馈",e); self.assertIn("原话支撑",e); self.assertIn("主播提出的设问",e)
 def test_full_pool_then_opportunity_checkpoint(self):
  c=read("references/runtime-contract.md"); self.assertLess(c.index("建立完整卖点池"),c.index("检测多视频机会")); self.assertIn("暂停生成正式成片",c); self.assertIn("不重复读取",c); self.assertNotIn("未选择时按单条默认完成",c)
 def test_selected_cut_coverage_is_individual(self):
  e=read("references/editorial-policy.md"); self.assertIn("每一条实际选中的成片",e); self.assertIn("方案并集不能补足",e)
 def test_fixed_output_and_prohibited_terms_are_preserved(self):
  runtime=read("references/runtime-current.md"); global_rules=read("references/global-rules.md")
  for title in ("一、文件解析结果","二、商品识别","三、最佳成片方案","四、作品标题与话题","五、原始 SRT 序号"): self.assertIn(title,runtime)
  for term in ("羊毛","皮草","羊绒","特殊动物绒","全金纺半高领"): self.assertIn(term,global_rules)
if __name__=="__main__": unittest.main()
