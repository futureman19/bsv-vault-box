from pathlib import Path
import json,hashlib,zipfile
from PIL import Image
R=Path(__file__).resolve().parent
required={'oman.blend','oman.glb','oman-v1.html','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','motion-output.txt'}
assert all((R/n).is_file() for n in required)
s=json.loads((R/'source-check.json').read_text());assert not s['collisions'] and s['collision_samples']==81
p=json.loads((R/'parity-check.json').read_text());assert max(p['source_to_glb_max'],p['glb_to_source_max'])<1e-5
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert {x['case'] for x in b}=={'desktop','mobile','corrupted GLB'}
for x in b[:2]:assert not x['errors'] and not x['external_requests'] and x['open_close'] and x['reduced_motion']
assert '# fail 0' in (R/'motion-output.txt').read_text()
assert (R/'oman-v1.html').stat().st_size<5000000
im=Image.open(R/'poster.png').convert('RGBA');assert im.getextrema()[3][1]>0 and max(im.convert('RGB').getextrema()[0])>30
exclude={'inventory.json','delivery-check.json','oman-v1-source.zip'}
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name not in exclude and not any(x in p.relative_to(R).parts for x in ['node_modules','__pycache__']) and p.suffix!='.blend1')
sha=lambda data:hashlib.sha256(data).hexdigest()
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files};assert required<=set(inv)
(R/'inventory.json').write_text(json.dumps(inv,indent=2));files.append(R/'inventory.json')
z=R/'oman-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
 for p in files:archive.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as archive:
 assert set(archive.namelist())==set(inv)|{'inventory.json'};assert archive.testzip() is None
 for p in files:assert archive.read(p.relative_to(R).as_posix())==p.read_bytes()
report={'status':'PASS','HTML_BYTES':(R/'oman-v1.html').stat().st_size,'GLB_BYTES':(R/'oman.glb').stat().st_size,'ZIP_BYTES':z.stat().st_size,'ZIP_SHA256':sha(z.read_bytes()),'inventory_entries':len(inv),'archive_readback':True,'required_artifacts_present':True,'checks_passed':['source','parity','theme','browser-desktop','browser-mobile','corrupt-glb','no-js','decoded-maps','motion','delivery']}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
