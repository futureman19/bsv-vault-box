from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
required={'zambia-v1.html','zambia.glb','zambia.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','geometry-check.json','author.py','maps.py','build.py','verify_source.py','verify_parity.py','verify_browser.py','verify_theme.py','verify_geometry.py','viewer.js','viewer.bundle.js','motion.mjs','template.html','maps/basalt-color.png','maps/basalt-normal.png','maps/basalt-roughness.png'}
assert all((R/p).is_file() for p in required)
assert (R/'zambia-v1.html').stat().st_size<5_000_000
s=json.loads((R/'source-check.json').read_text());assert s['collision_samples']==81 and not s['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert json.loads((R/'geometry-check.json').read_text())['status']=='PASS'
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert {x['case'] for x in b}=={'desktop','mobile','corrupted GLB'}
for x in b[:2]:assert not x['errors'] and not x['external_requests'] and x['open_close'] and x['reduced_motion']
skip={'inventory.json','delivery-check.json','zambia-v1-source.zip','codex-lane.log','lane-prompt.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name not in skip and not p.name.endswith('.blend1') and '__pycache__' not in p.parts)
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
assert required<=inv.keys()
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'zambia-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as out:
 for p in files+[R/'inventory.json']:out.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as inp:
 assert set(inp.namelist())==set(inv)|{'inventory.json'}
 for p,v in inv.items():
  data=inp.read(p);assert len(data)==v['bytes'] and hashlib.sha256(data).hexdigest()==v['sha256']
result={'status':'PASS','html_bytes':inv['zambia-v1.html']['bytes'],'glb_bytes':inv['zambia.glb']['bytes'],'required_artifacts_present':True,'inventory_files':len(inv),'zip_readback_verified':True,'zip_bytes':z.stat().st_size,'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'inventory_sha256':hashlib.sha256((R/'inventory.json').read_bytes()).hexdigest(),'exclusions':sorted(skip),'note':'Inventory excludes its own hash and packaging envelopes to avoid recursion; optional rejected Codex log omitted from package.'}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
