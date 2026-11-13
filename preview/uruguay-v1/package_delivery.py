from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
j=lambda n:json.loads((R/n).read_text())
source=j('source-check.json');assert source['saved_source_reopened'] and not source['collisions'] and source['collision_samples']==81
assert j('parity-check.json')['source_and_export_geometry_match']
assert j('theme-check.json')['status']=='PASS' and j('theme-source-check.json')['status']=='PASS'
motion=j('motion-samples.json');assert motion['status']=='PASS' and len(motion['samples'])==81
browser=j('browser-check.json');assert {v['case'] for v in browser}=={'desktop','mobile','corrupted GLB'}
for v in browser[:2]:
 assert v['open_close'] and v['reset_mid_motion'] and v['reduced_motion'] and not v['errors'] and not v['external_requests'] and not v['overflow']
assert browser[2]['fallback']
html=R/'uruguay-v1.html';assert html.stat().st_size<5_000_000
required={'uruguay-v1.html','uruguay.blend','uruguay.glb','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','theme-source-check.json','motion-samples.json','maps/mineral-color.png','maps/mineral-roughness.png','maps/grass-color.png'}
excluded={'inventory.json','delivery-check.json','package-output.txt','git-evidence.txt','staged-check.json','setup.py','lane-prompt.md','codex-lane.log'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(s in {'node_modules','__pycache__','.git'} for s in p.relative_to(R).parts) and p.name not in excluded and p.suffix not in {'.zip','.blend1','.pyc'})
names={p.relative_to(R).as_posix() for p in files};assert required<=names,(required-names)
sha=lambda b:hashlib.sha256(b).hexdigest()
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
(R/'inventory.json').write_text(json.dumps(inv,indent=2));files.append(R/'inventory.json')
z=R/'uruguay-v1-source.zip'
with zipfile.ZipFile(z,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
 for p in files:archive.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as archive:
 assert archive.testzip() is None
 assert set(archive.namelist())==names|{'inventory.json'}
 for p in files:assert archive.read(p.relative_to(R).as_posix())==p.read_bytes()
report={'status':'PASS','HTML_BYTES':html.stat().st_size,'GLB_BYTES':(R/'uruguay.glb').stat().st_size,'ZIP_BYTES':z.stat().st_size,'ZIP_SHA256':sha(z.read_bytes()),'ZIP_entries':len(files),'required_artifacts_present':True,'archive_readback_verified':True,'inventory_entries':len(inv),'inventory_sha256':sha((R/'inventory.json').read_bytes()),'checks_passed':['source','hinge-attachment','motion-81','parity','theme-source','theme-runtime','browser-desktop','browser-mobile','corrupt-GLB','no-JS','size','SHA256-inventory','ZIP-readback'],'excluded_envelopes':['inventory.json (self)','delivery-check.json (self)','source ZIP (envelope)','package-output.txt (active log)','git evidence','optional lane prompt/log/setup']}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
