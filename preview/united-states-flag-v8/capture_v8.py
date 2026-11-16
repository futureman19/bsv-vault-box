from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport=dict(width=1200,height=1000),device_scale_factor=2,reduced_motion='reduce');p=c.new_page();p.goto((R/'united-states-flag-v8.html').as_uri());p.wait_for_function('pilot.ready')
 for name,pos in [('front',[0,2.6,6]),('left',[-6,2.6,0]),('top',[0,8,.001])]:
  p.evaluate('(v)=>pilot.camera.position.set(...v)',pos);p.wait_for_timeout(300);p.locator('#stage').screenshot(path=str(R/f'v8-{name}-view.png'))
  if name!='top':
   p.locator('#open').click();p.wait_for_function('pilot.progress===1');p.locator('#stage').screenshot(path=str(R/f'v8-{name}-open.png'));p.locator('#reset').click();p.wait_for_function('pilot.progress===0')
 b.close()
