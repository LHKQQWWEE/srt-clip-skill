import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p): return (ROOT/p).read_text(encoding="utf-8")
class PurchaseDecision046Tests(unittest.TestCase):
 def test_complete_inventory_precedes_opening_and_multi_video_detection(self):
  c=read("references/runtime-contract.md"); self.assertLess(c.index("建立完整卖点池"),c.index("按共情优先层级比较")); self.assertLess(c.index("建立完整卖点池"),c.index("检测多视频机会"))
 def test_each_selected_video_covers_every_valid_point(self):
  e=read("references/editorial-policy.md"); f=read("references/final-check.md"); self.assertIn("每一条实际选中的成片",e); self.assertIn("全部有效独立购买信息",e); self.assertIn("多条中的其他成片不能补足本条",f)
 def test_point_granularity_keeps_examples_grouped_and_facts_distinct(self):
  e=read("references/editorial-policy.md"); self.assertIn("不把同一购买意义下的一组例子机械拆成多个卖点",e); self.assertIn("不同具体事实过度合并",e)
 def test_gate_pauses_and_restores_without_reanalysis(self):
  c=read("references/runtime-contract.md")
  for phrase in ("暂停生成正式成片","保存当前对话检查点","用户选择后恢复此状态","不重复读取","不重复识别","不重复检测"): self.assertIn(phrase,c)
  self.assertNotIn("未选择时按单条默认完成",c)
 def test_full_cut_competition_is_removed(self):
  e=read("references/editorial-policy.md"); h=read("references/highlight-selection.md")
  self.assertIn("不开启完整成片候选的资格评分",e); self.assertIn("不比较完整成片、不做六维评分",h)
 def test_low_value_does_not_remove_valid_information(self):
  e=read("references/editorial-policy.md"); h=read("references/highlight-selection.md"); self.assertIn("不能把低价值当作弱增量",h); self.assertIn("不赋予删除有效信息的权力",e)
 def test_fixed_five_parts_and_one_ai_remain(self):
  c=read("references/runtime-contract.md"); self.assertIn("一个 AI",c); self.assertIn("固定五部分交付",c); self.assertIn("不新增 Agent",c)
if __name__=="__main__": unittest.main()
