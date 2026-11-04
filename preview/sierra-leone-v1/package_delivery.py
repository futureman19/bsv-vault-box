from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
required={'sierra-leone-v1.html','sierra-leone.glb','sierra-leone.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','theme-check.json','parity-check.json','browser-check.json','extended-check.json','motion-output.txt'}
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert '# fail 0' in (R/'motion-output.txt').read_text()
assert (R/'sierra-leone-v1.html').stat().st_size<5000000
files=sorted(f for f in R.rglob('*') if f.is_file() and not any(x in f.parts for x in ['node_modules','__pycache__']) and f.suffix not in ['.zip','.blend1'] and f.name not in ['inventory.json','delivery-check.json','package-output.txt','git-evidence.txt'])
inv={f.relative_to(R).as_posix():{'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in files};assert required<=inv.keys()
(R/'inventory.json').write_text(json.dumps(inv,indent=2));files.append(R/'inventory.json')
z=R/'sierra-leone-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for f in files:a.write(f,f.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())=={f.relative_to(R).as_posix() for f in files};assert a.testzip() is None
 for f in files:assert a.read(f.relative_to(R).as_posix())==f.read_bytes()
r={'status':'PASS','HTML_BYTES':(R/'sierra-leone-v1.html').stat().st_size,'GLB_BYTES':(R/'sierra-leone.glb').stat().st_size,'ZIP_BYTES':z.stat().st_size,'ZIP_SHA256':hashlib.sha256(z.read_bytes()).hexdigest(),'required_artifacts_present':True,'zip_readback_verified':True,'inventory_entries':len(inv)}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
