from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
def sha(data):return hashlib.sha256(data).hexdigest()
checks={}
s=json.loads((R/'source-check.json').read_text());assert s['saved_source_reopened'] and s['collision_samples']==81 and not s['collisions'];checks['source_and_motion_sampling']='PASS'
p=json.loads((R/'parity-check.json').read_text());assert p['source_and_export_geometry_match'] and max(p['source_to_glb_max'],p['glb_to_source_max'])<1e-5;checks['source_export_parity']='PASS'
for f in ['theme-check.json','extended-check.json']:
 assert json.loads((R/f).read_text())['status']=='PASS';checks[f]='PASS'
b=json.loads((R/'browser-check.json').read_text());assert {x['case'] for x in b}=={'desktop','mobile','corrupted GLB'}
for c in b[:2]:
 assert c['offline_file'] and not c['errors'] and not c['external_requests'] and c['open_close'] and c['reset_mid_motion'] and c['reduced_motion'] and c['rotation'] and c['asset']['degenerate']==0 and c['asset']['nonfinite']==0 and c['asset']['open_projection_max_abs_ndc']<1
assert b[1]['touch_rotation'] and b[2]['fallback'];checks['offline_browser']='PASS'
assert '# pass 2' in (R/'motion-output.txt').read_text() and '# fail 0' in (R/'motion-output.txt').read_text();checks['motion_unit_tests']='PASS'
assert (R/'latvia-v1.html').stat().st_size<5000000;checks['html_budget']='PASS'
(R/'acceptance-check.json').write_text(json.dumps({'status':'PASS','checks':checks},indent=2))
required={'latvia-v1.html','latvia.glb','latvia.blend','mechanism.blend','poster.png','poster.jpg','README.md','design-brief.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json','acceptance-check.json','motion-output.txt'}
files=sorted(f for f in R.rglob('*') if f.is_file() and not any(part in {'node_modules','__pycache__'} for part in f.relative_to(R).parts) and f.suffix not in {'.zip','.blend1'} and f.name not in {'inventory.json','delivery-check.json','packaging-output.txt'})
names={f.relative_to(R).as_posix() for f in files};assert required<=names
inventory={f.relative_to(R).as_posix():{'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())} for f in files}
(R/'inventory.json').write_text(json.dumps(inventory,indent=2));files.append(R/'inventory.json');z=R/'latvia-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for f in files:a.write(f,f.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert len(a.namelist())==len(files) and required<=set(a.namelist()) and a.testzip() is None
 for f in files:assert a.read(f.relative_to(R).as_posix())==f.read_bytes()
out={'status':'PASS','HTML_BYTES':(R/'latvia-v1.html').stat().st_size,'GLB_BYTES':(R/'latvia.glb').stat().st_size,'ZIP_BYTES':z.stat().st_size,'ZIP_SHA256':sha(z.read_bytes()),'archive_entries':len(files),'required_artifacts_verified':sorted(required),'archive_readback_verified':True,'checks':checks}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
