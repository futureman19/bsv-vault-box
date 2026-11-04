from pathlib import Path
import hashlib,json,zipfile
from PIL import Image,ImageStat
R=Path(__file__).resolve().parent
skip={'inventory.json','delivery-check.json','guinea-source.zip'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.name not in skip and p.suffix!='.blend1')
required={'guinea.blend','guinea.glb','guinea-v1.html','poster.png','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json'}
assert required<={p.relative_to(R).as_posix() for p in files}
assert (R/'guinea-v1.html').stat().st_size<5_000_000
im=Image.open(R/'poster.png').convert('RGB');assert max(ImageStat.Stat(im).stddev)>10
s=json.loads((R/'source-check.json').read_text());assert s['collision_samples']==81 and not s['collisions']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'guinea-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for p in files+[R/'inventory.json']:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())==set(inv)|{'inventory.json'}
 for n,v in inv.items():
  data=a.read(n);assert len(data)==v['bytes'] and hashlib.sha256(data).hexdigest()==v['sha256']
r={'status':'PASS','html_bytes':(R/'guinea-v1.html').stat().st_size,'glb_bytes':(R/'guinea.glb').stat().st_size,'inventory_files':len(inv),'archive_bytes':z.stat().st_size,'archive_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'archive_readback':True,'poster_nonblank':True}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
