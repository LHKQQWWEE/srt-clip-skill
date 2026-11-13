#!/usr/bin/env python3
"""Validate exact, sentence-level cuts within selected subtitle cues."""


def extract_sentence_edits(plan, doc):
    source = {str(row['id']): row['text'] for row in doc['rows']}
    edits = {}
    for group in plan.get('groups', []):
        group_ids = {str(value) for value in group.get('ids', [])}
        specs = group.get('sentence_edits', [])
        if not isinstance(specs, list):
            raise ValueError('sentence edit list is invalid')
        for spec in specs:
            if not isinstance(spec, dict) or set(spec) != {'id', 'sentences'}:
                raise ValueError('sentence edit record must contain id and sentences')
            sid = str(spec['id'])
            if sid not in group_ids or sid not in source or sid in edits:
                raise ValueError('sentence edit ID must occur once in its selected group')
            note = group.get('note')
            if not isinstance(note, str) or '回听' not in note:
                raise ValueError('sentence edit group note must mark the in-cue cut point for re-listening')
            sentences = spec['sentences']
            if not isinstance(sentences, list) or len(sentences) < 2:
                raise ValueError('sentence edit needs multiple complete sentence parts')
            retained = []
            removed = []
            pieces = []
            for sentence in sentences:
                if not isinstance(sentence, dict) or set(sentence) != {'text', 'action'}:
                    raise ValueError('sentence edit part must contain text and action')
                text = sentence['text']
                action = sentence['action']
                if not isinstance(text, str) or not text or action not in ('保留', '剪除'):
                    raise ValueError('sentence edit parts need exact text and a 保留/剪除 action')
                pieces.append(text)
                (retained if action == '保留' else removed).append(text)
            if ''.join(pieces) != source[sid]:
                raise ValueError('sentence edit does not exactly account for the entire source cue: ' + sid)
            if not retained or not removed:
                raise ValueError('sentence edit must retain a clean sentence and remove a flagged sentence')
            edits[sid] = {'kept_text': ''.join(retained), 'removed_sentences': removed}
    return edits
