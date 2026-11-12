import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from check_highlights import validate
from multi_plan import render_multi, check_multi
from srt_fast import parse_duration_text


class CoverageDeliveryTests(unittest.TestCase):
    def setUp(self):
        self.doc = {'filename':'test.txt','input_type':'duration_text','count':3,'start':0,'end':90000,'rows':[
            {'id':str(i),'ord':i,'start':(i-1)*30000,'end':i*30000,'duration_raw':'30s','text':t}
            for i,t in [(1,'轻'),(2,'软'),(3,'归属不明')]]}
        self.plan={'theme':'试排','product_lines':['商品'],'title':'标题','topics':['一','二','三'],'subtitle_notes':[],
                   'groups':[{'ids':['2'],'function':'柔软','note':'序号2肤感待核实'}, {'ids':['1'],'function':'轻'}]}
        self.plans={'plans':[self.plan],'recommended':1}
        self.ledger={'highlights':[
            {'id':'h1','point':'轻','source_ids':['1'],'status':'入选','retained_ids':['1']},
            {'id':'h2','point':'柔软','source_ids':['2'],'status':'入选','retained_ids':['2']},
            {'id':'h3','point':'归属不明','source_ids':['3'],'status':'待核实','exception_kind':'商品归属不明','reason':'交叉讲解指代不清'}]}

    def test_omission_for_transition_is_not_accepted(self):
        self.ledger['highlights'][1]={'id':'h2','point':'柔软','source_ids':['2'],'status':'未入选','reason':'衔接不自然，故未采用'}
        with self.assertRaises(ValueError): validate(self.doc,self.plans,self.ledger)

    def test_only_recorded_explicit_exception_kinds_are_accepted(self):
        for kind in ('商品归属不明','已知不实','当前素材已拒审'):
            self.ledger['highlights'][2]['exception_kind']=kind
            self.assertEqual(validate(self.doc,self.plans,self.ledger),(3,2))
        self.ledger['highlights'][2]['exception_kind']='衔接困难'
        with self.assertRaises(ValueError): validate(self.doc,self.plans,self.ledger)

    def test_selected_doubt_is_placed_beside_group_and_coverage_follows_playback(self):
        answer=render_multi(self.doc,[self.plan],1,ledger=self.ledger)
        self.assertLess(answer.index('【2】软'),answer.index('序号2肤感待核实'))
        self.assertLess(answer.index('序号2肤感待核实'),answer.index('片段2'))
        coverage=answer.split('亮点覆盖',1)[1].split('四、',1)[0]
        self.assertLess(coverage.index('柔软'),coverage.index('轻'))
        self.assertIn('交叉讲解指代不清',coverage)
        self.assertIn('原话：归属不明',coverage)
        self.assertTrue(check_multi(answer,[self.plan]))
        with self.assertRaises(ValueError):
            check_multi(answer.replace('待核实／剪辑提醒：序号2肤感待核实',''),[self.plan],self.ledger,self.doc)
        with self.assertRaises(ValueError):
            check_multi(answer.replace('亮点覆盖（按成片播放顺序）：',''),[self.plan],self.ledger,self.doc)

    def test_one_cue_can_support_multiple_distinct_highlights(self):
        self.ledger['highlights'].append({'id':'h4','point':'另一个具体信息','source_ids':['2'],'status':'入选','retained_ids':['2']})
        answer=render_multi(self.doc,[self.plan],1,ledger=self.ledger)
        self.assertIn('另一个具体信息｜序号 2',answer)

    def test_known_subtitle_header_does_not_require_file_rewrite(self):
        for header in ('srt文案','str文案','C2完整精简版','切片文案','srt切片文案'):
            doc=parse_duration_text(header+'\n\n【字幕列表】\n1 1.5 原始字幕\n')
            self.assertEqual(doc['rows'][0]['text'],'原始字幕')

if __name__=='__main__': unittest.main()
