"""Build exact local archive and verify its explicit required file set."""
from pathlib import Path
import hashlib,json,zipfile
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent
required={'norway.blend','norway.glb','norway-v1.html','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','extended-check.json','theme-check.json','motion-output.txt'}
assert all((R/n).is_file() for n in required)
s=json.loads((R/'source-check.json').read_text());assert s['collision_samples']==81 and not s['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
for n in ['theme-check.json','extended-check.json']:assert json.loads((R/n).read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert len(b)==3
for x in b[:2]:assert not x['errors'] and not x['external_requests'] and x['open_close'] and x['reduced_motion'] and x['asset']['degenerate']==0
assert b[2]['fallback']
pic=np.asarray(Image.open(R/'poster.png').convert('RGBA'));assert pic[:,:,:3].max()>100 and (pic[:,:,3]>0).mean()>.1
assert (R/'norway-v1.html').stat().st_size<5_000_000
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(t in {'node_modules','__pycache__'} for t in p.relative_to(R).parts) and p.suffix not in {'.blend1','.zip'} and p.name not in {'inventory.json','delivery-check.json','delivery-output.txt'})
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
assert required<=manifest.keys()
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'norway-v1-source.zip'
with zipfile.ZipFile(z,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())==set(manifest)|{'inventory.json'} and a.testzip() is None
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
report={'status':'PASS','HTML_BYTES':(R/'norway-v1.html').stat().st_size,'GLB_BYTES':(R/'norway.glb').stat().st_size,'zip_bytes':z.stat().st_size,'zip_entries':len(files),'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'required_files_present':sorted(required),'archive_readback_verified':True,'poster_nonblack_verified':True,'inventory_entries':len(manifest)}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));print('DELIVERY PASS',json.dumps(report))
