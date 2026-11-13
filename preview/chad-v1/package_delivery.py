from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
excluded={'inventory.json','delivery-check.json','chad-v1-source.zip'}
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name not in excluded and not p.name.endswith('.blend1') and '__pycache__' not in p.parts and 'node_modules' not in p.parts)
required={'chad-v1.html','chad.glb','chad.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','fallback-check.json'}
assert required<={p.relative_to(R).as_posix() for p in files}
assert (R/'chad-v1.html').stat().st_size<5000000
s=json.loads((R/'source-check.json').read_text());assert not s['collisions'] and s['collision_samples']==81
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
for case in json.loads((R/'browser-check.json').read_text())[:2]:
 assert case['asset']['bytes']==(R/'chad.glb').stat().st_size
 assert not case['errors'] and not case['external_requests']
def record(data):return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
inv={p.relative_to(R).as_posix():record(p.read_bytes()) for p in files}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
zip_path=R/'chad-v1-source.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zip_path) as z:
 assert set(z.namelist())==set(inv)|{'inventory.json'}
 for name,rec in inv.items():assert record(z.read(name))==rec
r={'status':'PASS','html':record((R/'chad-v1.html').read_bytes()),'glb':record((R/'chad.glb').read_bytes()),'archive':record(zip_path.read_bytes()),'inventory_files':len(inv),'archive_readback':True,'required_artifacts_present':True}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
