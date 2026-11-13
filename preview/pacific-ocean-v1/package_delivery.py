"""Exact-byte inventory and allowlisted-source archive, independently read back."""
from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
excluded={'inventory.json','delivery-check.json','pacific-ocean-v1-source.zip','verification-output.txt','package-output.txt','lane-output.txt','lane-prompt.md','setup.py'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__','.git']) and p.name not in excluded and not p.name.endswith(('.blend1','.pyc')))
required={'pacific-ocean-v1.html','pacific-ocean.glb','pacific-ocean.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','.gitattributes','mechanism.blend'}
assert required.issubset({p.name for p in files})
def entry(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
inv={p.relative_to(R).as_posix():entry(p.read_bytes()) for p in files}
(R/'inventory.json').write_text(json.dumps(inv,indent=2),encoding='utf8')
z=R/'pacific-ocean-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,6) as a:
 for p in files+[R/'inventory.json']:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())==set(inv)|{'inventory.json'}
 for n,v in inv.items():assert entry(a.read(n))==v
 assert a.read('inventory.json')==(R/'inventory.json').read_bytes()
assert inv['pacific-ocean-v1.html']['bytes']<5_000_000
r={'status':'PASS','html_bytes':inv['pacific-ocean-v1.html']['bytes'],'glb_bytes':inv['pacific-ocean.glb']['bytes'],'inventory_entries':len(inv),'required_artifacts_present':sorted(required),'all_archive_bytes_verified':True,'archive':entry(z.read_bytes()),'inventory':entry((R/'inventory.json').read_bytes()),'exclusions':sorted(excluded),'note':'Inventory excludes itself, delivery envelope, archive and active verification log to avoid circular hashes. No dependencies or backups archived.'}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print('DELIVERY PASS',json.dumps(r))
