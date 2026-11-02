"""Verify current acceptance evidence and package an explicit complete local payload."""
from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
required={'design-brief.md','README.md','dr-congo.blend','dr-congo.glb','dr-congo-v1.html','mechanism.blend','poster.png','poster.jpg','author.py','maps.py','build.py','viewer.js','viewer.bundle.js','motion.mjs','template.html','THREE-LICENSE.txt','package.json','verify_source.py','verify_parity.py','verify_browser.py','verify_theme.py','tests.mjs','package_delivery.py','source-check.json','parity-check.json','browser-check.json','theme-check.json','hinge-attachment-check.json','desktop-closed.png','desktop-open.png','mobile-closed.png','mobile-open.png','maps/raffia-color.png','maps/raffia-normal.png','maps/raffia-roughness.png'}
assert all((R/n).is_file() for n in required),sorted(n for n in required if not (R/n).is_file())
source=json.loads((R/'source-check.json').read_text());assert source['collision_samples']==81 and not source['collisions'] and source['moving_meshes']>=100
parity=json.loads((R/'parity-check.json').read_text());assert parity['source_and_export_geometry_match'] and max(parity['source_to_glb_max'],parity['glb_to_source_max'])<1e-5
browser=json.loads((R/'browser-check.json').read_text());assert {x['case'] for x in browser}=={'desktop','mobile','corrupted GLB'}
for b in browser[:2]:
 assert b['offline_file'] and not b['external_requests'] and not b['errors'] and b['open_close'] and b['reset_mid_motion'] and b['reduced_motion'] and not b['overflow']
 assert b['asset']['bytes']==(R/'dr-congo.glb').stat().st_size and b['asset']['nonfinite']==b['asset']['degenerate']==0
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'theme-source-check.json').read_text())['status']=='PASS'
required.add('theme-source-check.json')
assert (R/'dr-congo-v1.html').stat().st_size<5_000_000
html=(R/'dr-congo-v1.html').read_text();import base64,re
embedded=base64.b64decode(re.search(r'<script id="asset"[^>]*>(.*?)</script>',html,re.S).group(1));assert embedded==(R/'dr-congo.glb').read_bytes()
def identity(p):return {'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
exclude={'inventory.json','delivery-check.json','dr-congo-v1-source.zip'}
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name not in exclude and p.suffix not in {'.blend1','.pyc'} and '__pycache__' not in p.parts and 'node_modules' not in p.parts)
inv={p.relative_to(R).as_posix():identity(p) for p in files};assert required<=set(inv)
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
archive=R/'dr-congo-v1-source.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(archive) as z:
 assert set(z.namelist())==set(inv)|{'inventory.json'}
 for n,d in inv.items():
  data=z.read(n);assert len(data)==d['bytes'] and hashlib.sha256(data).hexdigest()==d['sha256']
report={'status':'PASS','html':identity(R/'dr-congo-v1.html'),'glb':identity(R/'dr-congo.glb'),'source_archive':identity(archive),'inventory':identity(R/'inventory.json'),'payload_count':len(inv),'required_count':len(required),'all_required_present':True,'archive_readback_hashes_match':True,'embedded_glb_identical':True,'self_hash_policy':'inventory excludes itself, ZIP and delivery-check; ZIP contains inventory but not delivery-check','delivery_location':'this directory; exact HTML tested offline in place'}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));print('DELIVERY PASS',json.dumps(report))
