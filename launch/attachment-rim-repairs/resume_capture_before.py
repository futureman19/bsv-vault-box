from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parents[2]
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 for slug in ['algeria','guyana']:
  root=R/'preview'/f'{slug}-repair-v2'
  if not root.exists():continue
  out=root/'before-recapture';out.mkdir(exist_ok=True)
  for mode,w,h in [('desktop',1440,1080),('mobile',390,844)]:
   c=b.new_context(viewport={'width':w,'height':h},offline=True,reduced_motion='reduce',is_mobile=mode=='mobile',has_touch=mode=='mobile')
   p=c.new_page();p.goto((root/'historical-v1'/f'{slug}-v1.html').as_uri());p.wait_for_function('window.pilot?.ready');p.screenshot(path=str(out/f'{mode}-closed.png'))
   p.locator('#open').click();p.wait_for_function('pilot.progress===1');p.screenshot(path=str(out/f'{mode}-open.png'));c.close()
 b.close()
print('captured immutable Algeria and Guyana original-scale desktop/mobile closed/open')
