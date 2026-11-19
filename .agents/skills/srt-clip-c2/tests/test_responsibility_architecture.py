from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class ResponsibilityArchitectureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = read("SKILL.md")
        cls.constitution = read("references/ai-first-constitution.md")
        cls.editorial = read("references/editorial-policy.md")
        cls.final_check = read("references/final-check.md")
        cls.registry = read("references/product-knowledge-registry.md")

    def test_five_logical_responsibilities_are_named(self):
        for role in [
            "Chief Decision Editor",
            "Product Purchase-Decision Architect",
            "Product Facts & Boundaries Officer",
            "Purchase-Decision Editor",
            "Final Quality Auditor",
        ]:
            with self.subTest(role=role):
                self.assertIn(role, self.skill)

    def test_roles_are_one_ai_and_one_semantic_pass(self):
        self.assertIn("一个 AI、一次语义分析、一次终检", self.skill)
        self.assertIn("不是多个 Agent", self.skill)
        self.assertIn("不创建多个模型、串行 Agent", self.constitution)
        self.assertNotIn("第二轮语义分析", self.skill)

    def test_global_rules_and_factual_veto_are_not_overridable(self):
        self.assertIn("全局硬规则", self.skill)
        self.assertIn("可否决转化诉求", self.skill)
        self.assertIn("不能推翻否决", self.skill)
        self.assertIn("总决策编辑不能豁免已确认禁令", read("references/global-rules.md"))

    def test_prohibited_term_owner_and_user_authorization_boundary(self):
        global_rules = read("references/global-rules.md")
        self.assertIn("唯一正式词库", self.skill)
        self.assertIn("违禁词管理最终负责人", self.skill)
        self.assertIn("只有用户明确提出“更新违禁词”", global_rules)
        self.assertIn("未入正式词库", global_rules)
        self.assertIn("不得据此新增正式词条", global_rules)

    def test_formal_interception_is_separate_from_contextual_risk(self):
        global_rules = read("references/global-rules.md")
        self.assertIn("正式违禁词拦截与上下文合规风险提示分开处理", global_rules)
        self.assertIn("不直接删除整条字幕或整段内容", global_rules)
        self.assertIn("亮片织进纱线里面", global_rules)
        self.assertIn("不会掉", global_rules)
        self.assertIn("不等于认定合规", global_rules)

    def test_existing_roles_cover_context_and_audit_without_new_agents(self):
        self.assertIn("设计正式命中与风险提示的判断边界", self.skill)
        self.assertIn("不以词语相似度、单个字眼或绝对措辞自动扩禁", self.skill)
        self.assertIn("先判同事实→判新增信息→判说服增量→最后取舍", self.skill)
        self.assertIn("擅自扩围", self.skill)
        self.assertIn("不是多个 Agent", self.skill)

    def test_architect_sets_dynamic_structure_not_category_template(self):
        self.assertIn("动态决定内容路径", self.skill)
        self.assertIn("不按品类预设卖点类目或固定顺序", self.skill)
        self.assertIn("购买决策架构师", self.editorial)
        self.assertIn("内容结构根据本商品", self.constitution)

    def test_editor_uses_source_words_and_auditor_returns_local_fixes(self):
        self.assertIn("不润色或拼接造句", self.skill)
        self.assertIn("发现失败项时退回具体部分", self.skill)
        self.assertIn("局部修复", self.skill)
        self.assertIn("每条成片都按自己的核心购买角度逐项重评全部卖点", self.final_check)
        self.assertIn("总决策编辑不得跳过硬性失败项", self.final_check)

    def test_unregistered_category_does_not_block_processing(self):
        self.assertIn("没有适用知识包时", self.skill)
        self.assertIn("未注册类别仍可按 Universal Core 正常处理", self.registry)

    def test_existing_output_duration_and_source_contract_remain(self):
        self.assertIn("固定五部分交付", self.skill)
        self.assertIn("不设固定时长上限", self.skill)
        self.assertIn("保留原始字幕编号", self.skill)

    def test_all_points_reassessed_without_expanding_a_local_ban(self):
        self.assertIn("完整识别目标商品的全部有效卖点", self.skill)
        self.assertIn("按其核心购买角度，重新评估全部卖点", self.skill)
        global_rules = read("references/global-rules.md")
        self.assertIn("只排除命中的完整字幕序号", global_rules)
        self.assertIn("不能把前后字幕当作“上下文窗口”连带删除", global_rules)


if __name__ == "__main__":
    unittest.main()
