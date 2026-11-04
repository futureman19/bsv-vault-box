from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
excluded={'inventory.json','delivery-check.json','south-korea-v1-source.zip'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.name not in excluded and not p.name.endswith('.blend1'))
required={'south-korea.blend','south-korea.glb','south-korea-v1.html','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json'}
assert required<={p.relative_to(R).as_posix() for p in files}
sha=lambda b:hashlib.sha256(b).hexdigest()
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
assert inv['south-korea-v1.html']['bytes']<5_000_000
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'south-korea-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
 for p in files+[R/'inventory.json']:f.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as f:
 assert set(f.namelist())==set(inv)|{'inventory.json'}
 for name,data in inv.items():assert sha(f.read(name))==data['sha256']
out={'status':'PASS','html_bytes':inv['south-korea-v1.html']['bytes'],'glb_bytes':inv['south-korea.glb']['bytes'],'files':len(inv),'archive_bytes':z.stat().st_size,'archive_sha256':sha(z.read_bytes()),'required_artifacts_present':True,'archive_readback_verified':True}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
