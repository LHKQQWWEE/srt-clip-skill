"""Portable basic source safety tests, no private user data embedded."""
import copy, json, subprocess, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
import srt_fast

class Regression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory()
        cls.srt=Path(cls.tmp.name)/'synthetic.srt'
        cls.srt.write_text(''.join(f'{i}\n00:00:{i-1:02d},000 --> 00:00:{i:02d},000\n原话{i}\n\n' for i in range(1,51)),encoding='utf8')
        cls.doc=srt_fast.parse_once(cls.srt)
        cls.plan={'groups':[{'ids':list(range(1,51)), 'function':'合成测试，仅检验映射'}], 'theme':'合成主题', 'product_lines':['合成商品'], 'title':'合成标题','topics':['A','B','C'],'subtitle_notes':[]}

    @classmethod
    def tearDownClass(cls): cls.tmp.cleanup()

    def test_full_five_parts(self):
        out=srt_fast.render(self.doc,self.plan)
        for h in ['一、文件解析结果','二、商品识别','三、最佳成片方案','四、作品标题与话题','五、原始SRT序号']:
            self.assertIn(h,out)
        self.assertEqual(out.splitlines()[-1],','.join(map(str,range(1,51))))

    def test_source_reconstruction(self):
        out=srt_fast.render(self.doc,self.plan)
        self.assertIn('1 | 00:00:00,000 --> 00:00:01,000 | 原话1',out)
        self.assertIn('50 | 00:00:49,000 --> 00:00:50,000 | 原话50',out)

    def test_duration_guard(self):
        p=copy.deepcopy(self.plan);p['groups'][0]['ids']=[1,2,3]
        with self.assertRaisesRegex(ValueError,'45–90'):srt_fast.render(self.doc,p)

    def test_missing_id_guard(self):
        p=copy.deepcopy(self.plan);p['groups'][0]['ids']=[123]
        with self.assertRaisesRegex(ValueError,'absent'):srt_fast.render(self.doc,p)

    def test_duplicate_id_guard(self):
        p=copy.deepcopy(self.plan);p['groups'].append(copy.deepcopy(p['groups'][0]))
        with self.assertRaisesRegex(ValueError,'Repeated'):srt_fast.render(self.doc,p)

    def test_original_dup_id_guard(self):
        f=Path(self.tmp.name)/'duplicates.srt';f.write_text('1\n00:00:00,000 --> 00:00:01,000\nA\n\n1\n00:00:02,000 --> 00:00:03,000\nB')
        with self.assertRaisesRegex(ValueError,'Duplicate'):srt_fast.parse_once(f)

    def test_original_bad_time_guard(self):
        f=Path(self.tmp.name)/'badtime.srt';f.write_text('1\n00:00:03,000 --> 00:00:01,000\nA')
        with self.assertRaisesRegex(ValueError,'Nonpositive'):srt_fast.parse_once(f)

    def test_multigoods_index_preserved(self):
        f=Path(self.tmp.name)/'multigoods.srt';f.write_text('1\n00:00:00,000 --> 00:00:01,000\n长裙\n\n2\n00:00:01,000 --> 00:00:02,000\n耳环\n\n3\n00:00:02,000 --> 00:00:03,000\n长裙\n',encoding='utf8')
        self.assertEqual([r['text'] for r in srt_fast.parse_once(f)['rows']],['长裙','耳环','长裙'])

    def test_multiline_exact(self):
        f=Path(self.tmp.name)/'multiline.srt';f.write_text('1\n00:00:00,000 --> 00:00:01,000\n第一行\n第二行\n',encoding='utf8')
        self.assertEqual(srt_fast.parse_once(f)['rows'][0]['text'],'第一行\n第二行')

if __name__=='__main__':unittest.main(verbosity=2)

