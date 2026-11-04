from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
excluded={'inventory.json','delivery-check.json','source.zip','lane-output.txt','lane-prompt.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name not in excluded and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.suffix!='.blend1')
required={'congo.blend','congo.glb','republic-of-the-congo-v1.html','poster.png','README.md','design-brief.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','contract-check.json'}
assert required <= {p.name for p in files}
h=lambda b:hashlib.sha256(b).hexdigest()
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':h(p.read_bytes())} for p in files}
assert inv['republic-of-the-congo-v1.html']['bytes']<5000000
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
with zipfile.ZipFile(R/'source.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(R/'source.zip') as z:
 assert set(z.namelist())==set(inv)|{'inventory.json'}
 for name,v in inv.items():
  b=z.read(name);assert len(b)==v['bytes'] and h(b)==v['sha256'],name
result={'status':'PASS','html_bytes':inv['republic-of-the-congo-v1.html']['bytes'],'glb_bytes':inv['congo.glb']['bytes'],'payload_count':len(inv),'archive_readback':True,'required_files_present':True,'zip_bytes':(R/'source.zip').stat().st_size,'zip_sha256':h((R/'source.zip').read_bytes())}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
