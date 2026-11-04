from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
assert all(x['status']=='PASS' for x in json.loads((R/'acceptance.json').read_text()))
required={'peru-v1.html','peru.blend','peru.glb','mechanism.blend','poster.png','poster.jpg','README.md','design-brief.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json','.gitattributes'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__','.git']) and p.suffix not in ['.zip','.blend1'] and p.name not in ['inventory.json','delivery-check.json','lane-log.txt','lane-prompt.md','lane-result.txt'])
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files};assert required<=set(manifest)
assert manifest['peru-v1.html']['bytes']<5000000
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json');z=R/'peru-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())=={p.relative_to(R).as_posix() for p in files};assert a.testzip() is None
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
r={'status':'PASS','HTML_BYTES':manifest['peru-v1.html']['bytes'],'GLB_BYTES':manifest['peru.glb']['bytes'],'ZIP_BYTES':z.stat().st_size,'ZIP_SHA256':hashlib.sha256(z.read_bytes()).hexdigest(),'archive_entries':len(files),'required_artifacts_present':True,'archive_readback':True};(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
