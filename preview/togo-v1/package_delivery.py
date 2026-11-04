from pathlib import Path
from PIL import Image
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
checks=['source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json']
s=json.loads((R/checks[0]).read_text());assert s['collision_samples']==81 and not s['collisions']
p=json.loads((R/checks[1]).read_text());assert p['source_and_export_geometry_match']
assert json.loads((R/checks[2]).read_text())['status']=='PASS'
assert json.loads((R/checks[4]).read_text())['status']=='PASS'
for c in json.loads((R/checks[3]).read_text())[:2]:assert c['offline_file'] and not c['errors'] and not c['external_requests']
assert '# fail 0' in (R/'motion-output.txt').read_text()
h=R/'togo-v1.html';g=R/'togo.glb';assert h.stat().st_size<5_000_000
im=Image.open(R/'poster.png').convert('RGBA');assert im.getextrema()[3][1]>0 and max(im.convert('RGB').getextrema()[0])>40
allowed={'.py','.js','.mjs','.json','.md','.txt','.html','.png','.jpg','.blend','.glb'}
files=sorted(f for f in R.rglob('*') if f.is_file() and (f.parent==R or f.parent==R/'maps') and (f.suffix in allowed or f.name in ['.gitattributes','.gitignore']) and f.name not in ['inventory.json','delivery-check.json'])
required={'togo-v1.html','togo.glb','togo.blend','mechanism.blend','poster.png','README.md','design-brief.md',*checks}
assert required <= {f.name for f in files}
def sha(b):return hashlib.sha256(b).hexdigest()
manifest={f.relative_to(R).as_posix():{'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())} for f in files}
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'togo-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for f in files:a.write(f,f.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert len(a.namelist())==len(files) and a.testzip() is None
 for f in files:assert a.read(f.relative_to(R).as_posix())==f.read_bytes()
r={'status':'PASS','HTML_BYTES':h.stat().st_size,'GLB_BYTES':g.stat().st_size,'ZIP_BYTES':z.stat().st_size,'ZIP_entries':len(files),'zip_sha256':sha(z.read_bytes()),'archive_readback_verified':True,'explicit_required_artifacts_verified':sorted(required),'poster_nonblank':True}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
