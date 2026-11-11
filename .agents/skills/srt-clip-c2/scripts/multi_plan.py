#!/usr/bin/env python3
"""Render and check one C2 plan against one snapshot."""
import argparse
import json
import re
from pathlib import Path
from render_compact import render_compact

NAMES = ['一', '二', '三']
SERIAL = r'[1-9][0-9]*(?:,[1-9][0-9]*)*'

def ids_for(plan):
    ids = [str(i) for g in plan['groups'] for i in g['ids']]
    if not ids or any(not re.fullmatch(r'[1-9][0-9]*', x) for x in ids) or len(set(ids)) != len(ids):
        raise ValueError('invalid or duplicate IDs within a plan')
    return ids

def check_multi(answer, plans):
    if len(plans) != 1:
        raise ValueError('expected exactly one plan')
    expected = [ids_for(p) for p in plans]
    try:
        third = answer.split('三、', 1)[1].split('四、', 1)[0]
        fifth = answer.split('五、', 1)[1]
    except IndexError:
        raise ValueError('missing section')
    sections = re.split(r'(?m)^方案([一二三])(?:｜[^\n]*)?\s*$', third)
    if len(sections) != 1 + 2 * len(plans):
        raise ValueError('wrong plan section count')
    for i, ids in enumerate(expected):
        if sections[1+2*i] != NAMES[i] or re.findall(r'【([1-9][0-9]*)】', sections[2+2*i]) != ids:
            raise ValueError('third section plan order or IDs differ')
    match = re.search(r'```(?:text)?\r?\n([\s\S]*?)\r?\n```\s*$', fifth)
    if not match:
        raise ValueError('missing final fenced serial block')
    entries = re.split(r'\r?\n\r?\n', match.group(1))
    if len(entries) != len(expected) or any(not re.fullmatch(SERIAL, e) for e in entries):
        raise ValueError('serial block must contain one pure ID line per plan separated by blank lines')
    if [e.split(',') for e in entries] != expected:
        raise ValueError('serial block differs from plans')
    return True

def render_multi(doc, plans, recommended, allow_short_report=False):
    if len(plans) != 1 or recommended != 1:
        raise ValueError('invalid plan count or recommendation')
    firsts, thirds, fourths, sequences = [], [], [], []
    second = None
    for i, plan in enumerate(plans):
        ids_for(plan)
        output = render_compact(doc, plan, allow_short_report=allow_short_report)
        first, rest = output.split('\n二、商品识别', 1)
        two, rest = rest.split('\n三、', 1)
        three, rest = rest.split('\n四、作品标题与话题\n', 1)
        four, serial = rest.split('\n五、原始SRT序号（按成片播放顺序）\n', 1)
        if second is None: second = two
        elif second != two: raise ValueError('product identification differs across plans')
        label = '方案' + NAMES[i]
        firsts.append(label + '\n' + first.split('\n', 1)[1])
        third_head, third_body = three.split('\n', 1)
        if '短候选' in third_head: label += '｜短候选，非正式成片'
        thirds.append(label + '\n' + third_body)
        fourths.append(label + '\n' + four.strip())
        sequences.append(serial.strip())
    labels = '方案一'
    output = ('一、文件解析结果\n'+'\n\n'.join(firsts)+'\n\n二、商品识别'+second+
              '\n三、成片方案\n'+'\n\n'.join(thirds)+'\n\n四、作品标题与话题\n'+'\n\n'.join(fourths)+
              '\n\n五、原始SRT序号（按成片播放顺序）\n'+labels+'，序号依次如下：\n\n```text\n'+'\n\n'.join(sequences)+'\n```')
    check_multi(output, plans)
    return output

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--snapshot', required=True); p.add_argument('--plans', required=True)
    p.add_argument('--answer'); p.add_argument('--output'); p.add_argument('--allow-short-report', action='store_true')
    a = p.parse_args()
    batch = json.loads(Path(a.plans).read_text(encoding='utf-8-sig'))
    if a.answer:
        check_multi(Path(a.answer).read_text(encoding='utf-8-sig'), batch['plans'])
        print('MULTI SERIAL CHECK PASS')
    else:
        doc = json.loads(Path(a.snapshot).read_text(encoding='utf-8-sig'))
        result = render_multi(doc, batch['plans'], batch['recommended'], a.allow_short_report)
        if a.output: Path(a.output).write_text(result, encoding='utf-8')
        else: print(result)

if __name__ == '__main__': main()
