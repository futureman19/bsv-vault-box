"""Local-only exact inventory, acceptance aggregation and ZIP readback."""
from pathlib import Path
import json,hashlib,base64,re,zipfile
R=Path(__file__).resolve().parent
def read(n):return json.loads((R/n).read_text())
def digest(b):return hashlib.sha256(b).hexdigest()
html=(R/'equatorial-guinea-v1.html').read_bytes();glb=(R/'equatorial-guinea.glb').read_bytes()
assert len(html)<5_000_000
embedded=re.search(rb'<script id="asset"[^>]*>([^<]+)</script>',html).group(1)
assert base64.b64decode(embedded)==glb
poster=re.search(rb'data:image/jpeg;base64,([^"\s]+)',html).group(1);assert base64.b64decode(poster)==(R/'poster.jpg').read_bytes()
s=read('source-check.json');assert s['saved_source_reopened'] and s['collision_samples']==81 and not s['collisions'];assert s['moving_meshes']==89 and s['static_meshes']==45
p=read('parity-check.json');assert p['source_and_export_geometry_match'] and max(p['source_to_glb_max'],p['glb_to_source_max'])<1e-5
assert read('theme-source-check.json')['status']=='PASS'
b=read('browser-check.json');assert [x['case'] for x in b]==['desktop','mobile','corrupted GLB']
for x in b[:2]:
 assert x['asset']['bytes']==len(glb) and x['asset']['degenerate']==0 and x['asset']['nonfinite']==0
 assert not x['external_requests'] and not x['errors'] and not x['overflow']
 assert all(x[k] for k in ['offline_file','rotation','open_close','reset_mid_motion','reduced_motion'])
 assert x['asset']['open_projection_max_abs_ndc']<1
assert b[1]['touch_rotation'] and b[2]['fallback'] and b[2]['caught_loader_errors']
e=read('extended-check.json');assert e['status']=='PASS' and e['noJS_poster']
motion=(R/'motion-output.txt').read_text();assert 'fail 0' in motion and 'pass 2' in motion
required={'equatorial-guinea-v1.html','equatorial-guinea.glb','equatorial-guinea.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','author.py','maps.py','build.py','source-check.json','parity-check.json','theme-source-check.json','browser-check.json','extended-check.json','maps/basalt-color.png','maps/basalt-normal.png','maps/basalt-roughness.png'}
excluded={'inventory.json','delivery-check.json','equatorial-guinea-source.zip','delivery-output.txt','git-evidence.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name not in excluded and p.suffix not in ['.blend1','.pyc'] and '__pycache__' not in p.parts and 'node_modules' not in p.parts)
inventory={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for p in files}
assert required<=inventory.keys(),required-inventory.keys()
(R/'inventory.json').write_text(json.dumps(inventory,indent=2))
zpath=R/'equatorial-guinea-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(inventory)|{'inventory.json'}
 assert json.loads(z.read('inventory.json'))==inventory
 for n,item in inventory.items():
  data=z.read(n);assert len(data)==item['bytes'] and digest(data)==item['sha256']
checks=['source','81-pose-motion','hinge-attachments','parity','theme-source','GLTFLoader','desktop-file-browser','mobile-touch-file-browser','corrupt-GLB-fallback','no-JS-fallback','portable-maps','motion-unit-negative-controls','embedded-payload-identity','strict-HTML-size','SHA256-inventory','ZIP-readback']
result={'status':'PASS','html_bytes':len(html),'glb_bytes':len(glb),'html_sha256':digest(html),'glb_sha256':digest(glb),'checks_passed':checks,'inventory_files':len(inventory),'zip_bytes':zpath.stat().st_size,'zip_sha256':digest(zpath.read_bytes()),'zip_readback_verified':True,'inventory_sha256':digest((R/'inventory.json').read_bytes()),'exclusions':'inventory and delivery envelopes excluded from recursive inventory; backups/caches/dependencies excluded; git-evidence is post-packaging audit'}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2))
print('HTML_BYTES',len(html),'GLB_BYTES',len(glb))
for c in checks:print('PASS',c)
print('ZIP_BYTES',result['zip_bytes'],'INVENTORY_FILES',len(inventory))
