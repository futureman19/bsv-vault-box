from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
required={'south-sudan.blend','south-sudan.glb','south-sudan-v1.html','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','poster.png','motion-output.txt','theme-negative.txt'}
s=json.loads((R/'source-check.json').read_text());assert not s['collisions'] and s['collision_samples']==81
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert len(b)==3 and all(not x['errors'] and not x['external_requests'] for x in b[:2])
assert '# fail 0' in (R/'motion-output.txt').read_text()
assert 'AssertionError: Detached wetland ornament' in (R/'theme-negative.txt').read_text()
assert (R/'south-sudan-v1.html').stat().st_size<5000000
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.relative_to(R).parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.zip','.blend1'] and p.name not in ['inventory.json','delivery-check.json'])
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
assert required<=inv.keys()
(R/'inventory.json').write_text(json.dumps(inv,indent=2));files.append(R/'inventory.json')
z=R/'south-sudan-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())==set(inv)|{'inventory.json'} and a.testzip() is None
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
r={'status':'PASS','HTML_BYTES':(R/'south-sudan-v1.html').stat().st_size,'GLB_BYTES':(R/'south-sudan.glb').stat().st_size,'zip_bytes':z.stat().st_size,'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'inventory_files':len(inv),'explicit_required_set':sorted(required),'archive_readback_verified':True}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
