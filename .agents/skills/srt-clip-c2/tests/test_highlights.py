import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'check_highlights.py'

class HighlightCheckTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.snapshot = {'rows': [{'id': str(i), 'text': text} for i, text in [(1,'轻'),(2,'软'),(3,'柔软'),(4,'特殊功能')]]}
        self.plans = {'plans': [{'groups': [{'ids': ['1','2']}]}]}
        self.ledger = {'highlights': [
            {'id':'h1','point':'轻','source_ids':['1'],'status':'入选','retained_ids':['1']},
            {'id':'h2','point':'软','source_ids':['2'],'status':'入选','retained_ids':['2']},
            {'id':'h3','point':'柔软','source_ids':['3'],'status':'合并','merged_into':'h2','retained_ids':['2'],'reason':'与h2语义相同'},
            {'id':'h4','point':'功能','source_ids':['4'],'status':'待核实','exception_kind':'商品归属不明','reason':'需要核对商品归属依据'}
        ]}

    def tearDown(self):
        self.tmp.cleanup()

    def run_check(self):
        for name, obj in [('snapshot', self.snapshot), ('plans', self.plans), ('ledger', self.ledger)]:
            (self.root / (name+'.json')).write_text(json.dumps(obj,ensure_ascii=False),encoding='utf-8')
        return subprocess.run([sys.executable,'-S',str(SCRIPT),'--snapshot',str(self.root/'snapshot.json'),'--plans',str(self.root/'plans.json'),'--ledger',str(self.root/'ledger.json')],capture_output=True,text=True,encoding='utf-8')

    def test_complete_records_pass(self):
        r=self.run_check();self.assertEqual(r.returncode,0,r.stderr)

    def test_missing_or_nonexistent_sources_fail(self):
        for ids in ([],['99']):
            self.ledger['highlights'][0]['source_ids']=ids
            self.assertNotEqual(self.run_check().returncode,0)

    def test_selected_must_be_in_plan_and_source(self):
        self.ledger['highlights'][0]['retained_ids']=['4']
        self.assertNotEqual(self.run_check().returncode,0)

    def test_merged_target_must_exist_and_retain_target_source(self):
        self.ledger['highlights'][2]['merged_into']='unknown'
        self.assertNotEqual(self.run_check().returncode,0)
        self.ledger['highlights'][2]['merged_into']='h1'
        self.assertNotEqual(self.run_check().returncode,0)

    def test_nonselected_need_specific_reason(self):
        for reason in ('','精简','重复','时长'):
            self.ledger['highlights'][3]['reason']=reason
            self.assertNotEqual(self.run_check().returncode,0)

    def test_empty_duplicate_or_unrecognized_status_fail(self):
        self.ledger['highlights']=[]
        self.assertNotEqual(self.run_check().returncode,0)
        self.ledger['highlights']=[{'id':'x','point':'a','source_ids':['1'],'status':'unknown'}]
        self.assertNotEqual(self.run_check().returncode,0)
        self.ledger['highlights']=[{'id':'x','point':'a','source_ids':['1'],'status':'入选','retained_ids':['1']},{'id':'x','point':'b','source_ids':['2'],'status':'入选','retained_ids':['2']}]
        self.assertNotEqual(self.run_check().returncode,0)

if __name__=='__main__':
    unittest.main()

