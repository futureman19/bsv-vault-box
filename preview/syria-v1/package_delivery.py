from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
required={'syria-v1.html','syria.glb','syria.blend','mechanism.blend','poster.png','poster.jpg','README.md','design-brief.md','source-check.json','parity-check.json','browser-check.json','extended-check.json','theme-check.json','motion-output.txt'}
assert all((R/n).is_file() for n in required)
assert (R/'syria-v1.html').stat().st_size<5000000
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
for case in json.loads((R/'browser-check.json').read_text())[:2]:
 assert not case['errors'] and not case['external_requests'] and case['open_close'] and case['reduced_motion']
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(s in {'node_modules','__pycache__'} for s in p.relative_to(R).parts) and p.suffix not in {'.zip','.blend1'} and p.name not in {'inventory.json','delivery-check.json'})
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
assert required<=set(manifest)
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'syria-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
 for p in files:archive.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as archive:
 assert set(archive.namelist())=={p.relative_to(R).as_posix() for p in files}
 assert archive.testzip() is None
 for p in files:assert archive.read(p.relative_to(R).as_posix())==p.read_bytes()
report={'status':'PASS','HTML_BYTES':(R/'syria-v1.html').stat().st_size,'GLB_BYTES':(R/'syria.glb').stat().st_size,'archive_readback':True,'required_artifacts_present':True,'inventory_entries':len(manifest),'zip_bytes':z.stat().st_size,'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest()}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
