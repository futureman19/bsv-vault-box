from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
required={'el-salvador.blend','el-salvador.glb','el-salvador-v1.html','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-source-check.json','extended-check.json','acceptance-check.json','.gitattributes'}
assert json.loads((R/'acceptance-check.json').read_text())['status']=='PASS'
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert (R/'el-salvador-v1.html').stat().st_size<5_000_000
allowed={'.py','.js','.mjs','.json','.md','.txt','.html','.png','.jpg','.blend','.glb'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(s in p.relative_to(R).parts for s in ['node_modules','__pycache__']) and (p.suffix in allowed or p.name=='.gitattributes') and p.name not in ['inventory.json','delivery-check.json','packaging-output.txt','git-verification.txt'])
names={p.relative_to(R).as_posix() for p in files};assert required<=names,required-names
sha=lambda b:hashlib.sha256(b).hexdigest()
inventory={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
(R/'inventory.json').write_text(json.dumps(inventory,indent=2));files.append(R/'inventory.json')
z=R/'el-salvador-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
 for p in files:archive.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as archive:
 assert archive.testzip() is None and len(archive.namelist())==len(files)
 assert required<=set(archive.namelist())
 for p in files:assert archive.read(p.relative_to(R).as_posix())==p.read_bytes()
out={'status':'PASS','HTML_BYTES':(R/'el-salvador-v1.html').stat().st_size,'GLB_BYTES':(R/'el-salvador.glb').stat().st_size,'ZIP_BYTES':z.stat().st_size,'ZIP_ENTRIES':len(files),'zip_sha256':sha(z.read_bytes()),'required_artifacts_verified':sorted(required),'archive_readback_verified':True,'inventory_sha256':sha((R/'inventory.json').read_bytes()),'excluded_self_references':['inventory.json','delivery-check.json','el-salvador-v1-source.zip','packaging-output.txt','git-verification.txt'],'notes':'Source zip and file:// viewer remain in this folder; no external delivery copy or hosting.'}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
