from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
required={'costa-rica-v1.html','costa-rica.glb','costa-rica.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','extended-check.json','theme-source-check.json'}
files=[p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.zip','.blend1'] and p.name not in ['inventory.json','delivery-check.json','package-output.txt']]
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
assert required<=inv.keys();assert inv['costa-rica-v1.html']['bytes']<5000000
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
zpath=R/'costa-rica-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(inv)|{'inventory.json'}
 for n,v in inv.items():assert len(z.read(n))==v['bytes'] and sha(z.read(n))==v['sha256']
r={'status':'PASS','html_bytes':inv['costa-rica-v1.html']['bytes'],'glb_bytes':inv['costa-rica.glb']['bytes'],'inventory_entries':len(inv),'zip_bytes':zpath.stat().st_size,'zip_sha256':sha(zpath.read_bytes()),'archive_readback_all_hashes':True,'required_artifacts_present':True,'inventory_sha256':sha((R/'inventory.json').read_bytes()),'excluded':'node_modules, caches, blend1, ZIP/envelope/self-referential packaging logs'}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
