"""Exact byte inventory and archive readback; all writes stay in Fiji folder."""
from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
skip={'inventory.json','delivery-check.json','fiji-v1-source.zip','git-verification.txt'}
def eligible(p):
 return p.is_file() and p.name not in skip and not any(x in {'node_modules','__pycache__'} for x in p.relative_to(R).parts) and p.suffix not in {'.blend1','.pyc'}
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
files={p.relative_to(R).as_posix():identity(p.read_bytes()) for p in sorted(R.rglob('*')) if eligible(p)}
required={'fiji.glb','fiji.blend','fiji-v1.html','mechanism.blend','poster.png','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','acceptance-check.json','author.py','maps.py','verify_all.py','THREE-LICENSE.txt','.gitattributes'}
assert required<=set(files),required-set(files)
assert files['fiji-v1.html']['bytes']<5000000
(R/'inventory.json').write_text(json.dumps(files,indent=2),encoding='utf8')
zpath=R/'fiji-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for name in [*files,'inventory.json']:z.write(R/name,name)
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(files)|{'inventory.json'}
 for name,entry in files.items():assert identity(z.read(name))==entry,name
 assert z.read('inventory.json')==(R/'inventory.json').read_bytes()
result=dict(status='PASS',html_bytes=files['fiji-v1.html']['bytes'],glb_bytes=files['fiji.glb']['bytes'],inventory_count=len(files),required_artifacts_present=True,archive_readback=True,zip=identity(zpath.read_bytes()),inventory=identity((R/'inventory.json').read_bytes()),self_reference_exclusions=sorted(skip))
(R/'delivery-check.json').write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps(result,indent=2))
