import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if (SCRIPTS / "srt_tools.py").is_file():
    sys.path.insert(0, str(SCRIPTS))
    import srt_tools
    preprocess_text = srt_tools.preprocess_text
else:
    srt_tools = None
    preprocess_text = None


class PreprocessTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(preprocess_text, "srt_tools.py must implement preprocess_text")

    def test_multiline_source_is_kept_verbatim_in_rows_and_compact_table(self):
        source = (
            "1\n00:00:00,000 --> 00:00:01,250\n第一行原话\n第二行原话\n\n"
            "2\n00:00:02,000 --> 00:00:02,500\n普通说明"
        )

        report = preprocess_text(source, formal_terms=[])

        self.assertEqual(report["source_type"], "srt")
        self.assertEqual(report["counts"], {"parsed_blocks": 2, "total_blocks": 2})
        self.assertEqual(report["cues"][0]["original_text"], "第一行原话\n第二行原话")
        self.assertEqual(report["compact_table"][0]["original_text"], "第一行原话\n第二行原话")
        self.assertEqual(report["cues"][0]["duration_ms"], 1250)
        self.assertEqual(report["timeline_map"][1]["gap_from_previous_ms"], 750)

    def test_malformed_block_reports_exact_lines_and_keeps_parsed_rows(self):
        source = (
            "1\n00:00:00,000 --> 00:00:00,500\n保留这句\n\n"
            "broken cue\nnot a timestamp\n\n"
            "3\n00:00:01,000 --> 00:00:01,500\n这句也保留"
        )

        report = preprocess_text(source, formal_terms=[])

        self.assertEqual(report["status"], "BLOCKED")
        self.assertEqual(report["counts"], {"parsed_blocks": 2, "total_blocks": 3})
        self.assertEqual(report["parsed_ranges"], [
            {"start_line": 1, "end_line": 3, "cue_ids": ["1"]},
            {"start_line": 8, "end_line": 10, "cue_ids": ["3"]},
        ])
        self.assertEqual(report["unparsed_ranges"][0]["start_line"], 5)
        self.assertEqual(report["unparsed_ranges"][0]["end_line"], 6)
        self.assertTrue(report["unparsed_ranges"][0]["reason"])
        self.assertEqual(report["unparsed_ranges"][0]["source_text"], "broken cue\nnot a timestamp")
        self.assertEqual([cue["id"] for cue in report["cues"]], ["1", "3"])
        self.assertIsNone(report["timeline_map"][1]["gap_from_previous_ms"])

    def test_invalid_timecode_range_is_reported_as_unparsed_not_a_crash(self):
        source = "1\n00:61:00,000 --> 00:61:01,000\n这条时间码非法"

        report = preprocess_text(source, formal_terms=[])

        self.assertEqual(report["status"], "BLOCKED")
        self.assertEqual(report["counts"], {"parsed_blocks": 0, "total_blocks": 1})
        self.assertEqual(report["unparsed_ranges"][0]["start_line"], 1)
        self.assertEqual(report["unparsed_ranges"][0]["end_line"], 3)
        self.assertIn("minutes and seconds", report["unparsed_ranges"][0]["reason"])

    def test_duplicate_decreasing_ids_and_non_positive_spans_are_failures(self):
        source = (
            "2\n00:00:00,000 --> 00:00:00,500\nfirst\n\n"
            "1\n00:00:00,500 --> 00:00:00,500\nzero\n\n"
            "01\n00:00:00,500 --> 00:00:00,400\nnegative"
        )

        report = preprocess_text(source, formal_terms=[])
        codes = {item["code"] for item in report["diagnostics"]}

        self.assertEqual(report["status"], "FAIL")
        self.assertIn("duplicate_id", codes)
        duplicate = next(item for item in report["diagnostics"] if item["code"] == "duplicate_id")
        self.assertEqual(duplicate["cue_ids"], ["1", "01"])
        self.assertIn("numbering_inversion", codes)
        self.assertGreaterEqual(sum(code == "non_positive_duration" for code in [item["code"] for item in report["diagnostics"]]), 2)

    def test_direct_term_is_not_assembled_across_adjacent_cues(self):
        source = (
            "1\n00:00:00,000 --> 00:00:00,500\n這件就是羊\n\n"
            "2\n00:00:00,500 --> 00:00:01,000\n毛含量不清\n\n"
            "3\n00:00:01,000 --> 00:00:01,500\n特殊纖維，還做了防靜電處理"
        )

        report = preprocess_text(source, formal_terms=["羊毛"])

        self.assertEqual(report["direct_hits"], [])
        self.assertEqual([row["mark"] for row in report["compact_table"]], ["", "", ""])
        self.assertEqual(report["compact_table"][2]["original_text"], "特殊纖維，還做了防靜電處理")
        self.assertEqual(report["status"], "PASS")

    def test_duration_text_rows_receive_cumulative_spans_and_row_durations(self):
        source = "4 0.250 第一条原话\n5 0.750 第二条原话"

        report = preprocess_text(source, formal_terms=[])

        self.assertEqual(report["source_type"], "duration_text")
        self.assertEqual([cue["duration_ms"] for cue in report["cues"]], [250, 750])
        self.assertEqual([row["time_range"] for row in report["compact_table"]], [
            "00:00:00.000-00:00:00.250",
            "00:00:00.250-00:00:01.000",
        ])
        self.assertEqual(report["counts"], {"parsed_blocks": 2, "total_blocks": 2})

    def test_known_pasted_text_headers_are_recorded_without_blocking_duration_rows(self):
        source = "srt文案\n\n【字幕列表】\n1 0.500 第一条原话\n2 0.250 第二条原话"

        report = preprocess_text(source, formal_terms=[])

        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["counts"], {"parsed_blocks": 2, "total_blocks": 2})
        self.assertEqual(report["recognized_header_lines"], [
            {"line": 1, "text": "srt文案"},
            {"line": 3, "text": "【字幕列表】"},
        ])
        self.assertEqual([row["time_range"] for row in report["compact_table"]], [
            "00:00:00.000-00:00:00.500",
            "00:00:00.500-00:00:00.750",
        ])

    def test_duration_text_keeps_submillisecond_precision_until_aggregate_rounding(self):
        report = preprocess_text("4 0.0005 半毫秒一\n5 0.0005 半毫秒二", formal_terms=[])

        self.assertEqual([cue["duration_ms_exact"] for cue in report["cues"]], ["0.5", "0.5"])
        self.assertEqual([row["time_range"] for row in report["compact_table"]], [
            "00:00:00.000-00:00:00.0005",
            "00:00:00.0005-00:00:00.001",
        ])

    def test_malformed_duration_row_is_blocked_and_zero_duration_fails(self):
        report = preprocess_text("1 0 正文\nthis row cannot be parsed\n3 0.250 后续原话", formal_terms=[])

        self.assertEqual(report["status"], "BLOCKED")
        self.assertEqual(report["counts"], {"parsed_blocks": 2, "total_blocks": 3})
        self.assertIn("non_positive_duration", {item["code"] for item in report["diagnostics"]})
        self.assertEqual(report["unparsed_ranges"][0]["start_line"], 2)
        self.assertEqual(report["unparsed_ranges"][0]["reason"], "expected numbered duration row: ID duration_seconds original_text")
        self.assertEqual(report["compact_table"][1]["time_range"], "位置未知")
        self.assertIsNone(report["timeline_map"][1]["start_ms"])
        self.assertIsNone(report["timeline_map"][1]["end_ms"])

    def test_cli_emits_utf8_json_and_uses_blocked_exit_code(self):
        script = SCRIPTS / "srt_tools.py"
        scratch = Path(__file__).resolve().parents[4]
        with tempfile.TemporaryDirectory(dir=scratch) as temp_dir:
            source = Path(temp_dir) / "source.srt"
            source.write_text(
                "1\n00:00:00,000 --> 00:00:00,250\n羊毛表述\n\n"
                "2\n00:00:00,500 --> 00:00:00,750\n特殊纤维，防静电\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(script), "preprocess", str(source)],
                capture_output=True,
            )
            try:
                report = json.loads(result.stdout.decode("utf-8"))
            except UnicodeDecodeError:
                self.fail("preprocess CLI output must be UTF-8 JSON")
            self.assertEqual(result.returncode, 0)
            self.assertEqual(report["direct_hits"], [{"term": "羊毛", "cue_ids": ["1"]}])
            self.assertEqual([row["mark"] for row in report["compact_table"]], ["HIT", ""])

            broken = Path(temp_dir) / "broken.srt"
            broken.write_text("1\n00:00:00,000 --> 00:00:00,250\nok\n\nbroken block\n", encoding="utf-8")
            blocked = subprocess.run(
                [sys.executable, str(script), "preprocess", str(broken)],
                capture_output=True,
            )
            try:
                blocked_report = json.loads(blocked.stdout.decode("utf-8"))
            except UnicodeDecodeError:
                self.fail("blocked preprocess report must be UTF-8 JSON")
            self.assertEqual(blocked.returncode, 2)
            self.assertEqual(blocked_report["status"], "BLOCKED")

    def test_compact_text_table_has_three_columns_and_marks_hit_in_id_cell(self):
        report = preprocess_text(
            "1\n00:00:00,000 --> 00:00:00,250\n羊毛\n\n2\n00:00:00,250 --> 00:00:00,500\n普通话",
            formal_terms=["羊毛"],
        )

        rows = report["compact_table_text"].splitlines()
        self.assertEqual(rows[0], "序号|起-止|原文")
        self.assertEqual(len(rows[1].split("|")), 3)
        self.assertTrue(rows[1].startswith("1 HIT|"))


