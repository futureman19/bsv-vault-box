from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
s=json.loads((R/'source-check.json').read_text());assert s['collision_samples']==81 and not s['collisions']
p=json.loads((R/'parity-check.json').read_text());assert max(p['source_to_glb_max'],p['glb_to_source_max'])<1e-5
for n in ['theme-check.json','material-check.json']:assert json.loads((R/n).read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert len(b)==4
for c in b[:2]:assert c['offline_file'] and not c['external_requests'] and not c['errors'] and c['open_close'] and c['reduced_motion'] and c['asset']['open_projection_max_abs_ndc']<1
assert b[2]['fallback'] and b[3]['poster']
assert '# fail 0' in (R/'motion-output.txt').read_text()
h=R/'tunisia-v1.html';g=R/'tunisia.glb';assert h.stat().st_size<5_000_000
files=sorted(f for f in R.rglob('*') if f.is_file() and f.name not in ['inventory.json','delivery-check.json'] and f.suffix not in ['.zip','.blend1'] and not any(x in f.parts for x in ['node_modules','__pycache__']) and (f.parent==R or f.parent.name=='maps'))
required={'tunisia-v1.html','tunisia.blend','tunisia.glb','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','browser-check.json','parity-check.json','theme-check.json','material-check.json','motion-output.txt'}
assert required<={f.name for f in files}
def sha(b):return hashlib.sha256(b).hexdigest()
inventory={f.relative_to(R).as_posix():{'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())} for f in files}
(R/'inventory.json').write_text(json.dumps(inventory,indent=2));files.append(R/'inventory.json')
z=R/'tunisia-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for f in files:a.write(f,f.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert a.testzip() is None;assert set(a.namelist())==set(inventory)|{'inventory.json'}
 for n,v in inventory.items():assert sha(a.read(n))==v['sha256'] and len(a.read(n))==v['bytes']
r={'status':'PASS','HTML_BYTES':h.stat().st_size,'GLB_BYTES':g.stat().st_size,'ZIP_BYTES':z.stat().st_size,'ZIP_SHA256':sha(z.read_bytes()),'archive_entries':len(files),'exact_archive_readback':True,'required_artifacts_present':True,'checks_passed':['source','hinge-attachment','parity','theme-and-negative-control','material-and-runtime-ancestry','motion','browser-desktop-mobile','fallbacks','delivery']}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
