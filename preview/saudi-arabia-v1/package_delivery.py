from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
required={'saudi-arabia-v1.html','saudi-arabia.glb','saudi-arabia.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','extended-check.json','theme-check.json','negative-control.json','motion-check.json'}
assert all((R/n).is_file() for n in required)
assert (R/'saudi-arabia-v1.html').stat().st_size<5_000_000
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
for n in ['extended-check','theme-check','negative-control','motion-check']:assert json.loads((R/(n+'.json')).read_text())['status']=='PASS'
browser=json.loads((R/'browser-check.json').read_text());assert len(browser)==3
for c in browser[:2]:assert not c['external_requests'] and not c['errors'] and c['open_close'] and c['reduced_motion']
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.relative_to(R).parts for x in ['node_modules','__pycache__']) and p.name not in ['inventory.json','delivery-check.json'] and p.suffix not in ['.zip','.blend1'])
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
assert required<=set(manifest)
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'saudi-arabia-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())=={p.relative_to(R).as_posix() for p in files}
 assert a.testzip() is None
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
report={'status':'PASS','HTML_BYTES':(R/'saudi-arabia-v1.html').stat().st_size,'GLB_BYTES':(R/'saudi-arabia.glb').stat().st_size,'ZIP_BYTES':z.stat().st_size,'zip_sha256':sha(z.read_bytes()),'inventory_entries':len(manifest),'archive_entries':len(files),'required_artifacts_present':True,'archive_readback_verified':True,'scope':'local source folder and archive; no deployment or external delivery directory'}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
