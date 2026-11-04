from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
skip={'inventory.json','delivery-check.json','honduras-v1-source.zip'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(s in p.parts for s in ['node_modules','__pycache__']) and p.name not in skip and p.suffix!='.blend1')
required={'honduras-v1.html','honduras.glb','honduras.blend','mechanism.blend','poster.png','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json'}
assert required <= {p.name for p in files}
def ident(data):return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
inv={p.relative_to(R).as_posix():ident(p.read_bytes()) for p in files}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'honduras-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as f:
 for p in files+[R/'inventory.json']:f.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as f:
 assert set(f.namelist())==set(inv)|{'inventory.json'}
 for n,expected in inv.items():assert ident(f.read(n))==expected
 assert f.read('inventory.json')==(R/'inventory.json').read_bytes()
assert inv['honduras-v1.html']['bytes']<5000000
out={'status':'PASS','html_bytes':inv['honduras-v1.html']['bytes'],'glb_bytes':inv['honduras.glb']['bytes'],'inventory_entries':len(inv),'required_artifacts':sorted(required),'zip_readback_verified':True,'zip':ident(z.read_bytes()),'inventory':ident((R/'inventory.json').read_bytes())}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
