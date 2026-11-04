from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
excluded={'inventory.json','delivery-check.json','git-byte-check.json'}
files={p.relative_to(R).as_posix():p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.name not in excluded and p.suffix not in ['.zip','.blend1']}
required={'united-states-v1.html','united-states.glb','united-states.blend','mechanism.blend','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','poster.png'}
assert required<=files.keys();h=files['united-states-v1.html'].stat().st_size;g=files['united-states.glb'].stat().st_size;assert h<5000000
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert json.loads((R/'theme-check.json').read_text())['PASS'] and json.loads((R/'extended-check.json').read_text())['PASS']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
inv={n:{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for n,p in sorted(files.items())}
(R/'inventory.json').write_text(json.dumps(inv,indent=2));files['inventory.json']=R/'inventory.json'
zpath=R/'united-states-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for n,p in files.items():z.write(p,n)
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(files)
 for n,p in files.items():assert z.read(n)==p.read_bytes(),n
out={'PASS':True,'HTML_BYTES':h,'GLB_BYTES':g,'HTML_SHA256':sha((R/'united-states-v1.html').read_bytes()),'GLB_SHA256':sha((R/'united-states.glb').read_bytes()),'ZIP_BYTES':zpath.stat().st_size,'ZIP_SHA256':sha(zpath.read_bytes()),'inventory_entries':len(inv),'zip_entries':len(files),'required_artifacts_present':True,'archive_readback_verified':True}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print('DELIVERY PASS',json.dumps(out))
