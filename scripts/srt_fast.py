#!/usr/bin/env python3
"""srt切片文案 V3.0 FAST-LITE-1 ACTIVE.

One SRT byte read/parse -> one compact model scan -> one author-selected plan
-> source-only checked, frozen-format delivery. This deliberately DOES NOT
claim R8 Final Gate or automated semantic verification.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

TIME_RE = re.compile(r'^(\d{2,}:\d\d:\d\d,\d{3})\s*-->\s*(\d{2,}:\d\d:\d\d,\d{3})(?:\s+.*)?$')


def ms(s):
    h,m,rest=s.split(':'); sec,milli=rest.split(',')
    if not (0 <= int(m) < 60 and 0 <= int(sec) < 60):
        raise ValueError('invalid time '+s)
    return ((int(h)*60+int(m))*60+int(sec))*1000+int(milli)


def fmt(t):
    h,t=divmod(t,3600000); m,t=divmod(t,60000); s,z=divmod(t,1000)
    return f'{h:02d}:{m:02d}:{s:02d}.{z:03d}'


def parse_once(path):
    path=Path(path)
    if path.suffix.lower()!='.srt': raise ValueError('Only SRT allowed')
    raw=path.read_bytes()   # Exactly one read, no retries.
    decoded=None
    for enc in ('utf-8-sig','gb18030'):
        try: decoded=raw.decode(enc,'strict'); break
        except UnicodeDecodeError: pass
    if decoded is None: raise ValueError('Cannot strictly decode SRT')
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
                     'start':start,'end':end,'text':'\n'.join(lines[2:])})
    return {'filename':path.name,'count':len(rows),'start':min(r['start'] for r in rows),
            'end':max(r['end'] for r in rows),'rows':rows}


def scan(doc):
    print(f"FILE={doc['filename']} | CUES={doc['count']} | SPAN={fmt(doc['end']-doc['start'])}")
    print('FORMAT: 原SRT序号|原话（完整时间码保存在本地快照）')
    for r in doc['rows']:
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


def render(doc,plan):
    expected={'groups','theme','product_lines','title','topics','subtitle_notes'}
    if not isinstance(plan,dict) or set(plan)!=expected:
        raise ValueError('Plan requires exactly '+','.join(sorted(expected)))
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
        if not isinstance(rawg,dict) or set(rawg)!={'ids','function'}:raise ValueError('group shape invalid')
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
        groups.append((n,rawg['function'],g,a,b,cumulative,cumulative+span,gap))
        cumulative+=span;selected.update(ids);all_ids.extend(ids)
    if not 45000<=cumulative<=90000:
        raise ValueError('Selected duration is outside 45–90 seconds')
    serials=','.join(all_ids)
    third=['三、最佳成片方案',f"主推主题：{plan['theme']}",f'预计成片时长：{fmt(cumulative)}']
    for n,func,g,a,b,ts,te,gap in groups:
        third.append(f"片段{n}｜{func}｜预计成片 {fmt(ts)}–{fmt(te)}｜原SRT {fmt(a)}–{fmt(b)}｜源序号 {compress([r['id'] for r in g])}｜本组未覆盖间隔 {fmt(gap)}｜SRT源字幕定位")
        third.extend(f"{r['id']} | {r['start_raw']} --> {r['end_raw']} | {r['text']}" for r in g)
    notes=plan['subtitle_notes']
    if notes:
        if not isinstance(notes,list) or not all(isinstance(x,str) for x in notes):raise ValueError('subtitle_notes must be list')
        third.append('字幕疑点提醒：'+'；'.join(notes))
    parts=[
        '一、文件解析结果',
        '文件名称：'+doc['filename'],
        f"原始字幕数量：{doc['count']}条",
        f"原素材时间范围：{fmt(doc['start'])}–{fmt(doc['end'])}",
        f"素材总跨度：{fmt(doc['end']-doc['start'])}",
        f"入选字幕：{len(all_ids)}条，{len(groups)}组",
        f"预计成片时长：{fmt(cumulative)}",
        '来源核对：PASS（仅原字幕、时间码、序号与45–90秒检查；非R8验收）',
        '', '二、商品识别', *plan['product_lines'], '', *third, '',
        '四、作品标题与话题', '作品标题：'+plan['title'],
        '作品话题：'+' '.join(s if s.startswith('#') else '#'+s for s in plan['topics']),
        '', '五、原始SRT序号（按成片播放顺序）','复制后可直接用于剪辑定位：',
        '```text',serials,'```','',''+serials]
    return '\n'.join(parts)


def main():
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest='cmd',required=True)
    scanp=sub.add_parser('scan');scanp.add_argument('srt');scanp.add_argument('--snapshot',required=True)
    rend=sub.add_parser('render');rend.add_argument('--snapshot',required=True);rend.add_argument('--plan',required=True);rend.add_argument('--save')
    args=ap.parse_args()
    try:
        if args.cmd=='scan':
            doc=parse_once(args.srt)
            Path(args.snapshot).write_text(json.dumps(doc,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
            scan(doc)
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
