from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class ResponsibilityArchitectureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = read("references/runtime-current.md")
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
        self.assertIn("不代表新 Agent、模型或调用", self.skill)
        self.assertIn("不创建多个模型、串行 Agent", self.constitution)
        self.assertIn("不增加第二轮语义分析", self.skill)

    def test_global_rules_and_factual_veto_are_not_overridable(self):
        self.assertIn("全局硬规则", self.skill)
        self.assertIn("对硬边界有否决权", self.skill)
        self.assertIn("事实与边界官的否决不能由转化诉求推翻", self.skill)
        self.assertIn("总决策编辑不能豁免已确认禁令", read("references/global-rules.md"))

    def test_prohibited_term_owner_and_user_authorization_boundary(self):
        global_rules = read("references/global-rules.md")
        self.assertIn("唯一词库", self.skill)
        self.assertIn("总决策编辑是词库管理最终负责人", read("references/global-rules.md"))
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
        self.assertIn("设计正式命中与风险提示边界", self.skill)
        self.assertIn("完整读取目标商品的全部上下文和有效讲解窗口", self.skill)
        self.assertIn("禁止边读边锁定", self.skill)
        self.assertIn("候选资格门槛", self.skill)
        self.assertIn("完整候选成片", self.skill)
        self.assertIn("不得仅凭相同字眼、绝对措辞或风险推测扩展范围", self.skill)
        self.assertIn("先判同事实→判新增信息→判说服增量→最后取舍", self.skill)
        self.assertIn("低决策价值≠弱增量", self.skill)
        self.assertIn("每条多视频方案各自覆盖完整信息池", self.skill)
        self.assertIn("不得扩大硬禁范围", self.skill)
        self.assertIn("不创建多个模型、串行 Agent", self.skill)

    def test_architect_sets_dynamic_structure_not_category_template(self):
        self.assertIn("动态构建路径", self.skill)
        self.assertIn("不得退回固定类目模板或预设卖点顺序", self.constitution)
        self.assertIn("购买决策架构师", self.editorial)
        self.assertIn("内容结构根据本商品", self.constitution)

    def test_editor_uses_source_words_and_auditor_returns_local_fixes(self):
        self.assertIn("只能重排同一商品的完整原话", self.editorial)
        self.assertIn("失败时按根因只修复受影响片段", self.skill)
        self.assertIn("局部修复", self.skill)
        self.assertIn("每条成片都按自己的核心购买角度逐项重评全部卖点", self.final_check)
        self.assertIn("总决策编辑不得跳过硬性失败项", self.final_check)

    def test_unregistered_category_does_not_block_processing(self):
        self.assertIn("未注册类别不构成阻断", self.constitution)
        self.assertIn("未注册类别仍可按 Universal Core 正常处理", self.registry)

    def test_existing_output_duration_and_source_contract_remain(self):
        self.assertIn("固定五部分交付", self.skill)
        self.assertIn("不设固定时长上限", self.skill)
        self.assertIn("保留原始编号、原话、时间码/逐条时长和来源顺序", self.skill)

    def test_all_points_reassessed_without_expanding_a_local_ban(self):
        self.assertIn("识别其全部有效独立购买信息", self.skill)
        self.assertIn("每个候选从同一完整信息池独立排序并编排全部有效信息", self.skill)
        global_rules = read("references/global-rules.md")
        self.assertIn("只排除命中的完整字幕序号", global_rules)
        self.assertIn("不能把前后字幕当作“上下文窗口”连带删除", global_rules)


if __name__ == "__main__":
    unittest.main()
