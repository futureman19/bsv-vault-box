"""Inventory and verified source ZIP; no external writes or recursive hashes."""
from pathlib import Path
import json,hashlib,zipfile,base64,re
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
required={'seychelles-v1.html','seychelles.glb','seychelles.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','author.py','maps.py','build.py','verify_all.py','verify_theme.py','verify_source.py','verify_parity.py','verify_browser.py','verify_extended.py','tests.mjs','source-check.json','parity-check.json','browser-check.json','extended-check.json','theme-check.json','hinge-attachment-check.json','desktop-closed.png','desktop-open.png','mobile-closed.png','mobile-open.png','maps/granite-color.png','maps/granite-normal.png','maps/granite-roughness.png'}
exclude={'inventory.json','delivery-check.json','seychelles-v1-source.zip'}
paths=sorted(p for p in R.rglob('*') if p.is_file() and p.name not in exclude and not p.name.endswith(('.blend1','.pyc')) and '__pycache__' not in p.parts and 'node_modules' not in p.parts)
files={p.relative_to(R).as_posix():p.read_bytes() for p in paths};assert required<=files.keys(),required-files.keys()
html=files['seychelles-v1.html'];glb=files['seychelles.glb'];assert len(html)<5_000_000
embedded=re.search(rb'<script id="asset" type="application/octet-stream">(.*?)</script>',html,re.S).group(1);assert base64.b64decode(embedded)==glb
poster=re.search(rb'src="data:image/jpeg;base64,([^"]+)"',html).group(1);assert base64.b64decode(poster)==files['poster.jpg']
s=json.loads(files['source-check.json']);assert s['collision_samples']==81 and not s['collisions'] and s['moving_meshes']==21
assert json.loads(files['theme-check.json'])['status']=='PASS'
assert json.loads(files['extended-check.json'])['status']=='PASS'
assert json.loads(files['parity-check.json'])['source_and_export_geometry_match']
b=json.loads(files['browser-check.json']);assert len(b)==3
for case in b[:2]:assert case['asset']['bytes']==len(glb) and case['offline_file'] and not case['external_requests'] and not case['errors']
assert b[2]['fallback']
inventory={n:{'bytes':len(data),'sha256':sha(data)} for n,data in files.items()}
inv=json.dumps(inventory,indent=2).encode();(R/'inventory.json').write_bytes(inv)
zpath=R/'seychelles-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n,data in files.items():z.writestr(n,data)
 z.writestr('inventory.json',inv)
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(files)|{'inventory.json'}
 for n,data in files.items():assert z.read(n)==data
 assert z.read('inventory.json')==inv
result={'status':'PASS','HTML_BYTES':len(html),'GLB_BYTES':len(glb),'html_sha256':sha(html),'glb_sha256':sha(glb),'inventory_sha256':sha(inv),'inventory_files':len(files),'zip_bytes':zpath.stat().st_size,'zip_sha256':sha(zpath.read_bytes()),'zip_entries':len(files)+1,'required_artifacts_verified':sorted(required),'archive_readback_verified':True,'embedded_glb_and_poster_exact':True,'hash_exclusions':sorted(exclude)}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print(f"DELIVERY PASS HTML_BYTES {len(html)} GLB_BYTES {len(glb)} ZIP_ENTRIES {len(files)+1}")
