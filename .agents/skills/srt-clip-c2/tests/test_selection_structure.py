import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import srt_tools

SOURCE = "\n".join(
    (
        "1 0.5 这条裤子的版型很利落。",
        "2 0.5 腰线提起来，显得腿更长。",
        "3 0.5 面料摸起来很柔软。",
        "4 0.5 喜欢的可以点商品卡看看。",
        "5 0.5 这款全网最好，赶快下单。",
        "6 0.5 今天优惠价 99 元，库存只剩 2 件。",
        "7 0.5 这款当前 SKU 的日常标价是 199 元。",
    )
)


def selection_for(source, selected_ids=("1", "2", "3", "4")):
    return {
        "verification_mode": "script",
        "source_sha256": source.source_sha256,
        "selected_ids": list(selected_ids),
        "estimated_duration_seconds": 90,
        "selling_points": [
            {"id": "P1", "support_ids": ["1"], "necessary_evidence_ids": ["2"], "required_condition_ids": []},
            {"id": "P2", "support_ids": ["3"], "necessary_evidence_ids": [], "required_condition_ids": []},
        ],
        "roles": [
            {"cue_id": "1", "role": "独立卖点"},
            {"cue_id": "2", "role": "证据"},
            {"cue_id": "3", "role": "独立卖点"},
            {
                "cue_id": "4",
                "role": "适用促单原话",
                "cta_type": "直接行动型",
                "transaction_info": {"dynamic_items": [], "sku_list_price_verified": False},
            },
        ],
        "content_blocks": [
            {"id": "shape", "name": "版型", "cue_ids": ["1", "2"]},
            {"id": "fabric", "name": "穿着体验", "cue_ids": ["3"]},
            {"id": "promotion", "name": "促单", "cue_ids": ["4"]},
        ],
        "flags": [],
    }


def failure_codes(selection, source=None):
    source = source or srt_tools.parse_source(SOURCE)
    result = srt_tools.validate_selection(source, selection, formal_terms=None)
    return result, {row["code"] for row in result["hard_failures"]}


class SelectionStructureTests(unittest.TestCase):
    def setUp(self):
        self.source = srt_tools.parse_source(SOURCE)
        self.selection = selection_for(self.source)

    def test_valid_product_boards_and_last_promotion_board_pass(self):
        result, codes = failure_codes(self.selection, self.source)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(codes, set())

    def test_promotion_cue_cannot_support_or_rank_as_a_selling_point(self):
        self.selection["selling_points"][0]["support_ids"] = ["1", "4"]
        _, codes = failure_codes(self.selection, self.source)
        self.assertIn("promotion_in_selling_point_support", codes)

    def test_cta_must_have_a_distinct_promotion_classification(self):
        del self.selection["roles"][3]["cta_type"]
        _, codes = failure_codes(self.selection, self.source)
        self.assertIn("promotion_classification_required", codes)

    def test_recommendation_and_purchase_confidence_cta_classification_is_supported(self):
        self.selection["roles"][3]["cta_type"] = "种草/推荐/购买信心强化型"
        result, codes = failure_codes(self.selection, self.source)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(codes, set())

    def test_promotion_block_must_be_last(self):
        blocks = self.selection["content_blocks"]
        blocks[1], blocks[2] = blocks[2], blocks[1]
        self.selection["selected_ids"] = [cue for block in blocks for cue in block["cue_ids"]]
        _, codes = failure_codes(self.selection, self.source)
        self.assertIn("promotion_not_in_last_block", codes)

    def test_selected_cues_cannot_cross_and_reenter_a_board(self):
        self.selection["content_blocks"] = [
            {"id": "shape", "name": "版型", "cue_ids": ["1"]},
            {"id": "fabric", "name": "穿着体验", "cue_ids": ["2"]},
            {"id": "shape", "name": "版型", "cue_ids": ["3"]},
            {"id": "promotion", "name": "促单", "cue_ids": ["4"]},
        ]
        _, codes = failure_codes(self.selection, self.source)
        self.assertIn("duplicate_content_block_id", codes)

    def test_dynamic_price_offer_gift_benefit_countdown_and_scarcity_are_rejected_in_cta(self):
        role = self.selection["roles"][3]
        role["transaction_info"]["dynamic_items"] = ["成交价", "优惠", "赠品", "直播福利", "倒计时", "库存/稀缺"]
        _, codes = failure_codes(self.selection, self.source)
        self.assertIn("promotion_contains_dynamic_transaction_info", codes)

    def test_verified_current_sku_list_price_is_allowed_in_body(self):
        self.selection = selection_for(self.source, selected_ids=("1", "2", "3", "7", "4"))
        self.selection["selling_points"][1]["support_ids"].append("7")
        self.selection["roles"][3:3] = [{
            "cue_id": "7",
            "role": "证据",
            "transaction_info": {"dynamic_items": [], "sku_list_price_verified": True},
        }]
        self.selection["content_blocks"][1]["cue_ids"] = ["3", "7"]
        self.selection["content_blocks"][2]["cue_ids"] = ["4"]
        result, codes = failure_codes(self.selection, self.source)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(codes, set())

    def test_absolute_product_claims_remain_blocked_inside_promotion(self):
        self.selection = selection_for(self.source, selected_ids=("1", "2", "3", "5"))
        self.selection["selling_points"][1]["support_ids"] = ["3"]
        self.selection["roles"][3] = {
            "cue_id": "5",
            "role": "适用促单原话",
            "cta_type": "直接行动型",
            "transaction_info": {"dynamic_items": [], "sku_list_price_verified": False},
        }
        self.selection["content_blocks"][2]["cue_ids"] = ["5"]
        _, codes = failure_codes(self.selection, self.source)
        self.assertIn("selected_contextual_absolute_claim", codes)

    def test_duration_over_100_seconds_requires_a_review_without_forcing_omission(self):
        self.source = srt_tools.parse_source(SOURCE.replace("1 0.5 ", "1 120 "))
        self.selection = selection_for(self.source)
        self.selection["estimated_duration_seconds"] = 101.25
        _, codes = failure_codes(self.selection, self.source)
        self.assertIn("duration_review_required", codes)
        self.selection["duration_review"] = {
            "stage": "special_optimization_over_100",
            "outcome": "retain_all",
            "review_reason": "保留全部独立理由及必要证据、条件和衔接",
            "omitted_blocks": [],
        }
        result, codes = failure_codes(self.selection, self.source)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(codes, set())


if __name__ == "__main__":
    unittest.main()
