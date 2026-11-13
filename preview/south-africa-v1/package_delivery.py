from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
required={'design-brief.md','README.md','south-africa.blend','south-africa.glb','south-africa-v1.html','poster.png','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','motion-output.txt'}
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
browser=json.loads((R/'browser-check.json').read_text());assert len(browser)==3
assert all(not x['errors'] and not x['external_requests'] for x in browser[:2])
assert (R/'south-africa-v1.html').stat().st_size<5000000
excluded={'inventory.json','delivery-check.json'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(q in p.parts for q in ['node_modules','__pycache__']) and p.suffix not in ['.zip','.blend1'] and p.name not in excluded)
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files};assert required<=manifest.keys()
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json');z=R/'south-africa-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as f:
 for p in files:f.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as f:
 assert f.testzip() is None;assert set(f.namelist())=={p.relative_to(R).as_posix() for p in files}
 for p in files:assert f.read(p.relative_to(R).as_posix())==p.read_bytes()
out={'status':'PASS','HTML_BYTES':(R/'south-africa-v1.html').stat().st_size,'GLB_BYTES':(R/'south-africa.glb').stat().st_size,'ZIP_BYTES':z.stat().st_size,'zip_sha256':sha(z.read_bytes()),'required_artifacts_present':True,'archive_readback_verified':True,'inventory_entries':len(manifest)}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
