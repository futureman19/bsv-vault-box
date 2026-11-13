from pathlib import Path
import hashlib,json,zipfile
from PIL import Image
R=Path(__file__).resolve().parent
required={'madagascar-v1.html','madagascar.glb','madagascar.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json','motion-output.txt','maps/limestone-color.png','maps/limestone-roughness.png','maps/cleft-color.png'}
def check_sizes(html,glb):
 assert 0<html<5000000 and glb>0
h=(R/'madagascar-v1.html').stat().st_size;g=(R/'madagascar.glb').stat().st_size
check_sizes(h,g)
try:check_sizes(5000000,g)
except AssertionError:negative=True
else:raise AssertionError('Size negative control accepted')
s=json.loads((R/'source-check.json').read_text());assert s['collision_samples']==81 and not s['collisions']
p=json.loads((R/'parity-check.json').read_text());assert p['source_and_export_geometry_match']
for f in ['theme-check.json','extended-check.json']:assert json.loads((R/f).read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert {x['case'] for x in b}=={'desktop','mobile','corrupted GLB'}
for x in b[:2]:assert x['offline_file'] and not x['errors'] and not x['external_requests']
im=Image.open(R/'poster.png').convert('RGB');assert max(v[1]-v[0] for v in im.getextrema())>50
exclude={'inventory.json','delivery-check.json','madagascar-v1-source.zip'}
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name not in exclude and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.suffix!='.blend1')
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
assert required<=inv.keys()
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'madagascar-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
 a.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())==set(inv)|{'inventory.json'}
 for n,v in inv.items():
  data=a.read(n);assert len(data)==v['bytes'] and hashlib.sha256(data).hexdigest()==v['sha256']
out={'status':'PASS','HTML_bytes':h,'GLB_bytes':g,'ZIP_bytes':z.stat().st_size,'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'inventory_files':len(inv),'required_artifacts_present':True,'archive_readback_verified':True,'size_negative_control_rejected':negative}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
