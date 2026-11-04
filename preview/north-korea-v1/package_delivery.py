from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
required={'north-korea.blend','north-korea.glb','north-korea-v1.html','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','motion-output.txt'}
assert all((R/n).is_file() for n in required)
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
for n in ['theme-check.json','extended-check.json']:assert json.loads((R/n).read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert len(b)==3
assert all(not x['errors'] and not x['external_requests'] for x in b[:2])
assert '# fail 0' in (R/'motion-output.txt').read_text()
h=(R/'north-korea-v1.html').stat().st_size;g=(R/'north-korea.glb').stat().st_size;assert h<5000000
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.relative_to(R).parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.zip','.blend1'] and p.name not in ['inventory.json','delivery-check.json'])
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p)} for p in files};assert required<=set(inv)
(R/'inventory.json').write_text(json.dumps(inv,indent=2));files.append(R/'inventory.json');z=R/'north-korea-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert len(a.namelist())==len(files) and a.testzip() is None
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
r={'status':'PASS','HTML_BYTES':h,'GLB_BYTES':g,'ZIP_BYTES':z.stat().st_size,'zip_sha256':sha(z),'inventory_entries':len(inv),'archive_readback_verified':True,'required_artifacts_verified':sorted(required)}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print('DELIVERY PASS');print('HTML_BYTES',h,'GLB_BYTES',g)
