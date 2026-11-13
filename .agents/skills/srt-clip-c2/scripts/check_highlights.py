#!/usr/bin/env python3
"""Check a human-authored highlight ledger against a subtitle snapshot and plans.

This validates records and IDs only; it cannot discover missing highlights or
judge semantics, reading coverage, compliance, product facts, audio or video.
"""
import argparse
import json
import sys
from pathlib import Path
from sentence_edits import extract_sentence_edits

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
    if not isinstance(batch, list) or not 1 <= len(batch) <= 3:
        fail('between one and three plans required')
    plan_ids = []
    plan_edits = []
    for index, plan in enumerate(batch, 1):
        if not isinstance(plan, dict) or not isinstance(plan.get('groups'), list):
            fail('plan %d groups required' % index)
        ids = [str(i) for group in plan['groups'] for i in group.get('ids', [])]
        if not ids or len(ids) != len(set(ids)) or not set(ids) <= source_ids:
            fail('plan %d IDs are empty, duplicate, or absent from snapshot' % index)
        plan_ids.append(ids)
        plan_edits.append(extract_sentence_edits(plan, snapshot))
    plan_id_sets = [set(ids) for ids in plan_ids]
    items = ledger.get('highlights')
    if not isinstance(items, list) or not items:
        fail('at least one highlight required')
    by_key = {}
    multi = len(batch) > 1
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
        assignments = row.get('by_plan')
        if multi and not isinstance(assignments, dict):
            fail(key + ' needs by_plan records for every plan')
        if assignments is not None:
            expected_keys = {str(i) for i in range(1, len(batch) + 1)}
            if not isinstance(assignments, dict) or set(assignments) != expected_keys:
                fail(key + ' by_plan must name every plan exactly once')
        elif multi:
            fail(key + ' needs by_plan records for every plan')
        else:
            assignments = {'1': row}
        checked = {}
        for index, selected in enumerate(plan_id_sets, 1):
            assignment = assignments[str(index)]
            if not isinstance(assignment, dict):
                fail(key + ' plan assignment must be an object')
            status = assignment.get('status')
            if status == '侧重点省略':
                fail(key + ' focus-only omission is not allowed; include every supported highlight or use a documented source/product exception')
            allowed = ('入选','合并','未入选','待核实')
            if status not in allowed:
                fail(key + ' invalid status in plan %d' % index)
            if status in ('入选','合并'):
                kept = ids_value(assignment.get('retained_ids'), key + ' retained_ids')
                if not set(kept) <= selected:
                    fail(key + ' retained IDs absent from plan %d' % index)
                if status == '入选' and not set(kept) <= set(src):
                    fail(key + ' retained IDs absent from its source_ids')
            else:
                kept = []
            if status in ('合并','未入选','待核实'):
                reason = text_value(assignment.get('reason'), key + ' reason')
                if reason in VAGUE or len(reason) < 4:
                    fail(key + ' needs a specific explanation')
            if status in ('未入选','待核实') and assignment.get('exception_kind') not in EXCEPTIONS:
                fail(key + ' needs an allowed exception_kind; timing or transition alone is not an exception')
            excluded = assignment.get('excluded_sentences', [])
            if status in ('未入选','待核实'):
                if not isinstance(excluded, list):
                    fail(key + ' excluded_sentences must be a list')
                for sentence in excluded:
                    if not isinstance(sentence, dict) or set(sentence) != {'source_id','text'}:
                        fail(key + ' excluded sentence needs source_id and exact text')
                    sid = str(sentence['source_id'])
                    text = sentence['text']
                    source_text = next(row['text'] for row in rows if str(row['id']) == sid) if sid in source_ids else None
                    if sid not in src or not isinstance(text, str) or not text or text not in source_text:
                        fail(key + ' excluded sentence must be exact text from one of its source cues')
                    if sid in selected and text not in plan_edits[index-1].get(sid, {}).get('removed_sentences', []):
                        fail(key + ' selected source sentence is not removed by the plan: ' + sid)
            if status in ('未入选','待核实'):
                overlap = set(src) & selected
                for sid in overlap:
                    removed = plan_edits[index-1].get(sid, {}).get('removed_sentences', [])
                    listed = [item['text'] for item in excluded if str(item['source_id']) == sid]
                    if assignment.get('exception_kind') == '商品归属不明' or not removed or sorted(removed) != sorted(listed):
                        fail(key + ' exception overlaps selected ID without explicit partial-cut instructions: ' + sid)
            checked[str(index)] = (status, assignment, kept)
        by_key[key] = (row, checked)
    for index in range(1, len(batch) + 1):
        for key, (row, checked) in by_key.items():
            status, assignment, kept = checked[str(index)]
            if status == '合并':
                target_key = text_value(assignment.get('merged_into'), key + ' merged_into')
                target = by_key.get(target_key)
                target_assignment = target[1][str(index)] if target is not None else None
                if target is None or target_key == key or target_assignment[0] != '入选':
                    fail(key + ' must merge into an existing selected highlight in plan %d' % index)
                if not set(map(str, kept)) <= set(map(str, target_assignment[2])):
                    fail(key + ' retained IDs must match its merge target')
    for index, edits in enumerate(plan_edits, 1):
        for sid, edit in edits.items():
            for removed_text in edit['removed_sentences']:
                recorded = any(
                    checked[str(index)][0] in ('未入选','待核实') and
                    any(str(item['source_id']) == sid and item['text'] == removed_text
                        for item in checked[str(index)][1].get('excluded_sentences', []))
                    for _, checked in by_key.values()
                )
                if not recorded:
                    fail('sentence edit removal must appear in a source exception: ' + sid)
    return len(items), sum(len(ids) for ids in plan_ids)

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

