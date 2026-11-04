from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
load=lambda n:json.loads((R/n).read_text())
s=load('source-check.json');assert s['collision_samples']==81 and not s['collisions'] and s['saved_source_reopened']
assert load('parity-check.json')['source_and_export_geometry_match']
assert load('theme-check.json')['status']=='PASS' and load('extended-check.json')['status']=='PASS'
b=load('browser-check.json');assert {x['case'] for x in b}=={'desktop','mobile','corrupted GLB'}
for x in b[:2]:assert x['open_close'] and x['reduced_motion'] and not x['errors'] and not x['external_requests']
html=R/'atlantic-ocean-v1.html';assert html.stat().st_size<5000000
required={'atlantic.blend','atlantic.glb','atlantic-ocean-v1.html','design-brief.md','README.md','poster.png','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json'}
allowed={'.py','.js','.mjs','.json','.md','.txt','.html','.png','.jpg','.blend','.glb'}
files=sorted(p for p in R.rglob('*') if p.is_file() and (p.suffix in allowed or p.name=='.gitattributes') and p.name not in {'inventory.json','delivery-check.json'} and (p.parent==R or p.parent.name in {'initial','maps'}))
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
assert required<=manifest.keys()
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'atlantic-ocean-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())=={p.relative_to(R).as_posix() for p in files}
 assert a.testzip() is None
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
out=dict(status='PASS',HTML_BYTES=html.stat().st_size,GLB_BYTES=(R/'atlantic.glb').stat().st_size,ZIP_BYTES=z.stat().st_size,ZIP_SHA256=hashlib.sha256(z.read_bytes()).hexdigest(),archive_entries=len(files),required_artifacts_verified=True,archive_readback_verified=True,checks_passed=['source','parity','motion-81','theme','browser-desktop-mobile','extended','delivery'])
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
