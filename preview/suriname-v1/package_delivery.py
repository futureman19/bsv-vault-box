from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
required={'suriname.blend','suriname.glb','suriname-v1.html','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','extended-check.json','theme-source-check.json','hinge-attachment-check.json'}
assert (R/'suriname-v1.html').stat().st_size<5000000
source=json.loads((R/'source-check.json').read_text());assert source['collision_samples']==81 and not source['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
for name in ['extended-check.json','theme-source-check.json']:assert json.loads((R/name).read_text())['status']=='PASS'
browser=json.loads((R/'browser-check.json').read_text());assert {x['case'] for x in browser}=={'desktop','mobile','corrupted GLB'}
for b in browser[:2]:assert not b['errors'] and not b['external_requests'] and b['open_close'] and b['reduced_motion']
assert browser[2]['fallback']
excluded={'inventory.json','delivery-check.json','suriname-v1-source.zip','lane-log.txt','lane-prompt.txt','setup.py'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(s in ['node_modules','__pycache__'] for s in p.relative_to(R).parts) and p.name not in excluded and p.suffix not in ['.blend1','.pyc'])
inv={str(p.relative_to(R)).replace('\\','/'):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files};assert required<=set(inv)
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'suriname-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as out:
 for name in inv:out.write(R/name,name)
 out.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(z) as inp:
 assert set(inp.namelist())==set(inv)|{'inventory.json'}
 for name,item in inv.items():
  data=inp.read(name);assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256']
r=dict(status='PASS',html_bytes=(R/'suriname-v1.html').stat().st_size,glb_bytes=(R/'suriname.glb').stat().st_size,required_artifacts_present=True,archive_readback=True,inventory_files=len(inv),zip_bytes=z.stat().st_size,zip_sha256=hashlib.sha256(z.read_bytes()).hexdigest())
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print('DELIVERY PASS',json.dumps(r));print('HTML_BYTES',r['html_bytes'],'GLB_BYTES',r['glb_bytes'])
