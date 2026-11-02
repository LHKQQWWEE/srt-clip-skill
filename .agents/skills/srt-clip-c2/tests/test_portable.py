#!/usr/bin/env python3
"""Synthetic fixture only: verify C2 distribution with no external source dependence."""
from pathlib import Path
import tempfile, subprocess, json, importlib.util

ROOT=Path(__file__).resolve().parents[1]
src=ROOT/'scripts/srt_fast.py'
rend=ROOT/'scripts/render_compact.py'

def call(*args):
    p=subprocess.run(['python','-S',*map(str,args)],capture_output=True,text=True,encoding='utf-8')
    if p.returncode:raise AssertionError(f'command failed: {args}: {p.stderr}')
    return p.stdout

count=0
def check(cond,label):
    global count
    assert cond,label
    count+=1

with tempfile.TemporaryDirectory(prefix='c2_skill_') as t:
    t=Path(t); input_file=t/'synthetic.srt'; session=t/'snapshot.json'; plan=t/'plan.json'; output=t/'output.txt'
    rows=[]
    for i in range(12):
        beg=i*5000
        def tm(ms):
            hr,ms=divmod(ms,3600000);minute,ms=divmod(ms,60000);sec,mil=divmod(ms,1000)
            return f'{hr:02d}:{minute:02d}:{sec:02d},{mil:03d}'
        line=('轻薄透气，适合夏季使用' if i<6 else '根据实际尺码选购，喜欢可以下单')
        if i==2:line='保留原字幕第一行\n保留原字幕第二行'
        rows.append(f'{i+1}\n{tm(beg)} --> {tm(beg+4900)}\n{line}')
    input_file.write_text('\n\n'.join(rows)+'\n',encoding='utf-8')
    scan=call(src,'scan',input_file,'--snapshot',session)
    check('CUES=12' in scan,'scan count')
    check(session.exists(),'snapshot exists')
    snap=json.loads(session.read_text(encoding='utf-8'))
    check(snap['rows'][2]['text']=='保留原字幕第一行\n保留原字幕第二行','multiline preserved')
    payload={'groups':[{'ids':[1,2,3,4,5,6],'function':'开头钩子｜合成样例'},{'ids':[7,8,9,10,11,12],'function':'结尾促单｜合成样例'}], 'theme':'合成标题', 'product_lines':['合成商品讲解窗口：00:00:00.000–00:00:59.900'], 'title':'合成标题', 'topics':['合成话题甲','合成话题乙','合成话题丙'], 'subtitle_notes':[]}
    plan.write_text(json.dumps(payload,ensure_ascii=False),encoding='utf-8')
    txt=call(rend,'--snapshot',session,'--plan',plan,'--stdout')
    check(all(f'{i}、' in txt for i in ['一','二','三','四','五']),'5 sections')
    check('【3】保留原字幕第一行\n保留原字幕第二行' in txt,'source exact multiline')
    check('原SRT约 00:00–00:29｜序号 1–6' in txt,'coarse group locator')
    check('预计成片时长：00:00:59.800' in txt,'cumulative duration')
    check(txt.strip().endswith('1,2,3,4,5,6,7,8,9,10,11,12'),'last line ids')
    check('00:00:00,000 --> 00:00:04,900' not in txt,'no repeated full cue timestamps')
    check('成片 00:00.000' not in txt,'no per-group timecode')
    check(txt.count('1,2,3,4,5,6,7,8,9,10,11,12')==1,'no duplicated serials')
    check('【剪辑断点' not in txt,'synthetic contiguous input no misleading gap')
    call(rend,'--snapshot',session,'--plan',plan,'--output',output)
    check(output.read_text(encoding='utf-8')==txt.rstrip('\n'),'output bytes match stdout except newline')
    bad=dict(payload);bad['groups']=[{'ids':[1,2,3,4,5,6],'function':'1'},{'ids':[6,7,8,9,10,11,12],'function':'2'}]
    plan.write_text(json.dumps(bad,ensure_ascii=False),encoding='utf-8')
    reject=subprocess.run(['python','-S',str(rend),'--snapshot',str(session),'--plan',str(plan),'--stdout'],capture_output=True,text=True)
    check(reject.returncode!=0,'duplicates blocked')
    bad=dict(payload);bad['groups']=[{'ids':[1,2,3],'function':'too short'}]
    plan.write_text(json.dumps(bad,ensure_ascii=False),encoding='utf-8')
    reject=subprocess.run(['python','-S',str(rend),'--snapshot',str(session),'--plan',str(plan),'--stdout'],capture_output=True,text=True)
    check(reject.returncode!=0,'duration blocked')
print(f'{count}/{count} portable tests PASS')
