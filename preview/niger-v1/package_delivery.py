from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
excluded={'node_modules','__pycache__','.git'}
files=[p for p in R.rglob('*') if p.is_file() and not excluded.intersection(p.relative_to(R).parts) and p.name not in {'inventory.json','delivery-check.json','niger-v1-source.zip','codex-lane.log'} and p.suffix not in {'.blend1','.zip'}]
required={'niger-v1.html','niger.glb','niger.blend','poster.png','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json'}
assert required <= {p.name for p in files}
assert (R/'niger-v1.html').stat().st_size<5_000_000
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
zp=R/'niger-v1-source.zip'
with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zp) as z:
 assert set(z.namelist())==set(inv)|{'inventory.json'}
 for n,v in inv.items():
  data=z.read(n);assert len(data)==v['bytes'] and hashlib.sha256(data).hexdigest()==v['sha256']
r={'status':'PASS','html_bytes':(R/'niger-v1.html').stat().st_size,'glb_bytes':(R/'niger.glb').stat().st_size,'inventory_entries':len(inv),'archive_bytes':zp.stat().st_size,'archive_sha256':hashlib.sha256(zp.read_bytes()).hexdigest(),'archive_exact_readback':True,'required_artifacts_present':True}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
