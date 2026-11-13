from pathlib import Path
import hashlib,json,zipfile
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
s=json.loads((R/'source-check.json').read_text()); assert s['saved_source_reopened'] and s['collision_samples']==81 and not s['collisions']
p=json.loads((R/'parity-check.json').read_text());assert p['source_and_export_geometry_match']
for n in ['theme-check.json','motion-check.json','extended-check.json']:assert json.loads((R/n).read_text())['PASS']
b=json.loads((R/'browser-check.json').read_text());assert len(b)==3
for c in b[:2]:assert c['offline_file'] and c['open_close'] and c['reduced_motion'] and not c['external_requests'] and not c['errors']
assert b[2]['fallback']
a=np.asarray(Image.open(R/'poster.png').convert('RGBA'));assert np.mean(a[:,:,3]>0)>.10 and np.std(a[:,:,:3])>10
html=(R/'tajikistan-v1.html').read_bytes();assert len(html)<5_000_000
# Explicit required set catches missing deliverables, not only corrupted existing files.
required={'tajikistan.blend','tajikistan.glb','tajikistan-v1.html','design-brief.md','README.md','poster.png','poster.jpg','author.py','mechanism.blend','source-check.json','parity-check.json','browser-check.json','theme-check.json','motion-check.json','extended-check.json','maps/stone-color.png','maps/stone-roughness.png','maps/mineral.png'}
files=sorted(f for f in R.rglob('*') if f.is_file() and not any(x in f.relative_to(R).parts for x in ['node_modules','__pycache__']) and f.suffix not in {'.blend1','.zip'} and f.name not in {'inventory.json','delivery-check.json','package-output.txt','git-verification.txt'})
manifest={f.relative_to(R).as_posix():{'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())} for f in files}
assert required<=manifest.keys()
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'tajikistan-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for f in files:a.write(f,f.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert a.testzip() is None and len(a.namelist())==len(files)
 for f in files:assert a.read(f.relative_to(R).as_posix())==f.read_bytes()
report={'PASS':True,'HTML_BYTES':len(html),'GLB_BYTES':(R/'tajikistan.glb').stat().st_size,'HTML_SHA256':sha(html),'GLB_SHA256':sha((R/'tajikistan.glb').read_bytes()),'ZIP_BYTES':z.stat().st_size,'ZIP_SHA256':sha(z.read_bytes()),'entries':len(files),'required_artifacts_present':True,'archive_readback_verified':True,'poster_nonempty':True,'inventory_excludes':'itself, ZIP and delivery envelope; package-output and git-verification logs to avoid changing self-reference'}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));print('PASS delivery',json.dumps(report,indent=2))
