from pathlib import Path
import hashlib,json,zipfile
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent
load=lambda n:json.loads((R/n).read_text())
source=load('source-check.json');assert source['collision_samples']==81 and not source['collisions'] and source['moving_meshes']==21
assert load('parity-check.json')['source_and_export_geometry_match']
assert load('theme-check.json')['status']=='PASS' and load('theme-check.json')['negative_control']['detached_ornament_rejected']
assert load('extended-check.json')['status']=='PASS'
browser=load('browser-check.json');assert len(browser)==3
for case in browser[:2]:
 assert case['offline_file'] and not case['errors'] and not case['external_requests'] and case['reduced_motion'] and case['open_close'] and case['rotation']
assert browser[2]['fallback'] and browser[2]['caught_loader_errors']
a=np.asarray(Image.open(R/'poster.png').convert('RGBA'));coverage=float((a[:,:,3]>0).mean());assert coverage>.1 and a[:,:,:3].max()>100
assert (R/'bahamas-v1.html').stat().st_size<5_000_000
assert 'fail 0' in (R/'motion-output.txt').read_text()
required={'bahamas.blend','bahamas.glb','bahamas-v1.html','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','author.py','maps.py','maps/limestone.png','maps/roughness.png','maps/sand.png','.gitattributes'}
excluded={'inventory.json','delivery-check.json','bahamas-v1-source.zip','package-output.txt','git-verification.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(s in p.relative_to(R).parts for s in ['node_modules','__pycache__']) and p.name not in excluded and not p.name.endswith('.blend1'))
names={p.relative_to(R).as_posix() for p in files};assert required<=names
sha=lambda b:hashlib.sha256(b).hexdigest()
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'bahamas-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as arc:
 for p in files+[R/'inventory.json']:arc.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as arc:
 assert set(arc.namelist())==names|{'inventory.json'}
 for n,v in inv.items():assert len(arc.read(n))==v['bytes'] and sha(arc.read(n))==v['sha256']
checks=['source','parity','motion','theme','desktop-browser','mobile-browser','corrupt-GLB-fallback','no-JS-fallback','runtime-maps','poster','delivery']
out={'status':'PASS','html_bytes':(R/'bahamas-v1.html').stat().st_size,'glb_bytes':(R/'bahamas.glb').stat().st_size,'checks_passed':checks,'inventory_files':len(inv),'archive_entries':len(inv)+1,'archive_bytes':z.stat().st_size,'archive_sha256':sha(z.read_bytes()),'required_artifacts_present':True,'archive_readback_verified':True,'poster_nontransparent_fraction':coverage}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2))
for check in checks:print(check.upper()+' PASS')
print('HTML_BYTES',out['html_bytes'],'GLB_BYTES',out['glb_bytes']);print(json.dumps(out,indent=2))
