from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
required={'switzerland.blend','switzerland.glb','switzerland-v1.html','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','run-checks.json'}
assert all((R/n).is_file() for n in required)
assert (R/'switzerland-v1.html').stat().st_size<5000000
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert all(x['exit_code']==0 for x in json.loads((R/'run-checks.json').read_text()))
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.relative_to(R).parts for x in ['node_modules','__pycache__']) and p.name not in {'inventory.json','delivery-check.json','switzerland-v1-source.zip'} and p.suffix not in {'.blend1','.blend2'})
assert required.issubset({p.relative_to(R).as_posix() for p in files})
sha=lambda b:hashlib.sha256(b).hexdigest()
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
(R/'inventory.json').write_text(json.dumps(inv,indent=2));files.append(R/'inventory.json')
z=R/'switzerland-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert a.testzip() is None and len(a.namelist())==len(files)
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
out={'status':'PASS','HTML_BYTES':(R/'switzerland-v1.html').stat().st_size,'GLB_BYTES':(R/'switzerland.glb').stat().st_size,'ZIP_BYTES':z.stat().st_size,'zip_sha256':sha(z.read_bytes()),'entries':len(files),'required_artifacts_present':True,'archive_readback':True,'inventory':inv}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print({k:v for k,v in out.items() if k!='inventory'})
