from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
required={'saint-kitts-and-nevis-v1.html','saint-kitts-and-nevis.glb','saint-kitts-and-nevis.blend','mechanism.blend','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','poster.png','poster.jpg','desktop-closed.png','desktop-open.png','mobile-closed.png','mobile-open.png','maps/volcanic-color.png','maps/volcanic-normal.png','maps/volcanic-roughness.png'}
assert all((R/n).is_file() for n in required)
s=json.loads((R/'source-check.json').read_text());assert not s['collisions'] and s['collision_samples']==81
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
for name in ['theme-check.json','extended-check.json']:assert json.loads((R/name).read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert len(b)==3 and all(not x.get('errors',[]) and not x.get('external_requests',[]) for x in b)
html=R/'saint-kitts-and-nevis-v1.html';glb=R/'saint-kitts-and-nevis.glb';assert html.stat().st_size<5_000_000
excluded={'inventory.json','delivery-check.json','package-output.txt','git-evidence.txt','acceptance-output.txt'}
files=sorted(f for f in R.rglob('*') if f.is_file() and f.name not in excluded and f.suffix not in {'.zip','.blend1','.pyc','.log'} and not any(x in f.relative_to(R).parts for x in ['node_modules','__pycache__','.git']))
manifest={f.relative_to(R).as_posix():{'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in files}
assert required<=manifest.keys()
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'saint-kitts-and-nevis-v1-source.zip'
with zipfile.ZipFile(z,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for f in files:a.write(f,f.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert len(a.namelist())==len(files) and a.testzip() is None
 assert required<=set(a.namelist())
 for f in files:assert a.read(f.relative_to(R).as_posix())==f.read_bytes()
out={'status':'PASS','HTML_BYTES':html.stat().st_size,'GLB_BYTES':glb.stat().st_size,'ZIP_BYTES':z.stat().st_size,'archive_entries':len(files),'required_artifacts_verified':sorted(required),'archive_readback_verified':True,'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'inventory_sha256':hashlib.sha256((R/'inventory.json').read_bytes()).hexdigest(),'delivery':'in-folder; no separate copy or deployment'}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
