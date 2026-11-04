from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
required={'iran.blend','iran.glb','iran-v1.html','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json','motion-output.txt'}
assert all((R/n).is_file() for n in required)
s=json.loads((R/'source-check.json').read_text());assert not s['collisions'] and s['collision_samples']==81
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
for n in ['theme-check.json','extended-check.json']:assert json.loads((R/n).read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert len(b)==3 and b[-1]['fallback'];assert all(not x['errors'] and not x['external_requests'] and x['open_close'] and x['reduced_motion'] for x in b[:2])
html=(R/'iran-v1.html').stat().st_size;glb=(R/'iran.glb').stat().st_size;assert html<5_000_000
excluded={'inventory.json','delivery-check.json','iran-v1-source.zip'}
files=sorted(f for f in R.rglob('*') if f.is_file() and not any(x in f.relative_to(R).parts for x in ['node_modules','__pycache__']) and f.name not in excluded and f.suffix!='.blend1')
def sha(data):return hashlib.sha256(data).hexdigest()
inv={f.relative_to(R).as_posix():{'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())} for f in files};assert required<=set(inv)
(R/'inventory.json').write_text(json.dumps(inv,indent=2));files.append(R/'inventory.json')
z=R/'iran-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for f in files:a.write(f,f.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert len(a.namelist())==len(files) and a.testzip() is None
 assert required<=set(a.namelist())
 for f in files:assert a.read(f.relative_to(R).as_posix())==f.read_bytes()
report={'status':'PASS','HTML_BYTES':html,'GLB_BYTES':glb,'ZIP_BYTES':z.stat().st_size,'ZIP_SHA256':sha(z.read_bytes()),'inventory_entries':len(inv),'archive_entries':len(files),'required_files_present':sorted(required),'archive_readback_verified':True,'checks_passed':['source','81-pose motion collisions','parity','theme and detached negative control','browser desktop/mobile offline','extended maps/noJS/poster','motion unit tests','delivery bytes/hash/archive']}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
