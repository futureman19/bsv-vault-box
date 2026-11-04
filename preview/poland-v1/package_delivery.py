from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
for n in ['source-check.json','parity-check.json','design-check.json','theme-check.json','browser-check.json']:
 assert (R/n).exists()
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
for n in ['design-check.json','theme-check.json']:assert json.loads((R/n).read_text())['status']=='PASS'
assert (R/'poland-v1.html').stat().st_size<5000000
allowed={'.py','.js','.mjs','.json','.md','.txt','.html','.png','.jpg','.blend','.glb'}
files=sorted(p for p in R.rglob('*') if p.is_file() and (p.parent==R or p.parent.name in ['maps','initial']) and (p.suffix in allowed or p.name=='.gitattributes') and p.name not in ['inventory.json','delivery-check.json','verification-output.txt'])
inventory={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
required={'poland-v1.html','poland.blend','poland.glb','poster.png','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','design-check.json','.gitattributes'};assert required<=inventory.keys()
(R/'inventory.json').write_text(json.dumps(inventory,indent=2));files.append(R/'inventory.json');z=R/'poland-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as f:
 for p in files:f.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as f:
 assert f.testzip() is None and len(f.namelist())==len(files)
 for p in files:assert f.read(p.relative_to(R).as_posix())==p.read_bytes()
out={'status':'PASS','HTML_BYTES':(R/'poland-v1.html').stat().st_size,'GLB_BYTES':(R/'poland.glb').stat().st_size,'ZIP_BYTES':z.stat().st_size,'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'archive_readback_verified':True,'inventory_entries':len(inventory),'required_artifacts_verified':sorted(required)}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
