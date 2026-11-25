from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
PACKS=["product-knowledge-packs/womens-fashion.md","product-knowledge-packs/shoes.md","product-knowledge-packs/scarves.md"]
def read(path): return (ROOT/path).read_text(encoding="utf-8")
class ProductKnowledgePackTests(unittest.TestCase):
 def test_registry_is_optional_and_not_a_content_router(self):
  r=read("references/product-knowledge-registry.md"); self.assertIn("未注册类别仍可按 Universal Core 正常处理",r); self.assertNotIn("排他路由",r)
 def test_current_packs_exist_and_only_constrain_facts(self):
  for path in PACKS:
   text=read(path); self.assertTrue((ROOT/path).is_file()); self.assertIn("事实",text); self.assertIn("归属",text); self.assertNotIn("固定卖点顺序",text)
 def test_universal_rules_own_dynamic_structure(self):
  runtime=read("references/runtime-current.md"); editorial=read("references/editorial-policy.md")
  self.assertIn("动态顾客心理驱动",runtime); self.assertIn("内容结构",editorial); self.assertIn("不存在所有商品通用的段落成交模板",editorial)
 def test_no_old_category_routing_paths_remain(self):
  active=read("references/runtime-current.md")+read("references/product-knowledge-registry.md")+"".join(read(p) for p in PACKS)
  self.assertNotIn("categories/",active); self.assertNotIn("category-registry.md",active)
if __name__=="__main__": unittest.main()
