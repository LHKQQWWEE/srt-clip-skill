from pathlib import Path
import importlib.util
root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('render',root/'scripts/render_compact.py'); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
p={'theme':'t','product_lines':['p'],'groups':[{'ids':['1'],'function':'f'}],'title':'t','topics':['a','b','c'],'subtitle_notes':[]}
def run(ms, allow=False):
 d={'filename':'x','count':1,'start':0,'end':ms,'input_type':'duration_text','rows':[{'id':'1','ord':0,'start':0,'end':ms,'duration_raw':str(ms/1000),'text':'原话'}]}
 return mod.render_compact(d,p,allow)
for source_ms,cls in [(36000,'short'),(36001,'complete'),(36002,'complete'),(53999,'complete'),(54000,'normal'),(108000,'normal'),(108002,'normal'),(144000,'normal'),(108002,'normal'),(144000,'normal')]:
 if cls=='short':
  try: run(source_ms)
  except ValueError: pass
  else: raise AssertionError(('short accepted',source_ms))
  assert '短候选' in run(source_ms,True)
 else:
  result=run(source_ms)
  assert '最佳成片方案' in result and ('短候选' not in result),source_ms
  if cls=='complete': assert '不足45秒' in result
for source_ms in (144002,180000,360000):
 result=run(source_ms)
 assert '最佳成片方案' in result and '短候选' not in result,source_ms
print('duration boundaries PASS')


