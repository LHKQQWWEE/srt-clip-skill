import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = next(parent for parent in ROOT.parents if (parent / "plugin.json").is_file())


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def text_sha256(path):
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


class C2UniversalIntegrityTests(unittest.TestCase):
    def test_canonical_and_hidden_skill_mirrors_are_synchronized(self):
        mirror = PLUGIN / ".agents/skills/srt-clip-c2"

        def tracked_files(root):
            return {
                path.relative_to(root).as_posix(): path.read_bytes()
                for path in root.rglob("*")
                if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
            }

        self.assertEqual(tracked_files(ROOT), tracked_files(mirror))

    def test_required_sources_and_knowledge_packs_exist(self):
        for path in (
            "SKILL.md", "references/runtime-manifest.json", "references/runtime-current.md",
            "references/runtime-contract.md", "references/global-rules.md",
            "references/editorial-policy.md", "references/highlight-selection.md",
            "references/final-check.md", "scripts/srt_tools.py", "scripts/selection.schema.json",
            "tests/test_confirmed_workflow.py",
        ):
            self.assertTrue((ROOT / path).is_file(), path)
        for path in (
            "product-knowledge-packs/womens-fashion.md",
            "product-knowledge-packs/shoes.md",
            "product-knowledge-packs/scarves.md",
        ):
            self.assertTrue((ROOT / path).is_file(), path)

    def test_core_skill_plugin_and_generated_versions_are_aligned(self):
        plugin = json.loads((PLUGIN / "plugin.json").read_text(encoding="utf-8"))
        companion = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        manifest = json.loads(read("references/runtime-manifest.json"))
        self.assertEqual((PLUGIN / "VERSION").read_text(encoding="utf-8").strip(), "0.4.7")
        self.assertEqual((ROOT / "VERSION").read_text(encoding="utf-8").strip(), "0.4.41")
        self.assertEqual(plugin["version"], "0.4.41")
        self.assertEqual(companion["version"], plugin["version"])
        self.assertEqual(manifest["core_version"], "0.4.7")
        self.assertEqual(manifest["skill_version"], "0.4.41")
        self.assertIn("0.4.41", read("C2-Universal-Portable.md"))

    def test_plugin_identity_and_entry_prompts_remain_aligned(self):
        plugin = json.loads((PLUGIN / "plugin.json").read_text(encoding="utf-8"))
        companion = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        prompt = plugin["extensions"]["com.openai"]["interface"]["defaultPrompt"]
        self.assertEqual(plugin["name"], "srt-clip-c2")
        self.assertEqual(companion["name"], plugin["name"])
        self.assertEqual(plugin["skills"], "./skills")
        self.assertEqual(companion["skills"], "./skills")
        self.assertEqual(prompt, companion["interface"]["defaultPrompt"])
        self.assertEqual(prompt, read("agents/openai.yaml").split("default_prompt: ", 1)[1].strip().strip('"'))

    def test_product_then_opening_choice_and_independent_full_cuts_are_current(self):
        contract = read("references/runtime-contract.md")
        policy = read("references/clip-selection-policy.md")
        self.assertLess(contract.index("等待用户选择商品"), contract.index("确认后才为所选商品生成开头候选"))
        self.assertIn("所有达到现有质量门槛且彼此实质不同", policy)
        self.assertIn("用户最多选择 3 个候选", policy)
        self.assertIn("方案名称、开头原话、原始 SRT 序号、预估时长", policy)
        self.assertIn("不得预选", policy)
        self.assertIn("每个已选开头分别生成一条完整成片", policy)
        self.assertIn("每条常规时长方案须独立覆盖", policy)

    def test_dynamic_opening_rules_and_business_boundaries_remain(self):
        editorial = read("references/editorial-policy.md")
        final_check = read("references/final-check.md")
        self.assertIn("AI-First", read("references/runtime-contract.md"))
        self.assertIn("一个 AI", read("references/runtime-contract.md"))
        self.assertIn("动态顾客心理驱动", editorial)
        self.assertIn("开放式观看动力优先级", editorial)
        self.assertIn("候选池纳入其中全部合格候选", editorial)
        self.assertIn("不比较、评分或排名完整成片", editorial)
        self.assertIn("序号硬门", final_check)
        self.assertIn("不调用 Python、脚本或外部工具", final_check)

    def test_exact_prohibited_term_scope_and_five_part_output_remain(self):
        global_rules = read("references/global-rules.md")
        contract = read("references/runtime-contract.md")
        for term in ("羊毛", "皮草", "羊绒", "特殊动物绒", "全金纺半高领"):
            self.assertIn(term, global_rules)
        self.assertIn("不得扩大到未授权", global_rules)
        for title in ("一、文件解析结果", "二、商品识别", "三、最佳成片方案", "四、作品标题与话题", "五、原始 SRT 序号"):
            self.assertIn(title, contract)
        self.assertIn("不添加第六部分", contract)

    def test_runtime_bundle_hashes_and_source_map_are_current(self):
        manifest = json.loads(read("references/runtime-manifest.json"))
        self.assertTrue(manifest["source_map"])
        self.assertEqual(text_sha256(ROOT / manifest["runtime_file"]), manifest["runtime_sha256"])
        for source, digest in manifest["source_hashes"].items():
            self.assertEqual(text_sha256(ROOT / source), digest, source)

    def test_portable_is_generated_from_current_sources(self):
        import sys
        sys.path.insert(0, str(ROOT / "scripts"))
        import build_portable
        self.assertEqual((ROOT / "C2-Universal-Portable.md").read_text(encoding="utf-8"), build_portable.build())

    def test_update_protocol_and_tests_are_not_runtime_load_requirements(self):
        manifest = json.loads(read("references/runtime-manifest.json"))
        self.assertNotIn("references/update-protocol.md", manifest["source_files"])
        self.assertNotIn("references/update-protocol.md", manifest["required_files"])
        history = PLUGIN / "docs/history/releases"
        self.assertFalse(list(history.glob("*.md")) if history.exists() else [])


if __name__ == "__main__":
    unittest.main()
