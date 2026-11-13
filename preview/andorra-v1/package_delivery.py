from pathlib import Path
import json,hashlib,zipfile
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def load(n):return json.loads((R/n).read_text())
s=load('source-check.json');assert not s['collisions'] and s['collision_samples']==81
assert load('parity-check.json')['source_and_export_geometry_match']
assert load('theme-check.json')['status']=='PASS' and load('extended-check.json')['status']=='PASS'
b=load('browser-check.json');assert len(b)==3
for case in b[:2]:assert not case['errors'] and not case['external_requests'] and case['open_close'] and case['reduced_motion'] and not case['asset']['degenerate']
assert b[2]['fallback'];assert '# fail 0' in (R/'motion-output.txt').read_text()
assert 'Detached ornament rejected' in (R/'initial/negative-ornament.txt').read_text()
html=R/'andorra-v1.html';assert html.stat().st_size<5000000
im=np.array(Image.open(R/'poster.png').convert('RGBA'));assert (im[:,:,3]>0).mean()>.9 and im[:,:,:3].std()>10
required={'andorra-v1.html','andorra.glb','andorra.blend','mechanism.blend','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json','poster.png','poster.jpg','THREE-LICENSE.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.zip','.blend1'] and p.name not in ['inventory.json','delivery-check.json','package-output.txt'])
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
assert required<=set(manifest)
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'andorra-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as f:
 for p in files:f.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as f:
 assert set(f.namelist())==set(manifest)|{'inventory.json'} and f.testzip() is None
 for name,entry in manifest.items():assert len(f.read(name))==entry['bytes'] and sha(f.read(name))==entry['sha256']
out={'status':'PASS','HTML_BYTES':html.stat().st_size,'GLB_BYTES':(R/'andorra.glb').stat().st_size,'ZIP_BYTES':z.stat().st_size,'zip_sha256':sha(z.read_bytes()),'inventory_entries':len(manifest),'required_files_present':True,'archive_readback':True,'poster_nonblank':True,'checks_passed':['source','parity','theme','browser-desktop','browser-mobile','fallbacks','extended','motion','negative-control','delivery']}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
