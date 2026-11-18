"""Extract only immutable assigned candidates; verify before inspection."""
from pathlib import Path
import subprocess,json,hashlib
R=Path(__file__).resolve().parent
REPO=R.parents[1]
d=json.loads((REPO/'launch/collection-repairs/dispositions.json').read_text())
ids=d['remaining_finish_queue']; assert len(ids)==20 and len(set(ids))==20
rows=[]
for r in d['records']:
 if r['id'] not in ids: continue
 e=r['original_review']; folder=R/'baseline'/r['id'];folder.mkdir(parents=True,exist_ok=True)
 for role in ['viewer','marketing']:
  v=e[role];data=subprocess.check_output(['git','show',v['commit']+':'+v['path']],cwd=REPO)
  assert hashlib.sha256(data).hexdigest()==v['sha256']
  (folder/Path(v['path']).name).write_bytes(data)
 row={'id':r['id'],'original_review':e,'viewer':str((folder/Path(e['viewer']['path']).name).relative_to(REPO))}
 rows.append(row)
(R/'baseline.json').write_text(json.dumps(rows,indent=2))
print('Verified and extracted',len(rows),'viewers and marketing images')
