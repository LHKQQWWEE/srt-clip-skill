from dataclasses import dataclass
import unittest

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


def build_synthetic_999():
    windows = [
        (1, 150, "A"), (151, 299, "B"), (300, 499, "A"),
        (500, 699, "C"), (700, 899, "B"), (900, 999, "A"),
    ]
    unique_points = {80: "A-fit", 360: "A-fabric", 974: "A-late"}
    repeats = {85: "A-fit", 365: "A-fabric"}
    cues = []
    for i in range(1, 1000):
        start = (i - 1) * 1000
        product = next(label for first, last, label in windows if first <= i <= last)
        text = unique_points.get(i) or repeats.get(i) or f"{product}-filler"
        cues.append(Cue(i, start, start + 750, product, text))
    return cues


class LongContextStress(unittest.TestCase):
    def test_long_context_uses_one_global_pool_and_per_cut_duration_plan(self):
        root = __import__("pathlib").Path(__file__).resolve().parents[1]
        long_context = (root / "references" / "long-context-mode.md").read_text(encoding="utf-8")
        policy = (root / "references" / "clip-selection-policy.md").read_text(encoding="utf-8")
        self.assertIn("全部目标窗口读完后", long_context)
        self.assertIn("跨窗口重复表达", long_context)
        self.assertIn("全局竞争", long_context)
        self.assertIn("每个所选开头", long_context)
        self.assertIn("写稿前完成首次容量优化", long_context)
        self.assertIn("90 秒是有效信息密度目标", policy)
        self.assertIn("超过 100 秒须启动专项优化并逐条复核", policy)

    def test_999_cues_across_products_deduplicate_overlap_and_keep_late_unique_point(self):
        cues = build_synthetic_999()
        chunks = chunk_with_overlap(cues, chunk_size=200, overlap=5)
        raw_occurrences = [cue.idx for chunk in chunks for cue in chunk]
        merged = {cue.idx: cue for chunk in chunks for cue in chunk}
        target_a = [cue for cue in merged.values() if cue.product == "A"]

        self.assertEqual(len(cues), 999)
        self.assertGreater(len(raw_occurrences), 999)
        self.assertEqual(len(merged), 999)
        self.assertEqual(product_windows(list(merged.values()), "A"), [(1, 150), (300, 499), (900, 999)])
        self.assertIn("A-late", [cue.text for cue in target_a])
        self.assertEqual([cue.idx for cue in target_a].count(974), 1)

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

if __name__ == "__main__":
    unittest.main()
