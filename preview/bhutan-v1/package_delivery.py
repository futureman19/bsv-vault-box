"""Readback-verified in-folder source delivery; no external output paths."""
from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
excluded={'inventory.json','delivery-check.json','bhutan-v1-source.zip'}
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name not in excluded and '__pycache__' not in p.parts and 'node_modules' not in p.parts and not p.name.endswith('.blend1'))
required={'bhutan-v1.html','bhutan.glb','bhutan.blend','mechanism.blend','poster.png','poster.jpg','author.py','maps.py','verify_all.py','source-check.json','parity-check.json','browser-check.json','extended-check.json','theme-check.json','acceptance-check.json','design-brief.md','README.md','THREE-LICENSE.txt'}
names={p.relative_to(R).as_posix() for p in files};assert required<=names,required-names
for name in ['acceptance-check.json','theme-check.json','extended-check.json']:assert json.loads((R/name).read_text())['status']=='PASS'
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert (R/'bhutan-v1.html').stat().st_size<5_000_000
inventory={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
(R/'inventory.json').write_text(json.dumps(inventory,indent=2))
zpath=R/'bhutan-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==names|{'inventory.json'}
 for name,record in inventory.items():
  data=z.read(name);assert len(data)==record['bytes'] and hashlib.sha256(data).hexdigest()==record['sha256']
 assert z.read('inventory.json')==(R/'inventory.json').read_bytes()
r={'status':'PASS','html_bytes':inventory['bhutan-v1.html']['bytes'],'glb_bytes':inventory['bhutan.glb']['bytes'],'required_artifacts_present':True,'zip_entries':len(names)+1,'zip_readback_all_hashes_match':True,'zip_bytes':zpath.stat().st_size,'zip_sha256':hashlib.sha256(zpath.read_bytes()).hexdigest(),'inventory_sha256':hashlib.sha256((R/'inventory.json').read_bytes()).hexdigest(),'exclusions':sorted(excluded),'note':'Delivery is the exact in-folder HTML exercised by browser tests; no untested external copy.'}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print('DELIVERY PASS',json.dumps(r))
