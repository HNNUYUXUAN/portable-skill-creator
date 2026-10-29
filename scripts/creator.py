"""Portable Skill Creator: bounded local operations; no model API required."""
import argparse, ast, hashlib, json, os, platform, re, shutil, sys, tempfile, uuid
from pathlib import Path
from datetime import datetime, timezone

KINDS = {'bundle','rebuild','host','configure','input','unsupported'}
STATES = {'planned','executed','failed','unknown'}
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p,d):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_name(p.name+'.tmp')
    tmp.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    os.replace(tmp,p)
def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def clean(s):
    s=re.sub(r'https?://[^\s<>"]+', lambda m:m[0].split('?')[0].split('#')[0], str(s))
    s=re.sub(r'(?i)(bearer\s+)\S+',r'\1[REDACTED]',s)
    s=re.sub(r'(?i)((?:api[_-]?key|token|password|secret|authorization|cookie)\s*[=:]\s*)(?:"[^"]*"|\S+)',r'\1[REDACTED]',s)
    return s
def safe(root,rel):
    if not isinstance(rel,str) or not rel or '\\' in rel or ':' in rel:
        raise ValueError('Use package-relative forward-slash paths')
    p=(root/rel).resolve()
    if not p.is_relative_to(root.resolve()) or p==root.resolve(): raise ValueError('Path escapes package')
    # Reject reparse points even if their current target stays inside the package.
    q=root
    for part in Path(rel).parts:
        q=q/part
        if q.is_symlink() or (hasattr(q,'is_junction') and q.is_junction()): raise ValueError('Linked paths prohibited')
    return p
def allowed(rel):
    p=Path(rel)
    return not any(x in {'.git','.env','__pycache__','node_modules','.venv','sessions'} for x in p.parts) and p.suffix.lower() not in {'.pyc','.zip','.7z','.dll','.exe'} and not p.name.startswith('.env.')
def verify(root):
    root=Path(root).resolve(); errors=[]; m=read(root/'delivery.json')
    if m.get('schema_version')!=1: errors.append('Unsupported schema')
    if not m.get('name') or not m.get('version'): errors.append('Missing name/version')
    files=m.get('files',[])
    if not isinstance(files,list) or not all(isinstance(x,str) for x in files): raise ValueError('files must be a string list')
    if len(files)!=len(set(files)): errors.append('Duplicate files')
    for req in m.get('requirements',[]):
        if req.get('kind') not in KINDS or not req.get('id') or not req.get('handling'):
            errors.append('Incomplete requirement')
    for rel in files:
        try:
            p=safe(root,rel)
            if not allowed(rel): errors.append('Excluded file: '+rel)
            elif not p.is_file(): errors.append('Missing: '+rel)
            elif p.suffix=='.md':
                t=p.read_text(encoding='utf-8-sig')
                limit=4096 if rel=='SKILL.md' else 8192
                if len(t.encode('utf-8'))>limit: errors.append('Context limit: '+rel)
                for target in re.findall(r'\]\(([^)]+)\)',t):
                    if re.match(r'https?://',target) or target.startswith('#'): continue
                    target=target.split('#')[0]
                    resolved=(p.parent/target).resolve()
                    if not resolved.is_relative_to(root) or not resolved.is_file():
                        errors.append('Broken/outside link: '+rel+' -> '+target)
                    elif resolved.relative_to(root).as_posix() not in files:
                        errors.append('Link omitted from delivery: '+target)
        except (ValueError,UnicodeError) as e: errors.append(str(e)+': '+rel)
    if 'SKILL.md' not in files: errors.append('Missing entrypoint')
    for rel in files:
        if rel.startswith('references/zh-CN/'):
            other=rel.replace('references/zh-CN/','references/en/',1)
            if other not in files: errors.append('Missing language pair: '+rel)
            elif (root/rel).exists() and (root/other).exists():
                ids=lambda x:set(re.findall(r'\b[A-Z]{2,8}-\d+\b',(root/x).read_text(encoding='utf-8')))
                if ids(rel)!=ids(other): errors.append('Step IDs differ: '+rel)
    if not any(x.startswith('references/zh-CN/') for x in files): errors.append('Missing bilingual modules')
    return {'schema_version':1,'status':'pass' if not errors else 'fail','errors':errors,
            'scope':'structure_only','files':len(files)}

