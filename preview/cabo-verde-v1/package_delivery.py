from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
required={'cabo-verde-v1.html','cabo-verde.glb','cabo-verde.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','author.py','maps.py','build.py','verify_source.py','verify_parity.py','verify_theme.py','verify_browser.py','verify_extended.py','motion.mjs','viewer.js','template.html','maps/scoria-color.png','maps/scoria-normal.png','maps/scoria-roughness.png'}
assert (R/'cabo-verde-v1.html').stat().st_size<5000000
s=json.loads((R/'source-check.json').read_text());assert s['status']=='PASS' and s['collision_samples']==81 and not s['collisions']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert len(b)==3
for c in b[:2]:assert c['open_close'] and c['reduced_motion'] and not c['errors'] and not c['external_requests'] and c['asset']['bytes']==(R/'cabo-verde.glb').stat().st_size
exclude={'inventory.json','delivery-check.json','cabo-verde-v1-source.zip','delivery-output.txt','codex-lane.log','lane-prompt.md','build-output.txt'}
files={p.relative_to(R).as_posix():p for p in R.rglob('*') if p.is_file() and p.name not in exclude and '__pycache__' not in p.parts and p.suffix not in ['.blend1','.pyc']}
assert required<=set(files),required-set(files)
def record(p):return {'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
inv={n:record(p) for n,p in sorted(files.items())};(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'cabo-verde-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
 for n,p in files.items():f.write(p,n)
 f.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(z) as f:
 assert set(f.namelist())==set(files)|{'inventory.json'}
 for n,v in inv.items():assert hashlib.sha256(f.read(n)).hexdigest()==v['sha256']
r={'status':'PASS','html':record(R/'cabo-verde-v1.html'),'glb':record(R/'cabo-verde.glb'),'source_zip':record(z),'required_artifacts':sorted(required),'inventory_count':len(inv),'zip_readback_all_entries':True,'inventory_sha256':record(R/'inventory.json')['sha256'],'excluded_envelopes':sorted(exclude),'checks_passed':['source','81-pose motion','hinge attachment','parity','theme and negative crater control','browser desktop/mobile','corrupt GLB fallback','no-JS fallback','decoded maps','motion unit tests','size cap','SHA256 inventory','ZIP readback']}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print('DELIVERY PASS');print('HTML_BYTES',r['html']['bytes'],'GLB_BYTES',r['glb']['bytes']);print(json.dumps(r,indent=2))
