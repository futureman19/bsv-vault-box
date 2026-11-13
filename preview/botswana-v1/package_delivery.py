from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
excluded={'inventory.json','delivery-check.json','botswana-v1-source.zip','codex-lane.log','lane-prompt.md'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.name not in excluded and p.suffix!='.blend1')
required={'botswana.blend','botswana.glb','botswana-v1.html','poster.png','design-brief.md','README.md','source-check.json','parity-check.json','contract-check.json','browser-check.json','theme-check.json'}
assert required <= {p.name for p in files}
assert (R/'botswana-v1.html').stat().st_size<5000000
s=json.loads((R/'source-check.json').read_text());assert not s['collisions'] and s['collision_samples']==81
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
for n in ['contract','theme']:assert json.loads((R/f'{n}-check.json').read_text())['status']=='PASS'
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'botswana-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for p in files+[R/'inventory.json']:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())==set(inv)|{'inventory.json'}
 for n,v in inv.items():assert len(a.read(n))==v['bytes'] and sha(a.read(n))==v['sha256']
r={'status':'PASS','html_bytes':(R/'botswana-v1.html').stat().st_size,'glb_bytes':(R/'botswana.glb').stat().st_size,'inventory_files':len(inv),'zip_bytes':z.stat().st_size,'zip_sha256':sha(z.read_bytes()),'archive_readback':'all entries exact','required_artifacts_present':True}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
