import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import prohibited_term_guard as guard
import srt_tools


class Phase3AbsoluteTermTests(unittest.TestCase):
    def scan(self, *texts):
        cues = [guard.Cue(str(index), text) for index, text in enumerate(texts, 1)]
        return cues, guard.build_report(cues, guard.load_term_registry())

    def test_all_confirmed_absolute_phrases_are_registered_as_contextual_claims(self):
        entries = {entry.term: entry for entry in guard.load_term_registry()}
        confirmed = {
            "国家级", "最高级", "顶级", "首选", "绝无仅有",
            "史无前例", "第一", "最好", "全网最好",
        }
        self.assertTrue(confirmed <= entries.keys())
        self.assertTrue(all(entries[term].match_class == "contextual" for term in confirmed))
        self.assertIn("不含客观事实证明豁免", entries["首选"].trigger_condition)
        self.assertEqual(entries["最好"].confirmed_equivalents, ("全网没有比这件更好的",))

    def test_confirmed_product_claims_are_blocked_as_full_cues(self):
        examples = [
            "国家级品质", "最高级面料", "顶级工艺", "这件衣服是我的首选",
            "这是今年最值得推荐的首选搭配", "这款是你们购买的首选",
            "这件外套是搭配打底裤的首选", "绝无仅有的设计", "史无前例的品质",
            "销量第一", "全网第一", "行业第一", "品牌排名第一", "同类产品第一",
            "全网最好", "这件衣服最好", "这是最好的面料", "这是最好的品质",
            "这个款式就是最好的", "全网没有比这件更好的",
        ]
        cues, report = self.scan(*examples)
        self.assertEqual(report["excluded_full_cue_ids"], [cue.cue_id for cue in cues])
        self.assertEqual(report["contextual_block_ids"], [cue.cue_id for cue in cues])

    def test_first_and_best_ordinary_language_is_allowed(self):
        examples = [
            "第一件拿出来给大家看", "第一步先看版型", "第一条裤子是黑色的",
            "最好明天发货", "最好先看一下尺码", "你最好先试穿",
        ]
        cues, report = self.scan(*examples)
        self.assertEqual(report["excluded_full_cue_ids"], [])
        self.assertEqual(report["contextual_block_ids"], [])
        self.assertEqual(report["contextual_allow_ids"], [cue.cue_id for cue in cues])
        self.assertEqual(report["status"], "SCAN_COMPLETE")

    def test_uncertain_context_stays_review_only(self):
        cues, report = self.scan("这个说法里提到了第一，但没有商品排名含义", "它是全店比较靠前的一个款")
        self.assertEqual(report["excluded_full_cue_ids"], [])
        self.assertEqual(report["contextual_block_ids"], [])
        self.assertTrue(report["contextual_review_required"])
        self.assertEqual(report["status"], "REVIEW_CONTEXT")

    def test_allow_protection_runs_before_partial_direct_match(self):
        cues = [guard.Cue("7", "这件不起球"), guard.Cue("8", "这件不易起球")]
        report = guard.build_report(cues, guard.load_term_registry())
        self.assertEqual(report["excluded_full_cue_ids"], ["7"])
        self.assertEqual(report["direct_hits"], [{"cue_id": "7", "matched_terms": ["不起球"]}])

    def test_only_the_matching_claim_cue_is_excluded_and_original_ids_survive(self):
        cues = [
            guard.Cue("101", "第一件围巾拿给大家看"),
            guard.Cue("102", "这件围巾全网最好"),
            guard.Cue("103", "另一款针织衫的袖口是罗纹"),
        ]
        report = guard.build_report(cues, guard.load_term_registry())
        self.assertEqual(report["excluded_full_cue_ids"], ["102"])
        self.assertEqual(report["contextual_block_ids"], ["102"])
        self.assertEqual([cue.cue_id for cue in cues if cue.cue_id not in report["excluded_full_cue_ids"]], ["101", "103"])

    def test_cta_does_not_exempt_claim_and_price_rules_remain_separate(self):
        cues = [guard.Cue("9", "点击商品卡下单，这款顶级面料特别显身材。"), guard.Cue("10", "商品页标价为199元")]
        report = guard.build_report(cues, guard.load_term_registry())
        self.assertEqual(report["excluded_full_cue_ids"], ["9"])
        self.assertNotIn("10", report["excluded_full_cue_ids"])

    def test_unconfirmed_asr_lookalikes_do_not_become_hits(self):
        cues, report = self.scan("这件是国家计级活动款", "史无钱例的设计")
        self.assertEqual(report["contextual_candidates"], [])
        self.assertEqual(report["excluded_full_cue_ids"], [])
        self.assertEqual([item["cue_id"] for item in report["asr_suspicions"]], ["1", "2"])
        self.assertTrue(all(item["auto_blocked"] is False for item in report["asr_suspicions"]))
        self.assertEqual(report["status"], "REVIEW_CONTEXT")
        self.assertNotIn("国家计级", {alias for entry in guard.load_term_registry() for alias in entry.confirmed_equivalents})

    def test_confirmed_contextual_equivalent_is_separate_and_rechecked_in_final_copy(self):
        phrase = "全网没有比这件更好的"
        cues = [guard.Cue("15", phrase)]
        report = guard.build_report(cues, guard.load_term_registry(), selected_ids=["15"], final_text=phrase)
        self.assertEqual(report["contextual_candidates"], [])
        self.assertEqual(report["contextual_confirmed_equivalent_hits"][0]["matched_expressions"], [phrase])
        self.assertEqual(report["excluded_full_cue_ids"], ["15"])
        self.assertEqual(report["final_contextual_confirmed_equivalent_hits"][0]["source_cue_ids"], ["15"])
        self.assertEqual(report["status"], "FAIL")

    def test_selected_product_claim_fails_final_validation_but_ordinary_use_passes(self):
        blocked = [guard.Cue("20", "这款商品销量第一")]
        failed = guard.build_report(blocked, guard.load_term_registry(), selected_ids=["20"], final_text=blocked[0].text)
        self.assertEqual(failed["selected_contextual_hit_ids"], ["20"])
        self.assertEqual(failed["status"], "FAIL")

        allowed = [guard.Cue("21", "第一步先看版型")]
        passed = guard.build_report(allowed, guard.load_term_registry(), selected_ids=["21"], final_text=allowed[0].text)
        self.assertEqual(passed["selected_contextual_hit_ids"], [])
        self.assertEqual(passed["status"], "PASS")

    def test_srt_preprocess_and_final_gate_apply_the_same_context_rules(self):
        source_text = (
            "1\n00:00:00,000 --> 00:00:00,500\n第一步先看版型\n\n"
            "2\n00:00:00,500 --> 00:00:01,000\n这款商品销量第一\n"
        )
        report = srt_tools.preprocess_text(source_text)
        self.assertEqual(report["contextual_allow_ids"], ["1"])
        self.assertEqual(report["contextual_block_ids"], ["2"])
        self.assertEqual(report["excluded_full_cue_ids"], ["2"])
        self.assertEqual([row["mark"] for row in report["compact_table"]], ["", "HIT"])

        source = srt_tools.parse_source(source_text)
        selection = {
            "verification_mode": "script",
            "source_sha256": source.source_sha256,
            "selected_ids": ["2"],
            "selling_points": [{"id": "P1", "support_ids": ["2"]}],
            "roles": [{"cue_id": "2", "role": "独立卖点"}],
            "flags": [],
            "opening_choice": {"cue_ids": ["2"], "basis": "当前目标与素材适配"},
            "known_unaccelerated_ms": 500,
        }
        blocked = srt_tools.validate_selection(source, selection, final_text="这款商品销量第一")
        self.assertEqual(blocked["status"], "FAIL")
        failure_codes = {item["code"] for item in blocked["hard_failures"]}
        self.assertIn("selected_contextual_absolute_claim", failure_codes)
        self.assertIn("final_text_contextual_absolute_claim", failure_codes)


if __name__ == "__main__":
    unittest.main()
