from pathlib import Path
import json,hashlib,re,base64
R=Path(__file__).resolve().parent
required={'mozambique.blend','mozambique.glb','mozambique-v1.html','poster.png','poster.jpg','author.py','maps.py','build.py','source-check.json','parity-check.json','theme-check.json','browser-check.json','design-brief.md','README.md'}
files={str(p.relative_to(R)).replace('\\','/'):p for p in R.rglob('*') if p.is_file() and p.name not in ['inventory.json','delivery-check.json'] and '__pycache__' not in str(p) and p.suffix!='.blend1'}
assert required<=files.keys(),required-files.keys()
def ident(p):return {'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
inv={name:ident(p) for name,p in sorted(files.items())};(R/'inventory.json').write_text(json.dumps(inv,indent=2))
for name,record in json.loads((R/'inventory.json').read_text()).items():assert ident(R/name)==record
html=(R/'mozambique-v1.html').read_text();assert (R/'mozambique-v1.html').stat().st_size<5_000_000
encoded=re.search(r'<script id="asset" type="application/octet-stream">([^<]+)</script>',html).group(1)
assert base64.b64decode(encoded)==(R/'mozambique.glb').read_bytes()
assert base64.b64decode(re.search(r'data:image/jpeg;base64,([^"\s]+)',html).group(1))==(R/'poster.jpg').read_bytes()
s=json.loads((R/'source-check.json').read_text());assert s['collision_samples']==81 and not s['collisions'] and s['moving_meshes']==19
p=json.loads((R/'parity-check.json').read_text());assert max(p['source_to_glb_max'],p['glb_to_source_max'])<1e-5
b=json.loads((R/'browser-check.json').read_text());assert {x['case'] for x in b}=={'desktop','mobile','corrupted GLB'}
for x in b[:2]:assert not x['external_requests'] and not x['errors'] and x['asset']['bytes']==(R/'mozambique.glb').stat().st_size
assert json.loads((R/'theme-check.json').read_text())['result']=='PASS'
out={'result':'PASS','html_bytes':(R/'mozambique-v1.html').stat().st_size,'glb_bytes':(R/'mozambique.glb').stat().st_size,'inventory_files':len(inv),'inventory_sha256':ident(R/'inventory.json')['sha256'],'embedded_glb_exact':True,'embedded_actual_source_poster_exact':True,'all_inventory_hashes_readback':True,'exclusions':['inventory.json','delivery-check.json','__pycache__','*.blend1']}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
