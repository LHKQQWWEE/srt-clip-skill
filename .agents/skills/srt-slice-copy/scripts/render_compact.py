#!/usr/bin/env python3
"""C2 display only. All source/time/ID/duration validations delegated to frozen V3.0 engine."""
import argparse
import importlib.util
import json
from pathlib import Path

ENGINE = Path(__file__).resolve().parent / "srt_fast.py"
spec = importlib.util.spec_from_file_location("canonical_srt_fast", ENGINE)
v3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v3)


def rough_sec(ms: int) -> str:
    """Approximate locator, truncated to whole seconds and explicitly labeled 约."""
    sec = ms // 1000
    h, rest = divmod(sec, 3600)
    m, s = divmod(rest, 60)
    return f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def render_compact(doc: dict, plan: dict) -> str:
    verified = v3.render(doc, plan)  # raises on unverified sources, invalid groups or duration
    pre, remainder = verified.split("\n三、最佳成片方案\n", 1)
    is_text = doc.get("input_type") == "duration_text"
    if is_text:
        pre = pre.replace("\n文件名称：", "\n输入格式：逐条时长文本（无原始绝对时间码）\n文件名称：", 1)
    _, rest = remainder.split("\n四、作品标题与话题\n", 1)
    fourth, _ = rest.split("\n五、原始SRT序号（按成片播放顺序）\n", 1)
    byid = {r["id"]: r for r in doc["rows"]}
    source_ids = []
    total_ms = 0
    third = ["三、最佳成片方案", f"主推主题：{plan['theme']}"]
    for group in plan['groups']:
        selected = [byid[str(s)] for s in group['ids']]
        total_ms += max(r['end'] for r in selected) - min(r['start'] for r in selected)
    third.append(f"预计成片时长：{v3.fmt(total_ms)}")
    for number, group in enumerate(plan['groups'], 1):
        selected = [byid[str(s)] for s in group['ids']]
        source_ids += [r['id'] for r in selected]
        role = group['function'].split('｜',1)[0].strip()
        first = min(r['start'] for r in selected)
        last = max(r['end'] for r in selected)
        locator = (f"累计位置约 {rough_sec(first)}–{rough_sec(last)}（按逐条时长累加估算）"
                   if is_text else f"原SRT约 {rough_sec(first)}–{rough_sec(last)}")
        third += [f"片段{number}｜{role}",
                  f"{locator}｜序号 {v3.compress([r['id'] for r in selected])}"]
        for j,r in enumerate(selected):
            if not is_text and j and r['start']-selected[j-1]['end'] > 1000:
                third.append("【剪辑断点：前后字幕相隔超过1秒】")
            third.append(f"【{r['id']}】{r['text']}")
        third.append("")
    if plan['subtitle_notes']:
        third.append('字幕疑点提醒：'+'；'.join(x.rstrip('。； ') for x in plan['subtitle_notes'])+'。')
    serial = ','.join(source_ids)
    return '\n'.join([pre, '', '\n'.join(third).rstrip(), '',
                      '四、作品标题与话题', fourth.rstrip(), '',
                      '五、原始SRT序号（按成片播放顺序）', serial])


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--snapshot',required=True)
    p.add_argument('--plan',required=True)
    p.add_argument('--stdout',action='store_true')
    p.add_argument('--output')
    args=p.parse_args()
    if not args.stdout and not args.output:
        p.error('Use --stdout and/or --output')
    doc=json.loads(Path(args.snapshot).read_text(encoding='utf-8'))
    plan=json.loads(Path(args.plan).read_text(encoding='utf-8'))
    result=render_compact(doc,plan)
    if args.output: Path(args.output).write_text(result,encoding='utf-8')
    if args.stdout: print(result)

if __name__=='__main__':
    main()
