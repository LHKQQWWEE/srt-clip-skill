from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACKS = [
    "product-knowledge-packs/womens-fashion.md",
    "product-knowledge-packs/shoes.md",
    "product-knowledge-packs/scarves.md",
]

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class ProductKnowledgePackTests(unittest.TestCase):
    def test_registry_is_optional_and_not_a_content_router(self):
        registry = read("references/product-knowledge-registry.md")
        self.assertIn("不是类目路由器、内容模块或剪辑模板", registry)
        self.assertIn("未注册类别仍可按 Universal Core 正常处理", registry)
        self.assertIn("一个或多个知识包", registry)
        self.assertNotIn("排他路由", registry)
        self.assertNotIn("加载对应专项模块", registry)

    def test_all_current_knowledge_packs_exist(self):
        for path in PACKS:
            with self.subTest(path=path):
                self.assertTrue((ROOT / path).is_file())
                self.assertIn("不规定结构", read(path))

    def test_packs_only_constrain_product_facts(self):
        for path in PACKS:
            with self.subTest(path=path):
                text = read(path)
                self.assertIn("事实", text)
                self.assertIn("归属", text)
                self.assertNotIn("#穿搭", text)
                self.assertNotIn("#时尚营销", text)
                self.assertNotIn("固定卖点顺序", text)

    def test_dynamic_architecture_owns_structure(self):
        skill = read("references/runtime-current.md")
        editorial = read("references/editorial-policy.md")
        self.assertIn("内容结构根据本商品", skill)
        self.assertIn("不存在所有商品通用的段落成交模板、卖点顺序、成交次数或成交位置", editorial)
        self.assertIn("购买决策架构师", editorial)

    def test_no_old_category_routing_paths_remain(self):
        active = "\n".join(
            [read("references/runtime-current.md"), read("references/product-knowledge-registry.md")]
            + [read(path) for path in PACKS]
        )
        self.assertNotIn("categories/", active)
        self.assertNotIn("category-registry.md", active)


if __name__ == "__main__":
    unittest.main()
