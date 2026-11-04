from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
load=lambda n:json.loads((R/n).read_text())
assert load('source-check.json')['collision_samples']==81 and not load('source-check.json')['collisions']
assert load('parity-check.json')['source_and_export_geometry_match']
assert load('theme-check.json')['status']=='PASS' and load('extended-check.json')['status']=='PASS'
b=load('browser-check.json');assert len(b)==3
for c in b[:2]:
 assert c['offline_file'] and c['open_close'] and c['reset_mid_motion'] and c['reduced_motion']
 assert not c['external_requests'] and not c['errors'] and not c['overflow']
 assert c['asset']['degenerate']==0 and c['asset']['nonfinite']==0 and c['asset']['open_projection_max_abs_ndc']<1
assert b[2]['fallback'] and b[2]['caught_loader_errors']
assert '# fail 0' in (R/'motion-output.txt').read_text()
assert (R/'greece-v1.html').stat().st_size<5_000_000
required={'greece.blend','greece.glb','greece-v1.html','design-brief.md','README.md','mechanism.blend','poster.png','poster.jpg','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json'}
exclude={'inventory.json','delivery-check.json','package-output.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.zip','.blend1'] and p.name not in exclude)
sha=lambda data:hashlib.sha256(data).hexdigest()
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
assert required<=set(manifest)
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'greece-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert required<=set(a.namelist()) and len(a.namelist())==len(files) and a.testzip() is None
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
r={'status':'PASS','HTML_BYTES':(R/'greece-v1.html').stat().st_size,'GLB_BYTES':(R/'greece.glb').stat().st_size,'ZIP_BYTES':z.stat().st_size,'zip_sha256':sha(z.read_bytes()),'entries':len(files),'required_artifacts_present':True,'archive_readback_verified':True,'checks_passed':['source','parity','theme','motion','browser-desktop','browser-mobile','corrupt-GLB','no-JS','maps','delivery']}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
