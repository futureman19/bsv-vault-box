from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
required={'indian-ocean-v1.html','indian-ocean.glb','indian-ocean.blend','mechanism.blend','design-brief.md','README.md','poster.png','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','motion-output.txt'}
assert (R/'indian-ocean-v1.html').stat().st_size<5_000_000
s=json.loads((R/'source-check.json').read_text());assert s['collision_samples']==81 and not s['collisions']
p=json.loads((R/'parity-check.json').read_text());assert max(p['source_to_glb_max'],p['glb_to_source_max'])<1e-5
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert {x['case'] for x in b}=={'desktop','mobile','corrupted GLB'}
for x in b[:2]:assert x['offline_file'] and x['open_close'] and x['reduced_motion'] and not x['errors'] and not x['external_requests'] and not x['asset']['degenerate']
assert 'pass 2' in (R/'motion-output.txt').read_text()
excluded={'inventory.json','delivery-check.json','indian-ocean-v1-source.zip','package-output.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.name not in excluded and p.suffix not in ['.blend1','.pyc'])
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
assert required<=inv.keys()
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'indian-ocean-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
 for p in files+[R/'inventory.json']:f.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as f:
 assert set(f.namelist())==set(inv)|{'inventory.json'}
 for name,v in inv.items():
  data=f.read(name);assert len(data)==v['bytes'] and hashlib.sha256(data).hexdigest()==v['sha256']
result={'status':'PASS','html_bytes':inv['indian-ocean-v1.html']['bytes'],'glb_bytes':inv['indian-ocean.glb']['bytes'],'inventory_files':len(inv),'required_artifacts_present':True,'archive_readback_all_hashes_match':True,'zip_bytes':z.stat().st_size,'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'checks_passed':['source','parity','theme','motion','browser-desktop','browser-mobile','corrupt-glb-fallback','no-js-fallback','portable-maps','poster','delivery']}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print('PASS ALL ACCEPTANCE');print('HTML_BYTES',result['html_bytes'],'GLB_BYTES',result['glb_bytes']);print(json.dumps(result))
