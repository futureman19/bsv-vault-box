from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
required={'micronesia-v1.html','micronesia.glb','micronesia.blend','mechanism.blend','poster.png','poster.jpg','README.md','design-brief.md','author.py','build.py','maps.py','verify_source.py','verify_parity.py','verify_theme.py','verify_browser.py','verify_extended.py','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','motion-output.txt','maps/basalt-color.png','maps/basalt-roughness.png','maps/pale-color.png','.gitattributes'}
exclude={'inventory.json','delivery-check.json','package-output.txt','git-verification.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(s in p.parts for s in ['node_modules','__pycache__']) and p.name not in exclude and p.suffix not in ['.zip','.blend1','.pyc'])
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
assert required<=set(inv),required-set(inv)
assert inv['micronesia-v1.html']['bytes']<5_000_000
source=json.loads((R/'source-check.json').read_text());assert source['collision_samples']==81 and source['collisions']==[]
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
browser=json.loads((R/'browser-check.json').read_text());assert {r['case'] for r in browser}=={'desktop','mobile','corrupted GLB'}
for row in browser[:2]:assert not row['errors'] and not row['external_requests'] and row['open_close'] and row['reduced_motion']
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
zpath=R/'micronesia-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(inv)|{'inventory.json'}
 for name,entry in inv.items():
  data=z.read(name);assert len(data)==entry['bytes'] and hashlib.sha256(data).hexdigest()==entry['sha256']
out={'status':'PASS','html_bytes':inv['micronesia-v1.html']['bytes'],'glb_bytes':inv['micronesia.glb']['bytes'],'payload_files':len(inv),'explicit_required_artifacts':sorted(required),'all_archive_bytes_readback_verified':True,'zip_bytes':zpath.stat().st_size,'zip_sha256':hashlib.sha256(zpath.read_bytes()).hexdigest(),'inventory_sha256':hashlib.sha256((R/'inventory.json').read_bytes()).hexdigest()}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
