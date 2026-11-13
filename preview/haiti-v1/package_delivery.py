from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
required={'haiti-v1.html','haiti.glb','haiti.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','extended-check.json','theme-check.json','motion-check.txt'}
assert all((R/n).is_file() for n in required)
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert all(json.loads((R/n).read_text())['status']=='PASS' for n in ['theme-check.json','extended-check.json'])
html=(R/'haiti-v1.html').stat().st_size;glb=(R/'haiti.glb').stat().st_size;assert html<5000000
files=sorted(f for f in R.rglob('*') if f.is_file() and not any(n in f.relative_to(R).parts for n in ['node_modules','__pycache__']) and f.name not in {'inventory.json','delivery-check.json','haiti-v1-source.zip','delivery-output.txt','final-verification.txt'} and f.suffix not in {'.blend1','.log'})
assert required <= {f.name for f in files}
inv={f.relative_to(R).as_posix():{'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in files}
(R/'inventory.json').write_text(json.dumps(inv,indent=2));files.append(R/'inventory.json')
z=R/'haiti-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for f in files:a.write(f,f.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert len(a.namelist())==len(files) and a.testzip() is None
 for f in files:assert a.read(f.relative_to(R).as_posix())==f.read_bytes()
out={'status':'PASS','HTML_BYTES':html,'GLB_BYTES':glb,'ZIP_BYTES':z.stat().st_size,'inventory_entries':len(inv),'archive_entries':len(files),'archive_readback_verified':True,'required_artifacts_present':True,'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest()}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
