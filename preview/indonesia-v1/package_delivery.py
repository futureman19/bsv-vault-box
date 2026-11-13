from pathlib import Path
import hashlib,json,zipfile
from PIL import Image
R=Path(__file__).resolve().parent
required={'design-brief.md','README.md','indonesia.blend','mechanism.blend','indonesia.glb','indonesia-v1.html','poster.png','poster.jpg','source-check.json','parity-check.json','theme-check.json','pivot-check.json','browser-check.json','extended-check.json','motion-output.txt'}
assert all((R/n).is_file() for n in required)
source=json.loads((R/'source-check.json').read_text());assert not source['collisions'] and source['collision_samples']==81
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
for n in ['theme','pivot','extended']:assert json.loads((R/(n+'-check.json')).read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert {x['case'] for x in b}=={'desktop','mobile','corrupted GLB'}
assert all(not x['errors'] and not x['external_requests'] for x in b[:2])
assert '# fail 0' in (R/'motion-output.txt').read_text()
im=Image.open(R/'poster.png').convert('RGBA');assert im.getextrema()[3][1]>0 and max(v[1] for v in im.getextrema()[:3])>30
html=(R/'indonesia-v1.html').stat().st_size;glb=(R/'indonesia.glb').stat().st_size;assert html<5000000
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(a in p.relative_to(R).parts for a in ['node_modules','__pycache__']) and p.suffix not in ['.zip','.blend1'] and p.name not in ['inventory.json','delivery-check.json'])
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
assert required<=inv.keys()
(R/'inventory.json').write_text(json.dumps(inv,indent=2));files.append(R/'inventory.json')
z=R/'indonesia-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as out:
 for p in files:out.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as out:
 assert out.testzip() is None and len(out.namelist())==len(files)
 assert required<=set(out.namelist())
 for p in files:assert out.read(p.relative_to(R).as_posix())==p.read_bytes()
r={'status':'PASS','HTML_BYTES':html,'GLB_BYTES':glb,'ZIP_BYTES':z.stat().st_size,'ZIP_SHA256':hashlib.sha256(z.read_bytes()).hexdigest(),'archive_entries':len(files),'required_artifacts_present':True,'archive_exact_readback':True,'checks_passed':['source','parity','theme','pivots','motion','browser desktop/mobile','extended','delivery']}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
