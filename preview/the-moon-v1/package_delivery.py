from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
required={'the-moon-v1.html','the-moon.glb','the-moon.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','extended-check.json','theme-check.json'}
assert all((R/n).is_file() for n in required)
s=json.loads((R/'source-check.json').read_text());assert not s['collisions'] and s['collision_samples']==81
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert len(b)==3 and all(not v['errors'] and not v['external_requests'] for v in b[:2]) and b[2]['fallback']
assert (R/'the-moon-v1.html').stat().st_size<5_000_000
excluded={'inventory.json','delivery-check.json','lane-prompt.txt'}
allowed={'.py','.js','.mjs','.json','.md','.txt','.html','.png','.jpg','.blend','.glb'}
files=sorted(p for p in R.rglob('*') if p.is_file() and (p.suffix in allowed or p.name=='.gitattributes') and p.name not in excluded and (p.parent==R or p.parent.name in ['maps','initial']))
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
assert required<=manifest.keys()
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'the-moon-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as f:
 for p in files:f.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as f:
 assert set(f.namelist())=={p.relative_to(R).as_posix() for p in files};assert f.testzip() is None
 for p in files:assert f.read(p.relative_to(R).as_posix())==p.read_bytes()
out={'status':'PASS','HTML_bytes':(R/'the-moon-v1.html').stat().st_size,'GLB_bytes':(R/'the-moon.glb').stat().st_size,'ZIP_bytes':z.stat().st_size,'ZIP_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'ZIP_entries':len(files),'required_artifacts_present':True,'archive_readback_verified':True,'inventory_sha256':hashlib.sha256((R/'inventory.json').read_bytes()).hexdigest()}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
