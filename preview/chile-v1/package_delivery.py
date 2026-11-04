from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
required={'chile.blend','chile.glb','chile-v1.html','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json','motion-check.json','acceptance-check.json'}
assert all((R/n).is_file() for n in required)
assert json.loads((R/'acceptance-check.json').read_text())['status']=='PASS'
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert (R/'chile-v1.html').stat().st_size<5_000_000
excluded={'inventory.json','delivery-check.json','chile-v1-source.zip','verification-output.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(n in p.parts for n in ['node_modules','__pycache__']) and p.name not in excluded and p.suffix not in ['.blend1','.zip'])
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
assert required<=manifest.keys()
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'chile-v1-source.zip'
with zipfile.ZipFile(z,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert a.testzip() is None and len(a.namelist())==len(files)
 assert required<=set(a.namelist())
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
r={'status':'PASS','HTML_bytes':(R/'chile-v1.html').stat().st_size,'GLB_bytes':(R/'chile.glb').stat().st_size,'ZIP_bytes':z.stat().st_size,'ZIP_entries':len(files),'ZIP_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'archive_readback_verified':True,'required_artifact_set_verified':True,'inventory_exclusions':sorted(excluded),'no_external_delivery_copy':'The committed folder and its ZIP are the delivery; no separate output path.'}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
