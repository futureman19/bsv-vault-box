"""Aggregate strict assertions, inventory and verified source archive.
Inventory excludes itself, delivery-check and ZIP to avoid circular hashes.
Everything stays in the authorized Jordan folder. No external delivery writes.
"""
from pathlib import Path
import json,hashlib,zipfile,re,base64
R=Path(__file__).resolve().parent
required={'jordan-v1.html','jordan.glb','jordan.blend','mechanism.blend','poster.png','poster.jpg','maps/sandstone-color.png','maps/sandstone-roughness.png','maps/lid-color.png','README.md','design-brief.md','author.py','maps.py','build.py','verify_browser.py','verify_extended.py','verify_source.py','verify_parity.py','verify_theme_source.py','source-check.json','parity-check.json','theme-source-check.json','browser-check.json','extended-check.json','hinge-attachment-check.json','desktop-closed.png','desktop-open.png','desktop-open-rear.png','mobile-closed.png','mobile-open.png','mobile-fallback.png','mobile-nojs.png','THREE-LICENSE.txt'}
def load(n):return json.loads((R/n).read_text())
def digest(b):return hashlib.sha256(b).hexdigest()
s=load('source-check.json');assert s['saved_source_reopened'] and s['collision_samples']==81 and s['collisions']==[] and s['moving_meshes']==21 and s['static_meshes']==39
assert len(load('hinge-attachment-check.json')['intersecting_attachment_pairs'])==10
p=load('parity-check.json');assert p['source_and_export_geometry_match'] and max(p['source_to_glb_max'],p['glb_to_source_max'])<1e-5
assert load('theme-source-check.json')['status']=='PASS' and load('extended-check.json')['status']=='PASS'
b=load('browser-check.json');assert {x['case'] for x in b}=={'desktop','mobile','corrupted GLB'}
html=(R/'jordan-v1.html').read_bytes();glb=(R/'jordan.glb').read_bytes()
assert len(html)<5_000_000
for row in b[:2]:
 assert not row['external_requests'] and not row['errors'] and not row['overflow']
 assert all(row[k] for k in ['offline_file','rotation','open_close','reset_mid_motion','reduced_motion'])
 assert row['asset']['bytes']==len(glb) and row['asset']['degenerate']==row['asset']['nonfinite']==0 and row['asset']['open_projection_max_abs_ndc']<1
assert b[2]['fallback'] and b[2]['caught_loader_errors'] and not b[2]['unhandled_errors']
embedded=re.search(rb'<script id="asset" type="application/octet-stream">(.*?)</script>',html,re.S).group(1)
assert base64.b64decode(embedded)==glb
assert base64.b64encode((R/'poster.jpg').read_bytes()) in html
checks=['source-reopen','hollow-interior','hinge-attachment','81-pose-motion-collisions','source-export-parity','theme-source-and-negative-control','runtime-maps-and-parentage','desktop-file-offline','mobile-touch-file-offline','reduced-motion','corrupt-GLB-fallback','no-JS-fallback','motion-unit-tests','embedded-payload-parity','html-byte-budget']
assert '\u2139 fail 0' in (R/'motion-test-output.txt').read_text(encoding='utf8')
(R/'acceptance-check.json').write_text(json.dumps({'status':'PASS','checks_passed':checks,'html_bytes':len(html),'glb_bytes':len(glb)},indent=2))
excluded={'inventory.json','delivery-check.json','jordan-v1-source.zip'}
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name not in excluded and not p.name.endswith(('.blend1','.pyc')) and '__pycache__' not in p.parts)
names={p.relative_to(R).as_posix() for p in files};assert required<=names,required-names
assert not any('node_modules' in p.parts for p in files)
items=[{'path':p.relative_to(R).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for p in files]
(R/'inventory.json').write_text(json.dumps({'algorithm':'SHA-256','exclusions':sorted(excluded),'files':items},indent=2))
zpath=R/'jordan-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files:z.write(p,p.relative_to(R).as_posix())
 z.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==names|{'inventory.json'}
 for item in items:
  data=z.read(item['path']);assert len(data)==item['bytes'] and digest(data)==item['sha256']
 assert z.read('inventory.json')==(R/'inventory.json').read_bytes()
result={'status':'PASS','HTML_BYTES':len(html),'GLB_BYTES':len(glb),'ZIP_BYTES':zpath.stat().st_size,'html_sha256':digest(html),'glb_sha256':digest(glb),'zip_sha256':digest(zpath.read_bytes()),'inventory_sha256':digest((R/'inventory.json').read_bytes()),'inventory_files':len(items),'zip_entries':len(items)+1,'explicit_required_set_verified':True,'archive_readback_verified':True,'embedded_model_and_poster_match':True,'checks_passed':checks+['required-artifact-inventory','sha256-archive-readback']}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
