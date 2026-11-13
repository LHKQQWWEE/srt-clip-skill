#!/usr/bin/env python3
"""Render and check one to three C2 schemes against one snapshot."""
import argparse
import copy
import json
import re
from pathlib import Path

from render_compact import render_compact
from check_highlights import validate as validate_highlights

NAMES = ['一', '二', '三']
SERIAL = r'[1-9][0-9]*(?:,[1-9][0-9]*)*'
SERIAL_HEADING = '五、原始SRT序号（按成片播放顺序）'
FIXED_TOPICS = ('#穿搭', '#时尚营销')


def ids_for(plan):
    ids = [str(i) for g in plan['groups'] for i in g['ids']]
    if not ids or any(not re.fullmatch(r'[1-9][0-9]*', x) for x in ids) or len(set(ids)) != len(ids):
        raise ValueError('invalid or duplicate IDs within a plan')
    return ids


def _assignment(item, plan_index):
    if 'by_plan' in item:
        return item['by_plan'][str(plan_index)]
    return item


def coverage_text(ledger, plan, doc, plan_index=1):
    order = {sid: pos for pos, sid in enumerate(ids_for(plan))}
    current = [(_assignment(item, plan_index), item) for item in ledger['highlights']]
    selected = [(a, item) for a, item in current if a['status'] == '入选']
    selected.sort(key=lambda pair: min(order[str(i)] for i in pair[0]['retained_ids']))
    lines = ['亮点覆盖（按成片播放顺序）：']
    lines.extend('- ' + item['point'] + '｜序号 ' + ','.join(map(str, a['retained_ids'])) for a, item in selected)
    merged = [(a, item) for a, item in current if a['status'] == '合并']
    if merged:
        lines.append('同义合并：')
        lines.extend('- ' + item['point'] + '｜保留序号 ' + ','.join(map(str, a['retained_ids'])) + '｜' + a['reason'] for a, item in merged)
    omitted = [(a, item) for a, item in current if a['status'] == '侧重点省略']
    if omitted:
        lines.append('本版侧重点未选亮点：')
        lines.extend('- ' + item['point'] + '｜原因：' + a['reason'] for a, item in omitted)
    exceptions = [(a, item) for a, item in current if a['status'] in ('未入选', '待核实')]
    if exceptions:
        source = {str(row['id']): row['text'] for row in doc['rows']}
        lines.append('未编入的素材例外：')
        for a, item in exceptions:
            lines.append('- ' + item['point'] + '｜来源序号 ' + ','.join(map(str, item['source_ids'])) + '｜' + a['exception_kind'] + '：' + a['reason'])
            lines.extend('原话：' + source[str(sid)] for sid in item['source_ids'])
    return '\n'.join(lines)


def _topic_line(plan):
    generated = [s if s.startswith('#') else '#' + s for s in plan['topics']]
    if len(generated) != 3 or len(set(generated)) != 3 or set(generated) & set(FIXED_TOPICS):
        raise ValueError('each plan needs three unique generated topics, separate from fixed topics')
    return '作品话题：' + ' '.join(generated + list(FIXED_TOPICS))


