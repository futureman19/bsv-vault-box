from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
required={'rwanda.blend','rwanda.glb','rwanda-v1.html','mechanism.blend','poster.png','poster.jpg','author.py','maps.py','README.md','design-brief.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','contract-check.json','desktop-closed.png','desktop-open.png','mobile-closed.png','mobile-open.png','mobile-fallback.png','mobile-nojs.png','maps/earth.png','maps/wood.png','maps/ivory.png','THREE-LICENSE.txt'}
excluded={'inventory.json','delivery-check.json','rwanda-v1-source.zip','lane-output.txt','lane-prompt.md'}
files={p.relative_to(R).as_posix():p for p in R.rglob('*') if p.is_file() and p.name not in excluded and '__pycache__' not in p.parts and not p.name.endswith('.blend1') and 'node_modules' not in p.parts}
assert required<=set(files),required-set(files)
def record(data):return dict(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
inv={n:record(p.read_bytes()) for n,p in sorted(files.items())}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'rwanda-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as archive:
 for n,p in sorted(files.items()):archive.write(p,n)
 archive.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(z) as archive:
 assert set(archive.namelist())==set(files)|{'inventory.json'}
 for n in files:assert record(archive.read(n))==inv[n],n
 assert archive.read('inventory.json')==(R/'inventory.json').read_bytes()
assert inv['rwanda-v1.html']['bytes']<5000000
report=dict(status='PASS',html_bytes=inv['rwanda-v1.html']['bytes'],glb_bytes=inv['rwanda.glb']['bytes'],required_artifacts_present=True,archive_readback_verified=True,inventory_files=len(inv),archive=record(z.read_bytes()))
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));print('DELIVERY PASS',json.dumps(report))
