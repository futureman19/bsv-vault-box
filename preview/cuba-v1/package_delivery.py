from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
required={'cuba-v1.html','cuba.glb','cuba.blend','mechanism.blend','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','poster.png','poster.jpg','.gitattributes'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(s in p.parts for s in ['node_modules','__pycache__']) and p.suffix not in ['.blend1','.zip'] and p.name not in ['inventory.json','delivery-check.json','package-output.txt'])
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files};assert required<=manifest.keys()
assert not json.loads((R/'source-check.json').read_text())['collisions'];assert json.loads((R/'theme-check.json').read_text())['status']=='PASS';assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
h=manifest['cuba-v1.html']['bytes'];g=manifest['cuba.glb']['bytes'];assert h<5000000
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'cuba-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert a.testzip() is None;assert set(a.namelist())==set(manifest)|{'inventory.json'}
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
r={'status':'PASS','HTML_BYTES':h,'GLB_BYTES':g,'ZIP_BYTES':z.stat().st_size,'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'required_artifacts_verified':sorted(required),'zip_entries':len(files),'archive_readback':True}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
