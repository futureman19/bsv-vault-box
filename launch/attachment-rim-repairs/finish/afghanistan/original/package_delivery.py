from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
for n in ['source','parity','browser','extended','theme']:
 assert (R/(n+'-check.json')).is_file(),n
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
assert '# fail 0' in (R/'motion-output.txt').read_text()
html=R/'afghanistan-v1.html';glb=R/'afghanistan.glb';assert html.stat().st_size<5000000
required={'afghanistan-v1.html','afghanistan.glb','afghanistan.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json'}
exclude={'inventory.json','delivery-check.json','codex-output.txt','lane-prompt.txt','setup.py'}
files=sorted(f for f in R.rglob('*') if f.is_file() and not any(p in ['node_modules','__pycache__','.git'] for p in f.relative_to(R).parts) and f.suffix not in ['.zip','.blend1'] and f.name not in exclude)
sha=lambda b:hashlib.sha256(b).hexdigest()
manifest={f.relative_to(R).as_posix():{'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())} for f in files}
assert required<=set(manifest)
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'afghanistan-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as a:
 for f in files:a.write(f,f.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert a.testzip() is None and len(a.namelist())==len(files)
 for name,entry in manifest.items():assert sha(a.read(name))==entry['sha256'] and len(a.read(name))==entry['bytes']
r={'status':'PASS','HTML_BYTES':html.stat().st_size,'GLB_BYTES':glb.stat().st_size,'ZIP_BYTES':z.stat().st_size,'zip_sha256':sha(z.read_bytes()),'archive_readback_verified':True,'required_artifacts_present':True,'inventory_count':len(manifest),'location':'in-folder delivery; no separate copy'}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
