import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = next(path for path in ROOT.parents if (path / "plugin.json").is_file())
MANIFEST_PATH = ROOT / "references" / "runtime-manifest.json"


def read(relative):
    return (ROOT / relative).read_text(encoding="utf-8")


class ExecutionArchitectureBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(read("references/runtime-manifest.json"))
        cls.entry = read("SKILL.md")
        cls.runtime = read("references/runtime-current.md")
        cls.editorial = read("references/editorial-policy.md")
        cls.selection = read("references/highlight-selection.md")
        cls.auditor = read("references/final-check.md")

    def test_01_entry_loads_one_compiled_runtime_body(self):
        self.assertIn("references/runtime-current.md", self.entry)
        self.assertEqual(self.manifest["required_files"], ["references/runtime-current.md"])

    def test_02_entry_stays_small(self):
        self.assertLess(len(self.entry), 1600)

    def test_03_valid_versioned_summary_is_reused_and_invalidated_on_change(self):
        self.assertIn("execution-summary.json", self.entry)
        self.assertIn("摘要有效时直接复用", self.entry)
        self.assertIn("首次运行", self.entry)
        self.assertIn("版本不匹配", self.entry)
        self.assertIn("规则文件 SHA-256", self.entry)

    def test_04_manifest_metadata_binds_the_persistent_summary(self):
        self.assertIn("运行 manifest 哈希", self.entry)
        self.assertNotIn("runtime-manifest.json", self.manifest["required_files"])

    def test_05_compiler_check_is_clean(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/build_runtime.py"), "--check"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_06_runtime_digest_matches_the_manifest(self):
        actual = hashlib.sha256((ROOT / self.manifest["runtime_file"]).read_bytes()).hexdigest()
        self.assertEqual(actual, self.manifest["runtime_sha256"])

    def test_07_all_source_files_have_matching_hashes(self):
        self.assertEqual(set(self.manifest["source_files"]), set(self.manifest["source_hashes"]))
        for relative, expected in self.manifest["source_hashes"].items():
            with self.subTest(source=relative):
                self.assertEqual(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(), expected)

    def test_08_source_map_ids_are_unique(self):
        ids = [item["rule_id"] for item in self.manifest["source_map"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_09_source_map_covers_every_nonempty_source_line(self):
        mapped = {}
        for item in self.manifest["source_map"]:
            mapped.setdefault(item["source"], set()).add(item["source_line"])
        self.assertEqual(set(mapped), set(self.manifest["source_files"]))
        for relative in self.manifest["source_files"]:
            lines = read(relative).splitlines()
            expected = {i for i, line in enumerate(lines, 1) if line.strip()}
            self.assertEqual(mapped[relative], expected, relative)

    def test_10_mapped_runtime_lines_match_their_source_lines(self):
        runtime_lines = self.runtime.splitlines()
        for item in self.manifest["source_map"]:
            source_lines = read(item["source"]).splitlines()
            self.assertEqual(
                runtime_lines[item["runtime_line"] - 1],
                source_lines[item["source_line"] - 1],
                item["rule_id"],
            )

    def test_11_long_context_rules_stay_conditional(self):
        conditional = {item["path"] for item in self.manifest["conditional_files"]}
        self.assertIn("references/long-context-mode.md", conditional)
        self.assertNotIn("references/long-context-mode.md", self.manifest["required_files"])
        self.assertNotIn("# Long Context Mode", self.runtime)

    def test_12_product_packs_stay_conditional(self):
        self.assertIn("product-knowledge-packs/*.md", [item["path"] for item in self.manifest["conditional_files"]])
        for path in (ROOT / "product-knowledge-packs").glob("*.md"):
            self.assertNotIn(path.read_text(encoding="utf-8").strip(), self.runtime)

    def test_13_development_update_protocol_is_not_always_loaded(self):
        paths = {item["path"] for item in self.manifest["conditional_files"]}
        self.assertIn("references/update-protocol.md", paths)
        self.assertNotIn("references/update-protocol.md", self.manifest["required_files"])
        self.assertNotIn("# Update Protocol", self.runtime)

    def test_14_plugin_and_launcher_prompts_are_compact_and_identical(self):
        plugin = json.loads((PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8"))
        codex = json.loads((PLUGIN_ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        prompt = plugin["extensions"]["com.openai"]["interface"]["defaultPrompt"]
        self.assertEqual(prompt, codex["interface"]["defaultPrompt"])
        self.assertIn("runtime-current.md", prompt)
        self.assertIn("execution-summary.json", prompt)
        self.assertIn("clip-selection-policy.md", prompt)
        self.assertNotIn("manifest.required_files", prompt)
        self.assertLess(len(prompt), 1000)
        self.assertIn(prompt, read("agents/openai.yaml"))

    def test_15_portable_embeds_the_compiled_runtime_and_current_prompt(self):
        build = subprocess.run(
            [sys.executable, str(ROOT / "scripts/build_portable.py")],
            capture_output=True,
            text=True,
        )
        self.assertEqual(build.returncode, 0, build.stdout + build.stderr)
        portable = read("C2-Universal-Portable.md")
        plugin = json.loads((PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8"))
        prompt = plugin["extensions"]["com.openai"]["interface"]["defaultPrompt"]
        self.assertIn(self.runtime.strip(), portable)
        self.assertIn(prompt, portable)

    def test_16_point_pool_keeps_eligibility_separate_from_dynamic_value(self):
        self.assertIn("有效性与价值排序是两个判断", self.runtime)
        self.assertIn("不得固定某些卖点永远低价值", self.runtime)
        self.assertIn("不把某类商品信息固定成高、中、低等级", self.selection)

    def test_17_opening_comparison_is_dynamic_and_never_scores_full_cuts(self):
        self.assertIn("开头比较只覆盖开头本身", self.editorial)
        self.assertIn("开放式观看动力优先级", self.editorial)
        self.assertIn("存在合格的第一优先级开头候选，必须从这些候选中动态择优", self.editorial)
        self.assertIn("只有不存在合格的第一优先级候选时，才从其他有效钩子候选中择优", self.editorial)
        self.assertIn("同一最佳钩子对多个方案都真实适用", self.editorial)
        self.assertIn("动态顾客心理驱动钩子机制", self.editorial)
        self.assertIn("不比较、评分或排名完整成片", self.editorial)
        for dimension in ["顾客问题强度", "首屏停留价值", "核心理由完整度", "全卖点承载自然度", "叙事连贯度", "购买决策效率"]:
            self.assertNotIn(dimension, self.editorial)

    def test_18_machine_gate_does_not_judge_the_398_to_400_semantic_jump(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        import srt_tools

        source = srt_tools.parse_source(
            "398 2.36 而且面料全部是做三防的工艺\n"
            "399 5.48 这个三防还不只是说你这个水啊、可乐啊啥的啊\n"
            "400 3.56 而是水、可乐、咖啡、酱油"
        )
        selection = {
            "verification_mode": "script",
            "source_sha256": source.source_sha256,
            "selected_ids": ["398", "400"],
            "selling_points": [{"id": "P1", "support_ids": ["398"], "necessary_evidence_ids": ["400"], "required_condition_ids": []}],
            "roles": [{"cue_id": "398", "role": "独立卖点"}, {"cue_id": "400", "role": "证据"}],
            "flags": [],
        }
        result = srt_tools.validate_selection(source, selection, formal_terms=[])

        self.assertEqual(result["machine_gate_status"], "PASS")
        self.assertTrue(result["semantic_review_required"])
        self.assertIn("机器不判断", self.auditor)
        self.assertIn("AI 的语义判断", self.auditor)

    def test_19_mechanical_calls_are_optional_and_grouped(self):
        self.assertIn("非日常任务前置条件", self.runtime)
        self.assertIn("最多执行一次输入预处理", self.runtime)
        self.assertIn("选段组装时一次完成", self.runtime)
        self.assertIn("工具不可用时继续处理", self.runtime)

    def test_20_final_audit_is_single_pass_and_repairs_are_local_and_bounded(self):
        self.assertIn("现有一次终检", self.runtime)
        self.assertIn("只对实际写出的成片完成一次终检", self.runtime)
        self.assertIn("同一根因最多三轮实质修复", self.runtime)
        self.assertIn("只重出受影响段落，不重写整份五部分", self.runtime)

    def test_21_compact_preprocess_keeps_each_cue_once_and_preserves_parse_gaps(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        import srt_tools

        source = (
            "1\n00:00:00,000 --> 00:00:00,500\n普通句\n\n"
            "2\n00:00:00,500 --> 00:00:01,000\n羊毛命中\n\n"
            "bad\nnot a timestamp\n\n"
            "4\n00:00:02,000 --> 00:00:02,500\n后续句"
        )
        compact = srt_tools.preprocess_text(source, formal_terms=["羊毛"], compact=True)
        legacy = srt_tools.preprocess_text(source, formal_terms=["羊毛"])

        self.assertEqual(compact["format"], "c2-preprocess-compact-v1")
        self.assertEqual(compact["status"], "BLOCKED")
        self.assertEqual(compact["counts"], legacy["counts"])
        self.assertEqual(compact["unparsed_ranges"], legacy["unparsed_ranges"])
        self.assertEqual(compact["direct_hits"], legacy["direct_hits"])
        self.assertEqual([row["original_text"] for row in compact["rows"]], [cue["original_text"] for cue in legacy["cues"]])
        self.assertEqual([row["mark"] for row in compact["rows"]], ["", "HIT", ""])
        self.assertEqual([item["cue_count"] for item in compact["parsed_ranges"]], [2, 1])
        self.assertEqual(compact["parsed_ranges"][0]["cue_id_start"], "1")
        self.assertEqual(compact["parsed_ranges"][0]["cue_id_end"], "2")
        self.assertFalse(any(key in compact for key in ("cues", "compact_table", "timeline_map", "window_map_support")))

    def test_22_compact_cli_reduces_redundant_output_without_losing_source_rows(self):
        script = ROOT / "scripts" / "srt_tools.py"
        scratch = ROOT.parents[3]
        with tempfile.TemporaryDirectory(dir=scratch) as temp_dir:
            source = Path(temp_dir) / "source.txt"
            source.write_text("\n".join(f"{i} 0.250 第{i}条原始字幕" for i in range(1, 101)), encoding="utf-8")
            legacy = subprocess.run(
                [sys.executable, str(script), "preprocess", str(source)], capture_output=True, check=False
            )
            compact = subprocess.run(
                [sys.executable, str(script), "preprocess", str(source), "--compact"], capture_output=True, check=False
            )
            legacy_report = json.loads(legacy.stdout.decode("utf-8"))
            compact_report = json.loads(compact.stdout.decode("utf-8"))

        self.assertEqual(legacy.returncode, 0)
        self.assertEqual(compact.returncode, 0)
        self.assertEqual(len(compact_report["rows"]), 100)
        self.assertEqual(compact_report["rows"][-1]["original_text"], "第100条原始字幕")
        self.assertEqual(compact_report["counts"], legacy_report["counts"])
        self.assertLess(len(compact.stdout), len(legacy.stdout) * 0.7)


if __name__ == "__main__":
    unittest.main()
