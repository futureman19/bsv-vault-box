from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
files=[p for p in R.rglob('*') if p.is_file() and 'node_modules' not in p.parts and '__pycache__' not in p.parts and p.suffix not in ['.blend1','.zip'] and p.name not in ['inventory.json','delivery-check.json']]
required={'czechia.blend','czechia.glb','czechia-v1.html','poster.png','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json'}
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(files)}
assert required<=inv.keys();assert inv['czechia-v1.html']['bytes']<5000000
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'czechia-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as out:
 for p in files+[R/'inventory.json']:out.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as src:
 assert set(src.namelist())==set(inv)|{'inventory.json'}
 for n,d in inv.items():assert sha(src.read(n))==d['sha256']
r={'status':'PASS','html_bytes':inv['czechia-v1.html']['bytes'],'glb_bytes':inv['czechia.glb']['bytes'],'inventory_count':len(inv),'archive_bytes':z.stat().st_size,'archive_sha256':sha(z.read_bytes()),'zip_readback':True,'required_artifacts_present':True}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
