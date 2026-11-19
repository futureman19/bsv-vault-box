from pathlib import Path
from playwright.sync_api import sync_playwright
import json,hashlib
R=Path(__file__).resolve().parents[2];D=R/'launch/attachment-rim-repairs/finish'
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 for row in json.loads((D/'targets.json').read_text()):
  root=R/row['root'];out=root/'before';out.mkdir(exist_ok=True);cases=[]
  for mode,w,h in [('desktop',1440,1080),('mobile',390,844)]:
   c=b.new_context(viewport={'width':w,'height':h},offline=True,reduced_motion='reduce',is_mobile=mode=='mobile',has_touch=mode=='mobile');p=c.new_page()
   p.goto((R/row['viewer']).as_uri());p.wait_for_function('window.pilot?.ready');p.screenshot(path=str(out/f'{mode}-closed.png'))
   p.locator('#open').click();p.wait_for_function('pilot.progress===1');p.screenshot(path=str(out/f'{mode}-open.png'))
   cases.append({'mode':mode,'viewer_sha256':hashlib.sha256((R/row['viewer']).read_bytes()).hexdigest(),'open_endpoint':True});c.close()
  (out/'capture-check.json').write_text(json.dumps(cases,indent=2));print(row['id'],flush=True)
 b.close()
