#!/usr/bin/env python3
"""Render and check one C2 plan against one snapshot."""
import argparse
import json
import re
import copy
from pathlib import Path
from render_compact import render_compact
from check_highlights import validate as validate_highlights

NAMES = ['一', '二', '三']
SERIAL = r'[1-9][0-9]*(?:,[1-9][0-9]*)*'

def ids_for(plan):
    ids = [str(i) for g in plan['groups'] for i in g['ids']]
    if not ids or any(not re.fullmatch(r'[1-9][0-9]*', x) for x in ids) or len(set(ids)) != len(ids):
        raise ValueError('invalid or duplicate IDs within a plan')
    return ids

def coverage_text(ledger, plan, doc):
    order = {sid: pos for pos, sid in enumerate(ids_for(plan))}
    selected = [x for x in ledger['highlights'] if x['status'] == '入选']
    selected.sort(key=lambda x: min(order[str(i)] for i in x['retained_ids']))
    lines = ['亮点覆盖（按成片播放顺序）：']
    lines.extend('- ' + x['point'] + '｜序号 ' + ','.join(map(str, x['retained_ids'])) for x in selected)
    merged = [x for x in ledger['highlights'] if x['status'] == '合并']
    if merged:
        lines.append('同义合并：')
        lines.extend('- ' + x['point'] + '｜保留序号 ' + ','.join(map(str,x['retained_ids'])) + '｜' + x['reason'] for x in merged)
    exceptions = [x for x in ledger['highlights'] if x['status'] in ('未入选','待核实')]
    if exceptions:
        source = {str(row['id']): row['text'] for row in doc['rows']}
        lines.append('未编入的例外：')
        for x in exceptions:
            lines.append('- ' + x['point'] + '｜来源序号 ' + ','.join(map(str,x['source_ids'])) + '｜' + x['exception_kind'] + '：' + x['reason'])
            lines.extend('原话：' + source[str(sid)] for sid in x['source_ids'])
    return '\n'.join(lines)

def check_multi(answer, plans, ledger=None, doc=None):
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
        subtitle_section = sections[2+2*i].split('亮点覆盖（按成片播放顺序）：', 1)[0]
        if sections[1+2*i] != NAMES[i] or re.findall(r'【([1-9][0-9]*)】', subtitle_section) != ids:
            raise ValueError('third section plan order or IDs differ')
        if doc is not None:
            source = {str(r['id']): r['text'] for r in doc['rows']}
            for sid in ids:
                if not re.search(re.escape('【'+sid+'】'+source[sid]) + r'(?=\r?\n|$)', subtitle_section):
                    raise ValueError('source text missing or changed: ' + sid)
        if any(g.get('note') for g in plans[i]['groups']):
            group_sections = re.split(r'(?m)^片段[0-9]+｜', subtitle_section)[1:]
            if len(group_sections) != len(plans[i]['groups']):
                raise ValueError('group count differs')
            for group, section in zip(plans[i]['groups'], group_sections):
                if group.get('note') and '待核实／剪辑提醒：' + group['note'] not in section:
                    raise ValueError('group note missing from corresponding group')
    if ledger is not None and (doc is None or coverage_text(ledger, plans[0], doc) not in third):
        raise ValueError('highlight coverage absent or differs from ledger')
    match = re.search(r'```(?:text)?\r?\n([\s\S]*?)\r?\n```\s*$', fifth)
    if not match:
        raise ValueError('missing final fenced serial block')
    entries = re.split(r'\r?\n\r?\n', match.group(1))
    if len(entries) != len(expected) or any(not re.fullmatch(SERIAL, e) for e in entries):
        raise ValueError('serial block must contain one pure ID line per plan separated by blank lines')
    if [e.split(',') for e in entries] != expected:
        raise ValueError('serial block differs from plans')
    return True

def render_multi(doc, plans, recommended, allow_short_report=False, ledger=None):
    if len(plans) != 1 or recommended != 1:
        raise ValueError('invalid plan count or recommendation')
    if ledger is not None:
        validate_highlights(doc, {'plans': plans}, ledger)
    plans = copy.deepcopy(plans)
    if ledger is not None:
        for item in ledger['highlights']:
            if item['status'] == '入选' and item.get('note'):
                for group in plans[0]['groups']:
                    ids = set(map(str, group['ids'])) & set(map(str, item['retained_ids']))
                    if ids:
                        msg = '序号' + ','.join(sorted(ids, key=int)) + '：' + item['note']
                        group['note'] = (group.get('note', '') + '；' + msg).strip('；')
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
        thirds.append(label + '\n' + third_body + ('\n\n' + coverage_text(ledger, plan, doc) if ledger is not None else ''))
        fourths.append(label + '\n' + four.strip())
        sequences.append(serial.strip())
    labels = '方案一'
    output = ('一、文件解析结果\n'+'\n\n'.join(firsts)+'\n\n二、商品识别'+second+
              '\n三、成片方案\n'+'\n\n'.join(thirds)+'\n\n四、作品标题与话题\n'+'\n\n'.join(fourths)+
              '\n\n五、原始SRT序号（按成片播放顺序）\n'+labels+'，序号依次如下：\n\n```text\n'+'\n\n'.join(sequences)+'\n```')
    check_multi(output, plans, ledger, doc)
    return output

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--snapshot', required=True); p.add_argument('--plans', required=True)
    p.add_argument('--ledger', required=True, help='human-reviewed highlight ledger, required for delivery')
    p.add_argument('--answer'); p.add_argument('--output'); p.add_argument('--allow-short-report', action='store_true')
    a = p.parse_args()
    batch = json.loads(Path(a.plans).read_text(encoding='utf-8-sig'))
    ledger = json.loads(Path(a.ledger).read_text(encoding='utf-8-sig')) if a.ledger else None
    if a.answer:
        doc = json.loads(Path(a.snapshot).read_text(encoding='utf-8-sig')) if ledger is not None else None
        if ledger is not None:
            validate_highlights(doc, batch, ledger)
        expected = render_multi(doc, batch['plans'], batch['recommended'], True, ledger)
        answer = Path(a.answer).read_text(encoding='utf-8-sig')
        if answer.strip() != expected.strip():
            raise ValueError('answer differs from rendered source-checked delivery; regenerate or review changes')
        check_multi(answer, batch['plans'], ledger, doc)
        print('MULTI SERIAL CHECK PASS')
    else:
        doc = json.loads(Path(a.snapshot).read_text(encoding='utf-8-sig'))
        result = render_multi(doc, batch['plans'], batch['recommended'], a.allow_short_report, ledger)
        if a.output: Path(a.output).write_text(result, encoding='utf-8')
        else: print(result)

if __name__ == '__main__': main()
