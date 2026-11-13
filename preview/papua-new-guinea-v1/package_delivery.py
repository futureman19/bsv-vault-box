"""Exact-byte package, explicit required-set and archive readback gate."""
from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
required={'papua-new-guinea-v1.html','papua-new-guinea.glb','papua-new-guinea.blend','mechanism.blend','design-brief.md','README.md','author.py','maps.py','build.py','viewer.js','motion.mjs','template.html','poster.png','poster.jpg','source-check.json','parity-check.json','browser-check.json','extended-check.json','theme-source-check.json','desktop-closed.png','desktop-open.png','mobile-closed.png','mobile-open.png','maps/fibre-color.png','maps/fibre-roughness.png','maps/fibre-normal.png','.gitattributes'}
exclude={'inventory.json','delivery-check.json','papua-new-guinea-v1-source.zip','package-output.txt','git-verification.txt'}
paths=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.relative_to(R).parts for x in ['node_modules','__pycache__','.git']) and p.name not in exclude and not p.name.endswith(('.blend1','.pyc')))
records={str(p.relative_to(R)).replace('\\','/'):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths}
assert required<=records.keys(),required-records.keys()
assert records['papua-new-guinea-v1.html']['bytes']<5_000_000
for check in ['theme-source-check.json','extended-check.json']:assert json.loads((R/check).read_text())['status']=='PASS'
s=json.loads((R/'source-check.json').read_text());assert s['collision_samples']==81 and not s['collisions']
p=json.loads((R/'parity-check.json').read_text());assert p['source_and_export_geometry_match'] and max(p['source_to_glb_max'],p['glb_to_source_max'])<1e-5
b=json.loads((R/'browser-check.json').read_text());assert len(b)==3 and all(not c['external_requests'] and not c['errors'] and c['open_close'] and c['reduced_motion'] for c in b[:2]) and b[2]['fallback']
(R/'inventory.json').write_text(json.dumps(records,indent=2),encoding='utf8')
z=R/'papua-new-guinea-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as f:
 for n in records:f.write(R/n,n)
 f.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(z) as f:
 assert set(f.namelist())==set(records)|{'inventory.json'}
 for n,v in records.items():
  data=f.read(n);assert len(data)==v['bytes'] and hashlib.sha256(data).hexdigest()==v['sha256'],n
 assert f.read('inventory.json')==(R/'inventory.json').read_bytes()
r={'status':'PASS','html_bytes':records['papua-new-guinea-v1.html']['bytes'],'glb_bytes':records['papua-new-guinea.glb']['bytes'],'payload_files':len(records),'required_files':len(required),'exact_archive_inventory_and_hashes':True,'zip_bytes':z.stat().st_size,'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'inventory_sha256':hashlib.sha256((R/'inventory.json').read_bytes()).hexdigest(),'exclusions':sorted(exclude),'note':'Local package only; inventory excludes envelopes to avoid circular hashing.'}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
