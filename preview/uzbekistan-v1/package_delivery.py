from pathlib import Path
from PIL import Image
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
required={'uzbekistan-v1.html','uzbekistan.blend','uzbekistan.glb','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','motion-output.txt','negative-detach.txt'}
files=[p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.zip','.blend1'] and p.name not in ['inventory.json','delivery-check.json']]
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(files)}
assert required<=inv.keys();assert inv['uzbekistan-v1.html']['bytes']<5_000_000
assert json.loads((R/'source-check.json').read_text())['collisions']==[]
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
assert '# fail 0' in (R/'motion-output.txt').read_text()
assert 'AssertionError: Ornament detached from lid' in (R/'negative-detach.txt').read_text()
im=Image.open(R/'poster.png').convert('RGB');assert max(c[1]-c[0] for c in im.getextrema())>100
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'uzbekistan-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
 for n in inv:f.write(R/n,n)
 f.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(z) as f:
 assert set(f.namelist())==set(inv)|{'inventory.json'}
 for n,d in inv.items():assert sha(f.read(n))==d['sha256'] and len(f.read(n))==d['bytes']
out={'status':'PASS','html_bytes':inv['uzbekistan-v1.html']['bytes'],'glb_bytes':inv['uzbekistan.glb']['bytes'],'inventory_files':len(inv),'required_artifacts_present':True,'zip_inventory_and_hash_readback':True,'zip_bytes':z.stat().st_size,'zip_sha256':sha(z.read_bytes()),'inventory_sha256':sha((R/'inventory.json').read_bytes()),'poster_nonblack':True}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print('DELIVERY PASS',json.dumps(out))
