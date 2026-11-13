from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
source=json.loads((R/'source-check.json').read_text());assert not source['collisions'] and source['collision_samples']==81
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
browser=json.loads((R/'browser-check.json').read_text());assert len(browser)==3 and all(not c.get('errors') and not c.get('external_requests') for c in browser)
assert '# fail 0' in (R/'motion-output.txt').read_text()
html=R/'pakistan-v1.html';glb=R/'pakistan.glb';assert html.stat().st_size<5000000
required={'pakistan.blend','pakistan.glb','pakistan-v1.html','poster.png','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.relative_to(R).parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.zip','.blend1'] and p.name not in ['inventory.json','delivery-check.json'])
def sha(data):return hashlib.sha256(data).hexdigest()
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files};assert required<=set(manifest)
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'pakistan-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert a.testzip() is None and set(a.namelist())=={p.relative_to(R).as_posix() for p in files}
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
report=dict(status='PASS',HTML_BYTES=html.stat().st_size,GLB_BYTES=glb.stat().st_size,ZIP_BYTES=z.stat().st_size,ZIP_entries=len(files),zip_sha256=sha(z.read_bytes()),archive_readback_verified=True,required_artifacts_verified=True,checks_passed=['source','parity','theme','browser desktop/mobile','extended','motion','delivery'])
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
