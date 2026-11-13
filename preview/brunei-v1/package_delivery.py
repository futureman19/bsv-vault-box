from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
for n in ['source-check','parity-check','theme-check','browser-check','extended-check']:
 assert (R/(n+'.json')).exists()
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
assert '# fail 0' in (R/'motion-output.txt').read_text()
assert (R/'brunei-v1.html').stat().st_size<5_000_000
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.relative_to(R).parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.zip','.blend1'] and p.name not in ['inventory.json','delivery-check.json','packaging-output.txt'])
required={'brunei.blend','brunei.glb','brunei-v1.html','poster.png','poster.jpg','design-brief.md','README.md'}
assert required.issubset({p.name for p in files})
sha=lambda b:hashlib.sha256(b).hexdigest()
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
(R/'inventory.json').write_text(json.dumps(inv,indent=2));files.append(R/'inventory.json')
z=R/'brunei-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())=={p.relative_to(R).as_posix() for p in files}
 assert a.testzip() is None
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
r={'status':'PASS','HTML_BYTES':(R/'brunei-v1.html').stat().st_size,'GLB_BYTES':(R/'brunei.glb').stat().st_size,'ZIP_BYTES':z.stat().st_size,'zip_sha256':sha(z.read_bytes()),'inventory_entries':len(inv),'zip_entries':len(files),'exact_readback':True}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
