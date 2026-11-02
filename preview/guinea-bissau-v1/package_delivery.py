from pathlib import Path
import json,hashlib,zipfile,shutil
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
required={'guinea-bissau-v1.html','guinea-bissau.glb','guinea-bissau.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','author.py','maps.py','build.py','check_all.py','verify_theme.py','verify_source.py','verify_parity.py','verify_browser.py','verify_extended.py','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','acceptance-check.json','viewer.js','viewer.bundle.js','motion.mjs','tests.mjs','template.html','THREE-LICENSE.txt','package.json','maps/sediment.png','maps/roughness.png','maps/sand.png'}
files=[p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['delivery','__pycache__','node_modules']) and p.suffix not in ['.zip','.blend1','.pyc'] and p.name not in ['inventory.json','delivery-check.json','setup.py','lane-prompt.md','codex-lane.log']]
names={p.relative_to(R).as_posix() for p in files};assert required<=names,required-names
inventory={p.relative_to(R).as_posix():dict(bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for p in sorted(files)}
(R/'inventory.json').write_text(json.dumps(inventory,indent=2))
zpath=R/'guinea-bissau-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==names|{'inventory.json'}
 for n,v in inventory.items():assert sha(z.read(n))==v['sha256'] and len(z.read(n))==v['bytes']
 d=R/'delivery';d.mkdir(exist_ok=True)
 for n in ['guinea-bissau-v1.html','guinea-bissau.glb']: (d/n).write_bytes(z.read(n))
html=d/'guinea-bissau-v1.html';assert html.stat().st_size<5000000
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files']);c=b.new_context(offline=True);p=c.new_page();errors=[];requests=[]
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http:','https:')) else None)
 p.goto(html.as_uri());p.wait_for_function('pilot.ready');p.locator('#open').click();p.wait_for_function('pilot.progress===1');assert not errors and not requests;b.close()
result=dict(status='PASS',html_bytes=html.stat().st_size,glb_bytes=(d/'guinea-bissau.glb').stat().st_size,zip_bytes=zpath.stat().st_size,zip_sha256=sha(zpath.read_bytes()),inventory_sha256=sha((R/'inventory.json').read_bytes()),required_artifacts=sorted(required),archive_entries=len(names)+1,all_archived_hashes_verified=True,archived_html_offline_open=True,external_requests=requests,errors=errors)
shutil.rmtree(d)
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print('DELIVERY PASS');print('HTML_BYTES',result['html_bytes'],'GLB_BYTES',result['glb_bytes'])
