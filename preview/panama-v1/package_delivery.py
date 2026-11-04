from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
source=json.loads((R/'source-check.json').read_text());assert source['collision_samples']==81 and not source['collisions']
parity=json.loads((R/'parity-check.json').read_text());assert parity['source_and_export_geometry_match'] and max(parity['source_to_glb_max'],parity['glb_to_source_max'])<1e-5
for n in ['theme','extended']:assert json.loads((R/(n+'-check.json')).read_text())['status']=='PASS'
browser=json.loads((R/'browser-check.json').read_text());assert {x['case'] for x in browser}=={'desktop','mobile','corrupted GLB'}
for x in browser[:2]:assert x['open_close'] and x['rotation'] and x['reduced_motion'] and x['reset_mid_motion'] and not x['errors'] and not x['external_requests'] and not x['overflow']
assert browser[2]['fallback'] and browser[2]['caught_loader_errors']
assert (R/'panama-v1.html').stat().st_size<5_000_000
required={'panama.blend','panama.glb','panama-v1.html','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','THREE-LICENSE.txt'}
allowed={'.py','.js','.mjs','.json','.md','.txt','.html','.png','.jpg','.blend','.glb'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.relative_to(R).parts for x in ['node_modules','__pycache__']) and (p.suffix in allowed or p.name in ['.gitattributes','.gitignore']) and p.name not in {'inventory.json','delivery-check.json','package-output.txt','git-output.txt'})
names={p.relative_to(R).as_posix() for p in files};assert required<=names,required-names
sha=lambda b:hashlib.sha256(b).hexdigest()
inventory={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
(R/'inventory.json').write_text(json.dumps(inventory,indent=2));files.append(R/'inventory.json')
z=R/'panama-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())=={p.relative_to(R).as_posix() for p in files}
 assert a.testzip() is None
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
r={'status':'PASS','HTML_BYTES':(R/'panama-v1.html').stat().st_size,'GLB_BYTES':(R/'panama.glb').stat().st_size,'ZIP_BYTES':z.stat().st_size,'ZIP_SHA256':sha(z.read_bytes()),'inventory_entries':len(inventory),'archive_readback_verified':True,'required_artifacts_verified':sorted(required),'checks_passed':['source','81-pose-motion','hinge-attachment','parity','theme','negative-controls','browser-desktop','browser-mobile','extended','delivery']}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));print('ALL ACCEPTANCE CHECKS PASS')
