from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
required={'design-brief.md','README.md','thailand.blend','thailand.glb','thailand-v1.html','poster.png','poster.jpg','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','motion-output.txt'}
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
assert (R/'thailand-v1.html').stat().st_size<5000000
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.relative_to(R).parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.zip','.blend1'] and p.name not in ['inventory.json','delivery-check.json'])
inventory={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
assert required<=set(inventory)
(R/'inventory.json').write_text(json.dumps(inventory,indent=2));files.append(R/'inventory.json')
z=R/'thailand-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert required<=set(a.namelist());assert len(a.namelist())==len(files);assert a.testzip() is None
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
r={'status':'PASS','HTML_BYTES':(R/'thailand-v1.html').stat().st_size,'GLB_BYTES':(R/'thailand.glb').stat().st_size,'archive_entries':len(files),'required_artifacts_verified':sorted(required),'archive_readback':True,'zip_bytes':z.stat().st_size,'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest()}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
