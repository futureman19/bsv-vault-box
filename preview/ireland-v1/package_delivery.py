from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
required={'ireland.blend','ireland.glb','ireland-v1.html','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','motion-output.txt'}
assert all((R/f).is_file() for f in required)
s=json.loads((R/'source-check.json').read_text());assert s['collision_samples']==81 and not s['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
for name in ['theme-check.json','extended-check.json']:assert json.loads((R/name).read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert len(b)==3 and all(not row.get('errors',[]) and not row.get('external_requests',[]) for row in b)
assert '# fail 0' in (R/'motion-output.txt').read_text()
html=(R/'ireland-v1.html').stat().st_size;glb=(R/'ireland.glb').stat().st_size
assert html<5_000_000
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.relative_to(R).parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.zip','.blend1'] and p.name not in ['inventory.json','delivery-check.json','package-output.txt'])
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
assert required<=set(inv)
(R/'inventory.json').write_text(json.dumps(inv,indent=2));files.append(R/'inventory.json')
z=R/'ireland-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
 for p in files:archive.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as archive:
 assert set(archive.namelist())=={p.relative_to(R).as_posix() for p in files}
 assert archive.testzip() is None
 for p in files:assert archive.read(p.relative_to(R).as_posix())==p.read_bytes()
r={'status':'PASS','HTML_BYTES':html,'GLB_BYTES':glb,'ZIP_BYTES':z.stat().st_size,'zip_sha256':sha(z.read_bytes()),'inventory_entries':len(inv),'required_artifacts_present':True,'archive_readback_verified':True,'html_sha256':sha((R/'ireland-v1.html').read_bytes()),'glb_sha256':sha((R/'ireland.glb').read_bytes())}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
