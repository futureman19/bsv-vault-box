from pathlib import Path
import hashlib,json,zipfile
from PIL import Image
R=Path(__file__).resolve().parent
required={'lebanon.blend','lebanon.glb','lebanon-v1.html','poster.png','poster.jpg','README.md','design-brief.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','motion-output.txt','author.py','maps.py','mechanism.blend'}
skip={'inventory.json','delivery-check.json','staging-check.json','package-output.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.relative_to(R).parts for x in ['node_modules','__pycache__','.git']) and p.suffix not in ['.zip','.blend1'] and p.name not in skip)
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
assert required<=inv.keys();assert inv['lebanon-v1.html']['bytes']<5_000_000
im=Image.open(R/'poster.png').convert('RGB');assert max(im.getextrema()[0])>50
source=json.loads((R/'source-check.json').read_text());assert source['collision_samples']==81 and not source['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
browser=json.loads((R/'browser-check.json').read_text());assert {x['case'] for x in browser}=={'desktop','mobile','corrupted GLB'}
for c in browser[:2]:assert not c['errors'] and not c['external_requests'] and c['reduced_motion'] and c['open_close']
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'lebanon-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for n in inv:a.write(R/n,n)
 a.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())==set(inv)|{'inventory.json'}
 for n,v in inv.items():assert hashlib.sha256(a.read(n)).hexdigest()==v['sha256']
out={'status':'PASS','html_bytes':inv['lebanon-v1.html']['bytes'],'glb_bytes':inv['lebanon.glb']['bytes'],'files_in_inventory':len(inv),'required_artifacts_verified':sorted(required),'zip_bytes':z.stat().st_size,'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'archive_readback':True,'checks_passed':['source','parity','theme','browser-desktop','browser-mobile','corrupt-GLB','no-JS','motion','decoded-maps','delivery']}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print('PASS all acceptance checks');print('HTML_BYTES',out['html_bytes'],'GLB_BYTES',out['glb_bytes']);print('PASS SHA256 inventory and archive readback',len(inv),'files')
