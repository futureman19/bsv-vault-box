"""Stage the explicit new delivery payloads; independently verify indexed bytes."""
from pathlib import Path
import subprocess,json,hashlib,zipfile
R=Path(__file__).resolve().parents[2];out=R/'launch/attachment-rim-repairs';rows=json.loads((out/'resume-package-check.json').read_text());names=set()
for row in rows:names.update(row['inventory'])
for p in out.glob('resume*'):
 if p.is_file():names.add(p.relative_to(R).as_posix())
for n in ['README.md','OWNER-DECISIONS.md','.gitignore','continuation-ledger-v2.json','CONTINUATION-2.md','algeria-repair-v2-source.zip','guyana-repair-v2-source.zip','algeria-recovered-desktop-open.png','algeria-recovered-mobile-open.png','guyana-recovered-desktop-open.png','guyana-recovered-mobile-open.png']:
 names.add((out/n).relative_to(R).as_posix())
for start in range(0,len(names),40):subprocess.run(['git','add','-f','--',*sorted(names)[start:start+40]],cwd=R,check=True)
count=0
for row in rows:
 with zipfile.ZipFile(out/row['zip']) as z:
  inv=json.loads(z.read('INVENTORY.json'));assert inv==row['inventory']
  for name,v in inv.items():
   b=z.read(name);staged=subprocess.check_output(['git','show',':'+name],cwd=R)
   assert hashlib.sha256(b).hexdigest()==hashlib.sha256(staged).hexdigest()==v['sha256'];assert len(b)==len(staged)==v['bytes'];count+=1
# Frozen previous art and packages must not appear in the diff.
changed=subprocess.check_output(['git','diff','--cached','--name-only'],cwd=R,text=True).splitlines()
assert not any(p.startswith(('docs/','preview/ghana-repair-v2/','preview/chile-repair-v2/','launch/collection-repairs/')) for p in changed)
assert not any(p.endswith(('.blend1','.env')) or '/node_modules/' in p for p in changed)
assert not any(p.endswith(('ghana-repair-v2-source.zip','chile-repair-v2-source.zip')) for p in changed)
print(json.dumps({'archive_index_payload_comparisons':count,'staged_files':len(changed),'frozen_prior_assets_unchanged':True}))
