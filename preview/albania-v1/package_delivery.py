from pathlib import Path
import json,hashlib,zipfile
from PIL import Image
R=Path(__file__).resolve().parent
required={'albania-v1.html','albania.glb','albania.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json','motion-output.txt','negative-detached-output.txt','maps/stone-color.png','maps/stone-roughness.png','maps/slate-color.png'}
assert all((R/p).is_file() for p in required)
html=(R/'albania-v1.html').read_bytes();glb=(R/'albania.glb').read_bytes();assert len(html)<5000000
src=json.loads((R/'source-check.json').read_text());assert src['collision_samples']==81 and not src['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
for case in json.loads((R/'browser-check.json').read_text())[:2]:assert case['offline_file'] and not case['errors'] and not case['external_requests'] and case['reduced_motion']
assert '# pass 2' in (R/'motion-output.txt').read_text() and '# fail 0' in (R/'motion-output.txt').read_text()
assert 'AssertionError: Detached architecture' in (R/'negative-detached-output.txt').read_text()
im=Image.open(R/'poster.png').convert('RGB');assert max(im.getextrema()[0])-min(im.getextrema()[0])>50
excluded={'inventory.json','delivery-check.json','albania-v1-source.zip','package-output.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not {'node_modules','__pycache__'}&set(p.relative_to(R).parts) and p.name not in excluded and p.suffix!='.blend1')
def identity(data):return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
inv={p.relative_to(R).as_posix():identity(p.read_bytes()) for p in files};assert required<=set(inv)
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'albania-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as f:
 for p in files+[R/'inventory.json']:f.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as f:
 assert set(f.namelist())==set(inv)|{'inventory.json'}
 for name,expected in inv.items():assert identity(f.read(name))==expected,name
result={'status':'PASS','html_bytes':len(html),'glb_bytes':len(glb),'html':identity(html),'glb':identity(glb),'archive':identity(z.read_bytes()),'inventory_entries':len(inv),'required_artifacts_present':True,'zip_readback_all_hashes_match':True,'checks_passed':['source','parity','theme','browser-desktop','browser-mobile','extended','motion','negative-detached','delivery']}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
