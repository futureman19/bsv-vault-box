from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
H=lambda b:hashlib.sha256(b).hexdigest()
excluded={'node_modules','__pycache__','inventory.json','delivery-check.json','trinidad-and-tobago-v1-source.zip'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(a in excluded for a in p.relative_to(R).parts) and not p.name.endswith(('.blend1','.pyc')))
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':H(p.read_bytes())} for p in files}
required={'trinidad-and-tobago-v1.html','trinidad-and-tobago.glb','trinidad-and-tobago.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','motion-check.json'}
assert required<=inv.keys()
assert inv['trinidad-and-tobago-v1.html']['bytes']<5_000_000
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'trinidad-and-tobago-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as archive:
 for p in files+[R/'inventory.json']:archive.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as archive:
 assert set(archive.namelist())==set(inv)|{'inventory.json'}
 for n,e in inv.items():
  b=archive.read(n);assert len(b)==e['bytes'] and H(b)==e['sha256']
r={'status':'PASS','html_bytes':inv['trinidad-and-tobago-v1.html']['bytes'],'glb_bytes':inv['trinidad-and-tobago.glb']['bytes'],'inventoried_files':len(inv),'required_artifacts_present':True,'archive_readback_all_hashes_match':True,'zip_bytes':z.stat().st_size,'zip_sha256':H(z.read_bytes()),'inventory_sha256':H((R/'inventory.json').read_bytes()),'excluded':'node_modules, .blend1, pycache; inventory and delivery envelopes avoid circular hashes'}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print('DELIVERY PASS',json.dumps(r))
