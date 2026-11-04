from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
excluded={'inventory.json','delivery-check.json','saint-lucia-source.zip'}
files=[p for p in R.rglob('*') if p.is_file() and p.name not in excluded and 'node_modules' not in p.parts and '__pycache__' not in p.parts and not p.name.endswith('.blend1')]
required={'saint-lucia-v1.html','saint-lucia.glb','saint-lucia.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','extended-check.json','theme-check.json','motion-output.txt','.gitattributes'}
assert required<={p.relative_to(R).as_posix() for p in files}
assert (R/'saint-lucia-v1.html').stat().st_size<5000000
source=json.loads((R/'source-check.json').read_text());assert source['collision_samples']==81 and not source['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
checks=json.loads((R/'browser-check.json').read_text());assert len(checks)==3 and all(x['open_close'] and x['reduced_motion'] and not x['errors'] and not x['external_requests'] for x in checks[:2])
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(files)}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'saint-lucia-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,6) as out:
 for p in files+[R/'inventory.json']:out.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as archive:
 assert set(archive.namelist())==set(inv)|{'inventory.json'}
 for n,d in inv.items():assert len(archive.read(n))==d['bytes'] and sha(archive.read(n))==d['sha256']
result={'status':'PASS','html_bytes':(R/'saint-lucia-v1.html').stat().st_size,'glb_bytes':(R/'saint-lucia.glb').stat().st_size,'inventory_files':len(inv),'zip_bytes':z.stat().st_size,'zip_sha256':sha(z.read_bytes()),'archive_readback':'all inventory bytes and hashes match','exclusions':['node_modules','__pycache__','*.blend1','inventory and delivery manifest self-references']}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
