"""Exercise the HTML extracted from the delivery ZIP, not a source template."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import zipfile,hashlib,json,shutil
R=Path(__file__).resolve().parent;tmp=R/'delivery-verify';tmp.mkdir(exist_ok=True);html=tmp/'kiribati-v1.html'
with zipfile.ZipFile(R/'kiribati-v1-source.zip') as z:html.write_bytes(z.read('kiribati-v1.html'))
assert html.read_bytes()==(R/'kiribati-v1.html').read_bytes();cases=[]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
  for mobile in [False,True]:
   c=b.new_context(offline=True,viewport={'width':390 if mobile else 1440,'height':844 if mobile else 1080},is_mobile=mobile,has_touch=mobile,reduced_motion='reduce');p=c.new_page();errors=[];requests=[];p.on('pageerror',lambda e:errors.append(str(e)));p.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http:','https:')) else None);p.goto(html.as_uri());p.wait_for_function('pilot.ready');p.locator('#open').tap() if mobile else p.locator('#open').click();p.wait_for_function('pilot.progress===1');p.locator('#reset').tap() if mobile else p.locator('#reset').click();p.wait_for_function('pilot.progress===0');assert not errors and not requests;cases.append({'case':'mobile' if mobile else 'desktop','file_protocol':True,'offline':True,'open_reset':True,'errors':errors,'external_requests':requests});c.close()
  b.close()
 result={'status':'PASS','tested_html_sha256':hashlib.sha256(html.read_bytes()).hexdigest(),'cases':cases};(R/'delivery-copy-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
finally:shutil.rmtree(tmp)
