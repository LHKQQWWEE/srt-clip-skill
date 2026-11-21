from pathlib import Path
import json
import unittest


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = next(path for path in ROOT.parents if (path / "plugin.json").is_file())


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def assert_has(test, text, phrase):
    test.assertTrue(phrase in text, f"missing required policy phrase: {phrase}")


class PurchaseDecision046Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = read("SKILL.md")
        cls.editorial = read("references/editorial-policy.md")
        cls.selection = read("references/highlight-selection.md")
        cls.final_check = read("references/final-check.md")
        cls.active = "\n".join([cls.skill, cls.editorial, cls.selection, cls.final_check])

    def test_core_and_plugin_versions_are_current(self):
        self.assertEqual((PLUGIN_ROOT / "VERSION").read_text(encoding="utf-8").strip(), "0.4.6")
        manifest = json.loads((PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "0.4.15")
        assert_has(self, self.skill, "C2 Universal 0.4.6")

    def test_complete_inventory_precedes_candidate_generation(self):
        for phrase in ["先完整读取目标商品全部上下文", "候选购买路径", "禁止边读取边锁定最终核心角度", "第一个强卖点"]:
            assert_has(self, self.active, phrase)

    def test_single_clip_requires_every_valid_independent_point(self):
        for phrase in ["单条正式方案必须覆盖全部已确认有效独立卖点", "覆盖不足的候选不得进入评分和最终排名", "不能因低价值"]:
            assert_has(self, self.active, phrase)

    def test_low_decision_value_is_distinct_from_weak_increment(self):
        for phrase in ["低决策价值≠弱增量", "低价值但有效卖点必须保留", "弱增量"]:
            assert_has(self, self.active, phrase)

    def test_point_granularity_keeps_examples_grouped_and_facts_distinct(self):
        for phrase in ["有效独立购买信息", "不得机械拆碎", "不得过度合并造成信息遗漏", "证据覆盖不等于卖点覆盖"]:
            assert_has(self, self.active, phrase)

    def test_each_candidate_is_a_complete_path_scored_after_coverage_gate(self):
        for dimension in ["顾客问题强度", "首屏停留价值", "核心理由完整度", "全卖点承载自然度", "叙事连贯度", "购买决策效率"]:
            with self.subTest(dimension=dimension):
                assert_has(self, self.active, dimension)
        for phrase in ["评分对象是完整候选成片", "候选资格门槛", "候选分数接近时"]:
            assert_has(self, self.active, phrase)

    def test_single_and_multi_output_coverage_are_different_contracts(self):
        for phrase in ["单条正式方案必须覆盖全部已确认有效独立卖点", "每条多视频方案也都必须覆盖同一完整卖点池", "第一条固定取候选池综合第一", "机械 Top N", "同一候选池", "实质差异"]:
            assert_has(self, self.active, phrase)

    def test_time_pressure_trims_only_non_point_content_first(self):
        trim_section = self.selection.split("## 时长下限与动态取舍", 1)[-1].split("## 停止条件", 1)[0]
        order = [
            "机械性重复",
            "过度性重复",
            "弱增量",
            "泛夸赞",
            "普通过渡",
            "弱 CTA",
            "同一卖点的过多证明",
        ]
        missing = [term for term in order if term not in trim_section]
        self.assertFalse(missing, f"trim order terms are missing: {missing}")
        positions = [trim_section.index(term) for term in order]
        self.assertEqual(positions, sorted(positions))
        for phrase in ["时长压力不得删除有效独立卖点", "不设固定时长上限", "45 秒是一般成片的合理下限参考"]:
            assert_has(self, self.active, phrase)

    def test_stop_requires_full_coverage_and_necessary_support(self):
        for phrase in ["停止条件", "全部有效独立卖点已有承载表达", "必要证据和条件已经完整"]:
            assert_has(self, self.active, phrase)

    def test_existing_roles_and_final_audit_own_the_new_checks(self):
        for phrase in ["反锚定", "Product Purchase-Decision Architect", "Purchase-Decision Editor", "Chief Decision Editor", "Final Quality Auditor"]:
            assert_has(self, self.skill, phrase)
        for hard_failure in ["单条正式方案漏掉任何已确认有效独立卖点", "候选尚未完整编排全部有效卖点就评分", "机械 Top N", "低决策价值和弱增量混为一谈"]:
            with self.subTest(hard_failure=hard_failure):
                assert_has(self, self.final_check, hard_failure)

    def test_architecture_stays_ai_first_and_does_not_add_fixed_machinery(self):
        assert_has(self, self.skill, "一个 AI、一次语义分析、一次终检")
        assert_has(self, self.skill, "CTA 可选")
        self.assertFalse("必须运行 Python 才能" in self.active, "active rules introduced a mandatory Python gate")
        self.assertIn("不设固定卖点权重", self.active)
        self.assertFalse("每条字幕必须" in self.active, "active rules changed point coverage into cue-by-cue coverage")

    def test_real_case_regressions_are_recorded(self):
        cases = (PLUGIN_ROOT / "docs/history/releases/real-source-regression-0.4.5.md").read_text(encoding="utf-8")
        for case in ["鞋类长素材", "颗粒羊毛马甲", "短款大衣", "752 条玉米方便面"]:
            with self.subTest(case=case):
                self.assertIn(case, cases)


if __name__ == "__main__":
    unittest.main()
