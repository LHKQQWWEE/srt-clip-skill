from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = next(p for p in ROOT.parents if (p / "plugin.json").is_file())


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class PurchasePromptNeutralityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = read("references/runtime-current.md")
        cls.editorial = read("references/editorial-policy.md")
        cls.audit = read("references/final-check.md")
        cls.selection = read("references/highlight-selection.md")
        cls.environment = read("ENVIRONMENT.md")

    def test_purchase_prompt_is_optional_not_a_timing_gate(self):
        self.assertIn("购买推动是可选项", self.editorial)
        self.assertIn("不强制提前安排购买机会", self.editorial)
        self.assertIn("不因 CTA 较晚或某条成片没有 CTA 而判定失败", self.editorial)
        self.assertIn("购买推动是可选项", self.audit)
        self.assertIn("不强制提前安排购买机会", self.audit)

    def test_no_early_cta_or_truncation_requirement_remains_active(self):
        active = "\n".join([self.skill, self.editorial, self.audit, self.selection])
        obsolete = [
            "立即寻找最早合理成交机会",
            "每个前缀应已有完整购买理由",
            "后半段不得承担第一次说服",
            "低完播截断压力测试",
            "累计语义前缀仍没有完整购买理由和购买机会",
        ]
        for phrase in obsolete:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, active)

    def test_optional_action_still_keeps_its_own_context(self):
        self.assertIn("完整语义、商品/颜色/对象/条件", self.editorial)
        self.assertIn("价格或活动说明", self.editorial)
        self.assertIn("上架/链接状态", self.editorial)
        self.assertIn("完整语境", self.audit)

    def test_environment_and_launcher_do_not_restore_an_early_cta_gate(self):
        self.assertIn("CTA 是可选项", self.environment)
        self.assertNotIn("低完播截断压力测试", self.environment)
        manifest = json.loads((PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8"))
        interface = manifest["extensions"]["com.openai"]["interface"]
        prompt = interface["defaultPrompt"]
        self.assertIn("每次调用 C2", prompt)
        self.assertIn("不得使用历史摘要或旧缓存", prompt)
        self.assertIn("单条及每条多视频都覆盖完整卖点池", interface["longDescription"])
        self.assertIn("等待选择", interface["longDescription"])

    def test_no_hard_duration_ceiling(self):
        self.assertIn("取消 120 秒硬上限", self.selection)
        self.assertIn("不设固定时长上限", self.skill)
        self.assertNotIn("45–120 秒", self.selection)

    def test_current_core_and_package_versions(self):
        self.assertEqual((PLUGIN_ROOT / "VERSION").read_text(encoding="utf-8").strip(), "0.4.6")
        manifest = json.loads((PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8"))
        codex_manifest = json.loads((PLUGIN_ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "0.4.24")
        self.assertEqual(codex_manifest["version"], "0.4.24")


if __name__ == "__main__":
    unittest.main()
