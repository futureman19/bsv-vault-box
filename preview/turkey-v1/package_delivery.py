from pathlib import Path
import hashlib,json,zipfile
from PIL import Image
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
s=json.loads((R/'source-check.json').read_text());assert s['collision_samples']==81 and not s['collisions']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert len(b)==3
for case in b[:2]:assert case['offline_file'] and not case['errors'] and not case['external_requests'] and case['open_close'] and case['reduced_motion']
im=Image.open(R/'poster.png').convert('RGBA');assert im.getextrema()[3][1]>0 and max(im.convert('RGB').getextrema()[i][1] for i in range(3))>100
required={'turkey.glb','turkey.blend','turkey-v1.html','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','motion-output.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.blend1','.zip'] and p.name not in ['inventory.json','delivery-check.json'])
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
assert required<=manifest.keys();assert manifest['turkey-v1.html']['bytes']<5_000_000
(R/'inventory.json').write_text(json.dumps(manifest,indent=2))
z=R/'turkey-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for p in files+[R/'inventory.json']:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())==set(manifest)|{'inventory.json'};assert a.testzip() is None
 for n,v in manifest.items():assert len(a.read(n))==v['bytes'] and sha(a.read(n))==v['sha256']
report={'status':'PASS','HTML_BYTES':manifest['turkey-v1.html']['bytes'],'GLB_BYTES':manifest['turkey.glb']['bytes'],'ZIP_BYTES':z.stat().st_size,'zip_sha256':sha(z.read_bytes()),'inventory_entries':len(manifest),'required_artifacts_present':True,'archive_readback_verified':True,'poster_decoded_nonempty':True}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
