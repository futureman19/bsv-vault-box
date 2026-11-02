from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent;results=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 for label,w,h in [('desktop',1440,1080),('mobile',390,844)]:
  for kind in ['no-js','corrupt-glb']:
   c=b.new_context(offline=True,viewport={'width':w,'height':h},java_script_enabled=kind!='no-js');p=c.new_page();errors=[];requests=[];p.on('pageerror',lambda e:errors.append(str(e)));p.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http:','https:')) else None)
   if kind=='corrupt-glb':c.add_init_script("const orig=window.atob;window.atob=s=>s.startsWith('Z2xURg')?'invalid glb bytes':orig(s)")
   p.goto((R/'morocco-reference-v5.html').as_uri())
   if kind=='corrupt-glb':p.wait_for_function("document.querySelector('#status').textContent.includes('unavailable')")
   assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0')
   assert not errors and not requests and p.evaluate('document.documentElement.scrollWidth<=innerWidth')
   p.screenshot(path=str(R/f'{label}-{kind}.png'),full_page=True)
   results.append({'viewport':label,'case':kind,'poster_decoded_visible':True,'no_overflow':True,'external_requests':requests,'unhandled_errors':errors});c.close()
 b.close()
(R/'fallback-check.json').write_text(json.dumps(results,indent=2));print(results)
