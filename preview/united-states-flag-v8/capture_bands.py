from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport=dict(width=1440,height=1080),reduced_motion='reduce');p=c.new_page();p.goto((R/'united-states-flag-v7.html').as_uri());p.wait_for_function('pilot.ready')
 for name,pos in [('front',[0,3,7.5]),('left',[-8.2,3,0])]:
  p.evaluate('(v)=>pilot.camera.position.set(...v)',pos);p.wait_for_timeout(250);p.locator('#stage').screenshot(path=str(R/f'band-{name}-close.png'))
 b.close()
