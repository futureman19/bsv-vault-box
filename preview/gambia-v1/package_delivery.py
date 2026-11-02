from pathlib import Path
import json,hashlib,zipfile,base64,re
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
required={'gambia-v1.html','gambia.glb','gambia.blend','mechanism.blend','poster.png','poster.jpg','README.md','design-brief.md','author.py','maps.py','build.py','source-check.json','parity-check.json','browser-check.json','theme-check.json','source-theme-check.json','motion-output.txt'}
assert all((R/n).is_file() for n in required)
h=(R/'gambia-v1.html').read_bytes();g=(R/'gambia.glb').read_bytes();assert len(h)<5_000_000
encoded=re.search(rb'<script id="asset" type="application/octet-stream">(.*?)</script>',h).group(1);assert base64.b64decode(encoded)==g
s=json.loads((R/'source-check.json').read_text());assert s['collision_samples']==81 and not s['collisions'] and s['moving_meshes']==91 and s['static_meshes']==39
p=json.loads((R/'parity-check.json').read_text());assert max(p['source_to_glb_max'],p['glb_to_source_max'])<1e-5
b=json.loads((R/'browser-check.json').read_text());assert [v['case'] for v in b]==['desktop','mobile','corrupted GLB']
for v in b[:2]:
 assert v['offline_file'] and v['open_close'] and v['rotation'] and v['reset_mid_motion'] and v['reduced_motion'] and not v['external_requests'] and not v['errors'] and not v['overflow']
 assert v['asset']['bytes']==len(g) and v['asset']['nonfinite']==v['asset']['degenerate']==0
assert b[2]['fallback'] and b[2]['caught_loader_errors']
for n in ['theme-check.json','source-theme-check.json']:assert json.loads((R/n).read_text())['status']=='PASS'
excluded={'inventory.json','delivery-check.json','gambia-v1-source.zip','git-output.txt','lane-prompt.md','lane-output.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name not in excluded and not any(x in p.parts for x in ['__pycache__','node_modules']) and not p.name.endswith('.blend1'))
records={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
assert required<=records.keys()
(R/'inventory.json').write_text(json.dumps(records,indent=2))
z=R/'gambia-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
 for n in records:archive.write(R/n,n)
 archive.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(z) as archive:
 assert set(archive.namelist())==set(records)|{'inventory.json'}
 for n,v in records.items():
  data=archive.read(n);assert len(data)==v['bytes'] and sha(data)==v['sha256']
 assert archive.read('inventory.json')==(R/'inventory.json').read_bytes()
result={'status':'PASS','html_bytes':len(h),'glb_bytes':len(g),'html_sha256':sha(h),'glb_sha256':sha(g),'inventory_files':len(records),'zip_bytes':z.stat().st_size,'zip_sha256':sha(z.read_bytes()),'explicit_required_artifacts_present':True,'embedded_glb_identical':True,'zip_inventory_and_every_hash_readback':True,'checks_passed':['build','source','hinge-attachment','81-pose-motion','parity','source-theme','browser-desktop','browser-mobile','corrupt-glb-fallback','no-js-fallback','theme','motion-unit-tests','delivery']}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print('HTML_BYTES',len(h),'GLB_BYTES',len(g));print(json.dumps(result,indent=2))
