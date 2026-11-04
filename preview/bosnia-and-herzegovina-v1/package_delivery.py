from pathlib import Path
import hashlib,json,zipfile
from PIL import Image,ImageStat
R=Path(__file__).resolve().parent
html=R/'bosnia-and-herzegovina-v1.html';glb=R/'bosnia-and-herzegovina.glb'
def gate_size(n):assert n<5_000_000
try:gate_size(5_000_000)
except AssertionError:negative=True
else:raise AssertionError('Oversize HTML accepted')
gate_size(html.stat().st_size)
s=json.loads((R/'source-check.json').read_text());assert s['collision_samples']==81 and not s['collisions']
p=json.loads((R/'parity-check.json').read_text());assert p['source_and_export_geometry_match']
for f in ['theme-check.json','extended-check.json']:assert json.loads((R/f).read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert len(b)==3 and all(not c['errors'] and not c['external_requests'] and c['open_close'] and c['reduced_motion'] for c in b[:2]);assert b[2]['fallback']
assert '# fail 0' in (R/'motion-output.txt').read_text()
im=Image.open(R/'poster.png').convert('RGBA');assert sum(ImageStat.Stat(im.convert('RGB')).mean)>30;assert ImageStat.Stat(im.getchannel('A')).mean[0]>100
required={'design-brief.md','README.md','bosnia-and-herzegovina.blend','bosnia-and-herzegovina.glb','bosnia-and-herzegovina-v1.html','poster.png','poster.jpg','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json','motion-output.txt','maps/copper-color.png','maps/copper-roughness.png','maps/copper-normal.png'}
excluded={'inventory.json','delivery-check.json','bosnia-and-herzegovina-v1-source.zip','package-output.txt'}
files=[p for p in R.rglob('*') if p.is_file() and not {'node_modules','__pycache__'}.intersection(p.relative_to(R).parts) and p.name not in excluded and not p.name.endswith('.blend1')]
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)}
assert required<=set(inv)
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
zpath=R/'bosnia-and-herzegovina-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(inv)|{'inventory.json'}
 for name,item in inv.items():
  data=z.read(name);assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256'],name
out={'status':'PASS','html_bytes':html.stat().st_size,'glb_bytes':glb.stat().st_size,'oversized_negative_control_rejected':negative,'required_artifacts_present':True,'zip_readback_verified':True,'payload_files':len(inv),'source_zip_bytes':zpath.stat().st_size,'source_zip_sha256':hashlib.sha256(zpath.read_bytes()).hexdigest(),'inventory_sha256':hashlib.sha256((R/'inventory.json').read_bytes()).hexdigest()}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
