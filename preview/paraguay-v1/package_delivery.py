"""Bounded folder-local archive and final acceptance aggregation."""
from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
required={'paraguay-v1.html','paraguay.glb','paraguay.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','author.py','maps.py','build.py','verify_source.py','verify_parity.py','verify_theme.py','verify_browser.py','verify_extended.py','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','desktop-closed.png','desktop-open.png','mobile-closed.png','mobile-open.png','.gitattributes'}
excluded={'inventory.json','delivery-check.json','paraguay-v1-source.zip','package-output.txt'}
paths=sorted(p for p in R.rglob('*') if p.is_file() and p.name not in excluded and not any(q in p.parts for q in ['node_modules','__pycache__','.git']) and not p.name.endswith(('.blend1','.pyc')))
files={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in paths}
assert required<=files.keys(),required-files.keys()
assert files['paraguay-v1.html']['bytes']<5_000_000
source=json.loads((R/'source-check.json').read_text());assert source['collision_samples']==81 and not source['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
bs=json.loads((R/'browser-check.json').read_text());assert {x['case'] for x in bs}=={'desktop','mobile','corrupted GLB'}
for x in bs[:2]:
 assert x['offline_file'] and not x['errors'] and not x['external_requests'] and x['reduced_motion'] and x['reset_mid_motion'] and x['open_close']
 assert x['asset']['bytes']==files['paraguay.glb']['bytes']
assert bs[2]['fallback']
inv={'files':files,'exclusions':'inventory itself, delivery-check, zip envelope, active packaging output, dependencies and backups'}
(R/'inventory.json').write_text(json.dumps(inv,indent=2),encoding='utf8')
zpath=R/'paraguay-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in paths+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(files)|{'inventory.json'}
 for n,v in files.items():
  b=z.read(n);assert len(b)==v['bytes'] and sha(b)==v['sha256'],n
 assert z.read('inventory.json')==(R/'inventory.json').read_bytes()
r={'status':'PASS','html_bytes':files['paraguay-v1.html']['bytes'],'glb_bytes':files['paraguay.glb']['bytes'],'payload_files':len(files),'required_files_present':True,'archive_readback_all_hashes':True,'zip_bytes':zpath.stat().st_size,'zip_sha256':sha(zpath.read_bytes()),'inventory_sha256':sha((R/'inventory.json').read_bytes()),'checks_passed':['build','motion','source','hinge-attachment','parity','theme','browser-desktop','browser-mobile','corrupt-GLB-fallback','noJS-fallback','extended-maps','delivery']}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
