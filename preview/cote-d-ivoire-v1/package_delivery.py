from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
required={'design-brief.md','README.md','cote-d-ivoire.blend','cote-d-ivoire.glb','cote-d-ivoire-v1.html','poster.png','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json'}
assert all((R/n).is_file() for n in required)
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
assert (R/'cote-d-ivoire-v1.html').stat().st_size<5_000_000
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(s in p.parts for s in ['node_modules','__pycache__']) and p.suffix not in ['.zip','.blend1'] and p.name not in ['inventory.json','delivery-check.json'])
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
assert required<=manifest.keys()
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'cote-d-ivoire-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())=={p.relative_to(R).as_posix() for p in files};assert a.testzip() is None
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
out={'status':'PASS','HTML_BYTES':(R/'cote-d-ivoire-v1.html').stat().st_size,'GLB_BYTES':(R/'cote-d-ivoire.glb').stat().st_size,'zip_bytes':z.stat().st_size,'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'entries':len(files),'required_artifacts_present':sorted(required),'archive_readback':True}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
