import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RuntimeContractTests(unittest.TestCase):
    def setUp(self):
        self.skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.editorial = (ROOT / "references" / "editorial-policy.md").read_text(encoding="utf-8")
        self.final_check = (ROOT / "references" / "final-check.md").read_text(encoding="utf-8")
        self.schema = json.loads((ROOT / "scripts" / "selection.schema.json").read_text(encoding="utf-8"))

    def require(self, text, phrase):
        self.assertTrue(phrase in text, f"required contract phrase missing: {phrase}")

    def test_machine_and_ai_boundaries_keep_semantics_with_ai(self):
        self.require(self.skill, "机器判定与 AI 语义判断")
        for phrase in ("机器判定", "AI 语义判断", "risk_hint", "不得升级为硬失败"):
            self.require(self.final_check, phrase)
        for phrase in ("卖点池是否遗漏", "原话是否真正在真实上下文中支撑", "机器只验结构"):
            self.require(self.final_check, phrase)
        self.require(self.final_check, "特殊纤维")
        self.require(self.final_check, "防静电")

    def test_candidate_comparison_keeps_full_path_without_loser_transcripts(self):
        for phrase in ("完整序号顺序", "卖点 ID → 支撑序号", "必要证据", "必要条件", "六维", "落选候选不展开全文"):
            self.require(self.editorial, phrase)
        self.require(self.editorial, "prev_id → next_id")
        self.require(self.editorial, "候选不合格")

    def test_jump_checks_are_internal_and_failed_jumps_disqualify_candidate(self):
        self.require(self.editorial, "逐字对照原文")
        self.require(self.editorial, "不进入五部分交付")
        self.require(self.editorial, "跳点核验不成立")

    def test_output_limits_and_exceptions_are_explicit(self):
        self.assertRegex(self.skill, r"重要未采用内容.{0,30}最多 ?3 条")
        self.assertIn("每条一行", self.skill)
        for exception in ("合规风险", "事实待核实", "关键限制"):
            self.require(self.skill, exception)
        self.require(self.skill, "不计入三条限额")
        self.require(self.skill, "短句模板")

    def test_duration_rounding_and_single_shared_display_field_are_explicit(self):
        for phrase in ("连续组", "0.5ms 进位规则舍入到毫秒一次", "playback_duration_display", "不得各自重算"):
            self.require(self.skill, phrase)

    def test_five_part_output_and_local_repair_contract_remain(self):
        for phrase in ("固定五部分交付", "只重出受影响段落", "不重写整份五部分"):
            self.require(self.skill, phrase)

    def test_schema_has_five_roles_and_independent_flags(self):
        roles = self.schema["properties"]["roles"]["items"]["properties"]["role"]["enum"]
        self.assertEqual(roles, ["独立卖点", "证据", "条件", "必要衔接", "可选行动句"])
        flags = self.schema["properties"]["flags"]["items"]["properties"]["type"]["enum"]
        self.assertEqual(flags, ["fact_pending", "risk_hint", "key_limit"])


if __name__ == "__main__":
    unittest.main()
