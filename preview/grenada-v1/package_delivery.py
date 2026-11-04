from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
def sha(data):return hashlib.sha256(data).hexdigest()
required={'grenada-v1.html','grenada.glb','grenada.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','motion-output.txt'}
assert all((R/n).is_file() for n in required)
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
assert (R/'grenada-v1.html').stat().st_size<5000000
allowed={'.py','.js','.mjs','.json','.md','.txt','.html','.png','.jpg','.blend','.glb'}
files=sorted(p for p in R.rglob('*') if p.is_file() and (p.suffix in allowed or p.name in {'.gitattributes','.gitignore'}) and p.name not in {'inventory.json','delivery-check.json','verification-output.txt'} and (p.parent==R or p.parent.name in {'maps','initial'}))
inventory={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
assert required<=set(inventory)
(R/'inventory.json').write_text(json.dumps(inventory,indent=2));files.append(R/'inventory.json')
z=R/'grenada-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
 for p in files:archive.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as archive:
 assert archive.testzip() is None
 assert set(archive.namelist())=={p.relative_to(R).as_posix() for p in files}
 for p in files:assert archive.read(p.relative_to(R).as_posix())==p.read_bytes()
report={'status':'PASS','HTML_BYTES':(R/'grenada-v1.html').stat().st_size,'GLB_BYTES':(R/'grenada.glb').stat().st_size,'ZIP_BYTES':z.stat().st_size,'zip_sha256':sha(z.read_bytes()),'inventory_entries':len(inventory),'zip_entries':len(files),'required_artifacts_present':sorted(required),'archive_readback_verified':True,'inventory_exclusions':['inventory.json (self hash)','delivery-check.json (envelope)','source ZIP (envelope)','verification-output.txt (actively written log)','node_modules','__pycache__','blend1']}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));print('DELIVERY PASS');print('HTML_BYTES='+str(report['HTML_BYTES']));print('GLB_BYTES='+str(report['GLB_BYTES']))
