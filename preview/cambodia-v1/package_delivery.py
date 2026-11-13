from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
read=lambda n:json.loads((R/n).read_text())
s=read('source-check.json');assert s['collision_samples']==81 and not s['collisions']
p=read('parity-check.json');assert p['source_and_export_geometry_match'] and max(p['source_to_glb_max'],p['glb_to_source_max'])<1e-5
assert read('theme-check.json')['status']=='PASS' and read('extended-check.json')['status']=='PASS'
b=read('browser-check.json');assert len(b)==3
for x in b[:2]:
 assert x['offline_file'] and not x['errors'] and not x['external_requests'] and not x['overflow']
 assert all(x[k] for k in ['rotation','open_close','reset_mid_motion','reduced_motion'])
 assert x['asset']['degenerate']==0 and x['asset']['nonfinite']==0 and x['asset']['open_projection_max_abs_ndc']<1
assert b[2]['fallback'] and 'Detached ornament rejected' in (R/'theme-negative.txt').read_text()
assert '# pass 2' in (R/'motion-output.txt').read_text() and '# fail 0' in (R/'motion-output.txt').read_text()
assert (R/'cambodia-v1.html').stat().st_size<5000000
exclude={'inventory.json','delivery-check.json','cambodia-v1-source.zip'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.name not in exclude and not p.name.endswith('.blend1'))
required={'cambodia.blend','cambodia.glb','cambodia-v1.html','poster.png','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','maps/stone-color.png','maps/stone-roughness.png'}
assert required<={p.relative_to(R).as_posix() for p in files}
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'cambodia-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
 for p in files+[R/'inventory.json']:f.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as f:
 assert set(f.namelist())==set(inv)|{'inventory.json'}
 for name,v in inv.items():assert len(f.read(name))==v['bytes'] and sha(f.read(name))==v['sha256']
checks=['source','hinge-attachments','parity','theme','negative-control','motion','desktop-file','mobile-file','corrupt-fallback','no-js-fallback','texture-poster','delivery']
out={'status':'PASS','html_bytes':(R/'cambodia-v1.html').stat().st_size,'glb_bytes':(R/'cambodia.glb').stat().st_size,'payload_count':len(inv),'required_artifacts_present':True,'zip_readback':True,'zip_bytes':z.stat().st_size,'zip_sha256':sha(z.read_bytes()),'checks_passed':checks}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
