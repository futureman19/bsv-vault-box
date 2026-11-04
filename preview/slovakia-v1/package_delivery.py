from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
required={'slovakia-v1.html','slovakia.glb','slovakia.blend','mechanism.blend','poster.png','poster.jpg','README.md','design-brief.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json'}
def digest(b):return hashlib.sha256(b).hexdigest()
files=[p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__','.git']) and p.suffix not in ['.zip','.blend1','.log'] and p.name not in ['inventory.json','delivery-check.json','delivery-output.txt','git-proof.txt','lane-prompt.txt']]
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for p in files}
assert required<=inv.keys();assert inv['slovakia-v1.html']['bytes']<5000000
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'slovakia-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for n in sorted(inv):a.write(R/n,n)
 a.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())==set(inv)|{'inventory.json'}
 for n,v in inv.items():assert digest(a.read(n))==v['sha256'] and len(a.read(n))==v['bytes']
r={'status':'PASS','html_bytes':inv['slovakia-v1.html']['bytes'],'glb_bytes':inv['slovakia.glb']['bytes'],'zip_bytes':z.stat().st_size,'zip_sha256':digest(z.read_bytes()),'files':len(inv),'required_artifacts':True,'zip_readback':True}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
