from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
excluded={'inventory.json','delivery-check.json','source.zip','codex-lane.log','lane-prompt.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.name not in excluded and p.suffix!='.blend1')
required={'russia-v1.html','russia.glb','russia.blend','poster.png','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json'}
assert required <= {p.name for p in files}
def sha(b):return hashlib.sha256(b).hexdigest()
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
with zipfile.ZipFile(R/'source.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(R/'source.zip') as z:
 assert set(z.namelist())==set(inv)|{'inventory.json'}
 for n,v in inv.items():assert len(z.read(n))==v['bytes'] and sha(z.read(n))==v['sha256']
h=inv['russia-v1.html']['bytes'];g=inv['russia.glb']['bytes'];assert h<5000000
out={'status':'PASS','html_bytes':h,'glb_bytes':g,'inventory_entries':len(inv),'zip_readback':True,'zip_bytes':(R/'source.zip').stat().st_size,'zip_sha256':sha((R/'source.zip').read_bytes())}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
