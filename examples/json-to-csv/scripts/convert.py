import csv,json,sys
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
