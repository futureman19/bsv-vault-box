"""Exact required-artifact inventory, archive readback, embedded-payload and gate checks."""
from pathlib import Path
import json,hashlib,zipfile,re,struct,base64
R=Path(__file__).resolve().parent
required={'bangladesh.blend','bangladesh.glb','bangladesh-v1.html','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','author.py','helpers.py','maps.py','build.py','viewer.js','viewer.bundle.js','motion.mjs','template.html','THREE-LICENSE.txt','package.json','verify_source.py','verify_parity.py','verify_theme_source.py','verify_browser.py','verify_theme.py','tests.mjs','verify_delivery.py','verify_all.py','source-check.json','parity-check.json','theme-source-check.json','theme-check.json','browser-check.json','hinge-attachment-check.json','desktop-closed.png','desktop-open.png','desktop-lid-detail.png','mobile-closed.png','mobile-open.png','mobile-nojs.png','mobile-fallback.png','maps/jamdani-color.png','maps/weave-roughness.png','maps/weave-normal.png','maps/delta-green.png'}
def sha(b):return hashlib.sha256(b).hexdigest()
def load(n):return json.loads((R/n).read_text())
s=load('source-check.json');assert s['saved_source_reopened'] and s['collision_samples']>=81 and s['moving_meshes']>0 and s['static_meshes']>0 and not s['collisions'] and s['hollow_floor_ray_z']<.3
p=load('parity-check.json');assert p['source_and_export_geometry_match'] and max(p['source_to_glb_max'],p['glb_to_source_max'])<1e-5
assert len(load('hinge-attachment-check.json')['intersecting_attachment_pairs'])==10
for n in ['theme-source-check.json','theme-check.json']:assert load(n)['result']=='PASS'
b=load('browser-check.json');assert [x['case'] for x in b]==['desktop','mobile','corrupted GLB']
for x in b[:2]:
 assert all(x[k] for k in ['offline_file','rotation','open_close','reset_mid_motion','reduced_motion'])
 assert not x['external_requests'] and not x['errors'] and not x['overflow']
 assert x['asset']['nonfinite']==x['asset']['degenerate']==0 and x['asset']['open_projection_max_abs_ndc']<1
assert b[1]['touch_rotation'] and b[2]['fallback'] and b[2]['caught_loader_errors'] and not b[2]['unhandled_errors']
html=(R/'bangladesh-v1.html').read_bytes();glb=(R/'bangladesh.glb').read_bytes();assert len(html)<5000000
assert base64.b64decode(re.search(rb'<script id="asset"[^>]*>(.*?)</script>',html,re.S)[1])==glb
assert base64.b64decode(re.search(rb'src="data:image/jpeg;base64,([^"]+)"',html)[1])==(R/'poster.jpg').read_bytes()
assert not re.search(rb'<(?:script|link|img)[^>]+(?:src|href)=[\"\']https?://',html)
g=json.loads(glb[20:20+struct.unpack_from('<I',glb,12)[0]])
assert all('uri' not in x for x in g.get('buffers',[])) and all('bufferView' in x and 'uri' not in x for x in g.get('images',[]))
excluded={'inventory.json','delivery-check.json','bangladesh-v1-source.zip','verification-output.txt'}
paths=sorted(p for p in R.rglob('*') if p.is_file() and p.name not in excluded and not any(x in p.parts for x in ['__pycache__','node_modules','.git']) and p.suffix not in ['.blend1','.pyc'])
names={p.relative_to(R).as_posix() for p in paths};assert required<=names,required-names
inventory={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in paths}
(R/'inventory.json').write_text(json.dumps(inventory,indent=2))
archive=R/'bangladesh-v1-source.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in paths:z.write(p,p.relative_to(R).as_posix())
 z.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(archive) as z:
 assert set(z.namelist())==names|{'inventory.json'}
 for n,v in inventory.items():assert len(z.read(n))==v['bytes'] and sha(z.read(n))==v['sha256'],n
 assert z.read('inventory.json')==(R/'inventory.json').read_bytes()
result={'result':'PASS','html_bytes':len(html),'glb_bytes':len(glb),'html_sha256':sha(html),'glb_sha256':sha(glb),'inventory_entries':len(inventory),'required_artifacts':sorted(required),'archive_entries':len(inventory)+1,'archive_bytes':archive.stat().st_size,'archive_sha256':sha(archive.read_bytes()),'inventory_sha256':sha((R/'inventory.json').read_bytes()),'embedded_glb_exact':True,'embedded_poster_exact':True,'archive_readback':'all required paths and every entry hash verified','checks_passed':['source','81-pose motion sampling','hinge attachment','parity','theme source / channel continuity','theme runtime / negative control','desktop file browser','mobile touch file browser','reduced motion','corrupt GLB fallback','no-JS fallback','embedded payload identity','byte budget','inventory and ZIP readback'],'exclusions':'inventory excludes itself, delivery-check, ZIP and aggregate transcript to avoid circular hashing'}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print('DELIVERY PASS');print('HTML_BYTES',len(html),'GLB_BYTES',len(glb));print('INVENTORY_FILES',len(inventory),'ZIP_BYTES',archive.stat().st_size)
