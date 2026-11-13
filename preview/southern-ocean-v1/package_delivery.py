from pathlib import Path
import hashlib,json,zipfile,shutil
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent
excluded={'inventory.json','delivery-check.json','package-output.txt','git-verification.json'}
def digest(data):return hashlib.sha256(data).hexdigest()
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in {'node_modules','__pycache__','delivery-readback'} for x in p.relative_to(R).parts) and p.suffix not in {'.zip','.blend1'} and p.name not in excluded)
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for p in files}
required={'southern-ocean-v1.html','southern-ocean.glb','southern-ocean.blend','mechanism.blend','poster.png','poster.jpg','README.md','design-brief.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json','.gitattributes'}
assert required<=set(inv);assert inv['southern-ocean-v1.html']['bytes']<5000000
(R/'inventory.json').write_text(json.dumps(inv,indent=2),encoding='utf8')
zpath=R/'southern-ocean-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for n in [*inv,'inventory.json']:z.write(R/n,n)
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(inv)|{'inventory.json'}
 for n,entry in inv.items():assert digest(z.read(n))==entry['sha256'] and len(z.read(n))==entry['bytes']
 dest=R/'delivery-readback';dest.mkdir(exist_ok=True);z.extract('southern-ocean-v1.html',dest)
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True);c=b.new_context(offline=True,viewport={'width':390,'height':844},is_mobile=True,has_touch=True);p=c.new_page();errors=[];requests=[];p.on('pageerror',lambda e:errors.append(str(e)));p.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http:','https:')) else None)
 p.goto((dest/'southern-ocean-v1.html').as_uri());p.wait_for_function('pilot.ready');p.locator('#open').tap();p.wait_for_function('pilot.progress===1');p.locator('#reset').tap();p.wait_for_function('pilot.progress===0');assert not errors and not requests;c.close();b.close()
shutil.rmtree(dest)
out={'status':'PASS','html_bytes':inv['southern-ocean-v1.html']['bytes'],'glb_bytes':inv['southern-ocean.glb']['bytes'],'inventory_entries':len(inv),'required_artifacts_present':True,'zip_membership_exact':True,'zip_hashes_match':True,'extracted_html_offline_open_reset':True,'external_requests':requests,'errors':errors,'zip_bytes':zpath.stat().st_size,'zip_sha256':digest(zpath.read_bytes()),'inventory_sha256':digest((R/'inventory.json').read_bytes())}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print('DELIVERY PASS',json.dumps(out))
