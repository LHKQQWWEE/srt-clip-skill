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
    check('原始选段时长（1.0倍）：00:00:59.800' in txt,'source duration')
    check('预计1.2倍速成片时长：00:00:49.833' in txt,'1.2x final duration')
    check(txt.strip().endswith('1,2,3,4,5,6,7,8,9,10,11,12'),'last line ids')
    check('00:00:00,000 --> 00:00:04,900' not in txt,'no repeated full cue timestamps')
    check('成片 00:00.000' not in txt,'no per-group timecode')
    check(txt.count('1,2,3,4,5,6,7,8,9,10,11,12')==1,'no duplicated serials')
    check('【剪辑断点' not in txt,'synthetic contiguous input no misleading gap')
    spec=importlib.util.spec_from_file_location('final_check',ROOT/'scripts/check_final.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    check(mod.check(txt,payload),'final check accepts valid answer')
    serial='1,2,3,4,5,6,7,8,9,10,11,12'
    for broken in [serial.replace(',', '、'),serial.replace(',', '，'),serial.replace(',', ', ',1),serial.replace('1,2,','2,1,',1),serial.replace('1,2,','1,',1),serial+',12',serial+'\nextra']:
        try: mod.check(txt.rstrip('\n')[:-len(serial)]+broken,payload)
        except ValueError: check(True,'bad final serial rejected')
        else: raise AssertionError('bad final serial accepted')
    try: mod.check(txt.replace('【1】','【2】',1),payload)
    except ValueError: check(True,'third section mismatch rejected')
    else: raise AssertionError('third section mismatch accepted')
    call(rend,'--snapshot',session,'--plan',plan,'--output',output)
    check(output.read_text(encoding='utf-8')==txt.rstrip('\n'),'output bytes match stdout except newline')
    bad=dict(payload);bad['groups']=[{'ids':[1,2,3,4,5,6],'function':'1'},{'ids':[6,7,8,9,10,11,12],'function':'2'}]
    plan.write_text(json.dumps(bad,ensure_ascii=False),encoding='utf-8')
    reject=subprocess.run(['python','-S',str(rend),'--snapshot',str(session),'--plan',str(plan),'--stdout'],capture_output=True,text=True,encoding="utf-8")
    check(reject.returncode!=0,'duplicates blocked')
    bad=dict(payload);bad['groups']=[{'ids':[1,2,3],'function':'too short'}]
    plan.write_text(json.dumps(bad,ensure_ascii=False),encoding='utf-8')
    reject=subprocess.run(['python','-S',str(rend),'--snapshot',str(session),'--plan',str(plan),'--stdout'],capture_output=True,text=True,encoding="utf-8")
    check(reject.returncode!=0,'duration blocked')
    short=call(rend,'--snapshot',session,'--plan',plan,'--stdout','--allow-short-report')
    check('三、素材不足候选，非正式成片' in short and '时长未达45秒' in short,'short report clearly labelled')
    check('来源核对：PASS' not in short and '【1】' in short,'short report verifies sources without claiming duration passed')

    # Pasted duration-text mode uses the same snapshot and renderer, while the
    # cumulative positions remain explicitly labeled as estimates.
    text_file=t/'pasted.txt'; text_session=t/'text_snapshot.json'; text_plan=t/'text_plan.json'
    phrases=['轻薄透气，适合夏季使用' if i<6 else '根据实际尺码选购，喜欢可以下单' for i in range(12)]
    phrases[2]='保留原话：1,000单、3+1、79块9、1.4s'
    source='\n'.join(f'{i+1} 5.0s {phrases[i]}' for i in range(12))+'\n'
    text_file.write_text(source,encoding='utf-8')
    text_scan=call(src,'scan-text',text_file,'--snapshot',text_session)
    text_doc=json.loads(text_session.read_text(encoding='utf-8'))
    check(text_doc['input_type']=='duration_text','text input type')
    check(text_doc['count']==12 and text_doc['end']==60000,'text count and duration sum')
    check(text_doc['rows'][2]['text']==phrases[2],'text source exact including numeric phrases')
    check(text_doc['rows'][6]['start']==30000 and text_doc['rows'][11]['end']==60000,'text cumulative positions')
    check('非原始绝对视频时间' in text_scan and '3+1、79块9、1.4s' in text_scan,'scan labels estimates and preserves transcript')
    text_payload=dict(payload)
    text_payload['product_lines']=['合成商品讲解窗口：累计位置约00:00–01:00']
    text_plan.write_text(json.dumps(text_payload,ensure_ascii=False),encoding='utf-8')
    text_out=call(rend,'--snapshot',text_session,'--plan',text_plan,'--stdout')
    check('输入格式：逐条时长文本（无原始绝对时间码）' in text_out,'text format declared')
    check('累计位置约 00:00–00:30（按逐条时长累加估算）' in text_out,'first estimated locator')
    check('累计位置约 00:30–01:00（按逐条时长累加估算）' in text_out,'second estimated locator')
    check('原SRT约' not in text_out and '00:00:00,000 -->' not in text_out,'no false absolute SRT timestamps')
    check(f'【3】{phrases[2]}' in text_out,'render exact source words')
    check(text_out.strip().endswith('1,2,3,4,5,6,7,8,9,10,11,12'),'text output final source IDs')
    stdin_scan=subprocess.run(['python','-S',str(src),'scan-text','--stdin','--snapshot',str(t/'stdin.json')],
                              input=source,capture_output=True,text=True,encoding='utf-8')
    check(stdin_scan.returncode==0 and json.loads((t/'stdin.json').read_text(encoding='utf-8'))['count']==12,
          'stdin text input')
    for invalid,label,needle in [
        ('1 1.0s ok\nnot a cue\n','malformed row','line 2'),
        ('1 1.0s first\n01 1.0s duplicate\n','duplicate numeric ID','line 2'),
        ('1 0.000s zero\n','zero duration','line 1'),
        ('1 0.1234s too precise\n','submillisecond precision','line 1'),
    ]:
        bad_text=t/'invalid.txt';bad_text.write_text(invalid,encoding='utf-8')
        rejected=subprocess.run(['python','-S',str(src),'scan-text',str(bad_text),'--snapshot',str(t/'invalid.json')],
                               capture_output=True,text=True,encoding='utf-8')
        check(rejected.returncode!=0 and needle in rejected.stderr,label)
print(f'{count}/{count} portable tests PASS')
