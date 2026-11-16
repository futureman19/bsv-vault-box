"""Exact-byte portable source package. Inventory excludes its own envelope."""
from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
excluded={'inventory.json','delivery-check.json','remote-verification.json'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(s in ['node_modules','__pycache__'] for s in p.parts) and p.name not in excluded and p.suffix not in ['.zip','.blend1','.pyc'])
required={'united-states-flag-v2.html','united-states.glb','united-states.blend','mechanism.blend','author.py','maps.py','viewer.js','fireworks.js','poster.png','poster.jpg','README.md','package-lock.json','verify_source.py','verify_browser.py'}
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files};assert required<=inv.keys();assert inv['united-states-flag-v2.html']['bytes']<5_000_000
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
zp=R/'united-states-flag-v2-source.zip'
with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zp) as z:
 names=z.namelist();assert len(names)==len(set(names));assert required<=set(names);assert all(not n.startswith('/') and '..' not in Path(n).parts for n in names)
 for n,r in inv.items():b=z.read(n);assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],n
 assert json.loads(z.read('inventory.json'))==inv
report={'PASS':True,'required_artifacts':sorted(required),'payload_entries':len(inv),'zip_entries':len(names),'zip_bytes':zp.stat().st_size,'zip_sha256':hashlib.sha256(zp.read_bytes()).hexdigest(),'html_bytes':inv['united-states-flag-v2.html']['bytes'],'glb_bytes':inv['united-states.glb']['bytes'],'blend_bytes':inv['united-states.blend']['bytes']}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
