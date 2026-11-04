from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
exclude={'inventory.json','delivery-check.json','bolivia-v1-source.zip','setup.py'}
def digest(b):return hashlib.sha256(b).hexdigest()
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.name not in exclude and not p.name.endswith('.blend1'))
required={'bolivia.blend','bolivia.glb','bolivia-v1.html','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json'}
assert required<={p.relative_to(R).as_posix() for p in files}
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for p in files}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
zpath=R/'bolivia-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(inv)|{'inventory.json'}
 for n,v in inv.items():assert len(z.read(n))==v['bytes'] and digest(z.read(n))==v['sha256']
assert inv['bolivia-v1.html']['bytes']<5_000_000
out={'status':'PASS','html_bytes':inv['bolivia-v1.html']['bytes'],'glb_bytes':inv['bolivia.glb']['bytes'],'archive_bytes':zpath.stat().st_size,'archive_sha256':digest(zpath.read_bytes()),'inventory_entries':len(inv),'archive_readback_all_hashes':True,'required_artifacts_present':sorted(required)}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
