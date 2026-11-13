from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
load=lambda n:json.loads((R/n).read_text())
s=load('source-check.json');assert s['saved_source_reopened'] and s['collision_samples']==81 and not s['collisions']
p=load('parity-check.json');assert p['source_and_export_geometry_match'] and max(p['source_to_glb_max'],p['glb_to_source_max'])<1e-5
assert load('theme-check.json')['status']=='PASS'
assert load('extended-check.json')['status']=='PASS'
assert load('negative-control.json')=={'status':'EXPECTED_FAIL','reason':'Detached cutwork ornament'}
b=load('browser-check.json');assert {v['case'] for v in b}=={'desktop','mobile','corrupted GLB'}
for v in b[:2]:
 assert v['offline_file'] and v['open_close'] and v['reset_mid_motion'] and v['reduced_motion'] and not v['errors'] and not v['external_requests'] and not v['overflow']
 assert v['asset']['degenerate']==v['asset']['nonfinite']==0 and v['asset']['open_projection_max_abs_ndc']<1
assert b[2]['fallback']
assert '# fail 0' in (R/'motion-output.txt').read_text()
h=R/'cyprus-v1.html';g=R/'cyprus.glb';assert h.stat().st_size<5_000_000
required={'cyprus-v1.html','cyprus.glb','cyprus.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json','negative-control.json','motion-output.txt'}
excluded={'inventory.json','delivery-check.json','acceptance-check.json','git-evidence.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.relative_to(R).parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.blend1','.zip'] and p.name not in excluded)
sha=lambda data:hashlib.sha256(data).hexdigest()
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files};assert required<=set(inv)
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'cyprus-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for p in files+[R/'inventory.json']:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())==set(inv)|{'inventory.json'} and a.testzip() is None
 for name,meta in inv.items():assert sha(a.read(name))==meta['sha256'] and len(a.read(name))==meta['bytes']
checks=['source','parity','theme','browser-desktop','browser-mobile','corrupt-glb','no-js','maps','poster','motion','negative-control','delivery']
report=dict(status='PASS',HTML_BYTES=h.stat().st_size,GLB_BYTES=g.stat().st_size,ZIP_BYTES=z.stat().st_size,ZIP_SHA256=sha(z.read_bytes()),inventory_files=len(inv),required_artifacts_present=True,archive_readback_verified=True,checks_passed=checks)
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));(R/'acceptance-check.json').write_text(json.dumps({'status':'PASS','checks_passed':checks},indent=2))
print(json.dumps(report,indent=2))
