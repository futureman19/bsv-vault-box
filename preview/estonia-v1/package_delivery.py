from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
def load(n):return json.loads((R/n).read_text())
def digest(b):return hashlib.sha256(b).hexdigest()
s=load('source-check.json');assert s['saved_source_reopened'] and s['collision_samples']==81 and not s['collisions']
p=load('parity-check.json');assert p['source_and_export_geometry_match'] and max(p['source_to_glb_max'],p['glb_to_source_max'])<1e-5
assert load('theme-check.json')['status']=='PASS';assert load('extended-check.json')['status']=='PASS'
b=load('browser-check.json');assert len(b)==3
for x in b[:2]:
 assert x['offline_file'] and not x['errors'] and not x['external_requests'] and x['open_close'] and x['reduced_motion'] and not x['overflow']
 assert x['asset']['degenerate']==x['asset']['nonfinite']==0 and x['asset']['open_projection_max_abs_ndc']<1
assert b[1]['touch_rotation'] and b[2]['fallback']
assert '# pass 2' in (R/'motion-output.txt').read_text() and '# fail 0' in (R/'motion-output.txt').read_text()
assert 'AssertionError: Detached ornament rejected' in (R/'negative-detached-output.txt').read_text()
html=R/'estonia-v1.html';assert html.stat().st_size<5_000_000
assert '[truncated]' not in (R/'template.html').read_text()
checks=['source','parity','theme','browser-desktop','browser-mobile','extended','motion','negative-control','byte-cap']
accept={'status':'PASS','checks':{k:'PASS' for k in checks},'HTML_BYTES':html.stat().st_size,'GLB_BYTES':(R/'estonia.glb').stat().st_size}
(R/'acceptance-check.json').write_text(json.dumps(accept,indent=2))
allowed={'.py','.js','.mjs','.json','.md','.txt','.html','.png','.jpg','.blend','.glb'}
files=sorted(f for f in R.rglob('*') if f.is_file() and (f.suffix in allowed or f.name in {'.gitattributes','.gitignore'}) and f.name not in {'inventory.json','delivery-check.json'} and (f.parent==R or f.parent.name=='maps'))
required={'estonia.blend','estonia.glb','estonia-v1.html','poster.png','README.md','design-brief.md','source-check.json','parity-check.json','browser-check.json','acceptance-check.json'}
manifest={f.relative_to(R).as_posix():{'bytes':f.stat().st_size,'sha256':digest(f.read_bytes())} for f in files}
assert required<=set(manifest)
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'estonia-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
 for f in files:archive.write(f,f.relative_to(R).as_posix())
with zipfile.ZipFile(z) as archive:
 assert len(archive.namelist())==len(files);assert archive.testzip() is None
 assert required<=set(archive.namelist())
 for f in files:assert archive.read(f.relative_to(R).as_posix())==f.read_bytes()
r={**accept,'archive_readback_verified':True,'required_artifacts_present':True,'zip_entries':len(files),'zip_bytes':z.stat().st_size,'zip_sha256':digest(z.read_bytes()),'inventory_sha256':digest((R/'inventory.json').read_bytes()),'delivery':'This same in-folder tested HTML; no untested external copy'}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));print('ALL ACCEPTANCE CHECKS PASS')
