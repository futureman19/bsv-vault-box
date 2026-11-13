from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
load=lambda n:json.loads((R/n).read_text())
s=load('source-check.json');assert s['saved_source_reopened'] and s['collision_samples']==81 and not s['collisions']
p=load('parity-check.json');assert p['source_and_export_geometry_match'] and max(p['source_to_glb_max'],p['glb_to_source_max'])<1e-5
b=load('browser-check.json');assert len(b)==3
for x in b[:2]:
 assert x['offline_file'] and x['open_close'] and x['rotation'] and x['reset_mid_motion'] and x['reduced_motion'] and not x['overflow'] and not x['errors'] and not x['external_requests']
 assert x['asset']['nonfinite']==x['asset']['degenerate']==0 and x['asset']['open_projection_max_abs_ndc']<1
assert b[2]['fallback'] and not b[2]['unhandled_errors']
for name in ['extended','theme','palette','motion']:assert load(name+'-check.json')['status']=='PASS'
assert len(load('hinge-attachment-check.json')['intersecting_attachment_pairs'])==10
checks=['source','hinge-attachment','parity','browser','extended','theme','palette','motion','delivery']
html=R/'samoa-v1.html';glb=R/'samoa.glb';assert html.stat().st_size<5000000
required={'samoa-v1.html','samoa.glb','samoa.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','author.py','maps.py','build.py','.gitattributes'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.relative_to(R).parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.blend1','.zip'] and p.name not in ['inventory.json','delivery-check.json','delivery-output.txt','staged-check.json'])
sha=lambda x:hashlib.sha256(x).hexdigest()
inventory={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
assert required<=inventory.keys()
(R/'inventory.json').write_text(json.dumps(inventory,indent=2));files.append(R/'inventory.json')
z=R/'samoa-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert len(a.namelist())==len(files) and a.testzip() is None
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
r=dict(status='PASS',HTML_BYTES=html.stat().st_size,GLB_BYTES=glb.stat().st_size,ZIP_BYTES=z.stat().st_size,inventory_entries=len(inventory),archive_entries=len(files),archive_readback_verified=True,required_artifacts_verified=sorted(required),checks_passed=checks,html_sha256=sha(html.read_bytes()),glb_sha256=sha(glb.read_bytes()),zip_sha256=sha(z.read_bytes()))
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));print('ALL_ACCEPTANCE_CHECKS_PASS')
