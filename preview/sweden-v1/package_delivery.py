from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
checks={}
s=json.loads((R/'source-check.json').read_text());assert s['collision_samples']==81 and not s['collisions'];checks['source-motion']='PASS'
p=json.loads((R/'parity-check.json').read_text());assert p['source_and_export_geometry_match'] and max(p['source_to_glb_max'],p['glb_to_source_max'])<1e-5;checks['parity']='PASS'
for name in ['theme','extended']:
 assert json.loads((R/(name+'-check.json')).read_text())['status']=='PASS';checks[name]='PASS'
b=json.loads((R/'browser-check.json').read_text());assert {x['case'] for x in b}=={'desktop','mobile','corrupted GLB'}
for c in b[:2]:assert not c['errors'] and not c['external_requests'] and c['open_close'] and c['reduced_motion'] and c['asset']['bytes']==(R/'sweden.glb').stat().st_size
checks['browser']='PASS'
html=(R/'sweden-v1.html').read_bytes();assert len(html)<5_000_000;checks['size']='PASS'
required={'sweden.blend','sweden.glb','mechanism.blend','sweden-v1.html','poster.png','poster.jpg','README.md','design-brief.md','author.py','maps.py','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','.gitattributes'}
exclude={'inventory.json','delivery-check.json','sweden-v1-source.zip','package-output.txt'}
files={p.relative_to(R).as_posix():p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.blend1','.blend2'] and p.name not in exclude}
assert required<=files.keys()
inventory={name:{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for name,p in sorted(files.items())}
(R/'inventory.json').write_text(json.dumps(inventory,indent=2))
z=R/'sweden-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as out:
 for name,p in files.items():out.write(p,name)
 out.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(z) as inp:
 assert set(inp.namelist())==set(files)|{'inventory.json'}
 for name,item in inventory.items():
  data=inp.read(name);assert len(data)==item['bytes'] and sha(data)==item['sha256']
checks['archive-readback']='PASS'
r={'status':'PASS','checks':checks,'html_bytes':len(html),'glb_bytes':(R/'sweden.glb').stat().st_size,'payload_files':len(files),'zip_bytes':z.stat().st_size,'zip_sha256':sha(z.read_bytes()),'inventory_sha256':sha((R/'inventory.json').read_bytes()),'required_artifacts':sorted(required),'scope':'local source archive; not hosted or minted'}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
