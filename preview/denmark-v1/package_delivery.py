from pathlib import Path
import hashlib,json,zipfile
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent
html=R/'denmark-v1.html';glb=R/'denmark.glb'
assert html.stat().st_size<5000000
assert np.array(Image.open(R/'poster.png').convert('RGB')).std()>10
source=json.loads((R/'source-check.json').read_text());assert source['collision_samples']==81 and not source['collisions']
parity=json.loads((R/'parity-check.json').read_text());assert max(parity['source_to_glb_max'],parity['glb_to_source_max'])<1e-5
for n in ['theme','motion','extended']:assert json.loads((R/(n+'-check.json')).read_text())['status']=='PASS'
browser=json.loads((R/'browser-check.json').read_text());assert len(browser)==3
for x in browser[:2]:assert x['offline_file'] and not x['errors'] and not x['external_requests'] and x['reduced_motion'] and x['open_close'] and x['reset_mid_motion']
assert browser[2]['fallback']
exclude={'inventory.json','delivery-check.json','denmark-v1-source.zip','package-output.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name not in exclude and not any(x in p.parts for x in ['node_modules','__pycache__']) and not p.name.endswith('.blend1'))
required={'denmark-v1.html','denmark.glb','denmark.blend','mechanism.blend','README.md','design-brief.md','poster.png','source-check.json','browser-check.json','parity-check.json'}
assert required <= {str(p.relative_to(R)) for p in files}
def digest(b):return hashlib.sha256(b).hexdigest()
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for p in files}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'denmark-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as out:
 for p in files+[R/'inventory.json']:out.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as inp:
 assert set(inp.namelist())==set(inv)|{'inventory.json'}
 for n,v in inv.items():assert digest(inp.read(n))==v['sha256'] and len(inp.read(n))==v['bytes']
result={'status':'PASS','html_bytes':html.stat().st_size,'glb_bytes':glb.stat().st_size,'zip_bytes':z.stat().st_size,'zip_sha256':digest(z.read_bytes()),'inventory_files':len(inv),'required_artifacts_present':True,'zip_readback_all_hashes':True,'poster_pixel_variation':True,'all_acceptance_checks':'PASS'}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
