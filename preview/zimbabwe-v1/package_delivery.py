from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
checks=['source','parity','theme','browser','extended']
for n in checks:assert (R/(n+'-check.json')).is_file()
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
assert '# fail 0' in (R/'motion-output.txt').read_text()
assert (R/'zimbabwe-v1.html').stat().st_size<5_000_000
allowed={'.py','.js','.mjs','.json','.md','.txt','.html','.png','.jpg','.blend','.glb'}
files=sorted(p for p in R.rglob('*') if p.is_file() and (p.parent==R or p.parent.name=='maps') and (p.suffix in allowed or p.name in ['.gitattributes','.gitignore']) and p.name not in ['inventory.json','delivery-check.json'])
required={'zimbabwe.blend','zimbabwe.glb','zimbabwe-v1.html','poster.png','design-brief.md','README.md'}
assert required <= {p.name for p in files}
def sha(data):return hashlib.sha256(data).hexdigest()
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'zimbabwe-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert len(a.namelist())==len(files) and a.testzip() is None
 assert required <= set(a.namelist())
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
out={'status':'PASS','HTML_BYTES':(R/'zimbabwe-v1.html').stat().st_size,'GLB_BYTES':(R/'zimbabwe.glb').stat().st_size,'ZIP_BYTES':z.stat().st_size,'ZIP_SHA256':sha(z.read_bytes()),'inventory_entries':len(manifest),'archive_readback_verified':True,'required_artifacts_present':True}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
