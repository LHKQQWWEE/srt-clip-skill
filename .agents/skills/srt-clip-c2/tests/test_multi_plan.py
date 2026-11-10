from pathlib import Path
import importlib.util, sys
p = Path(__file__).resolve().parents[1] / 'scripts' / 'multi_plan.py'
sys.path.insert(0, str(p.parent))
spec = importlib.util.spec_from_file_location('multi_plan', p)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
base = {'groups':[{'ids':[1,2], 'function':'开头'}]}
plans = [base, {'groups':[{'ids':[2,1], 'function':'开头'}]}]
answer = '三、成片方案\n方案一\n【1】甲\n【2】乙\n方案二\n【2】乙\n【1】甲\n四、作品标题与话题\n五、原始SRT序号\n方案一推荐，方案二\n```text\n1,2\n\n2,1\n```'
assert m.check_multi(answer, plans)
for bad in [answer.replace('2,1\n```','1,2\n```'), answer.replace('【2】乙\n【1】甲','【1】甲\n【2】乙'), answer.replace('1,2\n\n2,1','1,2\n2,1'), answer.replace('```text','```text\n方案一')]:
    try: m.check_multi(bad, plans)
    except ValueError: pass
    else: raise AssertionError('invalid answer accepted')
print('multi checks PASS')
