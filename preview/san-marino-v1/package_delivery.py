from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
excluded={'inventory.json','delivery-check.json','san-marino-v1-source.zip','package-output.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__','.git']) and p.name not in excluded and p.suffix not in ['.blend1','.pyc'])
required={'san-marino.blend','san-marino.glb','san-marino-v1.html','poster.png','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json'}
assert required<={p.relative_to(R).as_posix() for p in files}
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'san-marino-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
 a.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())==set(inv)|{'inventory.json'}
 for name,v in inv.items():assert hashlib.sha256(a.read(name)).hexdigest()==v['sha256'] and len(a.read(name))==v['bytes']
assert inv['san-marino-v1.html']['bytes']<5000000
r={'status':'PASS','html_bytes':inv['san-marino-v1.html']['bytes'],'glb_bytes':inv['san-marino.glb']['bytes'],'payload_files':len(files),'archive_readback_verified':True,'zip_bytes':z.stat().st_size,'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'inventory_sha256':hashlib.sha256((R/'inventory.json').read_bytes()).hexdigest(),'excluded':'inventory and delivery envelopes are outside payload hashes; archive excludes itself/dependencies/backups/caches'}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
