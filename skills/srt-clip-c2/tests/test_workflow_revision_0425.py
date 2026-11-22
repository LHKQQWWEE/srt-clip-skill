import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def read(path): return (ROOT/path).read_text(encoding="utf-8")

class WorkflowRevision0425Tests(unittest.TestCase):
    def test_opening_only_comparison_is_empathy_first(self):
        editorial=read("references/editorial-policy.md")
        self.assertIn("共情优先", editorial)
        self.assertIn("共情入口优先", editorial)
        self.assertIn("只比较开头本身", editorial)
        self.assertIn("不为完整成片建立候选比赛", editorial)
        self.assertIn("不做六维评分", editorial)
        self.assertIn("不为完整成片建立候选比赛", editorial)

    def test_complete_pool_precedes_multi_video_gate_and_resume(self):
        contract=read("references/runtime-contract.md")
        pool=contract.index("建立完整卖点池")
        opportunity=contract.index("检测多视频机会")
        pause=contract.index("暂停生成正式成片")
        resume=contract.index("用户选择后恢复此状态")
        self.assertLess(pool, opportunity); self.assertLess(opportunity,pause); self.assertLess(pause,resume)
        for phrase in ("不重复读取", "不重复识别", "不重复检测"):
            self.assertIn(phrase,contract)
        self.assertNotIn("未选择时按单条默认完成",contract)

    def test_every_selected_cut_covers_the_complete_pool(self):
        editorial=read("references/editorial-policy.md")
        check=read("references/final-check.md")
        self.assertIn("每一条实际选中的成片",editorial)
        self.assertIn("每条选中的成片",check)
        self.assertIn("完整信息池",check)
        self.assertIn("多条中的其他成片不能补足本条",check)

    def test_original_eligible_purchase_prompt_is_required_but_never_invented(self):
        editorial=read("references/editorial-policy.md")
        self.assertIn("原文存在适用且合规的促单话术时，必须保留",editorial)
        self.assertIn("原文没有促单时，禁止编造、改写或补充",editorial)
        self.assertIn("不得跨商品移用话术",editorial)

    def test_duration_is_approximate_and_not_an_acceptance_or_split_gate(self):
        for text in (read("references/highlight-selection.md"),read("references/editorial-policy.md")):
            for forbidden in ("45 秒","45秒","120 秒","120秒","130 秒","130秒"):
                self.assertNotIn(forbidden,text)
        selection=read("references/highlight-selection.md")
        self.assertIn("只作约数参考",selection)
        self.assertIn("时长不参与质量验收",selection)
        self.assertIn("不触发拆条",selection)

    def test_only_selected_cuts_receive_final_audit(self):
        check=read("references/final-check.md")
        self.assertIn("仅为用户已选定且实际写出的成片",check)
        self.assertNotIn("未选成片也需终检",check)

    def test_runtime_manifest_has_real_source_hashes_and_source_map(self):
        manifest=json.loads(read("references/runtime-manifest.json"))
        runtime=read("references/runtime-current.md")
        self.assertEqual(manifest["core_version"],"0.4.6")
        self.assertTrue(manifest["source_map"])
        self.assertEqual(hashlib.sha256(runtime.encode()).hexdigest(),manifest["runtime_sha256"])
        for relative,digest in manifest["source_hashes"].items():
            self.assertEqual(hashlib.sha256((ROOT/relative).read_bytes()).hexdigest(),digest,relative)

    def test_fixed_five_parts_and_single_ai_architecture_remain(self):
        contract=read("references/runtime-contract.md")
        for phrase in ("一个 AI", "固定五部分交付", "不新增 Agent"):
            self.assertIn(phrase,contract)

    def test_real_material_replay_records_the_user_choice_checkpoint(self):
        report=read("tests/real-source-regression-0.4.6.md")
        self.assertIn("509/509 条",report)
        self.assertIn("waiting_for_user_choice",report)
        self.assertIn("没有生成任何未选成片",report)
        self.assertIn("0 项结构诊断",report)

if __name__=="__main__": unittest.main()
