from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
exclude={'inventory.json','delivery-check.json','delivery-output.txt','git-check.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not {'node_modules','__pycache__'}&set(p.relative_to(R).parts) and p.name not in exclude and p.suffix not in ['.zip','.blend1'])
required={'dominican-republic-v1.html','dominican-republic.glb','dominican-republic.blend','mechanism.blend','design-brief.md','README.md','poster.png','poster.jpg','source-check.json','parity-check.json','browser-check.json','extended-check.json','theme-source-check.json'}
assert required<={p.relative_to(R).as_posix() for p in files}
h=lambda b:hashlib.sha256(b).hexdigest()
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':h(p.read_bytes())} for p in files}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'dominican-republic-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as out:
 for p in files+[R/'inventory.json']:out.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as f:
 assert set(f.namelist())==set(inv)|{'inventory.json'}
 for name,m in inv.items():
  b=f.read(name);assert len(b)==m['bytes'] and h(b)==m['sha256']
html=inv['dominican-republic-v1.html']['bytes'];glb=inv['dominican-republic.glb']['bytes'];assert html<5000000
r={'status':'PASS','html_bytes':html,'glb_bytes':glb,'required_artifacts_verified':sorted(required),'inventory_count':len(inv),'zip_bytes':z.stat().st_size,'zip_sha256':h(z.read_bytes()),'archive_readback':True}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
