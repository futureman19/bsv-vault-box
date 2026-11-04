from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
required={'brazil.blend','brazil.glb','brazil-v1.html','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','extended-check.json','theme-check.json','motion-check.json','mechanism.blend','.gitattributes'}
assert all((R/n).is_file() for n in required)
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
assert (R/'brazil-v1.html').stat().st_size<5_000_000
allowed={'.py','.js','.mjs','.json','.md','.txt','.html','.png','.jpg','.blend','.glb'}
excluded={'inventory.json','delivery-check.json','verification-output.txt'}
files=sorted(f for f in R.rglob('*') if f.is_file() and (f.suffix in allowed or f.name=='.gitattributes') and f.name not in excluded and (f.parent==R or f.parent.name in {'maps','initial'}))
manifest={f.relative_to(R).as_posix():{'bytes':f.stat().st_size,'sha256':sha(f)} for f in files}
assert required.issubset(manifest)
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json');z=R/'brazil-v1-source.zip'
with zipfile.ZipFile(z,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for f in files:a.write(f,f.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert len(a.namelist())==len(files);assert a.testzip() is None;assert required.issubset(a.namelist())
 for f in files:assert a.read(f.relative_to(R).as_posix())==f.read_bytes()
r={'status':'PASS','HTML_bytes':(R/'brazil-v1.html').stat().st_size,'GLB_bytes':(R/'brazil.glb').stat().st_size,'ZIP_bytes':z.stat().st_size,'ZIP_entries':len(files),'zip_sha256':sha(z),'archive_readback_verified':True,'required_file_coverage':True,'inventory_entries':len(manifest)}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