def inspect(root):
    root=Path(root); findings=[]
    if not root.is_dir(): raise ValueError('Skill directory not found')
    patterns={'absolute_path':r'[A-Za-z]:[\\/][^\s"\x27<>]+','dotenv':r'dotenv_values|load_dotenv',
              'windows_binary':r'videoeditor\.dll|win32|win-64|python\.exe',
              'cloud_service':r'dashscope|bailian|ASR_MODEL|TTS_MODEL',
              'external_process':r'subprocess\.|Start-Process',
              'dynamic_import':r'__import__|importlib\.'}
    for p in root.rglob('*'):
        if not p.is_file() or p.name.startswith('.env') or p.suffix not in {'.md','.py','.ps1','.yml','.txt'}: continue
        if any(x in {'.git','.venv','__pycache__'} for x in p.parts): continue
        if p.stat().st_size>512000: continue
        t=p.read_text(encoding='utf-8-sig',errors='replace')
        for n,line in enumerate(t.splitlines(),1):
            for kind,pattern in patterns.items():
                if re.search(pattern,line,re.I):
                    findings.append({'file':p.relative_to(root).as_posix(),'line':n,'type':kind,'evidence':'static'})
    return {'schema_version':1,'findings':findings,'coverage':'heuristic; review dynamic dependencies and external resources','executed':False}

def session(args):
    root=Path(args.path); log=root/'events.jsonl'
    if args.action=='start':
        root.mkdir(parents=True,exist_ok=False)
        write(root/'session.json',{'schema_version':1,'id':str(uuid.uuid4()),'goal':clean(args.goal),'status':'active','host':clean(args.host),'model':clean(args.model)})
        log.touch()
    elif args.action=='record':
        meta=read(root/'session.json')
        if meta['status']!='active': raise ValueError('Session already finished')
        incoming=read(args.event)
        if incoming.get('status') not in STATES: raise ValueError('Invalid event status')
        event={k:clean(incoming[k]) for k in ('step','status','summary','evidence','next','request_id') if k in incoming}
        event.update(id=str(uuid.uuid4()),time=datetime.now(timezone.utc).isoformat())
        with log.open('a',encoding='utf-8') as f: f.write(json.dumps(event,ensure_ascii=False)+'\n')
    events=[json.loads(x) for x in log.read_text(encoding='utf-8').splitlines() if x.strip()]
    unresolved=[x for x in events if x['status'] in {'unknown','planned','failed'}]
    # Historical uncertain events remain visible until caller checks evidence; never infer success.
    if args.action=='finish':
        meta=read(root/'session.json'); meta['status']='finished_with_gaps' if unresolved else 'finished'
        write(root/'session.json',meta)
    checkpoint={'schema_version':1,'session':read(root/'session.json'),'events':len(events),'unresolved':unresolved,'last':events[-1] if events else None}
    write(root/'checkpoint.json',checkpoint)
    return checkpoint

def doctor(args):
    m=read(Path(args.path)/'delivery.json'); checks=[]
    for req in m.get('requirements',[]):
        probe=req.get('probe',{}); state='not_verified'
        if probe.get('type')=='env_present':
            state='present' if os.environ.get(probe.get('name','')) else 'missing'
        elif probe.get('type')=='command':
            state='discovered_not_executed' if shutil.which(probe.get('name','')) else 'missing'
        checks.append({'id':req['id'],'state':state,'remedy':req['handling']})
    return {'schema_version':1,'status':'needs_setup' if any(c['state']=='missing' for c in checks) else 'partial',
            'python':platform.python_version(),'os':platform.platform(),'architecture':platform.machine(),
            'checks':checks,'cloud_api_called':False,'scope':'local_presence_only'}

