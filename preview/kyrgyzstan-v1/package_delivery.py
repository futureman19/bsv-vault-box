from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
required={'kyrgyzstan-v1.html','kyrgyzstan.glb','kyrgyzstan.blend','mechanism.blend','poster.jpg','poster.png','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','acceptance-check.json','maps/felt-color.png','maps/felt-normal.png','maps/felt-roughness.png'}
exclude={'inventory.json','delivery-check.json','kyrgyzstan-v1-source.zip'}
paths=sorted(p for p in R.rglob('*') if p.is_file() and p.name not in exclude and '__pycache__' not in p.parts and not p.name.endswith('.blend1'))
def sha(b):return hashlib.sha256(b).hexdigest()
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in paths}
assert required<=set(inv),required-set(inv)
assert inv['kyrgyzstan-v1.html']['bytes']<5000000
assert json.loads((R/'acceptance-check.json').read_text())['status']=='PASS'
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'kyrgyzstan-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as f:
 for p in paths+[R/'inventory.json']:f.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as f:
 assert set(f.namelist())==set(inv)|{'inventory.json'}
 for name,entry in inv.items():
  b=f.read(name);assert len(b)==entry['bytes'] and sha(b)==entry['sha256']
result={'status':'PASS','html_bytes':inv['kyrgyzstan-v1.html']['bytes'],'glb_bytes':inv['kyrgyzstan.glb']['bytes'],'payload_files':len(inv),'required_artifacts_present':True,'zip_readback_all_hashes_match':True,'zip_bytes':z.stat().st_size,'zip_sha256':sha(z.read_bytes()),'inventory_sha256':sha((R/'inventory.json').read_bytes()),'exclusions':'inventory/check/archive exclude themselves to avoid recursive hashes; no caches or blend backups'}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print('DELIVERY PASS',json.dumps(result))
