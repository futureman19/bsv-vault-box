from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
excluded={'inventory.json','delivery-check.json','egypt-v1-source.zip'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.name not in excluded and not p.name.endswith('.blend1'))
required={'egypt-v1.html','egypt.glb','egypt.blend','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json'}
assert required <= {p.name for p in files}
assert (R/'egypt-v1.html').stat().st_size<5000000
inventory={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
(R/'inventory.json').write_text(json.dumps(inventory,indent=2))
z=R/'egypt-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for p in files+[R/'inventory.json']:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())==set(inventory)|{'inventory.json'}
 for name,identity in inventory.items():
  b=a.read(name);assert len(b)==identity['bytes'] and hashlib.sha256(b).hexdigest()==identity['sha256']
result={'status':'PASS','html_bytes':(R/'egypt-v1.html').stat().st_size,'glb_bytes':(R/'egypt.glb').stat().st_size,'archive_entries':len(inventory)+1,'archive_bytes':z.stat().st_size,'archive_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'inventory_sha256':hashlib.sha256((R/'inventory.json').read_bytes()).hexdigest(),'archive_readback_verified':True}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
