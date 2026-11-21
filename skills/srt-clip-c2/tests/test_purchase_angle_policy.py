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
        cls.skill = read("SKILL.md")
        cls.editorial = read("references/editorial-policy.md")
        cls.selection = read("references/highlight-selection.md")
        cls.global_rules = read("references/global-rules.md")
        cls.final_check = read("references/final-check.md")
        cls.rubric = read("tests/quality-rubric.md")

    def test_identify_all_points_and_rerate_them_for_each_video_angle(self):
        active = "\n".join([self.skill, self.editorial, self.selection, self.final_check])
        for phrase in [
            "先完整读取目标商品全部上下文",
            "识别全部有效独立购买信息并控制粒度",
            "每个候选都逐条复评并完整编排全部有效卖点",
            "单条正式方案必须覆盖全部已确认有效独立卖点",
            "每条多视频方案也都必须覆盖同一完整卖点池",
            "禁止边读取边锁定最终核心角度",
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

    def test_multi_clip_output_is_complete_and_differentiated(self):
        for phrase in ["每条都交付完整", "差异化组合", "每条方案必须各自覆盖全部有效独立卖点", "不得只更换开头"]:
            with self.subTest(phrase=phrase):
                assert_has(self, self.selection, phrase)
        assert_has(self, self.skill, "用户明确要求多条时，每条都须完整覆盖同一商品的全部有效卖点")

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
        self.assertEqual(manifest["version"], "0.4.20")
        self.assertTrue((ROOT / "tests/release-0.4.6-acceptance.md").is_file())
        self.assertFalse((ROOT / "tests/release-0.4.4-acceptance.md").exists())
        self.assertFalse((PLUGIN_ROOT / "docs/history").exists())


if __name__ == "__main__":
    unittest.main()
