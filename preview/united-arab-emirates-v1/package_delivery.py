from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
required={'uae.blend','uae.glb','united-arab-emirates-v1.html','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json'}
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
assert (R/'united-arab-emirates-v1.html').stat().st_size<5000000
files=sorted(f for f in R.rglob('*') if f.is_file() and not any(x in f.relative_to(R).parts for x in ['node_modules','__pycache__']) and f.suffix not in ['.zip','.blend1'] and f.name not in ['inventory.json','delivery-check.json'])
inventory={f.relative_to(R).as_posix():{'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in files}
assert required<=inventory.keys()
(R/'inventory.json').write_text(json.dumps(inventory,indent=2))
z=R/'united-arab-emirates-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for f in files+[R/'inventory.json']:a.write(f,f.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())==set(inventory)|{'inventory.json'}
 assert a.testzip() is None
 for n,v in inventory.items():assert hashlib.sha256(a.read(n)).hexdigest()==v['sha256']
r={'status':'PASS','HTML_BYTES':(R/'united-arab-emirates-v1.html').stat().st_size,'GLB_BYTES':(R/'uae.glb').stat().st_size,'ZIP_BYTES':z.stat().st_size,'ZIP_SHA256':hashlib.sha256(z.read_bytes()).hexdigest(),'payload_files':len(inventory),'required_artifacts_present':True,'archive_exact_hash_readback':True}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