SOURCE_WITH_GAPS = (
    "1\n00:00:00,000 --> 00:00:00,500\n主卖点\n\n"
    "2\n00:00:01,000 --> 00:00:01,500\n补充证据\n\n"
    "3\n00:00:02,000 --> 00:00:03,000\n未采用的衔接\n\n"
    "4\n00:00:04,000 --> 00:00:04,500\n适用条件"
)


class SelectionPipelineTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(srt_tools, "srt_tools.py must be importable")
        for name in ("validate_selection", "assemble_selection", "support_diff"):
            self.assertTrue(callable(getattr(srt_tools, name, None)), f"{name} must be implemented")

    def make_selection(self, source, selected_ids=("1", "2", "4"), mode="script"):
        return {
            "verification_mode": mode,
            "source_sha256": getattr(source, "source_sha256", "missing"),
            "selected_ids": list(selected_ids),
            "estimated_duration_seconds": 90,
            "content_blocks": [{"id": "body", "name": "商品信息", "cue_ids": list(selected_ids)}] if selected_ids else [],
            "selling_points": [
                {
                    "id": "P1",
                    "support_ids": ["1"],
                    "necessary_evidence_ids": ["2"],
                    "required_condition_ids": ["4"],
                }
            ],
            "roles": [
                {"cue_id": cue_id, "role": role}
                for cue_id, role in [("1", "独立卖点"), ("2", "证据"), ("4", "条件")]
                if cue_id in selected_ids
            ],
            "flags": [],
            "opening_choice": {"cue_ids": ["1"], "basis": "按当前目标顾客与素材动态判断"},
            "known_unaccelerated_ms": 150,
        }

    def test_manual_mode_reports_internal_status_without_claiming_script_gate(self):
        source = srt_tools.parse_source(SOURCE_WITH_GAPS)
        selection = self.make_selection(source, mode="manual")

        result = srt_tools.validate_selection(source, selection, formal_terms=[])

        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["verification_label"], "模型逐条对照")
        self.assertIsNone(result["machine_gate_status"])
        self.assertEqual(result["internal_status"], "PASS")

    def test_missing_source_and_unselected_point_support_fail_structural_gate(self):
        source = srt_tools.parse_source(SOURCE_WITH_GAPS)
        selection = self.make_selection(source, selected_ids=("1", "4"))
        selection["selling_points"][0]["support_ids"] = ["2", "99"]

        result = srt_tools.validate_selection(source, selection, formal_terms=[])
        codes = {item["code"] for item in result["hard_failures"]}

        self.assertEqual(result["status"], "FAIL")
        self.assertIn("support_id_not_selected", codes)
        self.assertIn("support_id_not_in_source", codes)
        self.assertEqual(result["risk_hints"], [])

    def test_source_hash_mismatch_fails_before_assembly(self):
        source = srt_tools.parse_source(SOURCE_WITH_GAPS)
        selection = self.make_selection(source)
        selection["source_sha256"] = "0" * 64

        result = srt_tools.assemble_selection(source, selection, formal_terms=[])

        self.assertFalse(result["assembled"])
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("source_hash_mismatch", {item["code"] for item in result["validation"]["hard_failures"]})

    def test_blocked_source_keeps_parsed_scope_visible(self):
        source = srt_tools.parse_source("1\n00:00:00,000 --> 00:00:00,500\n有效\n\nbad block\n")
        selection = self.make_selection(source, selected_ids=("1",))

        result = srt_tools.validate_selection(source, selection, formal_terms=["未出现的正式词"])

        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(result["analysis_started"])
        self.assertFalse(result["full_source_checked"])
        self.assertEqual(result["unparsed_ranges"], source.unparsed_ranges)
        self.assertEqual(result["direct_hits"], [])

    def test_each_selected_cue_has_exactly_one_role(self):
        source = srt_tools.parse_source(SOURCE_WITH_GAPS)
        selection = self.make_selection(source)
        selection["roles"].append({"cue_id": "1", "role": "必要衔接"})

        result = srt_tools.validate_selection(source, selection, formal_terms=[])

        self.assertEqual(result["status"], "FAIL")
        self.assertIn("role_cardinality", {item["code"] for item in result["hard_failures"]})

    def test_empty_selection_fails_structural_gate(self):
        source = srt_tools.parse_source(SOURCE_WITH_GAPS)
        selection = self.make_selection(source, selected_ids=())
        selection["selling_points"] = []
        selection["roles"] = []

        result = srt_tools.validate_selection(source, selection, formal_terms=[])

        self.assertEqual(result["status"], "FAIL")
        self.assertIn("empty_selection", {item["code"] for item in result["hard_failures"]})

    def test_direct_hit_in_selection_fails_and_nearby_risk_hint_is_only_transmitted(self):
        source_text = (
            "1\n00:00:00,000 --> 00:00:00,250\n羊毛\n\n"
            "2\n00:00:00,250 --> 00:00:00,500\n特殊纤维，防静电"
        )
        source = srt_tools.parse_source(source_text)
        selection = {
            "verification_mode": "script",
            "source_sha256": getattr(source, "source_sha256", "missing"),
            "selected_ids": ["2"],
            "estimated_duration_seconds": 90,
            "content_blocks": [{"id": "body", "name": "商品信息", "cue_ids": ["2"]}],
            "selling_points": [{"id": "P1", "support_ids": ["2"]}],
            "roles": [{"cue_id": "2", "role": "独立卖点"}],
            "flags": [{"type": "risk_hint", "cue_ids": ["2"], "note": "事实依据待核实"}],
        }

        risk_result = srt_tools.validate_selection(source, selection, formal_terms=["羊毛"])
        title_result = srt_tools.validate_selection(source, selection, formal_terms=["羊毛"], final_text="这款羊毛外套")
        selection["selected_ids"] = ["1", "2"]
        selection["content_blocks"][0]["cue_ids"] = ["1", "2"]
        selection["selling_points"][0]["support_ids"] = ["1", "2"]
        selection["roles"].append({"cue_id": "1", "role": "证据"})
        hit_result = srt_tools.validate_selection(source, selection, formal_terms=["羊毛"])

        self.assertEqual(risk_result["status"], "PASS")
        self.assertEqual(risk_result["risk_hints"], selection["flags"][:1])
        self.assertEqual(risk_result["hard_failures"], [])
        self.assertIn("final_text_direct_formal_term", {item["code"] for item in title_result["hard_failures"]})
        self.assertEqual(hit_result["status"], "FAIL")
        self.assertIn("selected_direct_formal_term", {item["code"] for item in hit_result["hard_failures"]})

    def test_flags_are_required_and_each_flag_must_match_the_contract(self):
        source = srt_tools.parse_source(SOURCE_WITH_GAPS)
        missing = self.make_selection(source)
        del missing["flags"]
        missing_result = srt_tools.validate_selection(source, missing, formal_terms=[])
        invalid_type = self.make_selection(source)
        invalid_type["flags"] = [{"type": "hard_fail", "cue_ids": ["1"], "note": "不得把风险提示升级为硬失败"}]
        invalid_type_result = srt_tools.validate_selection(source, invalid_type, formal_terms=[])
        invalid_shape = self.make_selection(source)
        invalid_shape["flags"] = [{"type": "risk_hint", "cue_ids": "1", "note": "不合法结构"}]
        invalid_shape_result = srt_tools.validate_selection(source, invalid_shape, formal_terms=[])

        self.assertIn("flags_missing", {item["code"] for item in missing_result["hard_failures"]})
        self.assertIn("invalid_flag_type", {item["code"] for item in invalid_type_result["hard_failures"]})
        self.assertIn("invalid_flag_structure", {item["code"] for item in invalid_shape_result["hard_failures"]})
        self.assertEqual(invalid_type_result["risk_hints"], [])

    def test_assembly_uses_contiguous_srt_spans_and_generates_text_and_sequence_once(self):
        source = srt_tools.parse_source(SOURCE_WITH_GAPS)
        selection = self.make_selection(source)

        result = srt_tools.assemble_selection(source, selection, formal_terms=[])
        repeated = srt_tools.assemble_selection(source, selection, formal_terms=[])

        self.assertEqual(result, repeated)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["source_sequence"], "1,2,4")
        self.assertEqual(result["body_text"], "主卖点\n补充证据\n适用条件")
        self.assertEqual(result["source_duration_ms"], 2000)
        self.assertEqual(result["playback_duration_ms"], 1817)
        self.assertEqual(result["source_duration_display"], "\u7ea6 2 \u79d2")
        self.assertEqual(result["playback_duration_display"], "\u7ea6 2 \u79d2")
        self.assertEqual([group["span_ms"] for group in result["source_groups"]], [1500, 500])

    def test_applicable_original_cta_role_is_valid_and_assembly_keeps_source_verbatim(self):
        source = srt_tools.parse_source("1 1.0 原文行动提示")
        selection = self.make_selection(source, selected_ids=("1",))
        selection["selling_points"] = []
        selection["roles"] = [{
            "cue_id": "1",
            "role": "适用促单原话",
            "cta_type": "直接行动型",
            "transaction_info": {"dynamic_items": [], "sku_list_price_verified": False},
        }]
        selection["content_blocks"] = [{"id": "promotion", "name": "促单", "cue_ids": ["1"]}]

        checked = srt_tools.validate_selection(source, selection, formal_terms=[])
        assembled = srt_tools.assemble_selection(source, selection, formal_terms=[])

        self.assertEqual(checked["status"], "PASS")
        self.assertEqual(assembled["status"], "PASS")
        self.assertEqual(assembled["body_text"], "原文行动提示")
        selection["roles"] = [{"cue_id": "1", "role": "可选行动句"}]
        legacy_role = srt_tools.validate_selection(source, selection, formal_terms=[])
        self.assertIn("invalid_role", {item["code"] for item in legacy_role["hard_failures"]})

    def test_duration_text_display_is_approximate_and_not_a_millisecond_claim(self):
        source = srt_tools.parse_source("7 0.003 一句话")
        selection = self.make_selection(source, selected_ids=("7",))
        selection["selling_points"][0]["support_ids"] = ["7"]
        selection["selling_points"][0]["necessary_evidence_ids"] = []
        selection["selling_points"][0]["required_condition_ids"] = []
        selection["roles"] = [{"cue_id": "7", "role": "独立卖点"}]
        selection["known_unaccelerated_ms"] = 0

        result = srt_tools.assemble_selection(source, selection, formal_terms=[])

        self.assertEqual(result["source_duration_ms"], 3)
        self.assertEqual(result["playback_duration_ms"], 3)
        self.assertEqual(result["playback_duration_display"], "\u7ea6 1 \u79d2\u5185")

    def test_fractional_duration_display_remains_approximate(self):
        source = srt_tools.parse_source("7 0.0005 第一句\n8 0.0005 第二句")
        selection = self.make_selection(source, selected_ids=("7", "8"))
        selection["selling_points"][0]["support_ids"] = ["7"]
        selection["selling_points"][0]["necessary_evidence_ids"] = ["8"]
        selection["selling_points"][0]["required_condition_ids"] = []
        selection["roles"] = [{"cue_id": "7", "role": "独立卖点"}, {"cue_id": "8", "role": "证据"}]
        selection["known_unaccelerated_ms"] = 0

        result = srt_tools.assemble_selection(source, selection, formal_terms=[])

        self.assertEqual(result["source_duration_ms_exact"], "1")
        self.assertEqual(result["source_duration_ms"], 1)
        self.assertEqual(result["playback_duration_ms"], 1)
        self.assertEqual(result["playback_duration_display"], "\u7ea6 1 \u79d2\u5185")

    def test_support_diff_reports_added_and_removed_ids_by_point(self):
        source = srt_tools.parse_source(SOURCE_WITH_GAPS)
        first = self.make_selection(source, selected_ids=("1", "2", "4"))
        second = self.make_selection(source, selected_ids=("1", "3", "4"))
        first["selling_points"][0]["support_ids"] = ["1", "2"]
        first["selling_points"][0]["necessary_evidence_ids"] = ["4"]
        second["selling_points"][0]["support_ids"] = ["1", "3"]
        second["selling_points"][0]["necessary_evidence_ids"] = []
        second["candidate_angle"] = "换一种完整表达角度"

        diff = srt_tools.support_diff(first, second)

        self.assertTrue(diff["same_source"])
        self.assertEqual(diff["support_changes"], [{
            "point_id": "P1",
            "added_ids": ["3"],
            "removed_ids": ["2"],
        }])
        self.assertEqual(diff["evidence_changes"], [{"point_id": "P1", "added_ids": [], "removed_ids": ["4"]}])
        self.assertEqual(diff["selected_added_ids"], ["3"])
        self.assertEqual(diff["selected_removed_ids"], ["2"])
        self.assertEqual(diff["opening_choices"], [first["opening_choice"], second["opening_choice"]])

    def test_support_diff_reports_point_pool_condition_role_and_hard_rule_changes(self):
        source = srt_tools.parse_source(SOURCE_WITH_GAPS)
        first = self.make_selection(source)
        second = self.make_selection(source)
        first["selling_points"].append({"id": "P2", "support_ids": ["2"], "necessary_evidence_ids": [], "required_condition_ids": []})
        second["selling_points"][0]["required_condition_ids"] = []
        second["selling_points"].append({"id": "P3", "support_ids": ["3"], "required_condition_ids": []})
        first["hard_rule_outcomes"] = [{"rule_id": "formal_terms", "status": "PASS"}]
        second["hard_rule_outcomes"] = [{"rule_id": "formal_terms", "status": "FAIL"}]
        second["roles"][0]["role"] = "证据"

        diff = srt_tools.support_diff(first, second)

        self.assertEqual(diff["point_pool_added_ids"], ["P3"])
        self.assertEqual(diff["point_pool_removed_ids"], ["P2"])
        self.assertEqual(diff["condition_changes"], [{"point_id": "P1", "added_ids": [], "removed_ids": ["4"]}])
        self.assertEqual(diff["role_changes"], [{"cue_id": "1", "first": "独立卖点", "second": "证据"}])
        self.assertFalse(diff["hard_rule_outcomes_stable"])
        self.assertEqual(diff["hard_rule_changes"], [{
            "rule_id": "formal_terms",
            "first": {"status": "PASS", "cue_ids": []},
            "second": {"status": "FAIL", "cue_ids": []},
        }])

    def test_support_diff_blocks_when_source_hash_changes(self):
        source = srt_tools.parse_source(SOURCE_WITH_GAPS)
        first = self.make_selection(source)
        second = self.make_selection(source)
        second["source_sha256"] = "f" * 64

        result = srt_tools.support_diff(first, second)

        self.assertEqual(result["status"], "BLOCKED")
        self.assertFalse(result["same_source"])
        self.assertTrue(result["semantic_review_required"])

    def test_support_diff_does_not_claim_rule_stability_when_no_outcomes_exist(self):
        source = srt_tools.parse_source(SOURCE_WITH_GAPS)
        first = self.make_selection(source)
        second = self.make_selection(source)
        first["hard_rule_outcomes"] = []
        second["hard_rule_outcomes"] = []

        result = srt_tools.support_diff(first, second)

        self.assertIsNone(result["hard_rule_outcomes_stable"])

    def test_selection_cli_assembles_same_input_deterministically(self):
        source_text = SOURCE_WITH_GAPS
        source = srt_tools.parse_source(source_text)
        selection = self.make_selection(source)
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[4]) as temp_dir:
            source_path = Path(temp_dir) / "source.srt"
            selection_path = Path(temp_dir) / "selection.json"
            source_path.write_text(source_text, encoding="utf-8")
            selection["source_sha256"] = hashlib.sha256(source_path.read_bytes()).hexdigest()
            selection_path.write_text(json.dumps(selection, ensure_ascii=False), encoding="utf-8")
            command = [sys.executable, str(SCRIPTS / "srt_tools.py"), "assemble", str(source_path), str(selection_path)]
            first = subprocess.run(command, capture_output=True)
            second = subprocess.run(command, capture_output=True)

            self.assertEqual(first.returncode, 0)
            self.assertEqual(first.stdout, second.stdout)
            result = json.loads(first.stdout.decode("utf-8"))
            self.assertEqual(result["source_sequence"], "1,2,4")
            self.assertEqual(result["fifth_part_sequence"], "1,2,4")
        self.assertEqual(result["playback_duration_display"], "\u7ea6 2 \u79d2")


