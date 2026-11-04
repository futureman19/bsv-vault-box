from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
excluded={'inventory.json','delivery-check.json','comoros-source.zip','codex-lane.log','lane-prompt.txt'}
files=[p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.name not in excluded and p.suffix!='.blend1']
required={'comoros.blend','comoros.glb','comoros-v1.html','README.md','design-brief.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json'}
assert required <= {p.name for p in files}
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)}
assert inv['comoros-v1.html']['bytes']<5000000
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'comoros-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
 for p in files+[R/'inventory.json']:f.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as f:
 assert set(f.namelist())==set(inv)|{'inventory.json'}
 for name,v in inv.items():
  b=f.read(name);assert len(b)==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256']
r={'status':'PASS','html_bytes':inv['comoros-v1.html']['bytes'],'glb_bytes':inv['comoros.glb']['bytes'],'inventory_entries':len(inv),'zip_readback':True,'zip_bytes':z.stat().st_size,'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest()}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
