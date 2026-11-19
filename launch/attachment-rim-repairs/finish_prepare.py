"""Immutable ten-target continuation inputs; never rewrites old checkpoints."""
import json, subprocess, hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2]
D=R/'launch/attachment-rim-repairs/finish';D.mkdir(exist_ok=True)
ledger=json.loads((R/'launch/attachment-rim-repairs/continuation-ledger-v2.json').read_text())
rows=[]
for slug in ledger['remaining_ids']:
 r=next(x for x in ledger['records'] if x['id']==slug)
 prefix=str(Path(r['viewer']['path']).parent).replace('\\','/')+'/'
 root=D/slug;root.mkdir(exist_ok=True)
 records=[]
 for name in subprocess.check_output(['git','ls-tree','-r','--name-only',r['source_commit'],'--',prefix],cwd=R,text=True).splitlines():
  rel=name[len(prefix):]
  if rel.endswith(('.zip','.blend1')):continue
  data=subprocess.check_output(['git','show',f"{r['source_commit']}:{name}"],cwd=R)
  dest=root/'original'/rel;dest.parent.mkdir(parents=True,exist_ok=True)
  if dest.exists():assert dest.read_bytes()==data
  else:dest.write_bytes(data)
  records.append({'path':rel,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
 viewer=root/'original'/Path(r['viewer']['path']).name
 assert hashlib.sha256(viewer.read_bytes()).hexdigest()==r['viewer']['sha256']
 (root/'immutable-source.json').write_text(json.dumps({'commit':r['source_commit'],'prefix':prefix,'files':records},indent=2))
 (root/'original-review.json').write_text(json.dumps(r['original_record'],indent=2))
 rows.append({'id':slug,'root':str(root.relative_to(R)).replace('\\','/'),'viewer':str(viewer.relative_to(R)).replace('\\','/'),'commit':r['source_commit']})
 print(slug,len(records),flush=True)
(D/'targets.json').write_text(json.dumps(rows,indent=2))
(D/'.gitattributes').write_text('* -text\n')
(D/'.gitignore').write_text('**/node_modules/\n**/__pycache__/\n*.blend1\n')
