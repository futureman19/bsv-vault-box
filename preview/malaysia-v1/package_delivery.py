from pathlib import Path
import hashlib,json,zipfile
from PIL import Image
R=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
s=json.loads((R/'source-check.json').read_text());assert not s['collisions'] and s['collision_samples']==81
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
for n in ['theme-check.json','extended-check.json']:assert json.loads((R/n).read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert {x['case'] for x in b}=={'desktop','mobile','corrupted GLB'}
for x in b[:2]:assert x['offline_file'] and x['open_close'] and x['reduced_motion'] and not x['errors'] and not x['external_requests']
assert '# fail 0' in (R/'motion-output.txt').read_text()
assert (R/'malaysia-v1.html').stat().st_size<5000000
im=Image.open(R/'poster.png').convert('RGB');assert max(im.getextrema()[0])>50
allowed={'.py','.js','.mjs','.json','.md','.txt','.html','.png','.jpg','.blend','.glb'}
files=sorted(p for p in R.rglob('*') if p.is_file() and (p.suffix in allowed or p.name in {'.gitattributes','.gitignore'}) and (p.parent==R or p.parent.name=='maps') and p.name not in {'inventory.json','delivery-check.json'})
required={'malaysia.blend','malaysia.glb','malaysia-v1.html','poster.png','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json'}
assert required<={p.name for p in files}
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'malaysia-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert len(a.namelist())==len(files) and a.testzip() is None
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
out={'status':'PASS','HTML_BYTES':(R/'malaysia-v1.html').stat().st_size,'GLB_BYTES':(R/'malaysia.glb').stat().st_size,'ZIP_BYTES':z.stat().st_size,'ZIP_SHA256':sha(z.read_bytes()),'archive_entries':len(files),'archive_readback':True,'required_artifacts_present':True}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
