from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
for n in ['source','parity','theme','browser','extended']:assert (R/(n+'-check.json')).is_file()
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
for n in ['theme','extended']:assert json.loads((R/(n+'-check.json')).read_text())['status']=='PASS'
for v in json.loads((R/'browser-check.json').read_text())[:2]:assert not v['errors'] and not v['external_requests'] and v['open_close'] and v['reduced_motion']
assert (R/'united-kingdom-v1.html').stat().st_size<5000000
allowed={'.py','.js','.mjs','.json','.md','.txt','.html','.png','.jpg','.blend','.glb'}
files=sorted(p for p in R.rglob('*') if p.is_file() and (p.suffix in allowed or p.name=='.gitattributes') and p.name not in {'inventory.json','delivery-check.json'} and (p.parent==R or p.parent.name in {'maps','initial'}))
required={'united-kingdom-v1.html','united-kingdom.glb','united-kingdom.blend','poster.png','design-brief.md','README.md','mechanism.blend','.gitattributes'}
assert required<={p.name for p in files}
def digest(b):return hashlib.sha256(b).hexdigest()
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for p in files}
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'united-kingdom-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert len(a.namelist())==len(files) and a.testzip() is None
 assert required<=set(a.namelist())
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
out={'status':'PASS','HTML_BYTES':(R/'united-kingdom-v1.html').stat().st_size,'GLB_BYTES':(R/'united-kingdom.glb').stat().st_size,'zip_bytes':z.stat().st_size,'zip_sha256':digest(z.read_bytes()),'inventory_entries':len(manifest),'required_artifacts_present':True,'zip_readback_all_entries':True}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
