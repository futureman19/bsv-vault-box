from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(n):return json.loads((R/n).read_text())
s=load('source-check.json');assert s['saved_source_reopened'] and s['collision_samples']==81 and not s['collisions']
p=load('parity-check.json');assert p['source_and_export_geometry_match'] and max(p['source_to_glb_max'],p['glb_to_source_max'])<1e-5
for name in ['source-contract-check.json','extended-check.json','theme-check.json']:assert load(name)['status']=='PASS'
b=load('browser-check.json');assert len(b)==3
for c in b[:2]:
 assert c['offline_file'] and not c['external_requests'] and not c['errors'] and not c['overflow'] and c['rotation'] and c['open_close'] and c['reset_mid_motion'] and c['reduced_motion']
 assert c['asset']['nonfinite']==0 and c['asset']['degenerate']==0 and c['asset']['open_projection_max_abs_ndc']<1
assert b[1]['touch_rotation'] and b[2]['fallback'] and not b[2]['unhandled_errors']
required={'cameroon-v1.html','cameroon.glb','cameroon.blend','mechanism.blend','design-brief.md','README.md','poster.png','poster.jpg','source-check.json','parity-check.json','browser-check.json','extended-check.json','theme-check.json','source-contract-check.json','desktop-closed.png','desktop-open.png','mobile-closed.png','mobile-open.png','author.py','maps.py','build.py','verify_source.py','verify_parity.py','verify_browser.py','verify_extended.py','verify_contract.py','tests.mjs','test_theme.py','motion.mjs','viewer.js','template.html','THREE-LICENSE.txt','maps/basalt-color.png','maps/basalt-roughness.png','maps/basalt-normal.png'}
allowed={'.py','.js','.mjs','.json','.md','.txt','.html','.png','.jpg','.blend','.glb'}
files=sorted(f for f in R.rglob('*') if f.is_file() and (f.suffix in allowed or f.name=='.gitattributes') and f.name not in {'inventory.json','delivery-check.json','implementation-brief.txt'} and (f.parent==R or f.parent.name in {'maps','initial'}))
names={f.relative_to(R).as_posix() for f in files};assert required<=names,required-names
manifest={f.relative_to(R).as_posix():{'bytes':f.stat().st_size,'sha256':sha(f)} for f in files}
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'cameroon-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for f in files:a.write(f,f.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert a.testzip() is None and len(a.namelist())==len(files) and required<=set(a.namelist())
 for f in files:assert a.read(f.relative_to(R).as_posix())==f.read_bytes()
html=R/'cameroon-v1.html';glb=R/'cameroon.glb';assert html.stat().st_size<5000000
out={'status':'PASS','HTML_BYTES':html.stat().st_size,'GLB_BYTES':glb.stat().st_size,'html_sha256':sha(html),'glb_sha256':sha(glb),'ZIP_BYTES':z.stat().st_size,'zip_sha256':sha(z),'ZIP_entries':len(files),'explicit_required_inventory_verified':True,'archive_readback_verified':True,'delivery_location':'this folder; exact tested HTML, no separate copied output','inventory_exclusions':'inventory itself, delivery envelope, source ZIP and implementation prompt to avoid recursion; no dependencies/backups/cache'}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
