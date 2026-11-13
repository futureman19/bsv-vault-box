from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
files=[p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.zip','.blend1'] and p.name not in ['inventory.json','delivery-check.json']]
required={'nicaragua-v1.html','nicaragua.glb','nicaragua.blend','poster.jpg','poster.png','design-brief.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json'}
assert required<={p.name for p in files}
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
zpath=R/'nicaragua-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(inv)|{'inventory.json'}
 for n,v in inv.items():assert sha(z.read(n))==v['sha256']
a=inv['nicaragua-v1.html']['bytes'];g=inv['nicaragua.glb']['bytes'];assert a<5000000
r={'status':'PASS','html_bytes':a,'glb_bytes':g,'inventory_files':len(inv),'required_artifacts_present':True,'archive_readback':True,'archive_bytes':zpath.stat().st_size,'archive_sha256':sha(zpath.read_bytes()),'inventory_sha256':sha((R/'inventory.json').read_bytes())}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print('DELIVERY PASS',json.dumps(r))
