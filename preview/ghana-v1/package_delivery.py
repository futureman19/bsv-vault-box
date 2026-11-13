from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
required={'ghana-v1.html','ghana.glb','ghana.blend','mechanism.blend','author.py','maps.py','build.py','viewer.js','motion.mjs','template.html','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','motion-check.json','maps/kente-color.png','maps/kente-roughness.png','maps/wood-color.png'}
exclude={'inventory.json','delivery-check.json','ghana-v1-source.zip'}
files={p.relative_to(R).as_posix():p for p in R.rglob('*') if p.is_file() and p.name not in exclude and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.blend1','.pyc']}
assert required<=files.keys(),required-files.keys()
assert files['ghana-v1.html'].stat().st_size<5000000
for name in ['source-check.json','parity-check.json','browser-check.json','theme-check.json','motion-check.json']:json.loads(files[name].read_text())
assert not json.loads(files['source-check.json'].read_text())['collisions']
assert json.loads(files['parity-check.json'].read_text())['source_and_export_geometry_match']
assert all(v.get('offline_file') and not v['external_requests'] and not v['errors'] for v in json.loads(files['browser-check.json'].read_text())[:2])
assert all(json.loads(files[n].read_text())['status']=='PASS' for n in ['theme-check.json','motion-check.json'])
inv={n:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for n,p in sorted(files.items())}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
zpath=R/'ghana-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n,p in files.items():z.write(p,n)
 z.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(files)|{'inventory.json'}
 for n,r in inv.items():
  b=z.read(n);assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],n
out={'status':'PASS','html_bytes':inv['ghana-v1.html']['bytes'],'glb_bytes':inv['ghana.glb']['bytes'],'payload_files':len(inv),'zip_entries':len(inv)+1,'required_artifacts_present':True,'archive_readback_all_hashes_match':True,'zip_bytes':zpath.stat().st_size,'zip_sha256':hashlib.sha256(zpath.read_bytes()).hexdigest(),'inventory_sha256':hashlib.sha256((R/'inventory.json').read_bytes()).hexdigest(),'inventory_exclusions':sorted(exclude),'delivery':'HTML is the exact tested in-folder file; no separate copied delivery'}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print('DELIVERY PASS',json.dumps(out))
