import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p): return (ROOT/p).read_text(encoding="utf-8")
class PurchaseReasonPolicyTests(unittest.TestCase):
 def test_complete_reason_keeps_evidence_and_conditions(self):
  e=read("references/editorial-policy.md"); self.assertIn("足够原话依据与必要条件",e); self.assertIn("必要证据/条件",e)
 def test_every_video_has_full_coverage_not_union_coverage(self):
  e=read("references/editorial-policy.md"); h=read("references/highlight-selection.md"); self.assertIn("每一条实际选中的成片",e); self.assertIn("多条并集不能补齐单条遗漏",h)
 def test_empathy_first_opening_and_customer_value(self):
  e=read("references/editorial-policy.md"); self.assertIn("共情入口优先",e); self.assertIn("具体顾客结果",e); self.assertIn("颜色、搭配、材质或外观表达不按关键词禁用或排除",e)
 def test_valid_points_are_not_removed_due_to_low_value_or_length(self):
  h=read("references/highlight-selection.md"); self.assertIn("不能把低价值当作弱增量",h); self.assertIn("不得因为预计时长",h); self.assertIn("不得因为预计时长过短或过长要求删减有效购买信息",h)
 def test_repetition_policy_still_uses_semantic_increments(self):
  e=read("references/editorial-policy.md"); self.assertIn("先判同事实",e); self.assertIn("新增信息",e); self.assertIn("说服增量",e)
 def test_global_bans_remain_scoped_and_category_neutral(self):
  g=read("references/global-rules.md"); self.assertIn("羊毛",g); self.assertIn("羊绒",g); self.assertIn("防静电不是正式禁词",g)
 def test_duration_has_no_acceptance_threshold(self):
  for p in ("references/editorial-policy.md","references/highlight-selection.md","references/final-check.md"):
   t=read(p); self.assertIn("约数",t); self.assertNotIn("45 秒",t); self.assertNotIn("120 秒",t); self.assertNotIn("130 秒",t)
 def test_multi_video_choice_does_not_default_after_opportunity(self):
  c=read("references/runtime-contract.md"); self.assertIn("暂停生成正式成片",c); self.assertIn("没有可行机会",c); self.assertNotIn("默认完成",c)
if __name__=="__main__": unittest.main()
