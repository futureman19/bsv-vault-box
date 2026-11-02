from pathlib import Path
import hashlib,json,zipfile,shutil
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent
required={'laos.blend','laos.glb','laos-v1.html','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','author.py','maps.py','build.py','viewer.js','motion.mjs','template.html','THREE-LICENSE.txt','source-check.json','parity-check.json','browser-check.json','extended-check.json','theme-check.json','design-check.json','negative-check.json','hinge-attachment-check.json','tests.mjs'}
assert all((R/n).is_file() for n in required)
s=json.loads((R/'source-check.json').read_text());assert s['collision_samples']==81 and not s['collisions'] and s['moving_meshes']>0
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
for name in ['theme-check','design-check','negative-check']:assert json.loads((R/(name+'.json')).read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert {x['case'] for x in b}=={'desktop','mobile','corrupted GLB'}
for x in b[:2]:
 assert not x['errors'] and not x['external_requests'] and not x['overflow'] and x['open_close'] and x['reset_mid_motion'] and x['reduced_motion']
 assert x['asset']['degenerate']==0 and x['asset']['nonfinite']==0
assert json.loads((R/'extended-check.json').read_text())['noJS_poster']
assert (R/'laos-v1.html').stat().st_size<5_000_000
allowed={'.py','.js','.mjs','.json','.md','.txt','.html','.png','.jpg','.blend','.glb'}
files=sorted(p for p in R.rglob('*') if p.is_file() and (p.suffix in allowed or p.name=='.gitattributes') and p.name not in {'inventory.json','delivery-check.json'} and (p.parent==R or p.parent==R/'maps'))
assert required<={p.relative_to(R).as_posix() for p in files}
def sha(data):return hashlib.sha256(data).hexdigest()
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'laos-v1-source.zip'
with zipfile.ZipFile(z,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
D=R/'delivery-probe';D.mkdir(exist_ok=True)
try:
 with zipfile.ZipFile(z) as a:
  assert a.testzip() is None and len(a.namelist())==len(files)
  assert required<=set(a.namelist())
  for p in files:
   name=p.relative_to(R).as_posix();assert not name.startswith('/') and '..' not in Path(name).parts;assert a.read(name)==p.read_bytes()
  (D/'laos-v1.html').write_bytes(a.read('laos-v1.html'))
 assert (D/'laos-v1.html').read_bytes()==(R/'laos-v1.html').read_bytes()
 with sync_playwright() as pw:
  browser=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
  context=browser.new_context(offline=True,viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
  p=context.new_page();errors=[];requests=[];p.on('pageerror',lambda e:errors.append(str(e)));p.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http:','https:')) else None)
  p.goto((D/'laos-v1.html').as_uri());p.wait_for_function('pilot.ready');p.locator('#open').tap();p.wait_for_function('pilot.progress===1');assert p.evaluate('pilot.asset.bytes')==(R/'laos.glb').stat().st_size
  assert not errors and not requests
  context.close();browser.close()
finally:shutil.rmtree(D)
report={'status':'PASS','HTML_BYTES':(R/'laos-v1.html').stat().st_size,'GLB_BYTES':(R/'laos.glb').stat().st_size,'ZIP_BYTES':z.stat().st_size,'ZIP_entries':len(files),'required_artifacts_present':True,'archive_readback_verified':True,'extracted_HTML_offline_mobile_open':True,'external_requests':requests,'errors':errors,'zip_sha256':sha(z.read_bytes()),'inventory_sha256':sha((R/'inventory.json').read_bytes())}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));print('DELIVERY PASS',json.dumps(report))
