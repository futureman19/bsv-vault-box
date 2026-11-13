from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
required={'colombia-v1.html','colombia.glb','colombia.blend','mechanism.blend','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','motion-output.txt','poster.png','poster.jpg','.gitattributes'}
assert all((R/n).is_file() for n in required)
s=json.loads((R/'source-check.json').read_text());assert s['collision_samples']==81 and not s['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
for n in ['theme','extended']:assert json.loads((R/(n+'-check.json')).read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert len(b)==3 and all(not c.get('errors',[]) for c in b)
assert (R/'colombia-v1.html').stat().st_size<5000000
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.zip','.blend1'] and p.name not in ['inventory.json','delivery-check.json','package-output.txt'])
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files};assert required<=inv.keys()
(R/'inventory.json').write_text(json.dumps(inv,indent=2));files.append(R/'inventory.json')
z=R/'colombia-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())==set(inv)|{'inventory.json'} and a.testzip() is None
 for n,v in inv.items():assert sha(a.read(n))==v['sha256']
r={'status':'PASS','HTML_BYTES':(R/'colombia-v1.html').stat().st_size,'GLB_BYTES':(R/'colombia.glb').stat().st_size,'ZIP_BYTES':z.stat().st_size,'ZIP_SHA256':sha(z.read_bytes()),'inventory_entries':len(inv),'archive_readback_verified':True,'required_artifacts_present':True,'checks_passed':['source','parity','theme','browser-desktop','browser-mobile','corrupt-GLB-fallback','no-JS-fallback','portable-maps','motion','delivery'],'limits':'mobile emulation; sampled surface collision, not continuous proof'}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
