from pathlib import Path
import hashlib,json,zipfile
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=json.loads((R/'source-check.json').read_text());assert not source['collisions'] and source['collision_samples']==81
parity=json.loads((R/'parity-check.json').read_text());assert parity['source_and_export_geometry_match'] and max(parity['source_to_glb_max'],parity['glb_to_source_max'])<1e-5
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'theme-negative-control.json').read_text())['status']=='FAIL'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
browser=json.loads((R/'browser-check.json').read_text());assert {x['case'] for x in browser}=={'desktop','mobile','corrupted GLB'}
for c in browser[:2]:assert c['open_close'] and c['reset_mid_motion'] and c['reduced_motion'] and not c['errors'] and not c['external_requests'] and c['asset']['open_projection_max_abs_ndc']<1
im=np.asarray(Image.open(R/'poster.png').convert('RGBA'));assert im[:,:,:3].max()>100 and (im[:,:,3]>0).mean()>.1
required={'timor-leste.blend','timor-leste.glb','timor-leste-v1.html','mechanism.blend','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json','motion-output.txt','poster.png','poster.jpg','.gitattributes'}
files=sorted(f for f in R.rglob('*') if f.is_file() and not any(s in f.parts for s in ['node_modules','__pycache__']) and f.suffix not in {'.zip','.blend1'} and f.name not in {'inventory.json','delivery-check.json','package-output.txt','git-verification.txt'})
manifest={f.relative_to(R).as_posix():{'bytes':f.stat().st_size,'sha256':sha(f)} for f in files};assert required<=manifest.keys();assert manifest['timor-leste-v1.html']['bytes']<5000000
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'timor-leste-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for f in files:a.write(f,f.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert len(a.namelist())==len(files) and a.testzip() is None
 for f in files:assert a.read(f.relative_to(R).as_posix())==f.read_bytes()
report={'status':'PASS','HTML_BYTES':manifest['timor-leste-v1.html']['bytes'],'GLB_BYTES':manifest['timor-leste.glb']['bytes'],'zip_bytes':z.stat().st_size,'zip_sha256':sha(z),'inventory_sha256':sha(R/'inventory.json'),'archive_entries':len(files),'archive_readback':True,'explicit_required_files_present':True,'poster_pixel_check':True,'checks_passed':['source','parity','theme','extended','browser','motion','negative-control rejection','delivery']}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
