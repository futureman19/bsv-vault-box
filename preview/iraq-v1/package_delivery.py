"""Bounded local delivery gate, no publishing. Inventory excludes itself/envelopes."""
from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
def h(b):return hashlib.sha256(b).hexdigest()
required={'iraq.blend','iraq.glb','iraq-v1.html','poster.png','poster.jpg','mechanism.blend','README.md','design-brief.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','author.py','maps.py','build.py','motion.mjs','viewer.js','template.html'}
assert all((R/n).is_file() for n in required)
s=json.loads((R/'source-check.json').read_text());assert s['collision_samples']==81 and not s['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert len(b)==3 and all(not r['errors'] and not r['external_requests'] for r in b[:2])
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
assert (R/'iraq-v1.html').stat().st_size<5000000
excluded={'inventory.json','delivery-check.json','iraq-v1-source.zip','package-output.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name not in excluded and not p.name.endswith(('.blend1','.pyc')) and '__pycache__' not in p.parts)
inventory={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':h(p.read_bytes())} for p in files}
assert required<=set(inventory)
(R/'inventory.json').write_text(json.dumps(inventory,indent=2))
z=R/'iraq-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
 for p in files+[R/'inventory.json']:f.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as f:
 assert set(f.namelist())==set(inventory)|{'inventory.json'}
 for n,v in inventory.items():assert len(f.read(n))==v['bytes'] and h(f.read(n))==v['sha256']
result={'status':'PASS','html_bytes':(R/'iraq-v1.html').stat().st_size,'glb_bytes':(R/'iraq.glb').stat().st_size,'inventory_entries':len(inventory),'archive_bytes':z.stat().st_size,'archive_sha256':h(z.read_bytes()),'archive_readback':True,'required_artifacts_present':True,'inventory_sha256':h((R/'inventory.json').read_bytes())}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
