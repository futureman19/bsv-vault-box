from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
load=lambda n:json.loads((R/n).read_text())
source=load('source-check.json');parity=load('parity-check.json');browser=load('browser-check.json');theme=load('theme-check.json');extended=load('extended-check.json')
assert source['collision_samples']==81 and not source['collisions'] and source['moving_meshes']==17
assert source['hollow_floor_ray_z']<.3
assert parity['source_and_export_geometry_match'] and max(parity['source_to_glb_max'],parity['glb_to_source_max'])<1e-5
assert theme['status']=='PASS' and extended['status']=='PASS'
assert [x['case'] for x in browser]==['desktop','mobile','corrupted GLB']
for case in browser[:2]:
 assert not case['errors'] and not case['external_requests'] and case['offline_file'] and case['open_close'] and case['reset_mid_motion'] and case['reduced_motion'] and not case['overflow']
 assert case['asset']['degenerate']==0 and case['asset']['nonfinite']==0 and case['asset']['open_projection_max_abs_ndc']<1
assert browser[1]['touch_rotation'] and browser[2]['fallback'] and extended['noJS_poster']
assert '# pass 2' in (R/'motion-output.txt').read_text() and '# fail 0' in (R/'motion-output.txt').read_text()
assert 'AssertionError: Crown must travel with the lid' in (R/'initial/detached-crown-negative.txt').read_text()
html=R/'austria-v1.html';glb=R/'austria.glb';assert html.stat().st_size<5_000_000
checks=['source','parity','theme','browser-desktop','browser-mobile','motion','extended','corrupt-GLB','no-JS','negative-control','byte-budget']
(R/'acceptance-check.json').write_text(json.dumps({'status':'PASS','checks_passed':checks,'negative_control':'Detached in-memory crown rejected; saved asset unchanged','HTML_BYTES':html.stat().st_size,'GLB_BYTES':glb.stat().st_size},indent=2))
allowed={'.py','.js','.mjs','.json','.md','.txt','.html','.png','.jpg','.blend','.glb'}
files=sorted(f for f in R.rglob('*') if f.is_file() and (f.suffix in allowed or f.name in {'.gitattributes','.gitignore'}) and f.name not in {'inventory.json','delivery-check.json','packaging-output.txt','git-evidence.txt'} and (f.parent==R or f.parent.name in {'maps','initial'}))
required={'austria.blend','austria.glb','austria-v1.html','design-brief.md','README.md','poster.png','mechanism.blend','acceptance-check.json'}
assert required.issubset({f.name for f in files})
sha=lambda b:hashlib.sha256(b).hexdigest()
manifest={f.relative_to(R).as_posix():{'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())} for f in files}
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'austria-v1-source.zip'
with zipfile.ZipFile(z,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as arc:
 for f in files:arc.write(f,f.relative_to(R).as_posix())
with zipfile.ZipFile(z) as arc:
 assert set(arc.namelist())=={f.relative_to(R).as_posix() for f in files}
 assert arc.testzip() is None
 for f in files:assert arc.read(f.relative_to(R).as_posix())==f.read_bytes()
report={'status':'PASS','HTML_BYTES':html.stat().st_size,'GLB_BYTES':glb.stat().st_size,'ZIP_BYTES':z.stat().st_size,'ZIP_SHA256':sha(z.read_bytes()),'entries':len(files),'required_artifacts_present':True,'archive_exact_readback':True,'inventory_exclusions':'inventory itself, ZIP and delivery-check avoid circular hashing; packaging/git logs excluded'}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2));print('ALL ACCEPTANCE CHECKS PASS')
