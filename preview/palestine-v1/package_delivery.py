from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
required={'palestine.blend','palestine.glb','palestine-v1.html','design-brief.md','README.md','poster.png','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','motion-output.txt','negative-control.txt'}
assert (R/'palestine-v1.html').stat().st_size<5000000
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert '# fail 0' in (R/'motion-output.txt').read_text()
assert 'AssertionError: detached ornament' in (R/'negative-control.txt').read_text()
for n in ['theme-check.json','extended-check.json']:assert json.loads((R/n).read_text())['status']=='PASS'
for case in json.loads((R/'browser-check.json').read_text()):
 if case['case']!='corrupted GLB':assert not case['errors'] and not case['external_requests'] and case['open_close']
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.relative_to(R).parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.zip','.blend1'] and p.name not in ['inventory.json','delivery-check.json'])
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files};assert required<=inv.keys()
(R/'inventory.json').write_text(json.dumps(inv,indent=2));files.append(R/'inventory.json')
z=R/'palestine-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())=={p.relative_to(R).as_posix() for p in files};assert a.testzip() is None
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
r={'status':'PASS','HTML_BYTES':(R/'palestine-v1.html').stat().st_size,'GLB_BYTES':(R/'palestine.glb').stat().st_size,'inventory_entries':len(inv),'zip_bytes':z.stat().st_size,'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'required_artifacts_present':True,'archive_readback':True}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
