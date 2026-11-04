from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
required={'marshall-islands-v1.html','marshall-islands.glb','marshall-islands.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','motion-output.txt','maps/weave-color.png','maps/weave-roughness.png'}
exclude={'inventory.json','delivery-check.json','marshall-islands-v1-source.zip','package-output.txt','git-verification.txt'}
def identity(data):return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
files={p.relative_to(R).as_posix():p for p in R.rglob('*') if p.is_file() and 'node_modules' not in p.parts and '__pycache__' not in p.parts and p.name not in exclude and not p.name.endswith('.blend1')}
assert required<=set(files),required-set(files)
html=(R/'marshall-islands-v1.html').read_bytes();assert len(html)<5_000_000
s=json.loads((R/'source-check.json').read_text());assert s['collision_samples']==81 and not s['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
for f in ['theme-check.json','extended-check.json']:assert json.loads((R/f).read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert len(b)==3 and all(not x['errors'] and not x['external_requests'] for x in b[:2]) and b[2]['fallback']
from PIL import Image
import numpy as np
median=np.median(np.asarray(Image.open(R/'maps/weave-color.png')),axis=(0,1));assert np.max(abs(median-np.array([186,151,96])))<18,median
inventory={n:identity(p.read_bytes()) for n,p in sorted(files.items())};(R/'inventory.json').write_text(json.dumps(inventory,indent=2))
zpath=R/'marshall-islands-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for n,p in files.items():z.write(p,n)
 z.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(files)|{'inventory.json'}
 for n,item in inventory.items():assert identity(z.read(n))==item,n
result={'status':'PASS','html':identity(html),'glb':identity((R/'marshall-islands.glb').read_bytes()),'archive':identity(zpath.read_bytes()),'inventory_count':len(inventory),'archive_readback':'all paths and bytes match','palette_median_rgb':median.tolist(),'required_artifacts':sorted(required),'exclusions':'node_modules, caches, Blender backups, recursive inventory/archive/check envelopes, actively written packaging/Git logs'}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
