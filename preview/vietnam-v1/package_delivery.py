from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
s=json.loads((R/'source-check.json').read_text());assert s['collision_samples']==81 and not s['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
for n in ['theme','extended']:assert json.loads((R/f'{n}-check.json').read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert len(b)==3
for c in b[:2]:assert c['open_close'] and c['reset_mid_motion'] and c['reduced_motion'] and not c['errors'] and not c['external_requests'] and c['asset']['degenerate']==0
assert '# fail 0' in (R/'motion-output.txt').read_text()
html=R/'vietnam-v1.html';assert 0<html.stat().st_size<5000000
required={'vietnam-v1.html','vietnam.glb','vietnam.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(k in p.parts for k in ['node_modules','__pycache__']) and p.suffix not in ['.blend1','.zip'] and p.name not in ['inventory.json','delivery-check.json','package-output.txt'])
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files};assert required<=set(manifest)
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json');z=R/'vietnam-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())=={p.relative_to(R).as_posix() for p in files};assert a.testzip() is None
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
r={'status':'PASS','HTML_BYTES':html.stat().st_size,'GLB_BYTES':(R/'vietnam.glb').stat().st_size,'HTML_SHA256':sha(html.read_bytes()),'GLB_SHA256':sha((R/'vietnam.glb').read_bytes()),'ZIP_BYTES':z.stat().st_size,'ZIP_SHA256':sha(z.read_bytes()),'zip_entries':len(files),'archive_required_set_and_byte_readback':True,'inventory_entries':len(manifest),'checks_passed':['source','parity','theme','browser desktop/mobile','extended','motion','delivery']}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
