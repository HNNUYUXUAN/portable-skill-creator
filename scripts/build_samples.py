"""Maintainer: assemble independent samples and explicit delivery manifests."""
import json, shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def put(p,t):
    p.parent.mkdir(parents=True,exist_ok=True); p.write_text(t,encoding='utf-8')
def manifest(p,name,requirements=[]):
    shutil.copy2(ROOT/'LICENSE',p/'LICENSE')
    files=sorted(x.relative_to(p).as_posix() for x in p.rglob('*') if x.is_file() and x.name not in {'delivery.json','installed.json'} and '__pycache__' not in x.parts)
    put(p/'delivery.json',json.dumps(dict(schema_version=1,name=name,version='0.1.0-dev',files=files,requirements=requirements),ensure_ascii=False,indent=2)+'\n')
tasks={
 'note-triage':(
 '将输入条目按明确标记 TODO、DONE、BLOCKED 分组，保留原文和顺序；未标记项放 unknown。不得推断完成。',
 'Group input items by explicit TODO, DONE and BLOCKED markers, preserving text and order. Unmarked items go to unknown; never infer completion.'),
 'json-to-csv':(
 '从技能根运行 PYTHON scripts/convert.py INPUT OUTPUT，其中 PYTHON 替换为 bootstrap 返回的解释器路径；输入是对象数组，每项必须仅有 name 和 count，name 为字符串，count 为非负整数且不是布尔值。输出 UTF-8 CSV。拒绝覆盖已有输出，先完整验证所有输入。',
 'Run PYTHON scripts/convert.py INPUT OUTPUT from this skill root; replace PYTHON with the executable returned by bootstrap. Input is an object array; each object has only name and count, with string name and nonnegative integer count, excluding booleans. Write UTF-8 CSV. Refuse existing outputs and validate all input first.'),
 'page-evidence':(
 '通过宿主已连接浏览器读取用户指定公开网址，记录最终URL、页面标题、一个可直接核对的事实和读取时间。使用真实页面证据；连接不可用时记录受阻，不用搜索摘要冒充浏览器读取。不需要登录的页面成功不代表登录权限验证。',
 'Read the user-specified public URL using the connected host browser. Record final URL, title, one directly verifiable fact and observation time. Use actual page evidence; report blocked if disconnected, never substitute search snippets. A public page does not validate login permissions.')
}
for name,(zh,en) in tasks.items():
    p=ROOT/'examples'/name
    put(p/'SKILL.md',f'---\nname: {name}\ndescription: {en.split(".")[0]}. {zh.split("。")[0]}。\n---\n# {name}\n\nChoose one language / 选择一种语言：\n\n- [中文](references/zh-CN/task.md)\n- [English](references/en/task.md)\n')
    for lang,t in [('zh-CN',zh),('en',en)]: put(p/'references'/lang/'task.md','# Task\n\nDEMO-1\n\n'+t+'\n')
    manifest(p,name,[dict(id='browser',kind='host',handling='Use the recipient host browser connector; verify actual page access')] if name=='page-evidence' else [])
p=ROOT/'examples'/'json-to-csv'
put(p/'scripts'/'convert.py',"""import csv,json,sys
from pathlib import Path
try:
    if len(sys.argv)!=3: raise ValueError('Usage: PYTHON scripts/convert.py INPUT OUTPUT')
    src,dst=map(Path,sys.argv[1:])
    if dst.exists(): raise ValueError('Output already exists; choose a new output path. Existing file preserved.')
    rows=json.loads(src.read_text(encoding='utf-8-sig'))
    if not isinstance(rows,list): raise ValueError('Expected array')
    for r in rows:
        if not isinstance(r,dict) or set(r)!={'name','count'} or not isinstance(r['name'],str) or type(r['count']) is not int or r['count']<0: raise ValueError('Invalid row')
    with dst.open('x',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['name','count']); w.writeheader(); w.writerows(rows)
except (ValueError,OSError) as error:
    print(str(error),file=sys.stderr); sys.exit(2)
""")
put(p/'examples'/'input.json','[{"name":"中文, item","count":2},{"name":"second","count":0}]\n')
shutil.copy2(ROOT/'scripts/bootstrap.ps1',p/'scripts/bootstrap.ps1')
(p/'assets').mkdir(exist_ok=True)
shutil.copy2(ROOT/'assets/runtime.json',p/'assets/runtime.json')
for lang in ['zh-CN','en']:
    q=p/'references'/lang/'task.md'
    with q.open('a',encoding='utf-8') as f:
        f.write('\nRun scripts/bootstrap.ps1 -Prepare to discover/create Python 3.12; use the returned executable. / 先运行 scripts/bootstrap.ps1 -Prepare，使用返回的解释器执行转换。\n')
manifest(p,'json-to-csv',[dict(id='python',kind='rebuild',handling='Run scripts/bootstrap.ps1 -Prepare. This stdlib-only sample needs no pip dependencies.',probe=dict(type='command',name='python'))])
put(ROOT/'examples'/'note-triage'/'examples'/'input.txt','TODO: review file\nDONE: save source\nBLOCKED: missing login\ncheck tomorrow\n')
manifest(ROOT/'examples'/'note-triage','note-triage')
files=sorted(x.relative_to(ROOT).as_posix() for folder in ['references','assets','examples'] for x in (ROOT/folder).rglob('*') if x.is_file() and '__pycache__' not in x.parts)
files+=['SKILL.md','scripts/creator.py','scripts/bootstrap.ps1','LICENSE']
put(ROOT/'delivery.json',json.dumps(dict(schema_version=1,name='portable-skill-creator',version='0.1.0-dev',files=sorted(files),requirements=[dict(id='python',kind='rebuild',handling='Run scripts/bootstrap.ps1 -Prepare, or pass -Python with Python 3.12.'),dict(id='host-files',kind='host',handling='Host must read/write task files and run commands; browser only for browser tasks.')]),ensure_ascii=False,indent=2)+'\n')
print('Built sample directories and allowlists')
