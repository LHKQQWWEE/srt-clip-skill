from pathlib import Path
import importlib.util, sys
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'scripts'))
spec=importlib.util.spec_from_file_location('multi_plan',root/'scripts/multi_plan.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
p={'groups':[{'ids':['1','2'],'function':'开头'}]}
a='三、成片方案\n方案一\n【1】甲\n【2】乙\n四、作品标题与话题\n五、原始SRT序号\n```text\n1,2\n```'
assert m.check_multi(a,[p])
for bad in [a.replace('1,2\n```','2,1\n```'), a.replace('【1】甲\n【2】乙','【2】乙\n【1】甲')]:
 try: m.check_multi(bad,[p])
 except ValueError: pass
 else: raise AssertionError('incorrect sequence accepted')
try: m.check_multi(a,[p,p])
except ValueError: pass
else: raise AssertionError('multiple plans accepted')
print('single plan checks PASS')
