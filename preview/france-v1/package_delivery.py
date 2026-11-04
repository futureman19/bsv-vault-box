from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
read=lambda n:json.loads((R/n).read_text())
s=read('source-check.json');p=read('parity-check.json');t=read('theme-check.json');e=read('extended-check.json');b=read('browser-check.json');n=read('theme-negative-control.json')
assert s['collision_samples']==81 and not s['collisions'] and s['moving_meshes']==177 and s['static_meshes']==39
assert p['source_and_export_geometry_match'] and max(p['source_to_glb_max'],p['glb_to_source_max'])<1e-5
assert t['status']=='PASS' and all(t['checks'].values()) and e['status']=='PASS'
assert n['status']=='FAIL' and n['checks']['all_tiles_move_with_lid'] is False
assert [x['case'] for x in b]==['desktop','mobile','corrupted GLB']
for x in b[:2]:
 assert x['offline_file'] and x['open_close'] and x['reduced_motion'] and x['reset_mid_motion'] and not x['errors'] and not x['external_requests'] and not x['overflow']
 assert x['asset']['nonfinite']==0 and x['asset']['degenerate']==0 and x['asset']['open_projection_max_abs_ndc']<1
assert b[2]['fallback'] and e['noJS_poster']
assert '# pass 2' in (R/'motion-output.txt').read_text() and '# fail 0' in (R/'motion-output.txt').read_text()
html=R/'france-v1.html';glb=R/'france.glb';assert html.stat().st_size<5_000_000
allowed={'.py','.js','.mjs','.json','.md','.txt','.html','.png','.jpg','.blend','.glb'}
files=sorted(f for f in R.rglob('*') if f.is_file() and (f.suffix in allowed or f.name in {'.gitattributes','.gitignore'}) and f.name not in {'inventory.json','delivery-check.json'} and (f.parent==R or f.parent.name in {'maps','initial'}))
required={'france-v1.html','france.glb','france.blend','mechanism.blend','poster.png','poster.jpg','README.md','design-brief.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json','motion-output.txt'}
sha=lambda data:hashlib.sha256(data).hexdigest()
manifest={f.relative_to(R).as_posix():{'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())} for f in files}
assert required<=manifest.keys()
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'france-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for f in files:a.write(f,f.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())=={f.relative_to(R).as_posix() for f in files}
 assert required<=set(a.namelist()) and a.testzip() is None
 for f in files:assert a.read(f.relative_to(R).as_posix())==f.read_bytes()
report={'status':'PASS','HTML_BYTES':html.stat().st_size,'GLB_BYTES':glb.stat().st_size,'ZIP_BYTES':z.stat().st_size,'ZIP_ENTRIES':len(files),'zip_sha256':sha(z.read_bytes()),'archive_readback_verified':True,'required_artifacts_present':True,'checks_passed':['source','hinge-attachments','81-pose-motion-collisions','parity','theme','negative-control-rejection','motion-unit-tests','desktop-offline','mobile-offline','corrupt-GLB-fallback','no-JS-fallback','extended','delivery-inventory']}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
