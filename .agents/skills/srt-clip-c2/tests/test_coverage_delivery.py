import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from check_highlights import validate
from multi_plan import render_multi, check_multi
from render_compact import render_compact
from srt_fast import parse_duration_text


class CoverageDeliveryTests(unittest.TestCase):
    def setUp(self):
        self.doc = {'filename':'test.txt','input_type':'duration_text','count':4,'start':0,'end':120000,'rows':[
            {'id':str(i),'ord':i,'start':(i-1)*30000,'end':i*30000,'duration_raw':'30s','text':t}
            for i,t in [(1,'轻'),(2,'软'),(3,'归属不明'),(4,'通勤搭配')]]}
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

    def test_multi_plan_rejects_focus_only_omission(self):
        second=dict(self.plan)
        second['groups']=[{'ids':['1'],'function':'开头'},{'ids':['4'],'function':'搭配'}]
        plans=[self.plan,second]
        ledger={'highlights':[
            {'id':'h1','point':'轻','source_ids':['1'],'by_plan':{
                '1':{'status':'入选','retained_ids':['1']},
                '2':{'status':'入选','retained_ids':['1']}}},
            {'id':'h2','point':'柔软','source_ids':['2'],'by_plan':{
                '1':{'status':'入选','retained_ids':['2']},
                '2':{'status':'侧重点省略','reason':'方案二聚焦轻盈外观'}}},
            {'id':'h3','point':'归属不明','source_ids':['3'],'by_plan':{
                '1':{'status':'待核实','exception_kind':'商品归属不明','reason':'无法确认目标商品'},
                '2':{'status':'待核实','exception_kind':'商品归属不明','reason':'无法确认目标商品'}}},
            {'id':'h4','point':'通勤搭配','source_ids':['4'],'by_plan':{
                '1':{'status':'侧重点省略','reason':'方案一聚焦面料和版型'},
                '2':{'status':'入选','retained_ids':['4']}}}
        ]}
        with self.assertRaises(ValueError): validate(self.doc,{'plans':plans},ledger)

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

    def test_refused_material_sentence_can_leave_clean_sentence_in_same_cue(self):
        self.doc['rows'][0]['text']='白鹅绒填充。面料还做了三防工艺。'
        self.plan['groups'][1]['note']='序号1保留独立完整句；句间剪点待回听'
        self.plan['groups'][1]['sentence_edits']=[{
            'id':'1','sentences':[
                {'text':'白鹅绒填充。','action':'剪除'},
                {'text':'面料还做了三防工艺。','action':'保留'}
            ]
        }]
        ledger={'highlights':self.ledger['highlights']+[
            {'id':'h4','point':'被拒审的材质句','source_ids':['1'],'status':'待核实',
             'exception_kind':'当前素材已拒审','reason':'平台明确指出该句违规',
             'excluded_sentences':[{'source_id':'1','text':'白鹅绒填充。'}]}]}
        self.assertEqual(validate(self.doc,self.plans,ledger),(4,2))
        answer=render_multi(self.doc,[self.plan],1,ledger=ledger)
        clip_section=answer.split('亮点覆盖（按成片播放顺序）：',1)[0]
        self.assertIn('【1】面料还做了三防工艺。',clip_section)
        self.assertNotIn('【1】白鹅绒填充。面料还做了三防工艺。',clip_section)
        self.assertIn('句间剪点待回听',clip_section)
        self.assertIn('当前素材已拒审：平台明确指出该句违规',answer)
        self.assertIn('风险核对用原句：序号1｜白鹅绒填充。',answer)
        with self.assertRaises(ValueError):
            check_multi(answer.replace('【1】面料还做了三防工艺。','【1】'+self.doc['rows'][0]['text']),[self.plan],ledger,self.doc)
        injected=answer.replace('【1】面料还做了三防工艺。','【1】面料还做了三防工艺。\n白鹅绒填充。')
        with self.assertRaisesRegex(ValueError,'clip section differs'):
            check_multi(injected,[self.plan],ledger,self.doc)

    def test_sentence_cut_requires_a_coverage_exception(self):
        self.doc['rows'][0]['text']='白鹅绒填充。面料还做了三防工艺。'
        self.plan['groups'][1]['note']='序号1保留独立完整句；句间剪点待回听'
        self.plan['groups'][1]['sentence_edits']=[{
            'id':'1','sentences':[
                {'text':'白鹅绒填充。','action':'剪除'},
                {'text':'面料还做了三防工艺。','action':'保留'}
            ]
        }]
        with self.assertRaisesRegex(ValueError,'sentence edit removal must appear'):
            validate(self.doc,self.plans,self.ledger)
        with self.assertRaisesRegex(ValueError,'highlight ledger'):
            render_multi(self.doc,[self.plan],1)

    def test_direct_compact_renderer_requires_prevalidated_sentence_exceptions(self):
        self.doc['rows'][0]['text']='白鹅绒填充。面料还做了三防工艺。'
        self.plan['groups'][1]['note']='序号1保留独立完整句；句间剪点待回听'
        self.plan['groups'][1]['sentence_edits']=[{
            'id':'1','sentences':[
                {'text':'白鹅绒填充。','action':'剪除'},
                {'text':'面料还做了三防工艺。','action':'保留'}
            ]
        }]
        with self.assertRaisesRegex(ValueError,'prevalidated source-exception ledger'):
            render_compact(self.doc,self.plan)

    def test_sentence_edit_must_account_for_the_entire_source_cue(self):
        self.doc['rows'][0]['text']='白鹅绒填充。面料还做了三防工艺。'
        self.plan['groups'][1]['sentence_edits']=[{
            'id':'1','sentences':[
                {'text':'白鹅绒填充。','action':'剪除'},
                {'text':'面料还做了三防。','action':'保留'}
            ]
        }]
        with self.assertRaisesRegex(ValueError,'sentence edit'):
            render_multi(self.doc,[self.plan],1,ledger=self.ledger)

    def test_one_cue_can_support_multiple_distinct_highlights(self):
        self.ledger['highlights'].append({'id':'h4','point':'另一个具体信息','source_ids':['2'],'status':'入选','retained_ids':['2']})
        answer=render_multi(self.doc,[self.plan],1,ledger=self.ledger)
        self.assertIn('另一个具体信息｜序号 2',answer)

    def test_unaccelerated_time_is_included(self):
        self.plan['unaccelerated_ms']=5000
        answer=render_multi(self.doc,[self.plan],1,ledger=self.ledger)
        self.assertIn('预计1.2倍速成片时长：00:00:55.000',answer)
        self.assertIn('已加计未加速时长：00:00:05.000',answer)

    def test_ledger_note_reaches_selected_group(self):
        self.ledger['highlights'][1]['note']='肤感待核实'
        answer=render_multi(self.doc,[self.plan],1,ledger=self.ledger)
        self.assertIn('序号2：肤感待核实',answer)

    def test_final_source_text_mutation_fails(self):
        answer=render_multi(self.doc,[self.plan],1,ledger=self.ledger)
        with self.assertRaises(ValueError):
            check_multi(answer.replace('【2】软','【2】硬'),[self.plan],self.ledger,self.doc)

    def test_exception_cannot_silently_enter_sequence(self):
        self.ledger['highlights'][2]['source_ids']=['1']
        with self.assertRaises(ValueError): validate(self.doc,self.plans,self.ledger)

    def test_known_subtitle_header_does_not_require_file_rewrite(self):
        for header in ('srt文案','str文案','C2完整精简版','切片文案','srt切片文案'):
            doc=parse_duration_text(header+'\n\n【字幕列表】\n1 1.5 原始字幕\n')
            self.assertEqual(doc['rows'][0]['text'],'原始字幕')

    def test_multi_plan_full_coverage_and_blank_line_serials(self):
        second=dict(self.plan)
        second['theme']='轻盈主线'
        second['title']='轻盈方案标题'
        second['topics']=['轻盈','通勤','版型']
        second['groups']=[{'ids':['1'],'function':'开头'},{'ids':['2'],'function':'面料'},{'ids':['4'],'function':'通勤搭配'}]
        self.plan['groups'].append({'ids':['4'],'function':'通勤搭配'})
        ledger={'highlights':[
            {'id':'h1','point':'轻','source_ids':['1'],'by_plan':{
                '1':{'status':'入选','retained_ids':['1']},
                '2':{'status':'入选','retained_ids':['1']}}},
            {'id':'h2','point':'柔软','source_ids':['2'],'by_plan':{
                '1':{'status':'入选','retained_ids':['2']},
                '2':{'status':'入选','retained_ids':['2']}}},
            {'id':'h3','point':'归属不明','source_ids':['3'],'by_plan':{
                '1':{'status':'待核实','exception_kind':'商品归属不明','reason':'交叉讲解指代不清'},
                '2':{'status':'待核实','exception_kind':'商品归属不明','reason':'交叉讲解指代不清'}}},
            {'id':'h4','point':'通勤搭配','source_ids':['4'],'by_plan':{
                '1':{'status':'入选','retained_ids':['4']},
                '2':{'status':'入选','retained_ids':['4']}}}
        ]}
        plans=[self.plan,second]
        self.assertEqual(validate(self.doc,{'plans':plans},ledger),(4,6))
        answer=render_multi(self.doc,plans,1,ledger=ledger)
        self.assertIn('方案一',answer)
        self.assertIn('方案二',answer)
        self.assertNotIn('本版侧重点未选亮点',answer)
        self.assertIn('通勤搭配｜序号 4',answer)
        self.assertIn('作品话题：#一 #二 #三 #穿搭 #时尚营销',answer)
        self.assertEqual(answer.count('#穿搭'),2)
        self.assertEqual(answer.count('#时尚营销'),2)
        self.assertIn('```text\n2,1,4\n\n1,2,4\n```',answer)
        self.assertTrue(check_multi(answer,plans,ledger,self.doc))
        changed=answer.replace('作品话题：#轻盈 #通勤 #版型 #穿搭 #时尚营销',
                               '作品话题：#错误 #通勤 #版型 #穿搭 #时尚营销')
        with self.assertRaises(ValueError): check_multi(changed,plans,ledger,self.doc)

    def test_three_plan_renderer_and_limit(self):
        second=dict(self.plan); second['title']='二号标题'; second['topics']=['柔软','日常','保暖']
        second['groups']=[{'ids':['1','2'],'function':'第二开头'}]
        third=dict(self.plan); third['title']='三号标题'; third['topics']=['版型','通勤','搭配']
        third['groups']=[{'ids':['2'],'function':'第三开头'},{'ids':['1'],'function':'承接'}]
        plans=[self.plan,second,third]
        ledger={'highlights':[
            {'id':'h1','point':'轻','source_ids':['1'],'by_plan':{
                str(i):{'status':'入选','retained_ids':['1']} for i in range(1,4)}},
            {'id':'h2','point':'柔软','source_ids':['2'],'by_plan':{
                str(i):{'status':'入选','retained_ids':['2']} for i in range(1,4)}},
            {'id':'h3','point':'归属不明','source_ids':['3'],'by_plan':{
                str(i):{'status':'待核实','exception_kind':'商品归属不明','reason':'交叉讲解指代不清'} for i in range(1,4)}}
        ]}
        answer=render_multi(self.doc,plans,1,ledger=ledger)
        self.assertIn('方案三',answer)
        self.assertEqual(answer.count('#穿搭'),3)
        self.assertEqual(answer.count('#时尚营销'),3)
        self.assertIn('```text\n2,1\n\n1,2\n\n2,1\n```',answer)
        with self.assertRaises(ValueError): render_multi(self.doc,plans+[self.plan],1,ledger=ledger)

    def test_focus_omission_never_becomes_valid_with_a_cut_note(self):
        second=dict(self.plan)
        plans=[self.plan,second]
        ledger={'highlights':[
            {'id':'h1','point':'轻','source_ids':['1'],'by_plan':{
                '1':{'status':'入选','retained_ids':['1']},'2':{'status':'入选','retained_ids':['1']}}},
            {'id':'h2','point':'柔软','source_ids':['2'],'by_plan':{
                '1':{'status':'入选','retained_ids':['2']},'2':{'status':'侧重点省略','reason':'方案二聚焦版型，不讲面料触感'}}},
            {'id':'h3','point':'归属不明','source_ids':['3'],'by_plan':{
                '1':{'status':'待核实','exception_kind':'商品归属不明','reason':'交叉讲解指代不清'},
                '2':{'status':'待核实','exception_kind':'商品归属不明','reason':'交叉讲解指代不清'}}}
        ]}
        with self.assertRaises(ValueError): validate(self.doc,{'plans':plans},ledger)
        second['groups'][0]['note']='序号2保留相关原话；剪除侧重点之外的语句；回听句内剪点'
        with self.assertRaises(ValueError): validate(self.doc,{'plans':plans},ledger)

    def test_multi_answer_cli_round_trip(self):
        second=dict(self.plan); second['title']='二号标题'; second['topics']=['柔软','日常','保暖']
        second['groups']=[{'ids':['1'],'function':'开头'},{'ids':['2'],'function':'面料'},{'ids':['4'],'function':'搭配'}]
        self.plan['groups'].append({'ids':['4'],'function':'搭配'})
        plans=[self.plan,second]
        ledger={'highlights':[
            {'id':'h1','point':'轻','source_ids':['1'],'by_plan':{
                '1':{'status':'入选','retained_ids':['1']},'2':{'status':'入选','retained_ids':['1']}}},
            {'id':'h2','point':'柔软','source_ids':['2'],'by_plan':{
                '1':{'status':'入选','retained_ids':['2']},'2':{'status':'入选','retained_ids':['2']}}},
            {'id':'h3','point':'归属不明','source_ids':['3'],'by_plan':{
                '1':{'status':'待核实','exception_kind':'商品归属不明','reason':'交叉讲解指代不清'},
                '2':{'status':'待核实','exception_kind':'商品归属不明','reason':'交叉讲解指代不清'}}},
            {'id':'h4','point':'通勤搭配','source_ids':['4'],'by_plan':{
                '1':{'status':'入选','retained_ids':['4']},
                '2':{'status':'入选','retained_ids':['4']}}}
        ]}
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            snapshot=root/'snapshot.json'; batch=root/'plans.json'; ledger_path=root/'ledger.json'; answer=root/'answer.txt'
            snapshot.write_text(json.dumps(self.doc,ensure_ascii=False),encoding='utf-8')
            batch.write_text(json.dumps({'plans':plans,'recommended':1},ensure_ascii=False),encoding='utf-8')
            ledger_path.write_text(json.dumps(ledger,ensure_ascii=False),encoding='utf-8')
            answer.write_text(render_multi(self.doc,plans,1,ledger=ledger),encoding='utf-8')
            script=Path(__file__).resolve().parents[1]/'scripts'/'multi_plan.py'
            command=[sys.executable,'-S',str(script),'--snapshot',str(snapshot),'--plans',str(batch),
                     '--ledger',str(ledger_path),'--answer',str(answer)]
            result=subprocess.run(command,capture_output=True,text=True,encoding='utf-8',
                                  env={**os.environ,'PYTHONIOENCODING':'utf-8'})
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertIn('MULTI SERIAL CHECK PASS',result.stdout)
            answer.write_text(answer.read_text(encoding='utf-8').replace('1,4','4,1'),encoding='utf-8')
            rejected=subprocess.run(command,capture_output=True,text=True,encoding='utf-8',
                                    env={**os.environ,'PYTHONIOENCODING':'utf-8'})
            self.assertNotEqual(rejected.returncode,0)

if __name__=='__main__': unittest.main()
