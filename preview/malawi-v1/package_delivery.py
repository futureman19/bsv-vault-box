"""Exact required-payload inventory, ZIP readback; excludes recursive envelopes."""
from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
required={'malawi-v1.html','malawi.glb','malawi.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','author.py','maps.py','build.py','run_checks.py','verify_source.py','verify_parity.py','verify_browser.py','verify_theme.py','source-check.json','parity-check.json','browser-check.json','theme-check.json','checks.json','desktop-closed.png','desktop-open.png','mobile-closed.png','mobile-open.png','motion.mjs','tests.mjs','THREE-LICENSE.txt'}
def identity(data):return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
exclude={'inventory.json','delivery-check.json','malawi-source.zip','package-log.txt'}
files=[p for p in R.rglob('*') if p.is_file() and p.name not in exclude and not p.name.endswith(('.blend1','.pyc')) and '__pycache__' not in p.parts and 'node_modules' not in p.parts]
names={p.relative_to(R).as_posix() for p in files};assert required<=names,required-names
assert (R/'malawi-v1.html').stat().st_size<5000000
checks=json.loads((R/'checks.json').read_text());assert len(checks)==6 and all(x['exit_code']==0 for x in checks)
inv={p.relative_to(R).as_posix():identity(p.read_bytes()) for p in sorted(files)}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'malawi-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as out:
 for p in files+[R/'inventory.json']:out.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as arc:
 assert set(arc.namelist())==names|{'inventory.json'}
 for name,record in inv.items():assert identity(arc.read(name))==record,name
 assert arc.read('inventory.json')==(R/'inventory.json').read_bytes()
result={'status':'PASS','html':identity((R/'malawi-v1.html').read_bytes()),'glb':identity((R/'malawi.glb').read_bytes()),'archive':identity(z.read_bytes()),'inventory':identity((R/'inventory.json').read_bytes()),'required_payload_verified':sorted(required),'archive_entries':len(names)+1,'readback_all_hashes_match':True,'exclusions':'self-referential inventory/delivery/ZIP envelopes, packaging stdout, caches and Blender backups; no delivery copy claimed'}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print('DELIVERY PASS');print('HTML_BYTES',result['html']['bytes'],'GLB_BYTES',result['glb']['bytes']);print('ZIP_ENTRIES',result['archive_entries'])
