from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
required={'liechtenstein.blend','liechtenstein.glb','liechtenstein-v1.html','mechanism.blend','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','poster.png','poster.jpg','motion-output.txt','theme-negative.txt'}
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
assert '# fail 0' in (R/'motion-output.txt').read_text()
assert 'AssertionError: Peak detached from lid' in (R/'theme-negative.txt').read_text()
for x in json.loads((R/'browser-check.json').read_text()):
 if 'asset' in x:assert not x['errors'] and not x['external_requests'] and x['open_close'] and x['reduced_motion']
html=(R/'liechtenstein-v1.html').stat().st_size;glb=(R/'liechtenstein.glb').stat().st_size;assert html<5000000
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(a in {'node_modules','__pycache__','.git'} for a in p.relative_to(R).parts) and p.suffix not in {'.zip','.blend1'} and p.name not in {'inventory.json','delivery-check.json'})
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files};assert required<=inv.keys()
(R/'inventory.json').write_text(json.dumps(inv,indent=2));files.append(R/'inventory.json');z=R/'liechtenstein-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())==set(inv)|{'inventory.json'};assert a.testzip() is None
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
r={'status':'PASS','HTML_BYTES':html,'GLB_BYTES':glb,'zip_bytes':z.stat().st_size,'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'inventory_entries':len(inv),'required_artifacts_verified':sorted(required),'archive_readback_verified':True}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
