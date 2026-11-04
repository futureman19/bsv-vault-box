from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
source=json.loads((R/'source-check.json').read_text());assert source['collision_samples']==81 and not source['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
for n in ['theme','extended']:assert json.loads((R/(n+'-check.json')).read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert {x['case'] for x in b}=={'desktop','mobile','corrupted GLB'}
for x in b[:2]:assert not x['errors'] and not x['external_requests'] and x['reduced_motion'] and x['open_close']
assert '# fail 0' in (R/'motion-output.txt').read_text()
assert 'Terrain detached from lid' in (R/'initial/detached-terrain-negative.txt').read_text()
h=R/'tanzania-v1.html';g=R/'tanzania.glb';assert h.stat().st_size<5000000
required={'design-brief.md','README.md','tanzania.blend','tanzania.glb','tanzania-v1.html','poster.png','poster.jpg','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json'}
allowed={'.md','.py','.js','.mjs','.json','.txt','.png','.jpg','.html','.blend','.glb'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(s in p.parts for s in ['node_modules','__pycache__']) and (p.suffix in allowed or p.name in ['.gitattributes','.gitignore']) and p.name not in ['inventory.json','delivery-check.json'])
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
assert required<=manifest.keys()
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'tanzania-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())=={p.relative_to(R).as_posix() for p in files};assert a.testzip() is None
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
out={'status':'PASS','HTML_BYTES':h.stat().st_size,'GLB_BYTES':g.stat().st_size,'ZIP_BYTES':z.stat().st_size,'ZIP_ENTRIES':len(files),'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'required_artifacts_present':True,'archive_readback_verified':True,'inventory_sha256':hashlib.sha256((R/'inventory.json').read_bytes()).hexdigest()}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
