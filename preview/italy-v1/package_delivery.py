from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
required={'italy-v1.html','italy.glb','italy.blend','mechanism.blend','design-brief.md','README.md','poster.png','poster.jpg','source-check.json','parity-check.json','theme-check.json','theme-negative.json','browser-check.json','extended-check.json','motion-output.txt'}
source=json.loads((R/'source-check.json').read_text());assert source['collision_samples']==81 and not source['collisions'];assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS';assert json.loads((R/'theme-negative.json').read_text())['status']=='FAIL';assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
for c in json.loads((R/'browser-check.json').read_text())[:2]:assert c['offline_file'] and not c['errors'] and not c['external_requests'] and c['asset']['nonfinite']==c['asset']['degenerate']==0
assert '# fail 0' in (R/'motion-output.txt').read_text();assert (R/'italy-v1.html').stat().st_size<5000000
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.relative_to(R).parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.zip','.blend1'] and p.name not in ['inventory.json','delivery-check.json'])
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files};assert required<=manifest.keys()
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json');z=R/'italy-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert required<=set(a.namelist());assert len(a.namelist())==len(files);assert a.testzip() is None
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
r={'status':'PASS','HTML_BYTES':(R/'italy-v1.html').stat().st_size,'GLB_BYTES':(R/'italy.glb').stat().st_size,'ZIP_BYTES':z.stat().st_size,'ZIP_SHA256':sha(z.read_bytes()),'payload_files':len(manifest),'archive_entries':len(files),'required_artifacts_present':True,'archive_readback_verified':True,'inventory':'inventory.json','self_reference_exclusions':['inventory.json','delivery-check.json','italy-v1-source.zip']};(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
