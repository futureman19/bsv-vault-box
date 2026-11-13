from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
excluded={'inventory.json','delivery-check.json','gabon-v1-source.zip'}
files=[p for p in R.rglob('*') if p.is_file() and p.name not in excluded and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.suffix!='.blend1']
required={'gabon.blend','gabon.glb','gabon-v1.html','poster.png','README.md','design-brief.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json'}
assert required<={p.name for p in files}
def ident(b):return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
inv={p.relative_to(R).as_posix():ident(p.read_bytes()) for p in sorted(files)}
assert inv['gabon-v1.html']['bytes']<5000000
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'gabon-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for p in files+[R/'inventory.json']:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())==set(inv)|{'inventory.json'}
 for n,v in inv.items():assert ident(a.read(n))==v
out=dict(status='PASS',html_bytes=inv['gabon-v1.html']['bytes'],glb_bytes=inv['gabon.glb']['bytes'],payload_files=len(inv),required_artifacts_present=True,zip_readback=True,archive=ident(z.read_bytes()))
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
