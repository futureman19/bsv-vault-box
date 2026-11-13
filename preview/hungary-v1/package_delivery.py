from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
source=json.loads((R/'source-check.json').read_text());assert source['collision_samples']==81 and not source['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
browser=json.loads((R/'browser-check.json').read_text());assert len(browser)==3
for row in browser[:2]:
 assert row['offline_file'] and row['open_close'] and row['reduced_motion'] and not row['errors'] and not row['external_requests']
assert browser[2]['fallback']
assert '# fail 0' in (R/'motion-output.txt').read_text()
assert 'AssertionError: Detached ornament' in (R/'negative-control.txt').read_text()
required={'hungary-v1.html','hungary.glb','hungary.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.blend1','.zip'] and p.name not in ['inventory.json','delivery-check.json','package-output.txt'])
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
assert required<=manifest.keys();assert manifest['hungary-v1.html']['bytes']<5000000
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'hungary-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())=={p.relative_to(R).as_posix() for p in files};assert a.testzip() is None
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
report={'status':'PASS','HTML_BYTES':manifest['hungary-v1.html']['bytes'],'GLB_BYTES':manifest['hungary.glb']['bytes'],'archive_entries':len(files),'required_artifacts_present':True,'archive_readback_verified':True,'zip_bytes':z.stat().st_size,'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'checks_passed':['source','parity','theme','browser-desktop','browser-mobile','motion','extended','negative-control','delivery']}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
