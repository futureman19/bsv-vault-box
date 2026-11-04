from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
excluded={'inventory.json','delivery-check.json','north-macedonia-v1-source.zip','package-output.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not {'node_modules','__pycache__'}&set(p.relative_to(R).parts) and p.name not in excluded and p.suffix!='.blend1')
names={p.relative_to(R).as_posix() for p in files}
assert {'north-macedonia-v1.html','north-macedonia.glb','north-macedonia.blend','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json','poster.png'}<=names
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'north-macedonia-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for p in files+[R/'inventory.json']:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())==names|{'inventory.json'}
 for n,v in inv.items():assert hashlib.sha256(a.read(n)).hexdigest()==v['sha256']
h=inv['north-macedonia-v1.html']['bytes'];g=inv['north-macedonia.glb']['bytes'];assert h<5000000
r={'status':'PASS','html_bytes':h,'glb_bytes':g,'inventory_entries':len(inv),'zip_bytes':z.stat().st_size,'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'archive_readback':True,'required_artifacts_present':True}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print('DELIVERY PASS',json.dumps(r))
