from pathlib import Path
import json,hashlib,zipfile
from PIL import Image
R=Path(__file__).resolve().parent
s=json.loads((R/'source-check.json').read_text());assert s['collision_samples']==81 and not s['collisions']
p=json.loads((R/'parity-check.json').read_text());assert p['source_and_export_geometry_match'] and max(p['source_to_glb_max'],p['glb_to_source_max'])<1e-5
for n in ['theme-check.json','extended-check.json']:assert json.loads((R/n).read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert {x['case'] for x in b}=={'desktop','mobile','corrupted GLB'}
for x in b[:2]:assert not x['errors'] and not x['external_requests'] and x['reduced_motion'] and x['open_close'] and x['reset_mid_motion'] and not x['overflow'] and x['asset']['degenerate']==x['asset']['nonfinite']==0
assert b[2]['fallback'] and not b[2]['unhandled_errors']
assert (R/'mongolia-v1.html').stat().st_size<5_000_000
im=Image.open(R/'poster.png').convert('RGBA');assert im.getchannel('A').getextrema()[1]>0 and max(im.convert('RGB').getextrema()[0])>20
required={'mongolia-v1.html','mongolia.glb','mongolia.blend','mechanism.blend','design-brief.md','README.md','poster.png','poster.jpg','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json'}
files=sorted(f for f in R.rglob('*') if f.is_file() and not any(v in f.parts for v in ['node_modules','__pycache__']) and f.suffix not in ['.zip','.blend1'] and f.name not in ['inventory.json','delivery-check.json','package-output.txt'])
inv={f.relative_to(R).as_posix():{'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in files};assert required<=inv.keys()
(R/'inventory.json').write_text(json.dumps(inv,indent=2));files.append(R/'inventory.json');z=R/'mongolia-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for f in files:a.write(f,f.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())==set(inv)|{'inventory.json'} and a.testzip() is None
 for f in files:assert a.read(f.relative_to(R).as_posix())==f.read_bytes()
out={'status':'PASS','HTML_BYTES':(R/'mongolia-v1.html').stat().st_size,'GLB_BYTES':(R/'mongolia.glb').stat().st_size,'ZIP_BYTES':z.stat().st_size,'ZIP_SHA256':hashlib.sha256(z.read_bytes()).hexdigest(),'inventory_entries':len(inv),'archive_entries':len(files),'required_artifacts_present':True,'archive_readback_verified':True,'checks_passed':['source','parity','theme','browser_desktop','browser_mobile','corrupt_glb','nojs','portable_maps','motion','delivery']}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
