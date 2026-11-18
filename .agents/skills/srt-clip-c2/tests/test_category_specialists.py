from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]

def read(path): return (ROOT/path).read_text(encoding="utf-8")

class CategorySpecialists(unittest.TestCase):
    def test_registry_new_modules(self):
        reg=read("references/category-registry.md")
        for filename in ["shoes.md","scarves.md","womens-fashion.md"]:
            self.assertIn("categories/"+filename,reg)
        self.assertIn("排他",reg)
    def test_exclusive_fashion_scope(self):
        fashion=read("categories/womens-fashion.md")
        self.assertIn("不叠加",fashion)
        self.assertIn("鞋类由",fashion)
        self.assertIn("围巾、围脖",fashion)
    def test_core_routes_and_output_unchanged(self):
        core=read("SKILL.md")
        self.assertIn("categories/shoes.md",core)
        self.assertIn("categories/scarves.md",core)
        self.assertIn("1.2 倍速",core)
        self.assertIn("120 秒",core)
        self.assertIn("固定五部分",core)
        self.assertIn("购买决策编辑器",core)
    def test_shoes_unique_semantics(self):
        s=read("categories/shoes.md")
        for x in ["高跟鞋","运动鞋","脚背","跟高","防滑","磨脚","画面待核实","跨款","鞋底结构","#穿搭"]:
            self.assertIn(x,s)
        self.assertIn("不同时加载",s)
        self.assertIn("不能拥有业务决策权",read("references/ai-first-constitution.md"))
    def test_scarves_unique_semantics(self):
        s=read("categories/scarves.md")
        for x in ["皮草","围脖","丝巾","披肩","肤感","龙猫毛","围法","干洗","敏感","建议买两条","#时尚营销"]:
            self.assertIn(x,s)
        self.assertIn("不并行加载",s)
    def test_portable_embeds_full_current_sources(self):
        p=read("C2-Universal-Portable.md")
        for path in ["SKILL.md","categories/womens-fashion.md","categories/shoes.md","categories/scarves.md","references/update-protocol.md"]:
            self.assertIn(read(path).strip(),p,path)
    def test_no_new_mandatory_tools(self):
        for path in ["categories/shoes.md","categories/scarves.md"]:
            s=read(path)
            self.assertNotIn("必须运行 Python",s)
            self.assertNotIn("必须先联网",s)
            self.assertNotIn("JSON 台账",s)
if __name__=="__main__": unittest.main()
