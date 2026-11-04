from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
read=lambda n:json.loads((R/n).read_text())
s=read('source-check.json');assert s['collision_samples']==81 and not s['collisions'];assert read('parity-check.json')['source_and_export_geometry_match']
assert read('theme-check.json')['PASS'] and read('extended-check.json')['PASS'] and read('negative-control.json')['PASS']
b=read('browser-check.json');assert {r['case'] for r in b}=={'desktop','mobile','corrupted GLB'}
for r in b[:2]:assert not r['errors'] and not r['external_requests'] and r['open_close'] and r['reduced_motion'] and r['asset']['degenerate']==r['asset']['nonfinite']==0
assert '# fail 0' in (R/'motion-output.txt').read_text()
html=R/'croatia-v1.html';glb=R/'croatia.glb';assert html.stat().st_size<5_000_000
exclude={'inventory.json','delivery-check.json'}
files=sorted(f for f in R.rglob('*') if f.is_file() and not any(p in {'node_modules','__pycache__'} for p in f.relative_to(R).parts) and f.name not in exclude and f.suffix not in {'.zip','.blend1'})
sha=lambda b:hashlib.sha256(b).hexdigest()
manifest={f.relative_to(R).as_posix():{'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())} for f in files}
required={'croatia.blend','croatia.glb','croatia-v1.html','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json','motion-output.txt'}
assert required<=manifest.keys()
(R/'inventory.json').write_text(json.dumps(manifest,indent=2))
z=R/'croatia-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for f in files+[R/'inventory.json']:a.write(f,f.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())==set(manifest)|{'inventory.json'} and a.testzip() is None
 for n,d in manifest.items():assert len(a.read(n))==d['bytes'] and sha(a.read(n))==d['sha256']
r={'PASS':True,'HTML_BYTES':html.stat().st_size,'GLB_BYTES':glb.stat().st_size,'html_sha256':sha(html.read_bytes()),'glb_sha256':sha(glb.read_bytes()),'zip_bytes':z.stat().st_size,'zip_sha256':sha(z.read_bytes()),'inventory_count':len(manifest),'required_artifacts_present':True,'archive_readback_verified':True}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print('DELIVERY PASS',json.dumps(r))
