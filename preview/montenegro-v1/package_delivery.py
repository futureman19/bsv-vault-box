from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
required={'montenegro-v1.html','montenegro.glb','montenegro.blend','mechanism.blend','poster.png','poster.jpg','README.md','design-brief.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json','THREE-LICENSE.txt'}
files={p.relative_to(R).as_posix():p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.zip','.blend1','.pyc'] and p.name not in ['inventory.json','delivery-check.json','package-output.txt','git-check.json']}
assert required<=files.keys(),required-files.keys()
assert files['montenegro-v1.html'].stat().st_size<5_000_000
source=json.loads((R/'source-check.json').read_text());assert source['collision_samples']==81 and not source['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
checks=json.loads((R/'browser-check.json').read_text());assert len(checks)==3
for c in checks[:2]:assert c['open_close'] and c['reset_mid_motion'] and c['reduced_motion'] and not c['errors'] and not c['external_requests']
assert checks[2]['fallback']
inventory={n:{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for n,p in sorted(files.items())}
(R/'inventory.json').write_text(json.dumps(inventory,indent=2))
zpath=R/'montenegro-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n,p in sorted(files.items()):z.write(p,n)
 z.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(files)|{'inventory.json'}
 for n,v in inventory.items():
  b=z.read(n);assert len(b)==v['bytes'] and sha(b)==v['sha256']
report={'status':'PASS','html_bytes':inventory['montenegro-v1.html']['bytes'],'glb_bytes':inventory['montenegro.glb']['bytes'],'payload_files':len(files),'required_artifacts_present':True,'zip_readback_verified':True,'zip_bytes':zpath.stat().st_size,'zip_sha256':sha(zpath.read_bytes()),'inventory_sha256':sha((R/'inventory.json').read_bytes()),'checks_passed':['source','parity','theme','browser desktop','browser mobile','fallback','no-JS','runtime maps and palette','motion tests','delivery']}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
