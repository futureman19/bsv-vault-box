from pathlib import Path
import json,hashlib
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent; REPO=R.parents[1]
rows=json.loads((R/'baseline.json').read_text());results=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 for row in rows:
  dest=R/'captures'/row['id'];dest.mkdir(parents=True,exist_ok=True)
  for mode,w,h in [('desktop',1280,900),('mobile',390,844)]:
   c=b.new_context(offline=True,viewport={'width':w,'height':h},device_scale_factor=1,has_touch=mode=='mobile',is_mobile=mode=='mobile',reduced_motion='reduce');p=c.new_page();errors=[];network=[]
   p.on('pageerror',lambda e:errors.append(str(e)));p.on('request',lambda r:network.append(r.url) if r.url.startswith(('http:','https:')) else None)
   path=REPO/row['viewer'];p.goto(path.as_uri());p.wait_for_function('window.pilot?.ready',timeout=90000);p.wait_for_timeout(200)
   state=p.evaluate('({asset:pilot.asset,dpr:devicePixelRatio,ratio:pilot.renderer.getPixelRatio(),samples:pilot.renderer.getContext().getParameter(pilot.renderer.getContext().SAMPLES),overflow:document.documentElement.scrollWidth>innerWidth})')
   for pose in ['closed','open']:
    if pose=='open':
     p.locator('#open').tap() if mode=='mobile' else p.locator('#open').click()
     p.wait_for_function('pilot.progress===1')
    p.screenshot(path=str(dest/f'{mode}-{pose}.png'),full_page=True)
   results.append({'id':row['id'],'mode':mode,'state':state,'errors':errors,'external_requests':network,'viewer_sha256':hashlib.sha256(path.read_bytes()).hexdigest()});c.close()
  (R/'capture-results.json').write_text(json.dumps(results,indent=2));print(row['id'],flush=True)
 b.close()
