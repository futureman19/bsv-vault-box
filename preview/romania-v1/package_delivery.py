from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
checks=['source-check.json','parity-check.json','browser-check.json','extended-check.json','theme-check.json','motion-check.json','hinge-attachment-check.json']
for n in checks:assert (R/n).is_file(),n
s=json.loads((R/'source-check.json').read_text()); assert s['collision_samples']==81 and not s['collisions'] and s['saved_source_reopened']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
for n in ['extended-check.json','theme-check.json','motion-check.json']:assert json.loads((R/n).read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert len(b)==3
for case in b[:2]:assert case['offline_file'] and case['open_close'] and case['reduced_motion'] and not case['errors'] and not case['external_requests']
assert b[2]['fallback']
html=R/'romania-v1.html';assert 0<html.stat().st_size<5_000_000
required={'romania.blend','romania.glb','romania-v1.html','poster.png','poster.jpg','design-brief.md','README.md','author.py','ornament.py','maps.py','mechanism.blend','.gitattributes',*checks}
files=sorted(f for f in R.rglob('*') if f.is_file() and (f.parent==R or f.parent.name in {'maps','initial'}) and f.name not in {'inventory.json','delivery-check.json','romania-v1-source.zip','package-output.txt','git-verification.txt'} and f.suffix not in {'.blend1','.pyc'} and not f.name.startswith('lane-'))
manifest={f.relative_to(R).as_posix():{'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in files}
assert required<=manifest.keys(),required-manifest.keys()
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'romania-v1-source.zip'
with zipfile.ZipFile(z,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for f in files:a.write(f,f.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert a.testzip() is None and set(a.namelist())=={f.relative_to(R).as_posix() for f in files}
 for f in files:assert a.read(f.relative_to(R).as_posix())==f.read_bytes()
report={'status':'PASS','HTML_BYTES':html.stat().st_size,'GLB_BYTES':(R/'romania.glb').stat().st_size,'ZIP_BYTES':z.stat().st_size,'ZIP_entries':len(files),'required_deliverables_present':True,'archive_readback_verified':True,'inventory_sha256':hashlib.sha256((R/'inventory.json').read_bytes()).hexdigest(),'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'checks_passed':checks,'scope':'Local art only; no chain services, minting or hosting'}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
