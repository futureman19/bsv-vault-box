from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
skip={'inventory.json','delivery-check.json','burundi-source.zip'}
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name not in skip and not any(x in p.parts for x in ['node_modules','__pycache__']) and not p.name.endswith('.blend1'))
required={'burundi.blend','burundi.glb','burundi-v1.html','poster.png','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','extended-check.json'}
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
assert required<=inv.keys()
assert inv['burundi-v1.html']['bytes']<5000000
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
with zipfile.ZipFile(R/'burundi-source.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(R/'burundi-source.zip') as z:
 assert set(z.namelist())==set(inv)|{'inventory.json'}
 for name,item in inv.items():
  data=z.read(name);assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256']
result={'status':'PASS','html_bytes':inv['burundi-v1.html']['bytes'],'glb_bytes':inv['burundi.glb']['bytes'],'inventory_entries':len(inv),'required_artifacts':sorted(required),'archive_readback':True,'archive_bytes':(R/'burundi-source.zip').stat().st_size,'archive_sha256':hashlib.sha256((R/'burundi-source.zip').read_bytes()).hexdigest()}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
