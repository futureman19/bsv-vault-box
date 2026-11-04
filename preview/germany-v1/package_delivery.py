from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
read=lambda n:json.loads((R/n).read_text())
source=read('source-check.json');assert source['collision_samples']==81 and not source['collisions']
assert read('parity-check.json')['source_and_export_geometry_match']
assert read('theme-check.json')['status']=='PASS'
assert read('extended-check.json')['status']=='PASS'
b=read('browser-check.json');assert len(b)==3
for row in b[:2]:
 assert row['offline_file'] and not row['external_requests'] and not row['errors']
 assert row['open_close'] and row['reset_mid_motion'] and row['reduced_motion']
 assert row['asset']['nonfinite']==row['asset']['degenerate']==0
assert b[2]['fallback']
assert '# fail 0' in (R/'motion-output.txt').read_text()
html=R/'germany-v1.html';glb=R/'germany.glb';assert html.stat().st_size<5_000_000
required={'germany-v1.html','germany.glb','germany.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','motion-output.txt','maps/wood-color.png','maps/wood-end.png','maps/wood-roughness.png'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(s in ('node_modules','__pycache__') for s in p.relative_to(R).parts) and p.suffix not in ('.zip','.blend1') and p.name not in ('inventory.json','delivery-check.json','package-output.txt','staging-output.txt'))
sha=lambda data:hashlib.sha256(data).hexdigest()
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
assert required<=set(manifest)
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'germany-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
 for p in files:archive.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as archive:
 assert set(archive.namelist())=={p.relative_to(R).as_posix() for p in files}
 assert archive.testzip() is None
 for p in files:assert archive.read(p.relative_to(R).as_posix())==p.read_bytes()
report={'status':'PASS','HTML_BYTES':html.stat().st_size,'GLB_BYTES':glb.stat().st_size,'html_sha256':sha(html.read_bytes()),'glb_sha256':sha(glb.read_bytes()),'archive_bytes':z.stat().st_size,'archive_sha256':sha(z.read_bytes()),'archive_entries':len(files),'required_deliverables_present':True,'archive_readback_verified':True,'checks_passed':['source','parity','theme','browser-desktop','browser-mobile','extended','motion','delivery']}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
for gate in report['checks_passed']:print(gate.upper()+' PASS')
print('HTML_BYTES',html.stat().st_size,'GLB_BYTES',glb.stat().st_size)
