from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
required={'new-zealand-v1.html','new-zealand.glb','new-zealand.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','pivot-check.json','theme-check.json','browser-check.json','extended-check.json','acceptance-check.json','desktop-closed.png','desktop-open.png','mobile-closed.png','mobile-open.png','author.py','maps.py','run_checks.py','package_delivery.py','.gitattributes'}
exclude={'inventory.json','delivery-check.json','new-zealand-v1-source.zip','prepare.py'}
paths=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.name not in exclude and not p.name.endswith(('.blend1','.pyc')))
files={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in paths}
assert required<=files.keys(),required-files.keys()
assert files['new-zealand-v1.html']['bytes']<5_000_000
checks=json.loads((R/'acceptance-check.json').read_text());assert checks['status']=='PASS' and all(x['status']=='PASS' for x in checks['checks'])
(R/'inventory.json').write_text(json.dumps({'files':files},indent=2))
zpath=R/'new-zealand-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in paths:z.write(p,p.relative_to(R).as_posix())
 z.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(files)|{'inventory.json'}
 for n,v in files.items():
  b=z.read(n);assert len(b)==v['bytes'] and sha(b)==v['sha256'],n
 assert z.read('inventory.json')==(R/'inventory.json').read_bytes()
report={'status':'PASS','html_bytes':files['new-zealand-v1.html']['bytes'],'glb_bytes':files['new-zealand.glb']['bytes'],'inventory_files':len(files),'required_files_present':True,'zip_readback_all_hashes_match':True,'zip_bytes':zpath.stat().st_size,'zip_sha256':sha(zpath.read_bytes()),'inventory_sha256':sha((R/'inventory.json').read_bytes()),'exclusions':'node_modules, caches, blend1, packaging envelopes; no self-referential hashes'}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));print('DELIVERY PASS',json.dumps(report))
