import sys
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import prohibited_term_guard as guard
import srt_tools


def registry():
    loader = getattr(guard, "load_term_registry", None)
    return loader() if callable(loader) else []


class ProhibitedTermGovernanceTests(unittest.TestCase):
    def test_registry_contains_only_approved_terms_and_full_governance_fields(self):
        entries = registry()
        self.assertTrue(entries, "the authoritative term registry must be machine-readable")
        by_term = {entry.term: entry for entry in entries}
        direct = {entry.term for entry in entries if entry.match_class == "direct"}
        contextual = {entry.term for entry in entries if entry.match_class == "contextual"}
        self.assertEqual(
            direct,
            {"羊毛", "皮草", "羊绒", "特殊动物绒", "全金纺半高领", "不起球", "兔毛", "羊皮"},
        )
        self.assertEqual(
            contextual,
            {"国家级", "最高级", "顶级", "首选", "绝无仅有", "史无前例", "第一", "最好", "全网最好"},
        )
        for entry in entries:
            for field in (
                "category",
                "source",
                "trigger_condition",
                "allowed_exceptions",
                "confirmed_equivalents",
                "scope",
                "test_cases",
                "version_record",
            ):
                self.assertTrue(hasattr(entry, field), f"{entry.term} is missing {field}")
            self.assertTrue(entry.source and entry.test_cases and entry.version_record)
        self.assertEqual(by_term["不起球"].allowed_exceptions, ("不易起球",))
        self.assertEqual(by_term["皮草"].confirmed_equivalents, ())

    def test_direct_hits_remove_only_their_full_cue_and_preserve_ids(self):
        cues = [
            guard.Cue("40", "版型在这里，长度到腰线"),
            guard.Cue("41", "这件不起球，穿起来舒服"),
            guard.Cue("42", "这件不易起球，表面比较平整"),
            guard.Cue("43", "这件羊绒混纺"),
            guard.Cue("44", "袖口有罗纹"),
            guard.Cue("45", "这件兔毛混纺针织衫"),
            guard.Cue("46", "这件哑光小羊皮真好搭"),
        ]
        report = guard.build_report(cues, registry())
        self.assertEqual(report["excluded_full_cue_ids"], ["41", "43", "45", "46"])
        self.assertEqual([hit["cue_id"] for hit in report["direct_hits"]], ["41", "43", "45", "46"])

    def test_down_keyword_is_title_and_topic_only_not_a_subtitle_ban(self):
        entries = {entry.term: entry for entry in registry()}
        self.assertNotIn("羽绒", entries)
        rules = (ROOT / "references" / "global-rules.md").read_text(encoding="utf-8")
        self.assertIn("标题与话题禁用“羽绒”", rules)
        self.assertIn("正文原话及商品识别不因此删除", rules)
        report = guard.build_report([guard.Cue("1", "穿羽绒服也好看")], registry())
        self.assertEqual(report["excluded_full_cue_ids"], [])

    def test_contextual_terms_distinguish_claims_from_ordinary_language(self):
        cues = [
            guard.Cue("1", "第一件拿给大家看"),
            guard.Cue("2", "第一步先看版型"),
            guard.Cue("3", "最好明天发货"),
            guard.Cue("4", "这件是本场首选"),
            guard.Cue("5", "这款顶级面料"),
        ]
        report = guard.build_report(cues, registry())
        self.assertEqual(report["excluded_full_cue_ids"], ["4", "5"])
        candidates = {hit["cue_id"] for hit in report.get("contextual_candidates", [])}
        self.assertEqual(candidates, {"1", "2", "3", "4", "5"})
        self.assertEqual(report["contextual_block_ids"], ["4", "5"])
        self.assertEqual(report["contextual_allow_ids"], ["1", "2", "3"])
        self.assertEqual(report["status"], "SCAN_COMPLETE")

    def test_each_confirmed_contextual_term_is_scanned_for_semantic_review(self):
        cues = [
            guard.Cue("11", "国家级面料工艺"),
            guard.Cue("12", "最高级工艺"),
            guard.Cue("13", "顶级面料"),
            guard.Cue("14", "这款是我的首选"),
            guard.Cue("15", "这件衣服绝无仅有"),
            guard.Cue("16", "史无前例的设计"),
            guard.Cue("17", "这款商品排名第一"),
            guard.Cue("18", "这是市场上最好的一款"),
        ]
        report = guard.build_report(cues, registry())
        self.assertEqual(report["excluded_full_cue_ids"], [str(i) for i in range(11, 19)])
        self.assertEqual(report["contextual_block_ids"], [str(i) for i in range(11, 19)])
        self.assertEqual(report["contextual_candidate_ids"], [str(i) for i in range(11, 19)])
        self.assertEqual(report["status"], "SCAN_COMPLETE")

    def test_full_net_best_is_blocked_even_inside_a_call_to_action(self):
        cues = [guard.Cue("19", "点击商品卡下单，这款全网最好。")]
        report = guard.build_report(cues, registry(), selected_ids=["19"], final_text=cues[0].text)
        self.assertEqual(report["excluded_full_cue_ids"], ["19"])
        self.assertEqual(report["selected_hit_ids"], ["19"])
        self.assertEqual(report["status"], "FAIL")

    def test_contextual_absolute_claim_in_a_call_to_action_is_still_blocked(self):
        cue = guard.Cue("20", "点击商品卡下单，这款顶级面料特别显身材。")
        report = guard.build_report([cue], registry())
        self.assertEqual(report["excluded_full_cue_ids"], ["20"])
        self.assertEqual([hit["cue_id"] for hit in report["contextual_candidates"]], ["20"])
        self.assertEqual(report["contextual_block_ids"], ["20"])
        self.assertEqual(report["status"], "SCAN_COMPLETE")

    def test_guard_cli_separates_context_review_from_confirmed_hit(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.txt"
            source.write_text("9 1.0 这款顶级面料\n", encoding="utf-8")
            review = subprocess.run(
                [sys.executable, str(Path(guard.__file__)), str(source)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
            )
            self.assertEqual(review.returncode, 0)
            self.assertEqual(json.loads(review.stdout)["contextual_block_ids"], ["9"])
            source.write_text("9 1.0 这款全网最好\n", encoding="utf-8")
            hit = subprocess.run(
                [sys.executable, str(Path(guard.__file__)), str(source), "--selected-ids", "9"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
            )
            self.assertEqual(hit.returncode, 1)
            report = json.loads(hit.stdout)
            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(report["selected_hit_ids"], ["9"])

    def test_unconfirmed_asr_variants_are_not_formal_hits_or_aliases(self):
        cues = [guard.Cue("7", "这件是国家计级活动款")]
        report = guard.build_report(cues, registry())
        self.assertEqual(report["direct_hits"], [])
        self.assertEqual(report.get("contextual_candidates", []), [])
        self.assertEqual(report["excluded_full_cue_ids"], [])
        self.assertNotIn("国家计级", {alias for entry in registry() for alias in entry.confirmed_equivalents})

    def test_unified_scanner_uses_registry_protection_and_never_joins_cues(self):
        source = (
            "1 0.5 第一件拿给大家看\n"
            "2 0.5 这款是顶级面料\n"
            "3 0.5 这件不起球\n"
            "4 0.5 这件不易起球\n"
            "5 0.5 这件是羊\n"
            "6 0.5 毛含量不清"
        )
        report = srt_tools.preprocess_text(source)
        self.assertEqual(report["direct_hits"], [{"term": "不起球", "cue_ids": ["3"]}])
        self.assertEqual(report["confirmed_equivalent_hits"], [])
        self.assertEqual(report["contextual_candidates"], [
            {"term": "顶级", "cue_ids": ["2"]},
            {"term": "第一", "cue_ids": ["1"]},
        ])
        self.assertTrue(report["semantic_review_required"])
        self.assertFalse(report["contextual_review_required"])
        self.assertEqual(report["contextual_block_ids"], ["2"])
        self.assertEqual(report["contextual_allow_ids"], ["1"])
        self.assertEqual([row["mark"] for row in report["compact_table"]], ["", "HIT", "HIT", "", "", ""])

    def test_multi_product_filter_preserves_neighboring_cues_and_original_sequence(self):
        cues = [
            guard.Cue("101", "第一件围巾拿给大家看"),
            guard.Cue("102", "这件围巾全网最好"),
            guard.Cue("103", "另一款针织衫的袖口是罗纹"),
        ]
        report = guard.build_report(cues, registry())
        self.assertEqual(report["excluded_full_cue_ids"], ["102"])
        self.assertEqual([cue.cue_id for cue in cues if cue.cue_id not in report["excluded_full_cue_ids"]], ["101", "103"])

    def test_real_price_is_not_a_banned_term_and_cta_price_rules_remain_separate(self):
        cue = guard.Cue("30", "主体商品页已核实价格为199元。")
        report = guard.build_report([cue], registry())
        rules = (ROOT / "references" / "global-rules.md").read_text(encoding="utf-8")
        editorial = (ROOT / "references" / "editorial-policy.md").read_text(encoding="utf-8")
        self.assertEqual(report["direct_hits"], [])
        self.assertIn("价格本身不是本词库的违禁词命中", rules)
        self.assertIn("真实商品标价可按原话保留", editorial)
        promotion = (ROOT / "references" / "promotion-policy.md").read_text(encoding="utf-8")
        self.assertIn("实时交易信息", promotion)
        self.assertIn("活动有效期", editorial)

    def test_absolute_terms_in_final_text_are_rescanned_with_the_original_source_id(self):
        cues = [guard.Cue("65", "面料不起球"), guard.Cue("66", "领口走线整齐")]
        report = guard.build_report(cues, registry(), selected_ids=["65", "66"], final_text="面料不起球\n领口走线整齐")
        self.assertEqual(report["selected_hit_ids"], ["65"])
        self.assertEqual([hit["cue_id"] for hit in report["final_text_hits"]], ["final_text"])
        self.assertEqual(report["final_text_hits"][0]["source_cue_ids"], ["65"])
        self.assertEqual(report["final_text_hits"][0]["selected_source_cue_ids"], ["65"])
        self.assertEqual(report["status"], "FAIL")

    def test_final_text_contextual_claim_is_rechecked_after_layout(self):
        cue = guard.Cue("81", "面料垂感自然")
        report = guard.build_report([cue], registry(), selected_ids=["81"], final_text="标题：顶级面料垂感")
        self.assertEqual(report["final_text_hits"], [])
        self.assertEqual([hit["cue_id"] for hit in report["final_contextual_candidates"]], ["final_text"])
        self.assertEqual(report["status"], "FAIL")

    def test_runtime_defines_the_required_scan_order_without_changing_other_rules(self):
        rules = (ROOT / "references" / "global-rules.md").read_text(encoding="utf-8")
        contract = (ROOT / "references" / "runtime-contract.md").read_text(encoding="utf-8")
        final_check = (ROOT / "references" / "final-check.md").read_text(encoding="utf-8")
        duration_policy = (ROOT / "references" / "clip-selection-policy.md").read_text(encoding="utf-8")
        self.assertIn("原始 SRT 扫描 → 违禁句过滤 → 卖点信息池建立 → 板块编排 → 最终成片复扫 → 序号核验", rules)
        self.assertIn("违禁句过滤", contract)
        self.assertIn("最终成片复扫", final_check)
        self.assertIn("用户最多选择 3 个", contract)
        self.assertIn("90 秒是有效信息密度目标", duration_policy)
        self.assertIn("100 秒可作为可接受参考", duration_policy)


if __name__ == "__main__":
    unittest.main()
