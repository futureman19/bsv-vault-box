from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent
required={'bahrain.blend','bahrain.glb','bahrain-v1.html','poster.png','poster.jpg','author.py','maps.py','verify_all.py','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json','acceptance-check.json','README.md','design-brief.md'}
files=[p for p in R.rglob('*') if p.is_file() and p.name not in {'inventory.json','delivery-check.json'} and '__pycache__' not in p.parts and not p.name.endswith('.blend1')]
assert required <= {p.relative_to(R).as_posix() for p in files}
assert json.loads((R/'acceptance-check.json').read_text())['status']=='PASS'
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
for name,data in json.loads((R/'inventory.json').read_text()).items():
 b=(R/name).read_bytes();assert len(b)==data['bytes'] and hashlib.sha256(b).hexdigest()==data['sha256']
h=inv['bahrain-v1.html']['bytes'];g=inv['bahrain.glb']['bytes'];assert h<5000000
out={'status':'PASS','HTML_BYTES':h,'GLB_BYTES':g,'inventory_files':len(inv),'sha256_readback_verified':True,'required_artifacts_present':True,'inventory_sha256':hashlib.sha256((R/'inventory.json').read_bytes()).hexdigest(),'excluded_self_referential_reports':['inventory.json','delivery-check.json']}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print('DELIVERY PASS',json.dumps(out))
