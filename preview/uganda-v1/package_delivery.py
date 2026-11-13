from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
read=lambda n:json.loads((R/n).read_text())
s=read('source-check.json');assert s['collision_samples']==81 and not s['collisions']
assert read('parity-check.json')['source_and_export_geometry_match']
assert read('theme-check.json')['status']=='PASS' and read('negative-control.json')['status']=='FAIL'
assert read('pivot-check.json')['status']=='PASS' and read('extended-check.json')['status']=='PASS'
b=read('browser-check.json');assert len(b)==3 and all(not x.get('errors',[]) and not x.get('external_requests',[]) for x in b)
assert '# fail 0' in (R/'motion-output.txt').read_text()
html=(R/'uganda-v1.html').stat().st_size;glb=(R/'uganda.glb').stat().st_size;assert html<5000000
skip={'inventory.json','delivery-check.json','uganda-v1-source.zip','git-byte-check.json'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.name not in skip and not p.name.endswith('.blend1'))
required={'uganda-v1.html','uganda.glb','uganda.blend','mechanism.blend','design-brief.md','README.md','poster.png','poster.jpg','source-check.json','parity-check.json','browser-check.json','theme-check.json','pivot-check.json','extended-check.json','mobile-closed.png','mobile-open.png','author.py','maps.py'}
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files};assert required<=set(inv)
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'uganda-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as f:
 for p in files+[R/'inventory.json']:f.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as f:
 assert set(f.namelist())==set(inv)|{'inventory.json'}
 for name,v in inv.items():
  data=f.read(name);assert len(data)==v['bytes'] and sha(data)==v['sha256']
r={'status':'PASS','HTML_BYTES':html,'GLB_BYTES':glb,'ZIP_BYTES':z.stat().st_size,'ZIP_SHA256':sha(z.read_bytes()),'inventory_files':len(inv),'required_files_verified':sorted(required),'archive_readback_verified':True,'checks_passed':['source','81-pose collision','parity','theme','negative-control rejection','pivot preservation','motion','browser desktop/mobile','extended/no-JS','delivery']}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