def check_multi(answer, plans, ledger=None, doc=None):
    if not 1 <= len(plans) <= 3:
        raise ValueError('expected between one and three plans')
    expected = [ids_for(p) for p in plans]
    try:
        third = re.search(r'(?s)三、成片方案\s*\n(.*?)\n四、作品标题与话题\s*\n', answer).group(1)
        fourth = re.search(r'(?s)四、作品标题与话题\s*\n(.*?)\n' + re.escape(SERIAL_HEADING) + r'\s*\n', answer).group(1)
        fifth = answer.split(SERIAL_HEADING, 1)[1]
    except (AttributeError, IndexError):
        raise ValueError('missing section')
    matches = list(re.finditer(r'(?m)^方案([一二三])(?:｜[^\n]*)?\s*$', third))
    title_matches = list(re.finditer(r'(?m)^方案([一二三])(?:｜[^\n]*)?\s*$', fourth))
    if len(matches) != len(plans) or len(title_matches) != len(plans):
        raise ValueError('wrong plan section count')
    source = {str(row['id']): row['text'] for row in doc['rows']} if doc is not None else {}
    for i, (ids, match) in enumerate(zip(expected, matches)):
        if match.group(1) != NAMES[i]:
            raise ValueError('plan order differs')
        end = matches[i + 1].start() if i + 1 < len(matches) else len(third)
        block = third[match.start():end].rstrip()
        subtitle_section = block.split('亮点覆盖（按成片播放顺序）：', 1)[0]
        if re.findall(r'【([1-9][0-9]*)】', subtitle_section) != ids:
            raise ValueError('third section plan order or IDs differ')
        if doc is not None:
            for sid in ids:
                if not re.search(re.escape('【' + sid + '】' + source[sid]) + r'(?=\r?\n|$)', subtitle_section):
                    raise ValueError('source text missing or changed: ' + sid)
        if any(g.get('note') for g in plans[i]['groups']):
            group_sections = re.split(r'(?m)^片段[0-9]+｜', subtitle_section)[1:]
            if len(group_sections) != len(plans[i]['groups']):
                raise ValueError('group count differs')
            for group, section in zip(plans[i]['groups'], group_sections):
                if group.get('note') and '待核实／剪辑提醒：' + group['note'] not in section:
                    raise ValueError('group note missing from corresponding group')
        if ledger is not None and (doc is None or coverage_text(ledger, plans[i], doc, i + 1) not in block):
            raise ValueError('plan highlight coverage differs from ledger')
        title_end = title_matches[i + 1].start() if i + 1 < len(title_matches) else len(fourth)
        title_block = fourth[title_matches[i].start():title_end]
        if title_matches[i].group(1) != NAMES[i]:
            raise ValueError('title section plan order differs')
        if 'title' in plans[i]:
            if '作品标题：' + plans[i]['title'] not in title_block or _topic_line(plans[i]) not in title_block:
                raise ValueError('title or topic list differs from plan')
    serial_block = re.search(r'```text\r?\n([\s\S]*?)\r?\n```\s*$', fifth)
    if not serial_block:
        raise ValueError('missing final fenced serial block')
    if fifth.count('```') != 2:
        raise ValueError('section five must contain exactly one code block')
    entries = re.split(r'\r?\n\r?\n', serial_block.group(1).strip())
    if len(entries) != len(expected) or any(not re.fullmatch(SERIAL, e) for e in entries):
        raise ValueError('serial block must contain one pure ID line per plan separated by blank lines')
    if [e.split(',') for e in entries] != expected:
        raise ValueError('serial block differs from plans')
    return True


