import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

import srt_fast
import multi_plan


def plan(groups, **changes):
    result = {
        'groups': groups,
        'theme': '合成主题',
        'product_lines': ['合成商品'],
        'title': '合成标题',
        'topics': ['话题甲', '话题乙', '话题丙'],
        'subtitle_notes': [],
    }
    result.update(changes)
    return result


class C2021RuleTests(unittest.TestCase):
    def test_two_minute_limit_includes_rounding_and_unaccelerated_time(self):
        at_limit = srt_fast.parse_duration_text('1 144.0s 原话')
        rendered = srt_fast.render(at_limit, plan([{'ids': ['1'], 'function': '主体'}]))
        self.assertIn('预计1.2倍速成片时长：00:02:00.000', rendered)

        over_limit = srt_fast.parse_duration_text('1 144.001s 原话')
        with self.assertRaisesRegex(ValueError, '120'):
            srt_fast.render(over_limit, plan([{'ids': ['1'], 'function': '主体'}]))

        with_extra = plan([{'ids': ['1'], 'function': '主体'}], unaccelerated_ms=1)
        with self.assertRaisesRegex(ValueError, '120'):
            srt_fast.render(at_limit, with_extra)

    def test_designated_phrase_is_rejected_from_clip_and_metadata(self):
        doc = srt_fast.parse_duration_text('1 40s 这是三醋酸的羊绒、羊毛毛衣。')
        with self.assertRaisesRegex(ValueError, 'forbidden phrase'):
            srt_fast.render(doc, plan([{'ids': ['1'], 'function': '主体'}]))

        clean = srt_fast.parse_duration_text('1 40s 这是小巧版型的毛衣。')
        with self.assertRaisesRegex(ValueError, 'forbidden phrase'):
            srt_fast.render(clean, plan([{'ids': ['1'], 'function': '主体'}], title='三醋酸羊绒羊毛毛衣'))

        split_phrase = srt_fast.parse_duration_text(
            '1 20s 这句话说到三醋酸的羊绒、\n2 20s 羊毛毛衣和它的版型'
        )
        with self.assertRaisesRegex(ValueError, 'forbidden phrase'):
            srt_fast.render(split_phrase, plan([{'ids': ['1', '2'], 'function': '主体'}]))

    def test_secondary_highlights_can_be_distributed_between_plans(self):
        doc = srt_fast.parse_duration_text(
            '1 20s 核心卖点\n2 20s 搭配颜色\n3 20s 适用场景'
        )
        plans = [
            plan([{'ids': ['1'], 'function': '核心'}, {'ids': ['2'], 'function': '搭配'}]),
            plan([{'ids': ['1'], 'function': '核心'}, {'ids': ['3'], 'function': '场景'}]),
        ]
        ledger = {'highlights': [
            {'id': 'h1', 'point': '核心理由', 'importance': '核心', 'source_ids': ['1'],
             'by_plan': {str(i): {'status': '入选', 'retained_ids': ['1']} for i in (1, 2)}},
            {'id': 'h2', 'point': '颜色搭配', 'importance': '次要', 'source_ids': ['2'],
             'by_plan': {'1': {'status': '入选', 'retained_ids': ['2']},
                         '2': {'status': '侧重点省略', 'reason': '方案二聚焦另一类穿搭场景'}}},
            {'id': 'h3', 'point': '使用场景', 'importance': '次要', 'source_ids': ['3'],
             'by_plan': {'1': {'status': '侧重点省略', 'reason': '方案一聚焦颜色搭配'},
                         '2': {'status': '入选', 'retained_ids': ['3']}}},
        ]}
        answer = multi_plan.render_multi(doc, plans, 1, ledger=ledger)
        self.assertIn('方案二聚焦另一类穿搭场景', answer)
        self.assertIn('方案一聚焦颜色搭配', answer)
        self.assertEqual(answer.count('【1】核心卖点'), 2)

    def test_secondary_highlight_cannot_be_omitted_from_every_plan_by_focus(self):
        doc = srt_fast.parse_duration_text('1 40s 核心卖点\n2 10s 次要搭配')
        plans = [
            plan([{'ids': ['1'], 'function': '核心'}]),
            plan([{'ids': ['1'], 'function': '核心'}], title='第二条标题'),
        ]
        ledger = {'highlights': [
            {'id': 'h-core', 'point': '核心理由', 'importance': '核心', 'source_ids': ['1'],
             'by_plan': {str(i): {'status': '入选', 'retained_ids': ['1']} for i in (1, 2)}},
            {'id': 'h-secondary', 'point': '次要搭配', 'importance': '次要', 'source_ids': ['2'],
             'by_plan': {str(i): {'status': '侧重点省略', 'reason': f'方案{i}侧重不同搭配方向'} for i in (1, 2)}},
        ]}
        with self.assertRaisesRegex(ValueError, 'must appear in at least one'):
            multi_plan.render_multi(doc, plans, 1, ledger=ledger)

    def test_designated_phrase_can_be_removed_as_a_complete_sentence(self):
        doc = srt_fast.parse_duration_text('1 40s 商品介绍完整句。三醋酸羊绒羊毛材质句。')
        selected = plan([{
            'ids': ['1'], 'function': '主体', 'note': '句内剪点待回听',
            'sentence_edits': [{'id': '1', 'sentences': [
                {'text': '商品介绍完整句。', 'action': '保留'},
                {'text': '三醋酸羊绒羊毛材质句。', 'action': '剪除'},
            ]}],
        }])
        ledger = {'highlights': [{
            'id': 'h-ban', 'point': '用户指定禁用材质句', 'source_ids': ['1'],
            'by_plan': {'1': {
                'status': '待核实', 'exception_kind': '用户指定禁用词句',
                'reason': '命中用户指定禁用表述，按完整句剪除',
                'excluded_sentences': [{'source_id': '1', 'text': '三醋酸羊绒羊毛材质句。'}],
            }},
        }]}
        answer = multi_plan.render_multi(doc, [selected], 1, ledger=ledger)
        clip = answer.split('四、作品标题与话题', 1)[0]
        self.assertIn('【1】商品介绍完整句。', clip)
        self.assertNotIn('【1】商品介绍完整句。三醋酸', clip)
        self.assertIn('三醋酸羊绒羊毛材质句。', answer.split('亮点覆盖', 1)[1])


if __name__ == '__main__':
    unittest.main()
