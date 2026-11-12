#!/usr/bin/env python3
"""srt-clip-c2 C2 0.2.16 source and duration checker.

One SRT byte read/parse -> one compact model scan -> one author-selected plan
-> source-only checked, frozen-format delivery. This deliberately DOES NOT
claim R8 Final Gate or automated semantic verification.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

TIME_RE = re.compile(r'^(\d{2,}:\d\d:\d\d,\d{3})\s*-->\s*(\d{2,}:\d\d:\d\d,\d{3})(?:\s+.*)?$')
DURATION_LINE_RE = re.compile(r'^[ \t]*(?P<id>\d+)[ \t]+(?P<duration>\d+(?:\.\d+)?)(?:s)?[ \t]+(?P<text>\S.*)$')


def ms(s):
    h,m,rest=s.split(':'); sec,milli=rest.split(',')
    if not (0 <= int(m) < 60 and 0 <= int(sec) < 60):
        raise ValueError('invalid time '+s)
    return ((int(h)*60+int(m))*60+int(sec))*1000+int(milli)


def fmt(t):
    h,t=divmod(t,3600000); m,t=divmod(t,60000); s,z=divmod(t,1000)
    return f'{h:02d}:{m:02d}:{s:02d}.{z:03d}'


def after_1_2x(source_ms):
    """Convert source-speed milliseconds to 1.2x runtime, half-up to 1 ms."""
    return (source_ms * 5 + 3) // 6


def srt_time(t):
    h,t=divmod(t,3600000); m,t=divmod(t,60000); s,z=divmod(t,1000)
    return f'{h:02d}:{m:02d}:{s:02d},{z:03d}'


def decode_bytes(raw, label):
    for enc in ('utf-8-sig','gb18030'):
        try: return raw.decode(enc,'strict')
        except UnicodeDecodeError: pass
    raise ValueError(f'Cannot strictly decode {label}')


def parse_once(path):
    path=Path(path)
    if path.suffix.lower()!='.srt': raise ValueError('Only SRT allowed')
    raw=path.read_bytes()   # Exactly one read, no retries.
    decoded=decode_bytes(raw,'SRT')
    blocks=re.split(r'\n[ \t]*\n+', decoded.replace('\r\n','\n').replace('\r','\n').strip('\n'))
    if not blocks or not blocks[0].strip(): raise ValueError('Empty SRT')
    rows=[]; ids=set()
    for ordinal,block in enumerate(blocks,1):
        lines=block.split('\n')
        if len(lines)<3 or not re.fullmatch(r'\d+',lines[0].strip()):
            raise ValueError(f'Invalid SRT block {ordinal}')
        mt=TIME_RE.fullmatch(lines[1])
        if not mt: raise ValueError(f'Invalid SRT time at {ordinal}')
        sid=lines[0].strip()
        if sid in ids: raise ValueError(f'Duplicate source number {sid}: manual disambiguation required')
        ids.add(sid)
        start,end=ms(mt[1]),ms(mt[2])
        if end<=start: raise ValueError(f'Nonpositive source cue at {ordinal}')
        rows.append({'ord':ordinal,'id':sid,'start_raw':mt[1], 'end_raw':mt[2],
                     'start':start,'end':end,'duration_ms':end-start,
                     'duration_raw':fmt(end-start),'text':'\n'.join(lines[2:])})
    return {'input_type':'srt','filename':path.name,'count':len(rows),'start':min(r['start'] for r in rows),
            'end':max(r['end'] for r in rows),'rows':rows}


def parse_duration_text(text, filename='<pasted text>'):
    """Parse one record per line: source ID, per-cue seconds, and exact text."""
    rows=[]; ids=set(); elapsed=0; record=0
    for line_no,line in enumerate(text.splitlines(),1):
        if not line.strip(): continue
        match=DURATION_LINE_RE.fullmatch(line)
        if not match:
            if record==0 and line.strip() in {'切片文案','srt文案','srt切片文案','str文案','C2完整精简版','【字幕列表】'}:
                continue
            raise ValueError(f'Invalid duration-text record at line {line_no}; expected "ID 0.8[s] transcript" (s suffix optional)')
        sid=match['id']; numeric_id=int(sid)
        if numeric_id<=0:
            raise ValueError(f'Source number must be positive at line {line_no}')
        if numeric_id in ids:
            raise ValueError(f'Duplicate source number {sid} at line {line_no}')
        ids.add(numeric_id)
        try: duration=Decimal(match['duration'])
        except InvalidOperation:
            raise ValueError(f'Invalid duration at line {line_no}') from None
        if duration.as_tuple().exponent < -3:
            raise ValueError(f'Duration has more than millisecond precision at line {line_no}')
        duration_ms=int(duration*1000)
        if duration_ms<=0:
            raise ValueError(f'Nonpositive duration at line {line_no}')
        start=elapsed; end=start+duration_ms; elapsed=end; record+=1
        rows.append({'ord':record,'id':sid,'start_raw':srt_time(start),'end_raw':srt_time(end),
                     'start':start,'end':end,'duration_ms':duration_ms,
                     'duration_raw':match['duration']+'s','text':match['text']})
    if not rows: raise ValueError('Empty duration-text input')
    return {'input_type':'duration_text','filename':filename,'count':len(rows),
            'start':0,'end':elapsed,'rows':rows}


def scan(doc):
    if doc.get('input_type')=='duration_text':
        print(f"FILE={doc['filename']} | CUES={doc['count']} | SUM_OF_CUE_DURATIONS_AT_SOURCE_SPEED_1.0X={fmt(doc['end'])}")
        print('FORMAT: 逐条时长文本；原素材1.0倍下的未缩放累计位置约（只累加字幕时长，不含字幕间隔，非原始绝对视频时间）|本条原素材时长|原话')
        for r in doc['rows']:
            sec=r['start']//1000; h,rest=divmod(sec,3600); m,s=divmod(rest,60)
            locator=f'{h:02d}:{m:02d}:{s:02d}' if h else f'{m:02d}:{s:02d}'
            print(f"{r['id']}@{locator}|{r['duration_raw']}|{r['text'].replace(chr(10),' / ')}")
        return
    print(f"FILE={doc['filename']} | CUES={doc['count']} | SPAN={fmt(doc['end']-doc['start'])}")
    print('FORMAT: 原SRT序号|原话（完整时间码保存在本地快照）')
    for r in doc['rows']:
        print(f"{r['id']}|{r['text'].replace(chr(10),' / ')}")


def scan_summary(doc, snapshot_path):
    """Print parse metadata only; the full parsed source remains in the snapshot."""
    total=fmt(doc['end']-doc['start'])
    label = 'SOURCE_DURATION_SUM' if doc.get('input_type') == 'duration_text' else 'SOURCE_SPAN'
    print(f"FILE={doc['filename']} | CUES={doc['count']} | {label}={total} | PARSE=PASS | SNAPSHOT={snapshot_path}")
    print('NOTE=complete rows are saved in the snapshot; this summary does not verify semantic quality')


def scan_page(doc, offset, limit):
    """Print a page from an existing snapshot without rereading the source."""
    if offset < 0 or limit <= 0:
        raise ValueError('Page offset must be nonnegative and limit must be positive')
    rows=doc['rows'][offset:offset+limit]
    if not rows:
        raise ValueError('Requested page is outside the snapshot')
    print(f"ROWS={offset+1}-{offset+len(rows)} OF {doc['count']}")
    if doc.get('input_type')=='duration_text':
        print('FORMAT: 逐条时长文本；原素材1.0倍下的未缩放累计位置约|本条原素材时长|原话')
        for r in rows:
            sec=r['start']//1000; h,rest=divmod(sec,3600); m,s=divmod(rest,60)
            locator=f'{h:02d}:{m:02d}:{s:02d}' if h else f'{m:02d}:{s:02d}'
            print(f"{r['id']}@{locator}|{r['duration_raw']}|{r['text'].replace(chr(10),' / ')}")
    else:
        print('FORMAT: 原SRT序号|原话')
        for r in rows:
            print(f"{r['id']}|{r['text'].replace(chr(10),' / ')}")


def compress(ids):
    out=[]; p=0
    while p<len(ids):
        q=p
        while q+1<len(ids) and int(ids[q+1])==int(ids[q])+1 and len(ids[q+1])==len(ids[p]):q+=1
        out.append(ids[p]+'–'+ids[q] if q>p else ids[p]); p=q+1
    return ','.join(out)


def covered(rows):
    iv=sorted((r['start'],r['end']) for r in rows)
    if not iv:return 0
    lo,hi=iv[0]; total=0
    for a,b in iv[1:]:
        if a>hi:total+=hi-lo;lo,hi=a,b
        else:hi=max(hi,b)
    return total+hi-lo


def render(doc,plan,allow_short_report=False):
    expected={'groups','theme','product_lines','title','topics','subtitle_notes'}
    if not isinstance(plan,dict) or not expected <= set(plan) or set(plan)-expected-{'unaccelerated_ms'}:
        raise ValueError('Plan requires exactly '+','.join(sorted(expected)))
    extra_ms = plan.get('unaccelerated_ms', 0)
    if not isinstance(extra_ms, int) or isinstance(extra_ms, bool) or extra_ms < 0:
        raise ValueError('unaccelerated_ms must be a nonnegative integer')
    if not isinstance(plan['groups'],list) or not plan['groups']:
        raise ValueError('No selected groups')
    if not all(isinstance(v,str) and v.strip() for v in [plan['theme'],plan['title']]):
        raise ValueError('Theme/title is empty')
    if not isinstance(plan['product_lines'],list) or not plan['product_lines'] or not all(isinstance(x,str) and x.strip() for x in plan['product_lines']):
        raise ValueError('Product identification missing')
    if not isinstance(plan['topics'],list) or len(plan['topics'])!=3 or not all(isinstance(x,str) and x.strip() for x in plan['topics']):
        raise ValueError('Exactly three topics required')
    byid={r['id']:r for r in doc['rows']}
    selected=set(); groups=[]; cumulative=0; windows=[]; all_ids=[]
    for n,rawg in enumerate(plan['groups'],1):
        if not isinstance(rawg,dict) or not {'ids','function'} <= set(rawg) or set(rawg)-{'ids','function','note'}:raise ValueError('group shape invalid')
        if 'note' in rawg and (not isinstance(rawg['note'],str) or not rawg['note'].strip()):raise ValueError('group note must be nonempty text')
        ids=[str(i) for i in rawg['ids']]
        if not ids or not isinstance(rawg['function'],str) or not rawg['function'].strip():raise ValueError('invalid group')
        if any(i not in byid for i in ids):raise ValueError('Selected ID absent from original SRT')
        if any(i in selected for i in ids):raise ValueError('Repeated selected source ID')
        g=[byid[i] for i in ids]
        if any(b['ord']!=a['ord']+1 for a,b in zip(g,g[1:])):
            raise ValueError('A group must contain consecutive original cues')
        if any(b['start']<a['start'] for a,b in zip(g,g[1:])):
            raise ValueError('Selected source timestamps reversed')
        a=min(x['start'] for x in g);b=max(x['end'] for x in g)
        for c,d in windows:
            if min(b,d)>max(a,c):raise ValueError('Overlap between original source groups')
        windows.append((a,b)); span=b-a; gap=span-covered(g)
        raw_start=cumulative; raw_end=cumulative+span
        groups.append((n,rawg['function'],g,a,b,raw_start,raw_end,gap))
        cumulative+=span;selected.update(ids);all_ids.extend(ids)
    final_ms=after_1_2x(cumulative)+extra_ms
    short_report = allow_short_report and 0 < final_ms <= 30000
    if final_ms <= 30000 and not short_report:
        raise ValueError('Estimated 1.2x final duration must be greater than 30 seconds unless short report is enabled')
    serials=','.join(all_ids)
    is_text=doc.get('input_type')=='duration_text'
    third=['三、最佳成片方案',f"主推主题：{plan['theme']}",f'原始选段时长（1.0倍）：{fmt(cumulative)}',f'预计1.2倍速成片时长：{fmt(final_ms)}']
    for n,func,g,a,b,raw_ts,raw_te,gap in groups:
        ts=after_1_2x(raw_ts); te=after_1_2x(raw_te)
        if is_text:
            third.append(f"片段{n}｜{func}｜原素材累计位置约 {fmt(a)}–{fmt(b)}（1.0倍，未缩放）｜源序号 {compress([r['id'] for r in g])}｜逐条时长文本定位（无原始绝对时间码）")
            third.extend(f"{r['id']} | {r['duration_raw']} | {r['text']}" for r in g)
        else:
            third.append(f"片段{n}｜{func}｜预计1.2倍速成片 {fmt(ts)}–{fmt(te)}｜原SRT位置（1.0倍）{fmt(a)}–{fmt(b)}｜源序号 {compress([r['id'] for r in g])}｜本组未覆盖间隔 {fmt(gap)}｜SRT源字幕定位")
            third.extend(f"{r['id']} | {r['start_raw']} --> {r['end_raw']} | {r['text']}" for r in g)
    notes=plan['subtitle_notes']
    if notes:
        if not isinstance(notes,list) or not all(isinstance(x,str) for x in notes):raise ValueError('subtitle_notes must be list')
        third.append('字幕疑点提醒：'+'；'.join(notes))
    parts=[
        '一、文件解析结果',
        '文件名称：'+doc['filename'],
        f"原始字幕数量：{doc['count']}条",
        (f"累计时长范围（估算）：{fmt(doc['start'])}–{fmt(doc['end'])}" if is_text else f"原素材时间范围：{fmt(doc['start'])}–{fmt(doc['end'])}"),
        (f"逐条时长合计：{fmt(doc['end']-doc['start'])}（未含字幕间隔）" if is_text else f"素材总跨度：{fmt(doc['end']-doc['start'])}"),
        f"入选字幕：{len(all_ids)}条，{len(groups)}组",
        f"原始选段时长（1.0倍）：{fmt(cumulative)}",
        f"预计1.2倍速成片时长：{fmt(final_ms)}",
        ('时长不超过30秒：短候选，非正式成片；来源结构核对通过，不代表语义、合规或音画通过' if short_report else (('素材不足45秒：大于30秒的完整方案，需说明原因；' if final_ms < 45000 else '') + ('来源核对：PASS（仅原话、原编号、逐条时长与1.2倍速后时长分级检查；累计位置为估算，不是原始视频时间码）' if is_text else '来源核对：PASS（仅原字幕、时间码、序号与1.2倍速后时长分级检查）'))),
        '', '二、商品识别', *plan['product_lines'], '', *third, '',
        '四、作品标题与话题', '作品标题：'+plan['title'],
        '作品话题：'+' '.join(s if s.startswith('#') else '#'+s for s in plan['topics']),
        '', '五、原始SRT序号（按成片播放顺序）','复制后可直接用于剪辑定位：',
        '```text',serials,'```','',''+serials]
    return '\n'.join(parts)


def main():
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest='cmd',required=True)
    scanp=sub.add_parser('scan');scanp.add_argument('srt');scanp.add_argument('--snapshot',required=True);scanp.add_argument('--summary',action='store_true')
    textp=sub.add_parser('scan-text');text_source=textp.add_mutually_exclusive_group(required=True)
    text_source.add_argument('text_file',nargs='?');text_source.add_argument('--stdin',action='store_true')
    textp.add_argument('--snapshot',required=True);textp.add_argument('--summary',action='store_true',help='Print metadata only after parsing and saving the complete snapshot')
    pagep=sub.add_parser('page');pagep.add_argument('--snapshot',required=True)
    pagep.add_argument('--offset',type=int,default=0);pagep.add_argument('--limit',type=int,required=True)
    rend=sub.add_parser('render');rend.add_argument('--snapshot',required=True);rend.add_argument('--plan',required=True);rend.add_argument('--save')
    args=ap.parse_args()
    try:
        if args.cmd=='scan':
            doc=parse_once(args.srt)
            Path(args.snapshot).write_text(json.dumps(doc,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
            scan_summary(doc,args.snapshot) if args.summary else scan(doc)
        elif args.cmd=='scan-text':
            if args.stdin:
                source=sys.stdin.read();filename='<stdin>'
            else:
                path=Path(args.text_file);source=decode_bytes(path.read_bytes(),'duration text');filename=path.name
            doc=parse_duration_text(source,filename)
            Path(args.snapshot).write_text(json.dumps(doc,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
            scan_summary(doc,args.snapshot) if args.summary else scan(doc)
        elif args.cmd=='page':
            doc=json.loads(Path(args.snapshot).read_text(encoding='utf-8'))
            scan_page(doc,args.offset,args.limit)
        else:
            doc=json.loads(Path(args.snapshot).read_text(encoding='utf-8'))
            plan=json.loads(Path(args.plan).read_text(encoding='utf-8'))
            text=render(doc,plan)
            if args.save:Path(args.save).write_text(text,encoding='utf-8')
            print(text)
    except (ValueError,KeyError,TypeError) as e:
        print('FAST-LITE blocked: '+str(e),file=sys.stderr)
        return 2
    return 0

if __name__=='__main__':raise SystemExit(main())