def export(root,dest):
    root=Path(root).resolve(); dest=Path(dest).resolve()
    report=verify(root)
    if report['status']!='pass': raise ValueError(json.dumps(report))
    if dest.exists() or dest.is_relative_to(root): raise ValueError('Destination must be new and outside source')
    m=read(root/'delivery.json'); dest.parent.mkdir(parents=True,exist_ok=True)
    stage=Path(tempfile.mkdtemp(prefix='psc-',dir=dest.parent))
    try:
        for rel in m['files']:
            source=safe(root,rel); target=stage/rel; target.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(source,target)
        write(stage/'delivery.json',m)
        write(stage/'installed.json',{'schema_version':1,'version':m['version'],'hashes':{r:digest(stage/r) for r in m['files']}})
        os.replace(stage,dest)
    finally:
        if stage.exists(): shutil.rmtree(stage)
    return {'status':'exported','path':str(dest),'validation':'structure_only'}

def backup_base(target):
    return target.parent.parent/'skill-backups'/hashlib.sha256(str(target).encode()).hexdigest()[:16]
def upgrade(source,target):
    source=Path(source).resolve(); target=Path(target).resolve()
    installed=read(target/'installed.json')
    conflicts=[r for r,h in installed['hashes'].items() if not safe(target,r).exists() or digest(safe(target,r))!=h]
    new=read(source/'delivery.json')
    conflicts += [r for r in new['files'] if r not in installed['hashes'] and safe(target,r).exists()]
    if conflicts: return {'status':'conflict','files':sorted(set(conflicts))}
    base=backup_base(target); base.mkdir(parents=True,exist_ok=True)
    staged=base/'staged'; backup=base/'previous'
    if staged.exists() or backup.exists(): raise ValueError('Existing staging/backup must be reviewed first')
    export(source,staged)
    # Preserve receiver-only files, including configuration; these are never exported.
    for p in target.rglob('*'):
        if p.is_file():
            rel=p.relative_to(target).as_posix()
            if rel not in installed['hashes'] and rel not in {'installed.json','delivery.json'}:
                safe(target,rel)
                q=staged/rel
                if q.exists(): raise ValueError('Receiver file collision: '+rel)
                q.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,q)
    os.replace(target,backup)
    try: os.replace(staged,target)
    except Exception: os.replace(backup,target); raise
    return {'status':'updated','backup':str(backup)}
def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='command',required=True)
    for name in ('verify','inspect','doctor'):
        p=sub.add_parser(name); p.add_argument('path'); p.add_argument('--out')
    for name in ('export','upgrade'):
        p=sub.add_parser(name); p.add_argument('path'); p.add_argument('destination')
    p=sub.add_parser('rollback'); p.add_argument('path')
    p=sub.add_parser('session'); p.add_argument('action',choices=['start','record','resume','finish']); p.add_argument('path')
    p.add_argument('--goal',default=''); p.add_argument('--host',default='unknown'); p.add_argument('--model',default='unknown'); p.add_argument('--event')
    args=ap.parse_args()
    try:
        if args.command=='session': result=session(args)
        elif args.command=='verify': result=verify(args.path)
        elif args.command=='inspect': result=inspect(args.path)
        elif args.command=='doctor': result=doctor(args)
        elif args.command=='export': result=export(args.path,args.destination)
        elif args.command=='upgrade': result=upgrade(args.path,args.destination)
        else:
            p=Path(args.path).resolve(); b=backup_base(p)/'previous'; held=backup_base(p)/'rolled-back'
            if not b.exists() or held.exists(): raise ValueError('No backup or rollback destination occupied')
            os.replace(p,held)
            try: os.replace(b,p)
            except Exception: os.replace(held,p); raise
            result={'status':'rolled_back','retained':str(held)}
        if getattr(args,'out',None): write(args.out,result); print(json.dumps({'status':result.get('status','recorded'),'report':args.out}))
        else: print(json.dumps(result,ensure_ascii=True,indent=2))
        return 1 if result.get('status') in {'fail','conflict'} else 0
    except (ValueError,OSError,KeyError,json.JSONDecodeError) as e:
        print(json.dumps({'status':'error','message':clean(str(e))})); return 2
if __name__=='__main__': sys.exit(main())
