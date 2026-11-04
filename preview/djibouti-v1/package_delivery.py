from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
excluded={'inventory.json','delivery-check.json','djibouti-v1-source.zip','package-output.txt','codex-lane.log','lane-prompt.txt','prepare_author.py'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.name not in excluded and p.suffix!='.blend1')
required={'djibouti-v1.html','djibouti.glb','djibouti.blend','mechanism.blend','poster.png','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json'}
assert required <= {p.name for p in files}
assert (R/'djibouti-v1.html').stat().st_size<5_000_000
sha=lambda b:hashlib.sha256(b).hexdigest()
inventory={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
(R/'inventory.json').write_text(json.dumps(inventory,indent=2))
zpath=R/'djibouti-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(inventory)|{'inventory.json'}
 for n,v in inventory.items():assert sha(z.read(n))==v['sha256'] and len(z.read(n))==v['bytes']
r={'status':'PASS','html_bytes':(R/'djibouti-v1.html').stat().st_size,'glb_bytes':(R/'djibouti.glb').stat().st_size,'payload_files':len(inventory),'zip_bytes':zpath.stat().st_size,'zip_sha256':sha(zpath.read_bytes()),'zip_readback_verified':True,'required_artifacts_present':True}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
