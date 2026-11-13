from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
required={'georgia-v1.html','georgia.glb','georgia.blend','mechanism.blend','poster.png','poster.jpg','README.md','design-brief.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','author.py','maps.py','verify_source.py','verify_parity.py','verify_browser.py','verify_theme.py','tests.mjs'}
files=[p for p in R.rglob('*') if p.is_file() and p.suffix not in ['.zip','.pyc','.blend1'] and p.name not in ['inventory.json','delivery-check.json','package-output.txt'] and '__pycache__' not in p.parts]
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)}
assert required<=inv.keys();assert inv['georgia-v1.html']['bytes']<5000000
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'georgia-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for p in files+[R/'inventory.json']:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())==set(inv)|{'inventory.json'}
 for n,v in inv.items():assert hashlib.sha256(a.read(n)).hexdigest()==v['sha256']
r={'status':'PASS','HTML_BYTES':inv['georgia-v1.html']['bytes'],'GLB_BYTES':inv['georgia.glb']['bytes'],'ZIP_BYTES':z.stat().st_size,'ZIP_SHA256':hashlib.sha256(z.read_bytes()).hexdigest(),'archive_entries':len(inv)+1,'required_artifacts_present':True,'archive_readback_verified':True,'inventory_scope':'all payload except self and packaging envelopes; no recursive hashes'}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print('DELIVERY PASS',json.dumps(r))