def render_multi(doc, plans, recommended, allow_short_report=False, ledger=None):
    if not 1 <= len(plans) <= 3 or not isinstance(recommended, int) or not 1 <= recommended <= len(plans):
        raise ValueError('invalid plan count or recommendation')
    if ledger is not None:
        validate_highlights(doc, {'plans': plans}, ledger)
    plans = copy.deepcopy(plans)
    if ledger is not None:
        for item in ledger['highlights']:
            for index, plan in enumerate(plans, 1):
                assignment = _assignment(item, index)
                if assignment['status'] == '入选' and assignment.get('note'):
                    for group in plan['groups']:
                        ids = set(map(str, group['ids'])) & set(map(str, assignment['retained_ids']))
                        if ids:
                            msg = '序号' + ','.join(sorted(ids, key=int)) + '：' + assignment['note']
                            group['note'] = (group.get('note', '') + '；' + msg).strip('；')
    rendered = []
    second = None
    for index, plan in enumerate(plans):
        ids_for(plan)
        output = render_compact(doc, plan, allow_short_report=allow_short_report)
        first, rest = output.split('\n二、商品识别', 1)
        two, rest = rest.split('\n三、', 1)
        three, rest = rest.split('\n四、作品标题与话题\n', 1)
        four, _ = rest.split('\n' + SERIAL_HEADING + '\n', 1)
        if second is None:
            second = two
        elif second != two:
            raise ValueError('product identification differs across plans')
        label = '方案' + NAMES[index]
        third_head, third_body = three.split('\n', 1)
        if '短候选' in third_head:
            label += '｜短候选，非正式成片'
        third = label + '\n' + third_body
        if ledger is not None:
            third += '\n\n' + coverage_text(ledger, plan, doc, index + 1)
        rendered.append({'label': label, 'first': first, 'third': third, 'fourth': label + '\n' + four.strip(), 'ids': ','.join(ids_for(plan))})
    if len(plans) == 1:
        first_section = '一、文件解析结果\n' + rendered[0]['label'] + '\n' + rendered[0]['first'].split('\n', 1)[1]
    else:
        all_lines = rendered[0]['first'].splitlines()
        variable_prefixes = ('入选字幕：', '原始选段时长（1.0倍）：', '预计1.2倍速成片时长：', '素材不足45秒：', '时长不超过30秒：', '来源核对：')
        common = [line for line in all_lines[1:] if not line.startswith(variable_prefixes)]
        summaries = []
        for item in rendered:
            metrics = [line for line in item['first'].splitlines()[1:] if line.startswith(variable_prefixes)]
            summaries.append(item['label'] + '\n' + '\n'.join(metrics))
        first_section = '一、文件解析结果\n' + '\n'.join(common) + '\n\n' + '\n\n'.join(summaries)
    labels = '、'.join('方案' + name for name in NAMES[:len(plans)])
    serial_caption = ('方案一的序号如下：' if len(plans) == 1 else labels + '的序号依次如下：')
    output = (first_section + '\n\n二、商品识别' + second +
              '\n三、成片方案\n' + '\n\n'.join(item['third'] for item in rendered) +
              '\n\n四、作品标题与话题\n' + '\n\n'.join(item['fourth'] for item in rendered) +
              '\n\n' + SERIAL_HEADING + '\n' + serial_caption + '\n\n```text\n' +
              '\n\n'.join(item['ids'] for item in rendered) + '\n```')
    check_multi(output, plans, ledger, doc)
    return output


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--snapshot', required=True)
    p.add_argument('--plans', required=True)
    p.add_argument('--ledger', required=True, help='human-reviewed highlight ledger, required for delivery')
    p.add_argument('--answer')
    p.add_argument('--output')
    p.add_argument('--allow-short-report', action='store_true')
    a = p.parse_args()
    batch = json.loads(Path(a.plans).read_text(encoding='utf-8-sig'))
    ledger = json.loads(Path(a.ledger).read_text(encoding='utf-8-sig')) if a.ledger else None
    if a.answer:
        doc = json.loads(Path(a.snapshot).read_text(encoding='utf-8-sig')) if ledger is not None else None
        if ledger is not None:
            validate_highlights(doc, batch, ledger)
        expected = render_multi(doc, batch['plans'], batch['recommended'], True, ledger)
        answer = Path(a.answer).read_text(encoding='utf-8-sig')
        try:
            first, rest = answer.split('\n二、商品识别', 1)
            expected_first, expected_rest = expected.split('\n二、商品识别', 1)
        except ValueError:
            raise ValueError('missing product section')
        if not first.startswith(expected_first) or rest.strip() != expected_rest.strip():
            raise ValueError('answer differs from rendered source-checked delivery; regenerate or review changes')
        check_multi(answer, batch['plans'], ledger, doc)
        print('MULTI SERIAL CHECK PASS')
    else:
        doc = json.loads(Path(a.snapshot).read_text(encoding='utf-8-sig'))
        result = render_multi(doc, batch['plans'], batch['recommended'], a.allow_short_report, ledger)
        if a.output:
            Path(a.output).write_text(result, encoding='utf-8')
        else:
            print(result)


if __name__ == '__main__':
    main()
