import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p): return (ROOT/p).read_text(encoding="utf-8")
class RuntimeContractTests(unittest.TestCase):
 def test_machine_and_ai_boundaries_keep_semantics_with_ai(self):
  f=read("references/final-check.md"); self.assertIn("机器不判断",f); self.assertIn("AI 的语义判断",f); self.assertIn("risk_hint",f); self.assertIn("信息池完整性",f)
 def test_opening_compares_only_empathy_first_openings(self):
  e=read("references/editorial-policy.md"); self.assertIn("共情优先",e); self.assertIn("只比较开头",e); self.assertIn("不为完整成片建立候选比赛",e); self.assertIn("不开启完整成片候选的资格评分",e)
 def test_multi_video_gate_and_checkpoint_contract(self):
  c=read("references/runtime-contract.md"); self.assertLess(c.index("建立完整卖点池"),c.index("检测多视频机会"));
  for phrase in ("暂停生成正式成片","保存当前对话检查点","恢复此状态","不重复读取","不重复识别","不重复检测"): self.assertIn(phrase,c)
 def test_final_check_is_limited_to_selected_cuts(self):
  f=read("references/final-check.md"); self.assertIn("仅为用户已选定且实际写出的成片",f); self.assertIn("不终检未选主题",f.split("## 失败修复",1)[0])
 def test_duration_and_cta_contract(self):
  h=read("references/highlight-selection.md"); e=read("references/editorial-policy.md"); self.assertIn("只作约数参考",h); self.assertIn("不参与质量验收",h); self.assertIn("不触发拆条",h); self.assertIn("原文存在适用且合规的促单话术时，必须保留",e); self.assertIn("原文没有促单时，禁止编造、改写或补充",e)
 def test_five_part_output_and_one_ai_remain(self):
  c=read("references/runtime-contract.md"); self.assertIn("一个 AI",c); self.assertIn("固定五部分交付",c); self.assertIn("不重写整份五部分",c)
 def test_schema_has_selection_level_contract_not_full_cut_competition(self):
  schema=json.loads(read("scripts/selection.schema.json")); props=schema["properties"]; self.assertIn("opening_choice",props); self.assertNotIn("multi_video_opportunity",props); self.assertNotIn("checkpoint_status",props); self.assertIn("current conversation",schema["description"]); self.assertNotIn("candidate_comparison",props); self.assertNotIn("jump_checks",props); self.assertEqual(props["roles"]["items"]["properties"]["role"]["enum"],["独立卖点","证据","条件","必要衔接","适用促单原话"])
  self.assertEqual(props["flags"]["items"]["properties"]["type"]["enum"],["fact_pending","risk_hint","key_limit"])
if __name__=="__main__": unittest.main()
