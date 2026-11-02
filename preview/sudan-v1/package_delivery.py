"""Exact nonrecursive inventory, complete ZIP readback and extracted-file browser proof."""
from pathlib import Path
import hashlib,json,zipfile,shutil
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent
excluded={'inventory.json','delivery-check.json','sudan-v1-source.zip'}
required={'sudan-v1.html','sudan.glb','sudan.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','author.py','maps.py','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json','motion-sampling.json','acceptance-summary.json','THREE-LICENSE.txt','maps/sand-color.png','maps/sand-normal.png','maps/sand-roughness.png'}
def digest(b):return hashlib.sha256(b).hexdigest()
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name not in excluded and p.suffix not in ['.blend1','.pyc'] and not any(x in p.parts for x in ['__pycache__','node_modules','_delivery_verify']))
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for p in files}
assert required<=set(inv),required-set(inv)
assert inv['sudan-v1.html']['bytes']<5_000_000
(R/'inventory.json').write_text(json.dumps(inv,indent=2),encoding='utf8')
archive=R/'sudan-v1-source.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(archive) as z:
 assert set(z.namelist())==set(inv)|{'inventory.json'}
 for n,entry in inv.items():
  data=z.read(n);assert len(data)==entry['bytes'] and digest(data)==entry['sha256'],n
 assert z.read('inventory.json')==(R/'inventory.json').read_bytes()
 # Extraction target is in the task's allowed directory; test actual archived HTML.
 delivery=R/'_delivery_verify';delivery.mkdir(exist_ok=True)
 html=delivery/'sudan-v1.html';html.write_bytes(z.read('sudan-v1.html'))
assert digest(html.read_bytes())==inv['sudan-v1.html']['sha256']
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':390,'height':844},is_mobile=True,has_touch=True,reduced_motion='reduce')
 p=c.new_page();errors=[];requests=[]
 p.on('pageerror',lambda e:errors.append(str(e)))
 p.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http:','https:')) else None)
 p.goto(html.as_uri());p.wait_for_function('pilot.ready');assert p.evaluate('pilot.asset.bytes')==inv['sudan.glb']['bytes']
 p.locator('#open').tap();p.wait_for_function('pilot.progress===1');p.locator('#reset').tap();p.wait_for_function('pilot.progress===0')
 assert not errors and not requests
 c.close();b.close()
shutil.rmtree(delivery)
out={'status':'PASS','html_bytes':inv['sudan-v1.html']['bytes'],'glb_bytes':inv['sudan.glb']['bytes'],'html_sha256':inv['sudan-v1.html']['sha256'],'glb_sha256':inv['sudan.glb']['sha256'],'inventory_files':len(inv),'required_artifacts_present':sorted(required),'zip_entries':len(inv)+1,'zip_bytes':archive.stat().st_size,'zip_sha256':digest(archive.read_bytes()),'every_zip_entry_hash_readback':True,'extracted_html_offline_mobile_open_reset':True,'external_requests':requests,'unhandled_errors':errors,'exclusions':'Inventory and delivery result excluded from self-hashing; ZIP includes inventory, excludes itself and delivery-check.'}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2),encoding='utf8');print('DELIVERY PASS');print(json.dumps(out,indent=2))
