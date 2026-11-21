from dataclasses import dataclass
import json
from pathlib import Path
import unittest


SKILL_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = next(parent for parent in SKILL_ROOT.parents if (parent / "plugin.json").is_file())


def read_skill_file(relative_path):
    return (SKILL_ROOT / relative_path).read_text(encoding="utf-8")

@dataclass
class Cue:
    idx: int
    start_ms: int
    end_ms: int
    product: str
    text: str


def build_synthetic_2000():
    # 2000 cues * 3.6 seconds = exactly 2 hours.
    cues=[]
    windows=[
        (1,300,"A"),(301,550,"B"),(551,800,"A"),(801,1200,"C"),
        (1201,1500,"A"),(1501,1700,"B"),(1701,1900,"A"),(1901,2000,"C"),
    ]
    def product_for(i):
        for a,b,p in windows:
            if a <= i <= b: return p
        raise AssertionError(i)
    unique_points={120:"A-fit",620:"A-fabric",1280:"A-use",1770:"A-detail"}
    reinforcements={180:"A-fit",700:"A-fabric",1350:"A-use",1810:"A-detail"}
    for i in range(1,2001):
        start=(i-1)*3600
        p=product_for(i)
        label=unique_points.get(i) or reinforcements.get(i) or f"{p}-filler"
        cues.append(Cue(i,start,start+3000,p,label))
    return cues


def chunk_with_overlap(cues, chunk_size=500, overlap=10):
    out=[]; start=0
    while start < len(cues):
        end=min(len(cues), start+chunk_size)
        out.append(cues[start:end])
        if end == len(cues): break
        start=end-overlap
    return out


def product_windows(cues, product):
    result=[]; start=None; prev=None
    for c in cues:
        if c.product == product:
            if start is None: start=c.idx
            prev=c.idx
        elif start is not None:
            result.append((start,prev)); start=None; prev=None
    if start is not None: result.append((start,prev))
    return result


class LongContextStress(unittest.TestCase):
    def test_two_hour_2000_cues(self):
        cues=build_synthetic_2000()
        self.assertEqual(len(cues),2000)
        self.assertEqual(2000*3600,7_200_000)
        self.assertEqual(cues[-1].start_ms+3600,7_200_000)

    def test_four_discrete_target_windows_survive_chunking(self):
        cues=build_synthetic_2000()
        self.assertEqual(product_windows(cues,"A"),[(1,300),(551,800),(1201,1500),(1701,1900)])
        chunks=chunk_with_overlap(cues)
        covered={c.idx for chunk in chunks for c in chunk}
        self.assertEqual(covered,set(range(1,2001)))

    def test_unique_and_reinforcement_points_exist_across_windows(self):
        cues=build_synthetic_2000()
        a=[c for c in cues if c.product=="A"]
        labels=[c.text for c in a]
        for label in ["A-fit","A-fabric","A-use","A-detail"]:
            self.assertEqual(labels.count(label),2)

    def test_every_active_entry_requires_full_skill_and_required_rule_reads(self):
        skill = read_skill_file("SKILL.md")
        gate_heading = "## 每次触发的完整读取门禁"
        self.assertTrue(gate_heading in skill, "full-read gate is missing")
        self.assertLess(skill.index(gate_heading), skill.index("## 1. 唯一入口与版本优先级"))
        for required_reference in [
            "SKILL.md 全文",
            "references/global-rules.md",
            "references/editorial-policy.md",
            "references/highlight-selection.md",
            "references/final-check.md",
        ]:
            with self.subTest(required_reference=required_reference):
                self.assertTrue(
                    required_reference in skill[: skill.index("## 1. 唯一入口与版本优先级")],
                    f"missing required read: {required_reference}",
                )

        manifest = json.loads((PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8"))
        codex_manifest = json.loads((PLUGIN_ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        prompts = [
            manifest["extensions"]["com.openai"]["interface"]["defaultPrompt"],
            codex_manifest["interface"]["defaultPrompt"],
            read_skill_file("agents/openai.yaml"),
        ]
        for prompt in prompts:
            with self.subTest(prompt=prompt[:40]):
                self.assertTrue(
                    "完整读取当前 SKILL.md 全文" in prompt,
                    "active trigger prompt does not require the current Skill body",
                )

    def test_long_context_recovers_from_source_and_blocks_analysis_until_verified(self):
        long_context = read_skill_file("references/long-context-mode.md")
        for required_behavior in [
            "从原始附件或可访问来源",
            "自动续读",
            "动态决定分段大小",
            "原始序号、时间码和内容",
            "首尾范围",
            "序号覆盖",
            "不得要求用户回复“继续”",
            "完整读取并核验通过后",
            "不能虚构恢复缺失内容",
        ]:
            with self.subTest(required_behavior=required_behavior):
                self.assertTrue(
                    required_behavior in long_context,
                    f"missing long-context behavior: {required_behavior}",
                )

if __name__ == "__main__":
    unittest.main()
