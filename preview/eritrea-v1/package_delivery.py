from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
required={'eritrea.blend','eritrea.glb','eritrea-v1.html','mechanism.blend','poster.png','README.md','design-brief.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','motion-check.json','contract-check.json','material-check.json'}
def sha(b):return hashlib.sha256(b).hexdigest()
def check_sizes(h,g):assert 0<h<5000000 and g>0
h=(R/'eritrea-v1.html').stat().st_size;g=(R/'eritrea.glb').stat().st_size;check_sizes(h,g)
try:check_sizes(5000000,g)
except AssertionError:negative=True
else:raise AssertionError('Byte gate did not reject boundary')
s=json.loads((R/'source-check.json').read_text());assert not s['collisions'] and s['collision_samples']==81
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
for f in ['theme-check.json','motion-check.json','contract-check.json','material-check.json']:assert json.loads((R/f).read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert len(b)==3 and all(not x['errors'] and not x['external_requests'] for x in b[:2]) and b[2]['fallback']
files=[p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.blend1','.zip'] and p.name not in ['inventory.json','delivery-check.json','delivery-output.txt']]
inv={p.relative_to(R).as_posix():dict(bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for p in files};assert required<=set(inv)
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'eritrea-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as out:
 for f in sorted(inv):out.write(R/f,f)
 out.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(z) as src:
 assert set(src.namelist())==set(inv)|{'inventory.json'}
 for f,v in inv.items():assert sha(src.read(f))==v['sha256'] and len(src.read(f))==v['bytes']
r=dict(status='PASS',html_bytes=h,glb_bytes=g,inventory_files=len(inv),required_files_verified=sorted(required),archive_bytes=z.stat().st_size,archive_sha256=sha(z.read_bytes()),archive_readback=True,byte_limit_negative_rejected=negative)
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print('DELIVERY_PASS',json.dumps(r))
