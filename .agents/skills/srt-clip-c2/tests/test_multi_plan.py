from pathlib import Path
import importlib.util, sys
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'scripts'))
spec=importlib.util.spec_from_file_location('multi_plan',root/'scripts/multi_plan.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
p={'groups':[{'ids':['1','2'],'function':'开头'}]}
p2={'groups':[{'ids':['2','1'],'function':'开头'}]}
p3={'groups':[{'ids':['3'],'function':'结尾'}]}
a=('三、成片方案\n方案一\n【1】甲\n【2】乙\n\n方案二\n【2】乙\n【1】甲\n'
   '四、作品标题与话题\n方案一\n作品标题：甲\n作品话题：#甲 #穿搭 #时尚营销\n\n'
   '方案二\n作品标题：乙\n作品话题：#乙 #穿搭 #时尚营销\n'
   '五、原始SRT序号（按成片播放顺序）\n方案一、方案二的序号依次如下：\n\n'
   '```text\n1,2\n\n2,1\n```')
assert m.check_multi(a,[p,p2])
for bad in [a.replace('1,2\n\n2,1\n```','2,1\n\n2,1\n```'),
            a.replace('【1】甲\n【2】乙','【2】乙\n【1】甲',1),
            a.replace('方案一、方案二的序号依次如下：',
                      '方案一、方案二的序号依次如下：\n\n```text\n额外代码框\n```')]:
    try: m.check_multi(bad,[p,p2])
    except ValueError: pass
    else: raise AssertionError('incorrect multi-plan sequence accepted')
a3=a.replace('四、作品标题与话题','方案三\n【3】丙\n四、作品标题与话题')
a3=a3.replace('五、原始SRT序号（按成片播放顺序）','方案三\n作品标题：丙\n作品话题：#丙 #穿搭 #时尚营销\n五、原始SRT序号（按成片播放顺序）')
a3=a3.replace('方案一、方案二的序号依次如下：','方案一、方案二、方案三的序号依次如下：')
a3=a3.replace('2,1\n```','2,1\n\n3\n```')
assert m.check_multi(a3,[p,p2,p3])
try: m.check_multi(a,[p,p2,p3,p])
except ValueError: pass
else: raise AssertionError('more than three plans accepted')
print('multi-plan checks PASS')
