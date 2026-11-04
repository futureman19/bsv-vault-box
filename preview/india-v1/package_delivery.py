from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
load=lambda n:json.loads((R/n).read_text())
s=load('source-check.json');assert s['collision_samples']==81 and not s['collisions']
assert load('parity-check.json')['source_and_export_geometry_match']
assert load('theme-check.json')['status']=='PASS'
assert load('extended-check.json')['status']=='PASS'
b=load('browser-check.json');assert {c['case'] for c in b}=={'desktop','mobile','corrupted GLB'}
for c in b[:2]:
 assert c['open_close'] and c['reduced_motion'] and c['reset_mid_motion'] and not c['errors'] and not c['external_requests']
assert b[2]['fallback']
assert (R/'india-v1.html').stat().st_size<5000000
required={'india-v1.html','india.glb','india.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','motion-output.txt','desktop-closed.png','desktop-open.png','mobile-closed.png','mobile-open.png'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.zip','.blend1'] and p.name not in ['inventory.json','delivery-check.json','git-check.json'])
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
assert required<=set(manifest)
(R/'inventory.json').write_text(json.dumps(manifest,indent=2))
z=R/'india-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for p in files+[R/'inventory.json']:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())==set(manifest)|{'inventory.json'} and a.testzip() is None
 for n,m in manifest.items():assert hashlib.sha256(a.read(n)).hexdigest()==m['sha256']
r={'status':'PASS','HTML_BYTES':(R/'india-v1.html').stat().st_size,'GLB_BYTES':(R/'india.glb').stat().st_size,'ZIP_BYTES':z.stat().st_size,'ZIP_SHA256':hashlib.sha256(z.read_bytes()).hexdigest(),'inventory_count':len(manifest),'required_artifacts_present':True,'archive_readback':True,'checks_passed':['source','hinge-attachment','parity','theme-negative-control','original-pivots','motion','browser-desktop','browser-mobile','corrupt-glb-fallback','no-js-fallback','runtime-textures','delivery']}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
