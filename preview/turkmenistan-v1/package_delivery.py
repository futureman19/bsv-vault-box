from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
checks={}
def load(n):return json.loads((R/n).read_text())
s=load('source-check.json');assert s['collision_samples']==81 and not s['collisions'];checks['source']='PASS'
p=load('parity-check.json');assert max(p['source_to_glb_max'],p['glb_to_source_max'])<1e-5;checks['parity']='PASS'
t=load('theme-check.json');assert t['status']=='PASS' and t['detached_parent_negative_control_rejected'];checks['theme']='PASS'
b=load('browser-check.json');assert {x['case'] for x in b}=={'desktop','mobile','corrupted GLB'}
for x in b[:2]:
 assert x['offline_file'] and x['open_close'] and x['reset_mid_motion'] and x['reduced_motion'] and not x['errors'] and not x['external_requests'] and not x['overflow']
 assert x['asset']['degenerate']==0 and x['asset']['nonfinite']==0 and x['asset']['open_projection_max_abs_ndc']<1
assert b[2]['fallback'] and b[2]['caught_loader_errors'];checks['browser']='PASS'
e=load('extended-check.json');assert e['status']=='PASS' and e['noJS_poster'];checks['extended']='PASS'
assert 'pass 2' in (R/'motion-output.txt').read_text(encoding='utf8');checks['motion']='PASS'
html=R/'turkmenistan-v1.html';glb=R/'turkmenistan.glb';assert html.stat().st_size<5000000;checks['size']='PASS'
(R/'acceptance-check.json').write_text(json.dumps(checks,indent=2))
allowed={'.py','.js','.mjs','.json','.md','.txt','.html','.png','.jpg','.blend','.glb'}
files=sorted(f for f in R.rglob('*') if f.is_file() and (f.suffix in allowed or f.name in {'.gitattributes','.gitignore'}) and f.name not in {'inventory.json','delivery-check.json','package-output.txt','git-verification.txt'} and (f.parent==R or f.parent.name=='maps'))
required={'turkmenistan.blend','turkmenistan.glb','turkmenistan-v1.html','mechanism.blend','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','poster.png','poster.jpg','mobile-closed.png','mobile-open.png'}
manifest={f.relative_to(R).as_posix():{'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in files};assert required<=manifest.keys()
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'turkmenistan-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for f in files:a.write(f,f.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert a.testzip() is None and len(a.namelist())==len(files)
 assert required<=set(a.namelist())
 for f in files:assert a.read(f.relative_to(R).as_posix())==f.read_bytes()
r={'status':'PASS','HTML_BYTES':html.stat().st_size,'GLB_BYTES':glb.stat().st_size,'ZIP_BYTES':z.stat().st_size,'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'archive_entries':len(files),'required_artifacts_present':True,'archive_readback_verified':True,'checks':checks}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
