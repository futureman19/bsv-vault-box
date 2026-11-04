from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
skip={'inventory.json','delivery-check.json','solomon-islands-v1-source.zip','package-output.txt'}
files=[p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.name not in skip and not p.name.endswith('.blend1')]
required={'solomon-islands.blend','solomon-islands.glb','solomon-islands-v1.html','poster.png','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json'}
names={p.relative_to(R).as_posix() for p in files};assert required<=names
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
zpath=R/'solomon-islands-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(inv)|{'inventory.json'}
 for n,v in inv.items():assert hashlib.sha256(z.read(n)).hexdigest()==v['sha256'] and len(z.read(n))==v['bytes']
h=inv['solomon-islands-v1.html']['bytes'];g=inv['solomon-islands.glb']['bytes'];assert h<5000000
out={'status':'PASS','html_bytes':h,'glb_bytes':g,'inventory_entries':len(inv),'required_deliverables_present':True,'zip_readback_all_hashes_match':True,'zip_bytes':zpath.stat().st_size,'zip_sha256':hashlib.sha256(zpath.read_bytes()).hexdigest(),'excludes':['node_modules','__pycache__','.blend1','recursive inventory/delivery envelopes','actively written package-output.txt']}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