class ReplayFixtureTests(unittest.TestCase):
    def test_synthetic_replay_passes_gate_and_produces_support_diff(self):
        fixture_dir = ROOT / "tests" / "fixtures"
        source_path = fixture_dir / "runtime-replay.srt"
        source_bytes = source_path.read_bytes()
        source = srt_tools.parse_source(
            source_bytes.decode("utf-8-sig"),
            source_sha256=hashlib.sha256(source_bytes).hexdigest(),
        )
        first = json.loads((fixture_dir / "runtime-replay-selection-a.json").read_text(encoding="utf-8"))
        second = json.loads((fixture_dir / "runtime-replay-selection-b.json").read_text(encoding="utf-8"))
        saved_diff = json.loads((fixture_dir / "runtime-replay-support-diff.json").read_text(encoding="utf-8"))

        first_gate = srt_tools.validate_selection(source, first)
        first_gate_repeat = srt_tools.validate_selection(source, first)
        second_gate = srt_tools.validate_selection(source, second)
        first_assembly = srt_tools.assemble_selection(source, first)
        first_assembly_repeat = srt_tools.assemble_selection(source, first)
        diff = srt_tools.support_diff(first, second)

        self.assertEqual(diff, saved_diff)
        self.assertEqual(first_gate["status"], "PASS")
        self.assertEqual(first_gate, first_gate_repeat)
        self.assertEqual(second_gate["status"], "PASS")
        self.assertEqual(first_gate["machine_gate_status"], "PASS")
        self.assertIsNone(second_gate["machine_gate_status"])
        self.assertEqual(first_gate["flags"], first["flags"])
        self.assertEqual(first_gate["risk_hints"], first["flags"][1:])
        self.assertNotIn("6", first["selected_ids"])
        self.assertIn("6", first_gate["direct_hits"][0]["cue_ids"])
        self.assertEqual(first_gate["hard_failures"], [])
        self.assertEqual(first_assembly, first_assembly_repeat)
        self.assertEqual(first_assembly["fifth_part_sequence"], "1,2,3,4,5")
        self.assertTrue(diff["same_source"])
        self.assertTrue(diff["hard_rule_outcomes_stable"])
        self.assertTrue(diff["sequence_order_changed"])
        self.assertEqual(diff["selected_sequences"], [["1", "2", "3", "4", "5"], ["3", "1", "2", "4", "5"]])
        self.assertEqual(diff["evidence_changes"], [{"point_id": "P1", "added_ids": [], "removed_ids": ["2"]}])
        self.assertEqual(diff["support_changes"], [{"point_id": "P1", "added_ids": ["2"], "removed_ids": []}])
        self.assertEqual(diff["opening_choices"], [first["opening_choice"], second["opening_choice"]])
        self.assertNotIn("candidate_comparison", first)
        self.assertNotIn("candidate_comparison", second)

    def test_check_and_diff_cli_commands_emit_expected_json(self):
        fixture_dir = ROOT / "tests" / "fixtures"
        source = fixture_dir / "runtime-replay.srt"
        first = fixture_dir / "runtime-replay-selection-a.json"
        second = fixture_dir / "runtime-replay-selection-b.json"
        script = SCRIPTS / "srt_tools.py"

        gate_run = subprocess.run(
            [sys.executable, str(script), "check", str(source), str(first)],
            capture_output=True,
        )
        diff_run = subprocess.run(
            [sys.executable, str(script), "diff", str(first), str(second)],
            capture_output=True,
        )

        self.assertEqual(gate_run.returncode, 0)
        self.assertEqual(diff_run.returncode, 0)
        gate = json.loads(gate_run.stdout.decode("utf-8"))
        diff = json.loads(diff_run.stdout.decode("utf-8"))
        self.assertEqual(gate["machine_gate_status"], "PASS")
        self.assertTrue(diff["same_source"])
        self.assertTrue(diff["semantic_review_required"])

if __name__ == "__main__":
    unittest.main()
