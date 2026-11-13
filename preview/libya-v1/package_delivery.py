from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent
required=['libya-v1.html','libya.glb','libya.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','motion-output.txt','maps/ochre.png','maps/roughness.png','maps/sand.png']
assert all((R/n).is_file() for n in required)
assert (R/'libya-v1.html').stat().st_size<5_000_000
source=json.loads((R/'source-check.json').read_text());assert source['collision_samples']==81 and not source['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
browser=json.loads((R/'browser-check.json').read_text());assert {x['case'] for x in browser}=={'desktop','mobile','corrupted GLB'}
for c in browser[:2]:assert c['offline_file'] and c['reduced_motion'] and c['open_close'] and not c['errors'] and not c['external_requests'] and not c['overflow']
assert json.loads((R/'extended-check.json').read_text())['noJS_poster']
assert 'fail 0' in (R/'motion-output.txt').read_text(encoding='utf8')
files=[p for p in R.rglob('*') if p.is_file() and p.name not in ['inventory.json','delivery-check.json'] and '__pycache__' not in p.parts and not p.name.endswith('.blend1')]
inventory={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)}
(R/'inventory.json').write_text(json.dumps(inventory,indent=2))
for n,v in json.loads((R/'inventory.json').read_text()).items():
 b=(R/n).read_bytes();assert len(b)==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256']
result={'status':'PASS','HTML_BYTES':inventory['libya-v1.html']['bytes'],'GLB_BYTES':inventory['libya.glb']['bytes'],'inventory_count':len(inventory),'inventory_sha256':hashlib.sha256((R/'inventory.json').read_bytes()).hexdigest(),'required_files':required,'inventory_readback_verified':True,'exclusions':['inventory.json (self hash)','delivery-check.json (envelope)','__pycache__','.blend1']}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
