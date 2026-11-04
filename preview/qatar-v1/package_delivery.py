from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
required={'qatar-v1.html','qatar.glb','qatar.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json'}
assert all((R/x).is_file() for x in required)
assert (R/'qatar-v1.html').stat().st_size<5_000_000
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
allowed={'.py','.js','.mjs','.json','.md','.txt','.html','.png','.jpg','.blend','.glb'}
files=sorted(p for p in R.rglob('*') if p.is_file() and (p.parent==R or p.parent.name=='maps') and (p.suffix in allowed or p.name in {'.gitattributes','.gitignore'}) and p.name not in {'inventory.json','delivery-check.json'})
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
assert required<=manifest.keys();(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'qatar-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert len(a.namelist())==len(files) and a.testzip() is None
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
r={'status':'PASS','HTML_BYTES':(R/'qatar-v1.html').stat().st_size,'GLB_BYTES':(R/'qatar.glb').stat().st_size,'ZIP_BYTES':z.stat().st_size,'ZIP_SHA256':hashlib.sha256(z.read_bytes()).hexdigest(),'inventory_entries':len(manifest),'archive_readback':True,'required_artifacts_present':True}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
