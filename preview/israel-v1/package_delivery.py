from pathlib import Path
import hashlib,json,zipfile,shutil
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent
required={'israel-v1.html','israel.glb','israel.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','author.py','maps.py','build.py','viewer.js','motion.mjs','verify_browser.py','verify_source.py','verify_parity.py','verify_contract.py','verify_theme.py','source-check.json','parity-check.json','contract-check.json','browser-check.json','theme-check.json','maps/limestone-color.png','maps/limestone-normal.png','maps/limestone-roughness.png'}
excluded={'inventory.json','delivery-check.json','israel-v1-source.zip'}
files={p.relative_to(R).as_posix():p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__','delivery-extracted']) and p.name not in excluded and p.suffix!='.blend1'}
assert required<=files.keys(),required-files.keys()
def record(p):return {'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
assert files['israel-v1.html'].stat().st_size<5_000_000
source=json.loads((R/'source-check.json').read_text());assert source['collision_samples']==81 and not source['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'contract-check.json').read_text())['status']=='PASS'
browser=json.loads((R/'browser-check.json').read_text());assert {x['case'] for x in browser}=={'desktop','mobile','corrupted GLB'}
for x in browser[:2]:assert not x['errors'] and not x['external_requests'] and x['open_close'] and x['reset_mid_motion'] and x['reduced_motion']
manifest={k:record(v) for k,v in sorted(files.items())};(R/'inventory.json').write_text(json.dumps(manifest,indent=2)+'\n')
archive=R/'israel-v1-source.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,p in sorted(files.items()):z.write(p,n)
 z.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(archive) as z:
 assert set(z.namelist())==set(files)|{'inventory.json'}
 for n,r in manifest.items():
  d=z.read(n);assert len(d)==r['bytes'] and hashlib.sha256(d).hexdigest()==r['sha256']
 D=R/'delivery-extracted';D.mkdir(exist_ok=True);(D/'israel-v1.html').write_bytes(z.read('israel-v1.html'))
assert record(D/'israel-v1.html')==manifest['israel-v1.html']
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files']);c=b.new_context(offline=True,viewport={'width':390,'height':844},has_touch=True,is_mobile=True,reduced_motion='reduce');p=c.new_page();requests=[];errors=[]
 p.on('request',lambda r:requests.append(r.url) if r.url.startswith(('https:','http:')) else None);p.on('pageerror',lambda e:errors.append(str(e)))
 p.goto((D/'israel-v1.html').as_uri());p.wait_for_function('pilot.ready');p.locator('#open').tap();p.wait_for_function('pilot.progress===1');p.locator('#reset').tap();p.wait_for_function('pilot.progress===0');assert not requests and not errors;c.close();b.close()
shutil.rmtree(D)
result={'status':'PASS','html':manifest['israel-v1.html'],'glb':manifest['israel.glb'],'blend':manifest['israel.blend'],'archive':record(archive),'inventory':record(R/'inventory.json'),'payload_file_count':len(manifest),'required_file_count':len(required),'zip_exact_inventory_and_hash_readback':True,'extracted_offline_file_browser_open_reset':True,'external_requests':requests,'errors':errors}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2)+'\n');print('DELIVERY PASS');print(json.dumps(result,indent=2))
