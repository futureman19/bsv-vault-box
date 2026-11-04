"""Exact-byte folder-local deliverable, archive readback and explicit gate aggregation."""
from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
load=lambda n:json.loads((R/n).read_text())
s=load('source-check.json');assert not s['collisions'] and s['collision_samples']==81 and s['saved_source_reopened']
p=load('parity-check.json');assert p['source_and_export_geometry_match'] and max(p['source_to_glb_max'],p['glb_to_source_max'])<1e-5
assert load('theme-check.json')['status']=='PASS' and len(load('theme-check.json')['negative_controls_rejected'])==2
assert load('extended-check.json')['status']=='PASS'
b=load('browser-check.json');assert [x['case'] for x in b]==['desktop','mobile','corrupted GLB']
assert all(not x['errors'] and not x['external_requests'] and x['open_close'] and x['reduced_motion'] for x in b[:2]);assert b[2]['fallback']
assert 'fail 0' in (R/'motion-output.txt').read_text()
html=R/'vanuatu-v1.html';glb=R/'vanuatu.glb';assert 0<html.stat().st_size<5_000_000
required={'vanuatu-v1.html','vanuatu.glb','vanuatu.blend','mechanism.blend','author.py','maps.py','build.py','design-brief.md','README.md','poster.png','poster.jpg','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','desktop-closed.png','desktop-open.png','mobile-closed.png','mobile-open.png','.gitattributes','.gitignore'}
allow={'.py','.js','.mjs','.json','.md','.txt','.html','.png','.jpg','.blend','.glb'}
files=sorted(p for p in R.rglob('*') if p.is_file() and (p.parent==R or p.parent.name in {'maps','initial'}) and (p.suffix in allow or p.name in {'.gitattributes','.gitignore'}) and p.name not in {'inventory.json','delivery-check.json','package-output.txt'})
sha=lambda b:hashlib.sha256(b).hexdigest()
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
assert required<=manifest.keys(),required-manifest.keys()
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'vanuatu-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())=={p.relative_to(R).as_posix() for p in files};assert a.testzip() is None
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
checks=['source','81-pose motion collisions','hinge attachment','source-export parity','theme and negative controls','runtime texture channels','desktop file://','mobile-emulated file://','corrupt GLB fallback','no-JS fallback','motion unit tests','HTML byte budget','archive readback','SHA-256 inventory']
r={'status':'PASS','HTML_BYTES':html.stat().st_size,'GLB_BYTES':glb.stat().st_size,'ZIP_BYTES':z.stat().st_size,'ZIP_ENTRIES':len(files),'zip_sha256':sha(z.read_bytes()),'inventory_sha256':sha((R/'inventory.json').read_bytes()),'checks_passed':checks,'required_artifacts_verified':sorted(required),'archive_readback_verified':True}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));print('ALL ACCEPTANCE CHECKS PASS')
