"""Byte inventory + archive readback + actual extracted HTML offline smoke.
No uploads or writes outside this directory. Inventory excludes its own hash
and delivery/ZIP envelopes to avoid recursion.
"""
from pathlib import Path
import hashlib,json,zipfile,shutil
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent
required={'lesotho-v1.html','lesotho.glb','lesotho.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','maps/basalt-color.png','maps/basalt-roughness.png','maps/woven-indigo.png','author.py','maps.py','build.py','verify_source.py','verify_parity.py','test_theme.py','verify_browser.py','verify_extended.py','tests.mjs','motion.mjs','viewer.js','template.html','THREE-LICENSE.txt'}
def digest(p):return {'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
exclude={'inventory.json','delivery-check.json','lesotho-v1-source.zip'}
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name not in exclude and not any(part in {'delivery','__pycache__','node_modules'} for part in p.relative_to(R).parts) and not p.name.endswith(('.blend1','.pyc')))
inv={p.relative_to(R).as_posix():digest(p) for p in files};assert required<=inv.keys(),required-inv.keys()
assert inv['lesotho-v1.html']['bytes']<5_000_000
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'lesotho-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
 for p in files+[R/'inventory.json']:archive.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as archive:
 assert set(archive.namelist())==set(inv)|{'inventory.json'}
 for n,v in inv.items():
  b=archive.read(n);assert len(b)==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256'],n
# Copy the exact viewer as shipped, reopen file:// with network disabled.
d=R/'delivery';d.mkdir(exist_ok=True);dest=d/'lesotho-v1.html';shutil.copy2(R/'lesotho-v1.html',dest);assert digest(dest)==inv['lesotho-v1.html']
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files']);c=b.new_context(offline=True,viewport={'width':390,'height':844},is_mobile=True,has_touch=True);p=c.new_page();errors=[];requests=[];p.on('pageerror',lambda e:errors.append(str(e)));p.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http:','https:')) else None)
 p.goto(dest.as_uri());p.wait_for_function('pilot.ready');p.locator('#open').tap();p.wait_for_function('pilot.progress===1');assert not errors and not requests;p.locator('#reset').tap();p.wait_for_function('pilot.progress===0');c.close();b.close()
result={'status':'PASS','html_bytes':inv['lesotho-v1.html']['bytes'],'glb_bytes':inv['lesotho.glb']['bytes'],'files':len(inv),'required_artifacts_complete':True,'archive_inventory_and_hashes_verified':True,'zip':digest(z),'inventory':digest(R/'inventory.json'),'copied_html_offline_mobile_open_reset':True,'external_requests':requests,'errors':errors}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print('DELIVERY PASS',json.dumps(result))
