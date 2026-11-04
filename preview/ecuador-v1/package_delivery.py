from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
excluded={'inventory.json','delivery-check.json','ecuador-v1-source.zip','lane-log.txt','lane-prompt.txt','lane-summary.txt','setup.py','verification-output.txt'}
files=[p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.name not in excluded and p.suffix not in ['.blend1','.pyc']]
files.sort();required={'ecuador-v1.html','ecuador.glb','ecuador.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json','verification-check.json','.gitattributes'}
assert required<=set(p.relative_to(R).as_posix() for p in files)
def sha(b):return hashlib.sha256(b).hexdigest()
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
(R/'inventory.json').write_text(json.dumps(inv,indent=2),encoding='utf8')
z=R/'ecuador-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as out:
 for p in files+[R/'inventory.json']:out.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as inp:
 assert set(inp.namelist())==set(inv)|{'inventory.json'}
 for n,entry in inv.items():
  b=inp.read(n);assert len(b)==entry['bytes'] and sha(b)==entry['sha256']
 assert inp.read('inventory.json')==(R/'inventory.json').read_bytes()
h=(R/'ecuador-v1.html').stat().st_size;g=(R/'ecuador.glb').stat().st_size;assert h<5000000
r={'status':'PASS','html_bytes':h,'glb_bytes':g,'inventory_entries':len(inv),'zip_bytes':z.stat().st_size,'zip_sha256':sha(z.read_bytes()),'inventory_sha256':sha((R/'inventory.json').read_bytes()),'exact_archive_inventory_and_readback':True,'required_artifacts_present':True}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
