from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
exclude={'inventory.json','delivery-check.json','malta-source.zip','verify-all.log','package-run.log'}
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name not in exclude and not any(x in p.parts for x in ['node_modules','__pycache__']) and not p.name.endswith('.blend1'))
h=lambda b:hashlib.sha256(b).hexdigest()
inv={p.relative_to(R).as_posix():dict(bytes=p.stat().st_size,sha256=h(p.read_bytes())) for p in files}
required={'malta-v1.html','malta.glb','malta.blend','mechanism.blend','design-brief.md','README.md','poster.png','poster.jpg','source-check.json','parity-check.json','browser-check.json','theme-source-check.json','extended-check.json','acceptance-check.json'}
assert required<=inv.keys();assert inv['malta-v1.html']['bytes']<5000000
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'malta-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
 for p in files+[R/'inventory.json']:f.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as f:
 assert set(f.namelist())==set(inv)|{'inventory.json'}
 for n,v in inv.items():assert h(f.read(n))==v['sha256'] and len(f.read(n))==v['bytes'],n
 assert f.read('inventory.json')==(R/'inventory.json').read_bytes()
out=dict(status='PASS',html_bytes=inv['malta-v1.html']['bytes'],glb_bytes=inv['malta.glb']['bytes'],inventory_files=len(inv),zip_bytes=z.stat().st_size,zip_sha256=h(z.read_bytes()),required_deliverables_verified=True,archive_readback=True)
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
