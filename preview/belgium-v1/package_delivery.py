from pathlib import Path
import hashlib,json,zipfile
from PIL import Image
R=Path(__file__).resolve().parent
required={'belgium-v1.html','belgium.glb','belgium.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','extended-check.json','theme-check.json','motion-output.txt'}
assert all((R/n).is_file() for n in required)
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert json.loads((R/'theme-check.json').read_text())['negative_control']['detached_ornament_rejected']
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert len(b)==3
for x in b[:2]:assert not x['errors'] and not x['external_requests'] and x['open_close'] and x['reset_mid_motion'] and x['reduced_motion']
assert '# fail 0' in (R/'motion-output.txt').read_text()
assert (R/'belgium-v1.html').stat().st_size<5_000_000
im=Image.open(R/'poster.png').convert('RGBA');assert im.getextrema()[3][1]>0 and max(v[1] for v in im.getextrema()[:3])>100
excluded={'inventory.json','delivery-check.json','lane-prompt.txt','lane-output.txt','setup.py','package-output.txt','git-verification.txt'}
allowed={'.py','.js','.mjs','.json','.md','.txt','.html','.png','.jpg','.blend','.glb'}
files=sorted(p for p in R.rglob('*') if p.is_file() and (p.parent==R or p.parent.name=='maps') and (p.suffix in allowed or p.name in {'.gitattributes','.gitignore'}) and p.name not in excluded)
names={p.relative_to(R).as_posix() for p in files};assert required<=names
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'belgium-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert a.testzip() is None and len(a.namelist())==len(files)
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
report={'status':'PASS','HTML_BYTES':(R/'belgium-v1.html').stat().st_size,'GLB_BYTES':(R/'belgium.glb').stat().st_size,'ZIP_BYTES':z.stat().st_size,'ZIP_entries':len(files),'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'required_artifacts_present':True,'archive_readback_verified':True,'poster_real_image_nonblank':True,'inventory_payload_count':len(manifest)}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));print('DELIVERY PASS',json.dumps(report))
