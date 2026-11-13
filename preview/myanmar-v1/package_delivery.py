from pathlib import Path
import json,hashlib,zipfile
from PIL import Image
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
s=json.loads((R/'source-check.json').read_text());assert s['collision_samples']==81 and not s['collisions']
p=json.loads((R/'parity-check.json').read_text());assert p['source_and_export_geometry_match'] and max(p['source_to_glb_max'],p['glb_to_source_max'])<1e-5
for f in ['theme-check.json','extended-check.json','pivot-check.json']:assert json.loads((R/f).read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert len(b)==3 and all(not c['errors'] and not c['external_requests'] and c['reduced_motion'] and c['open_close'] for c in b[:2]);assert b[2]['fallback']
assert '# fail 0' in (R/'motion-output.txt').read_text()
html=(R/'myanmar-v1.html').read_bytes();assert len(html)<5000000
im=Image.open(R/'poster.png').convert('RGB');assert max(v[1]-v[0] for v in im.getextrema())>50
exclude={'inventory.json','delivery-check.json','package-output.txt','git-evidence.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(s in p.parts for s in ['node_modules','__pycache__']) and p.name not in exclude and p.suffix not in ['.zip','.blend1'])
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
required={'myanmar-v1.html','myanmar.glb','myanmar.blend','mechanism.blend','poster.png','README.md','design-brief.md','source-check.json','parity-check.json','browser-check.json','theme-check.json'};assert required<=set(inv)
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'myanmar-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as archive:
 for p in files+[R/'inventory.json']:archive.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as archive:
 assert set(archive.namelist())==set(inv)|{'inventory.json'}
 for n,v in inv.items():assert sha(archive.read(n))==v['sha256'] and len(archive.read(n))==v['bytes']
out={'status':'PASS','html_bytes':len(html),'glb_bytes':(R/'myanmar.glb').stat().st_size,'inventory_files':len(inv),'zip_bytes':z.stat().st_size,'zip_sha256':sha(z.read_bytes()),'archive_readback':True,'required_artifacts_present':True,'checks_passed':['source','81-pose collision sampling','hinge attachments','parity','theme and negative control','pivots','motion','desktop/mobile offline browser','extended maps/noJS','delivery']}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
