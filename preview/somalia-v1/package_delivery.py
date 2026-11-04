from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
h=lambda b:hashlib.sha256(b).hexdigest()
exclude={'inventory.json','delivery-check.json','somalia-v1-source.zip','package-output.txt','git-verification.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and 'node_modules' not in p.parts and '__pycache__' not in p.parts and p.name not in exclude and not p.name.endswith('.blend1'))
required={'somalia-v1.html','somalia.glb','somalia.blend','mechanism.blend','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','poster.png'}
assert required<=set(p.relative_to(R).as_posix() for p in files)
assert (R/'somalia-v1.html').stat().st_size<5000000
inventory={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':h(p.read_bytes())} for p in files}
(R/'inventory.json').write_text(json.dumps(inventory,indent=2))
zpath=R/'somalia-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(inventory)|{'inventory.json'}
 for n,v in inventory.items():
  b=z.read(n);assert len(b)==v['bytes'] and h(b)==v['sha256'],n
out={'status':'PASS','html_bytes':(R/'somalia-v1.html').stat().st_size,'glb_bytes':(R/'somalia.glb').stat().st_size,'payload_count':len(inventory),'required_artifacts_present':True,'all_archive_entries_readback_verified':True,'zip_bytes':zpath.stat().st_size,'zip_sha256':h(zpath.read_bytes()),'inventory_sha256':h((R/'inventory.json').read_bytes())}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print('DELIVERY PASS',json.dumps(out))
