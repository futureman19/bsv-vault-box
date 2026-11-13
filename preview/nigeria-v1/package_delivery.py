from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
excluded={'inventory.json','delivery-check.json','nigeria-v1-source.zip'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.suffix!='.blend1' and p.name not in excluded)
def digest(b):return hashlib.sha256(b).hexdigest()
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for p in files}
required={'nigeria.blend','nigeria.glb','nigeria-v1.html','poster.png','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','source-theme-check.json','maps/indigo-color.png','maps/indigo-roughness.png','maps/indigo-normal.png'}
assert required<=inv.keys();assert inv['nigeria-v1.html']['bytes']<5000000
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'nigeria-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as out:
 for p in files+[R/'inventory.json']:out.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as f:
 assert set(f.namelist())==set(inv)|{'inventory.json'}
 for n,v in inv.items():assert len(f.read(n))==v['bytes'] and digest(f.read(n))==v['sha256']
result={'status':'PASS','html_bytes':inv['nigeria-v1.html']['bytes'],'glb_bytes':inv['nigeria.glb']['bytes'],'inventory_files':len(inv),'archive_readback':True,'archive_bytes':z.stat().st_size,'archive_sha256':digest(z.read_bytes())}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
