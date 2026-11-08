#!/usr/bin/env python3
"""Check a prepared C2 response against the frozen plan, not the chat UI."""
import argparse
import json
import re
from pathlib import Path

def check(answer, plan):
    ids = [str(i) for group in plan['groups'] for i in group['ids']]
    if not ids or any(not re.fullmatch(r'[1-9][0-9]*', i) for i in ids) or len(ids) != len(set(ids)):
        raise ValueError('plan contains invalid or duplicate IDs')
    lines = answer.rstrip('\r\n').splitlines()
    if not lines or not re.fullmatch(r'[1-9][0-9]*(?:,[1-9][0-9]*)*', lines[-1]):
        raise ValueError('last line must be ASCII comma-separated IDs without spaces')
    if lines[-1].split(',') != ids:
        raise ValueError('last line differs from plan in order or content')
    try:
        third = answer.split('三、', 1)[1].split('四、', 1)[0]
    except IndexError:
        raise ValueError('third or fourth section missing')
    if re.findall(r'【([1-9][0-9]*)】', third) != ids:
        raise ValueError('third section differs from plan in order or content')
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--answer', required=True)
    parser.add_argument('--plan', required=True)
    args = parser.parse_args()
    check(Path(args.answer).read_text(encoding='utf-8'), json.loads(Path(args.plan).read_text(encoding='utf-8-sig')))
    print('FINAL SERIAL CHECK PASS')
