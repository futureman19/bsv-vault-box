from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
required={'venezuela-v1.html','venezuela.glb','venezuela.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json','THREE-LICENSE.txt','.gitattributes'}
assert all((R/f).is_file() for f in required)
source=json.loads((R/'source-check.json').read_text());assert source['collision_samples']==81 and not source['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
bs=json.loads((R/'browser-check.json').read_text())
for d in bs[:2]:assert d['asset']['bytes']==(R/'venezuela.glb').stat().st_size and not d['external_requests'] and not d['errors']
assert len(bs)==3 and bs[2]['fallback']
assert (R/'venezuela-v1.html').stat().st_size<5000000
allowed={'.py','.js','.mjs','.json','.md','.txt','.html','.png','.jpg','.blend','.glb'}
files=sorted(f for f in R.rglob('*') if f.is_file() and (f.suffix in allowed or f.name in {'.gitattributes','.gitignore'}) and f.name not in {'inventory.json','delivery-check.json'} and (f.parent==R or f.parent.name in {'maps','initial'}))
manifest={f.relative_to(R).as_posix():{'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())} for f in files}
assert required<=manifest.keys()
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'venezuela-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for f in files:a.write(f,f.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert a.testzip() is None and set(a.namelist())=={f.relative_to(R).as_posix() for f in files}
 for f in files:assert a.read(f.relative_to(R).as_posix())==f.read_bytes()
out={'status':'PASS','HTML_BYTES':(R/'venezuela-v1.html').stat().st_size,'GLB_BYTES':(R/'venezuela.glb').stat().st_size,'archive_bytes':z.stat().st_size,'archive_sha256':sha(z.read_bytes()),'inventory_entries':len(manifest),'archive_entries':len(files),'archive_readback_verified':True,'required_artifacts_verified':sorted(required),'delivery_location':'this folder; no separate copy or hosted URL'}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
