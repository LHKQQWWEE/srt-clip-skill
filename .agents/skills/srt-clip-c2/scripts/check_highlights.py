#!/usr/bin/env python3
"""Check a human-authored highlight ledger against a subtitle snapshot and plan.

This validates records and IDs only; it cannot discover missing highlights or
judge semantics, reading coverage, compliance, product facts, audio or video.
"""
import argparse
import json
import sys
from pathlib import Path

VAGUE = {'重复','精简','时长','超时','衔接','风险','不选','无','无理由'}
EXCEPTIONS = {'商品归属不明', '已知不实', '当前素材已拒审'}

def fail(message):
    raise ValueError(message)

def text_value(value, label):
    if not isinstance(value, str) or not value.strip():
        fail(label + ' must be nonempty text')
    return value.strip()

def ids_value(value, label):
    if not isinstance(value, list) or not value:
        fail(label + ' must be a nonempty ID list')
    result = [str(x) for x in value]
    if any(not x.isdecimal() or int(x) <= 0 for x in result) or len(set(result)) != len(result):
        fail(label + ' has invalid or duplicate IDs')
    return result

def validate(snapshot, plans, ledger):
    rows = snapshot.get('rows')
    if not isinstance(rows, list) or not rows:
        fail('snapshot rows required')
    source_ids = [str(row['id']) for row in rows]
    if len(set(source_ids)) != len(source_ids):
        fail('snapshot IDs must be unique')
    source_ids = set(source_ids)
    batch = plans.get('plans')
    if not isinstance(batch, list) or len(batch) != 1:
        fail('exactly one plan required')
    plan_ids = [str(i) for group in batch[0].get('groups', []) for i in group.get('ids', [])]
    if not plan_ids or len(plan_ids) != len(set(plan_ids)) or not set(plan_ids) <= source_ids:
        fail('plan IDs are empty, duplicate, or absent from snapshot')
    selected = set(plan_ids)
    items = ledger.get('highlights')
    if not isinstance(items, list) or not items:
        fail('at least one highlight required')
    by_key = {}
    for row in items:
        if not isinstance(row, dict):
            fail('highlight must be an object')
        key = text_value(row.get('id'), 'highlight id')
        if key in by_key:
            fail('duplicate highlight id: ' + key)
        text_value(row.get('point'), key + ' point')
        src = ids_value(row.get('source_ids'), key + ' source_ids')
        if not set(src) <= source_ids:
            fail(key + ' references missing snapshot IDs')
        status = row.get('status')
        if status not in ('入选','合并','未入选','待核实'):
            fail(key + ' invalid status')
        if status in ('入选','合并'):
            kept = ids_value(row.get('retained_ids'), key + ' retained_ids')
            if not set(kept) <= selected:
                fail(key + ' retained IDs absent from plan')
            if status == '入选' and not set(kept) <= set(src):
                fail(key + ' retained IDs absent from its source_ids')
        if status in ('合并','未入选','待核实'):
            reason = text_value(row.get('reason'), key + ' reason')
            if reason in VAGUE or len(reason) < 4:
                fail(key + ' needs a specific explanation')
        if status in ('未入选','待核实') and row.get('exception_kind') not in EXCEPTIONS:
            fail(key + ' needs an allowed exception_kind; timing or transition alone is not an exception')
        if status in ('未入选','待核实'):
            overlap = set(src) & selected
            for sid in overlap:
                groups = [g for g in batch[0]['groups'] if sid in set(map(str, g['ids']))]
                note = ' '.join(str(g.get('note', '')) for g in groups)
                if row.get('exception_kind') == '商品归属不明' or not (sid in note and '保留' in note and '剪除' in note and '回听' in note):
                    fail(key + ' exception overlaps selected ID without explicit partial-cut instructions: ' + sid)
        by_key[key] = row
    for key, row in by_key.items():
        if row['status'] == '合并':
            target_key = text_value(row.get('merged_into'), key + ' merged_into')
            target = by_key.get(target_key)
            if target is None or target_key == key or target['status'] != '入选':
                fail(key + ' must merge into an existing selected highlight')
            if not set(map(str, row['retained_ids'])) <= set(map(str, target['retained_ids'])):
                fail(key + ' retained IDs must match its merge target')
    return len(items), len(plan_ids)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--snapshot', required=True)
    parser.add_argument('--plans', required=True)
    parser.add_argument('--ledger', required=True)
    args = parser.parse_args()
    try:
        objects = [json.loads(Path(p).read_text(encoding='utf-8-sig')) for p in (args.snapshot,args.plans,args.ledger)]
        count, nids = validate(*objects)
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print('HIGHLIGHT RECORD CHECK FAIL: ' + str(exc), file=sys.stderr)
        return 1
    print('HIGHLIGHT RECORD CHECK PASS: %d records; %d plan IDs. Does not check semantic completeness, factual accuracy, audio/video, or compliance.' % (count,nids))
    return 0

if __name__ == '__main__':
    sys.exit(main())

