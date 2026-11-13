from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
def digest(b):return hashlib.sha256(b).hexdigest()
source=json.loads((R/'source-check.json').read_text());assert source['collision_samples']==81 and not source['collisions']
parity=json.loads((R/'parity-check.json').read_text());assert parity['source_and_export_geometry_match']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
browser=json.loads((R/'browser-check.json').read_text());assert len(browser)==3
for c in browser[:2]:assert c['open_close'] and c['reduced_motion'] and not c['errors'] and not c['external_requests']
assert browser[2]['fallback'];assert 'MOTION PASS' in (R/'motion-output.txt').read_text()
html=R/'antigua-and-barbuda-v1.html';glb=R/'antigua-and-barbuda.glb';assert html.stat().st_size<5_000_000
skip={'inventory.json','delivery-check.json','antigua-and-barbuda-v1-source.zip','git-verification.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not {'node_modules','__pycache__'}.intersection(p.relative_to(R).parts) and p.name not in skip and not p.name.endswith('.blend1'))
required={'antigua-and-barbuda-v1.html','antigua-and-barbuda.glb','antigua-and-barbuda.blend','mechanism.blend','design-brief.md','README.md','poster.png','source-check.json','parity-check.json','browser-check.json','theme-check.json','.gitattributes'}
assert required.issubset({p.relative_to(R).as_posix() for p in files})
inventory={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for p in files}
(R/'inventory.json').write_text(json.dumps(inventory,indent=2))
z=R/'antigua-and-barbuda-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
 for p in files+[R/'inventory.json']:f.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as f:
 assert set(f.namelist())==set(inventory)|{'inventory.json'}
 for n,v in inventory.items():assert digest(f.read(n))==v['sha256'] and len(f.read(n))==v['bytes']
out=dict(status='PASS',html_bytes=html.stat().st_size,glb_bytes=glb.stat().st_size,inventory_entries=len(inventory),archive_bytes=z.stat().st_size,archive_sha256=digest(z.read_bytes()),required_artifacts_present=True,archive_readback=True,checks_passed=['source','parity','theme','browser-desktop','browser-mobile','corrupt-GLB','no-JS','decoded-maps','poster','motion','delivery'])
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
