from pathlib import Path
import hashlib,json,zipfile,shutil
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent;D=Path('C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-morocco-atlas-v2');D.mkdir(exist_ok=True)
required={'morocco-atlas-v2.html','morocco.glb','morocco.blend','mechanism.blend','author.py','materials.py','build.py','viewer.js','motion.mjs','template.html','README.md','poster.jpg','poster.png','three-pass-review.jpg','reference-comparison.jpg','before-after-closed.jpg','before-after-open.jpg','before-after-detail.jpg','checkpoints/pass1-materials.png','checkpoints/pass2-tilework.png','checkpoints/pass3-ridge-hardware.png'}
exclude={'maps.py','render_review.py','compare.py','inspect_parts.py','verify_reexport.py','inventory.json','delivery-check.json'}
files=[p for p in R.rglob('*') if p.is_file() and p.suffix in {'.py','.js','.mjs','.json','.html','.glb','.blend','.png','.jpg','.md','.txt'} and p.name not in exclude and 'node_modules' not in p.parts]
inventory={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files};assert required<=inventory.keys(),required-inventory.keys()
(R/'inventory.json').write_text(json.dumps(inventory,indent=2));files.append(R/'inventory.json')
z=R/'morocco-atlas-v2-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
 for p in files:archive.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as archive:
 assert required<=set(archive.namelist())
 for name,entry in inventory.items():assert hashlib.sha256(archive.read(name)).hexdigest()==entry['sha256']
files.append(z)
for p in files:
 target=D/p.relative_to(R);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target);assert hashlib.sha256(target.read_bytes()).digest()==hashlib.sha256(p.read_bytes()).digest()
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files']);c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();requests=[];errors=[];p.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http:','https:')) else None);p.on('pageerror',lambda e:errors.append(str(e)));p.goto((D/'morocco-atlas-v2.html').as_uri());p.wait_for_function('pilot.ready');assert p.evaluate('pilot.asset.bytes')==(D/'morocco.glb').stat().st_size;p.locator('#open').click();p.wait_for_function('pilot.progress===1');p.locator('#reset').click();p.wait_for_function('pilot.progress===0');p.screenshot(path=str(D/'delivery-opened-offline.png'));assert not requests and not errors;b.close()
result={'copied_files':len(files),'zip_entries_verified':len(inventory),'required_artifacts_verified':sorted(required),'delivery_html_offline_open_reset':True,'requests':requests,'errors':errors,'html_bytes':(D/'morocco-atlas-v2.html').stat().st_size,'glb_bytes':(D/'morocco.glb').stat().st_size,'blend_bytes':(D/'morocco.blend').stat().st_size,'zip_bytes':z.stat().st_size}
for root in [R,D]:(root/'delivery-check.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
