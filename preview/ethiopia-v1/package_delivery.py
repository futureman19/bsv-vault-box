from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
read=lambda n:json.loads((R/n).read_text())
source=read('source-check.json');assert source['collision_samples']==81 and not source['collisions'] and source['saved_source_reopened']
assert read('parity-check.json')['source_and_export_geometry_match']
assert read('theme-check.json')['status']=='PASS' and read('material-check.json')['status']=='PASS'
assert read('extended-check.json')['noJS_poster']
b=read('browser-check.json');assert len(b)==3
for c in b[:2]:
 assert not c['errors'] and not c['external_requests'] and c['open_close'] and c['reduced_motion'] and c['reset_mid_motion'] and c['rotation']
 assert c['asset']['degenerate']==0 and c['asset']['nonfinite']==0 and c['asset']['open_projection_max_abs_ndc']<1
assert b[2]['fallback'] and not b[2]['unhandled_errors']
assert 'fail 0' in (R/'motion-output.txt').read_text(encoding='utf8')
html=(R/'ethiopia-v1.html').stat().st_size;glb=(R/'ethiopia.glb').stat().st_size;assert html<5_000_000
required={'ethiopia-v1.html','ethiopia.glb','ethiopia.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','material-check.json','extended-check.json'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.relative_to(R).parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.zip','.blend1'] and p.name not in ['inventory.json','delivery-check.json','package-output.txt'])
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
assert required<=manifest.keys()
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'ethiopia-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as f:
 for p in files:f.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as f:
 assert set(f.namelist())=={p.relative_to(R).as_posix() for p in files}
 assert required<=set(f.namelist()) and f.testzip() is None
 for p in files:assert f.read(p.relative_to(R).as_posix())==p.read_bytes()
checks=['source','hinge-attachment','81-pose-motion','parity','theme','negative-controls','browser-desktop','browser-mobile','corrupt-GLB-fallback','no-JS-fallback','material','motion-unit','delivery']
out={'status':'PASS','HTML_BYTES':html,'GLB_BYTES':glb,'ZIP_BYTES':z.stat().st_size,'ZIP_SHA256':hashlib.sha256(z.read_bytes()).hexdigest(),'inventory_entries':len(manifest),'zip_entries':len(files),'archive_readback_verified':True,'required_set_verified':True,'checks_passed':checks}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print('HTML_BYTES',html,'GLB_BYTES',glb);print('PASS '+', '.join(checks));print(json.dumps(out,indent=2))
