from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
excluded={'inventory.json','delivery-check.json','mauritius-source.zip'}
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
files={p.relative_to(R).as_posix():p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__','.git']) and p.name not in excluded and not p.name.endswith('.blend1')}
required={'mauritius-v1.html','mauritius.glb','mauritius.blend','mechanism.blend','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','poster.png','poster.jpg','tests.mjs'}
assert required<=files.keys()
assert files['mauritius-v1.html'].stat().st_size<5000000
inventory={k:identity(p.read_bytes()) for k,p in sorted(files.items())}
(R/'inventory.json').write_text(json.dumps(inventory,indent=2))
z=R/'mauritius-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as out:
 for k,p in sorted(files.items()):out.write(p,k)
 out.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(z) as inp:
 assert set(inp.namelist())==set(files)|{'inventory.json'}
 for k,v in inventory.items():assert identity(inp.read(k))==v,k
result={'status':'PASS','html_bytes':inventory['mauritius-v1.html']['bytes'],'glb_bytes':inventory['mauritius.glb']['bytes'],'inventory_entries':len(files),'archive':identity(z.read_bytes()),'archive_readback_matches':True,'required_artifacts_present':True,'exclusions':'inventory/check/archive envelopes excluded from payload hashes to prevent recursion; dependencies/caches excluded'}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print('DELIVERY PASS',json.dumps(result))
