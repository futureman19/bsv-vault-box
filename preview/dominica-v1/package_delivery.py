from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
def digest(b):return hashlib.sha256(b).hexdigest()
exclude={'inventory.json','delivery-check.json','dominica-source.zip'}
files=sorted(p for p in R.rglob('*') if p.is_file() and 'node_modules' not in p.parts and '__pycache__' not in p.parts and p.name not in exclude and p.suffix not in ['.blend1','.pyc'] and p.name not in ['lane-prompt.txt','setup.py'])
required={'dominica-v1.html','dominica.glb','dominica.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-source-check.json','extended-check.json','acceptance-check.json','.gitattributes'}
assert required <= {p.relative_to(R).as_posix() for p in files}
assert json.loads((R/'acceptance-check.json').read_text())['status']=='PASS'
html=(R/'dominica-v1.html').stat().st_size;glb=(R/'dominica.glb').stat().st_size;assert html<5000000
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for p in files}
(R/'inventory.json').write_text(json.dumps(inv,indent=2),encoding='utf8')
zpath=R/'dominica-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(inv)|{'inventory.json'}
 for n,v in inv.items():assert len(z.read(n))==v['bytes'] and digest(z.read(n))==v['sha256'],n
 assert z.read('inventory.json')==(R/'inventory.json').read_bytes()
out={'status':'PASS','HTML_BYTES':html,'GLB_BYTES':glb,'ZIP_BYTES':zpath.stat().st_size,'zip_sha256':digest(zpath.read_bytes()),'inventory_sha256':digest((R/'inventory.json').read_bytes()),'inventory_entries':len(inv),'archive_readback_verified':True,'required_artifacts_verified':sorted(required),'note':'Inventory excludes itself and packaging envelopes to avoid circular hashes; no external delivery copy.'}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print('DELIVERY PASS',json.dumps(out))
