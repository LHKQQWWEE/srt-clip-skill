from pathlib import Path
import json
import unittest


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = next(p for p in ROOT.parents if (p / "plugin.json").is_file())


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def assert_has(test, text, phrase):
    if phrase not in text:
        test.fail(f"missing required policy phrase: {phrase}")


class PurchaseAnglePolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = read("references/runtime-current.md")
        cls.editorial = read("references/editorial-policy.md")
        cls.selection = read("references/highlight-selection.md")
        cls.global_rules = read("references/global-rules.md")
        cls.final_check = read("references/final-check.md")
        cls.rubric = read("tests/quality-rubric.md")

    def test_identify_all_points_and_rerate_them_for_each_video_angle(self):
        active = "\n".join([self.skill, self.editorial, self.selection, self.final_check])
        for phrase in [
            "完整读取目标商品的全部上下文和有效讲解窗口",
            "识别其全部有效独立购买信息",
            "每条候选路径使用同一完整信息集，独立重新评估全部有效卖点",
            "单条正式方案必须覆盖全部已确认有效独立卖点",
            "每条多视频方案也都必须覆盖同一完整卖点池",
            "禁止边读边锁定最终核心角度",
            "候选资格门槛",
            "评分对象是完整候选成片",
        ]:
            with self.subTest(phrase=phrase):
                assert_has(self, active, phrase)
        self.assertNotIn("不要求完整卖点清单", active)
        self.assertNotIn("不得为追求 100% 覆盖", active)

    def test_each_clip_angle_can_change_a_points_value(self):
        for phrase in ["同一卖点在不同成片中可以有不同价值等级", "逐条复评", "不得沿用另一条成片的价值排序"]:
            with self.subTest(phrase=phrase):
                assert_has(self, self.selection, phrase)

    def test_opening_compares_attention_hooks_across_the_full_transcript(self):
        active = "\n".join([self.editorial, self.final_check])
        for phrase in [
            "区分吸引顾客关注的问题、回应顾客问题、提供购买依据",
            "具体数字、使用时长、洗涤次数和主播经历不自动获得开头优先权",
            "核心主题只决定重点展开和内容组织，不限定开头候选范围",
            "开头与紧随其后的必要回应作为一个完整入口比较",
        ]:
            with self.subTest(phrase=phrase):
                assert_has(self, active, phrase)

    def test_final_check_requires_problem_response_match_and_preserves_hooks(self):
        for phrase in [
            "因主题名称跳过全文中更有竞争力的开头候选",
            "仅因具体数字、使用经历或商品介绍就判定首屏价值更高",
            "问题型开头与后续商品回应不对应",
            "问题段较长就直接淘汰",
            "主播设问不得写成真实顾客反馈",
        ]:
            with self.subTest(phrase=phrase):
                assert_has(self, self.final_check, phrase)

    def test_multi_clip_output_is_complete_and_differentiated(self):
        for phrase in ["每条都交付完整", "差异化组合", "每条方案必须各自覆盖全部有效独立卖点", "不得只更换开头"]:
            with self.subTest(phrase=phrase):
                assert_has(self, self.selection, phrase)
        assert_has(self, self.selection, "明确的核心购买角度")
        assert_has(self, self.skill, "每条多视频方案各自覆盖完整信息池")

    def test_purchase_prompt_is_optional_and_never_forced_early(self):
        active = "\n".join([
            self.skill,
            self.editorial,
            self.final_check,
            self.rubric,
            (PLUGIN_ROOT / "START-HERE.md").read_text(encoding="utf-8"),
            (PLUGIN_ROOT / "docs/platform-adapter-interface.md").read_text(encoding="utf-8"),
        ])
        assert_has(self, active, "购买推动是可选项")
        assert_has(self, active, "不强制提前安排购买机会")
        for obsolete in [
            "立即寻找最早合理成交机会",
            "每个前缀应已有完整购买理由",
            "后半段不得承担第一次说服",
            "低完播截断压力测试",
        ]:
            with self.subTest(obsolete=obsolete):
                self.assertFalse(obsolete in active, f"obsolete active rule remains: {obsolete}")

    def test_explicit_prohibited_term_drops_only_its_full_matching_cue(self):
        formal_list = self.global_rules.split("## 正式禁用词库", 1)[1].split("\n## ", 1)[0]
        self.assertIn("`羊毛`", formal_list)
        self.assertIn("`皮草`", formal_list)
        self.assertIn("只排除命中的完整字幕序号", self.global_rules)
        self.assertIn("不连带前后字幕序号", self.global_rules)
        self.assertIn("风险提示本身不能触发删除", self.global_rules)
        self.assertIn("一次字幕命中不能触发对整段、整条候选或整份输入的防御性淘汰", self.global_rules)
        self.assertIn("不得仅凭“皮”“草”“皮裤”“皮裙”或“毛绒”扩展", formal_list)
        self.assertIn("防静电不是正式禁词", self.global_rules)

    def test_current_release_versions_and_only_current_acceptance(self):
        self.assertEqual((PLUGIN_ROOT / "VERSION").read_text(encoding="utf-8").strip(), "0.4.6")
        manifest = json.loads((PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "0.4.24")
        self.assertTrue((ROOT / "tests/release-0.4.6-acceptance.md").is_file())
        self.assertFalse((ROOT / "tests/release-0.4.4-acceptance.md").exists())
        self.assertFalse((PLUGIN_ROOT / "docs/history").exists())


if __name__ == "__main__":
    unittest.main()
