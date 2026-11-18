"""Extract exact immutable sources into new continuation folders."""
import json,subprocess,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2]
ledger=json.loads((R/'launch/attachment-rim-repairs/continuation-ledger.json').read_text())
for slug in ['algeria','guyana']:
 r=next(r for r in ledger['records'] if r['id']==slug); dest=R/'preview'/f'{slug}-repair-v2'; dest.mkdir(exist_ok=False)
 prefix=f'preview/{slug}-v1/'
 names=subprocess.check_output(['git','ls-tree','-r','--name-only',r['source_commit'],'--',prefix],cwd=R,text=True).splitlines()
 records=[]
 for name in names:
  rel=name[len(prefix):]
  if rel.endswith(('.zip','.blend1')):continue
  data=subprocess.check_output(['git','show',f"{r['source_commit']}:{name}"],cwd=R)
  p=dest/'historical-v1'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
  records.append({'path':rel,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
 assert hashlib.sha256((dest/'historical-v1'/f'{slug}-v1.html').read_bytes()).hexdigest()==r['viewer']['sha256']
 (dest/'.gitattributes').write_text('* -text\n');(dest/'.gitignore').write_text('node_modules/\n*.blend1\n__pycache__/\n')
 (dest/'immutable-source.json').write_text(json.dumps({'commit':r['source_commit'],'files':records},indent=2))
 print(slug,len(records))
