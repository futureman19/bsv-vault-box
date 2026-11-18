from pathlib import Path
import sys,json,subprocess,zipfile,io,hashlib
R=Path(__file__).resolve().parent;REPO=R.parents[1]
sys.path.insert(0,str(REPO/'launch/collection-repairs'))
from package_repairs import safe_names,old_inventory
out=[]
for row in json.loads((R/'baseline.json').read_text()):
 e=row['original_review'];checks=[]
 for a in e['source_archives']:
  raw=subprocess.check_output(['git','show',a['commit']+':'+a['path']],cwd=REPO)
  assert hashlib.sha256(raw).hexdigest()==a['sha256'] and len(raw)==a['bytes']
  with zipfile.ZipFile(io.BytesIO(raw)) as z:
   safe_names(z.namelist());assert z.testzip() is None
   files={n:z.read(n) for n in z.namelist()}
  inv=old_inventory(files);matches=[]
  for f in [e['viewer'],*e.get('source_models',e.get('model_sources',[]))]:
   name=Path(f['path']).name;assert name in files
   data=files[name];assert hashlib.sha256(data).hexdigest()==f['sha256'],(row['id'],name)
   matches.append(name)
  checks.append({'archive':a,'members':len(files),'fresh_inventory':inv,'exact_selected_payloads':matches})
 out.append({'id':row['id'],'archives':checks,'pass':True})
 (R/'source-package-check.json').write_text(json.dumps(out,indent=2));print(row['id'],len(files),flush=True)
assert len(out)==20
