from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
H=lambda b:hashlib.sha256(b).hexdigest()
required={'slovenia.glb','slovenia.blend','slovenia-v1.html','design-brief.md','README.md','poster.png','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','motion-output.txt','.gitattributes'}
exclude={'inventory.json','delivery-check.json','slovenia-v1-source.zip','package-output.txt','git-evidence.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.name not in exclude and not p.name.endswith(('.blend1','.pyc')))
inventory={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':H(p.read_bytes())} for p in files};assert required<=inventory.keys()
assert inventory['slovenia-v1.html']['bytes']<5_000_000
s=json.loads((R/'source-check.json').read_text());assert not s['collisions'] and s['collision_samples']==81
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
for n in ['theme-check.json','extended-check.json']:assert json.loads((R/n).read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert len(b)==3
for c in b[:2]:assert not c['errors'] and not c['external_requests'] and c['open_close'] and c['reduced_motion']
(R/'inventory.json').write_text(json.dumps(inventory,indent=2))
z=R/'slovenia-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as a:
 for p in files+[R/'inventory.json']:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())==set(inventory)|{'inventory.json'}
 for name,item in inventory.items():assert H(a.read(name))==item['sha256'] and len(a.read(name))==item['bytes']
result={'status':'PASS','html_bytes':inventory['slovenia-v1.html']['bytes'],'glb_bytes':inventory['slovenia.glb']['bytes'],'zip_bytes':z.stat().st_size,'zip_sha256':H(z.read_bytes()),'inventory_sha256':H((R/'inventory.json').read_bytes()),'payload_files':len(inventory),'required_artifacts_present':True,'zip_readback_hashes_match':True,'excludes':'node_modules, caches, backup .blend1, inventory/ZIP/report self references'}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
