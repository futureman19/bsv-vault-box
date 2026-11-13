from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
R=Path(__file__).resolve().parent;root=R.parents[1]
m=json.loads((R/'inventory.json').read_text());bad=[]
for rel,rec in m['files'].items():
 data=(R/rel).read_bytes()
 if len(data)!=rec['bytes'] or hashlib.sha256(data).hexdigest()!=rec['sha256']:bad.append(rel)
 if '--staged' in sys.argv:
  data=subprocess.check_output(['git','show',':'+(R/rel).relative_to(root).as_posix()],cwd=root)
  if len(data)!=rec['bytes'] or hashlib.sha256(data).hexdigest()!=rec['sha256']:bad.append('STAGED:'+rel)
with zipfile.ZipFile(R/'morocco-finish-v7-source.zip') as z:
 assert len(z.namelist())==len(set(z.namelist()))
 assert set(m['required_files'])<=set(z.namelist())
 for rel,rec in m['files'].items():
  if hashlib.sha256(z.read(rel)).hexdigest()!=rec['sha256']:bad.append('ZIP:'+rel)
 assert z.read('inventory.json')==(R/'inventory.json').read_bytes()
print('INVENTORY_FILES',len(m['files']),'INVENTORY_MISMATCHES',len(bad),'STAGED','--staged' in sys.argv)
assert not bad,bad
