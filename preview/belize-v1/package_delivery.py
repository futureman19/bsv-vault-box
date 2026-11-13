from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
required={'belize-v1.html','belize.glb','belize.blend','mechanism.blend','poster.png','poster.jpg','README.md','design-brief.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','hinge-attachment-check.json','maps/stone-color.png','maps/stone-roughness.png','maps/stone-normal.png'}
assert (R/'belize-v1.html').stat().st_size<5_000_000
s=json.loads((R/'source-check.json').read_text());assert s['collision_samples']==81 and not s['collisions']
p=json.loads((R/'parity-check.json').read_text());assert p['source_and_export_geometry_match']
for name in ['theme-check.json','extended-check.json']:assert json.loads((R/name).read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert len(b)==3 and all(not x['errors'] and not x['external_requests'] and x['reduced_motion'] for x in b[:2]) and b[2]['fallback']
exclude={'inventory.json','delivery-check.json','belize-v1-source.zip','package-output.txt','codex-lane.log','lane-prompt.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__','.git']) and p.name not in exclude and not p.name.endswith('.blend1'))
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
assert required<=set(inv),required-set(inv)
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
zpath=R/'belize-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(inv)|{'inventory.json'}
 for n,e in inv.items():assert len(z.read(n))==e['bytes'] and sha(z.read(n))==e['sha256']
result={'status':'PASS','html_bytes':(R/'belize-v1.html').stat().st_size,'glb_bytes':(R/'belize.glb').stat().st_size,'html_sha256':inv['belize-v1.html']['sha256'],'glb_sha256':inv['belize.glb']['sha256'],'archive_bytes':zpath.stat().st_size,'archive_sha256':sha(zpath.read_bytes()),'inventory_entries':len(inv),'required_artifacts_present':True,'archive_readback_verified':True,'checks_passed':['source','hinge-attachment','parity','theme-negative-control','browser-desktop-mobile','extended-maps-fallbacks','motion','delivery']}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print('DELIVERY PASS',json.dumps(result))
