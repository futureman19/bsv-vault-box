from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
excluded={'inventory.json','delivery-check.json','sri-lanka-v1-source.zip','verification-output.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name not in excluded and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.suffix!='.blend1')
required={'design-brief.md','README.md','sri-lanka.blend','sri-lanka.glb','sri-lanka-v1.html','poster.png','poster.jpg','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','motion-output.txt','verify_all.py'}
assert required.issubset({p.relative_to(R).as_posix() for p in files})
sha=lambda b:hashlib.sha256(b).hexdigest()
inventory={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
(R/'inventory.json').write_text(json.dumps(inventory,indent=2))
zp=R/'sri-lanka-v1-source.zip'
with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zp) as z:
 assert set(z.namelist())==set(inventory)|{'inventory.json'}
 for n,v in inventory.items():
  b=z.read(n);assert len(b)==v['bytes'] and sha(b)==v['sha256']
 assert z.read('inventory.json')==(R/'inventory.json').read_bytes()
html=(R/'sri-lanka-v1.html').stat().st_size;glb=(R/'sri-lanka.glb').stat().st_size;assert html<5_000_000
result={'status':'PASS','html_bytes':html,'glb_bytes':glb,'payload_count':len(inventory),'required_artifacts_present':True,'zip_readback_all_hashes':True,'zip_bytes':zp.stat().st_size,'zip_sha256':sha(zp.read_bytes()),'inventory_sha256':sha((R/'inventory.json').read_bytes()),'excluded_envelopes':sorted(excluded),'note':'inventory excludes itself, ZIP, delivery-check and active wrapper output to avoid circular identities'}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print('DELIVERY PASS',json.dumps(result))
