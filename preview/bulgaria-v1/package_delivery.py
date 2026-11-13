from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
required={'bulgaria-v1.html','bulgaria.glb','bulgaria.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','material-check.json','motion-output.txt'}
assert all((R/f).is_file() for f in required)
assert (R/'bulgaria-v1.html').stat().st_size<5000000
source=json.loads((R/'source-check.json').read_text());assert source['collision_samples']==81 and not source['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'material-check.json').read_text())['status']=='PASS'
browser=json.loads((R/'browser-check.json').read_text());assert {x['case'] for x in browser}=={'desktop','mobile','corrupted GLB','no-JS'}
assert all(not x['errors'] and not x['external_requests'] for x in browser[:2])
assert '# fail 0' in (R/'motion-output.txt').read_text()
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.zip','.blend1'] and p.name not in ['inventory.json','delivery-check.json'])
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files};assert required<=manifest.keys()
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'bulgaria-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())=={p.relative_to(R).as_posix() for p in files}
 assert a.testzip() is None
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
result=dict(status='PASS',HTML_BYTES=(R/'bulgaria-v1.html').stat().st_size,GLB_BYTES=(R/'bulgaria.glb').stat().st_size,zip_bytes=z.stat().st_size,zip_sha256=sha(z.read_bytes()),archive_entries=len(files),required_artifacts=sorted(required),archive_readback=True)
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
