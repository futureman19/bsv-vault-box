from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[2];root=R/'preview/panama-repair-v2'
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True);c=b.new_context(offline=True,viewport={'width':390,'height':844},is_mobile=True,has_touch=True);p=c.new_page();p.goto((root/'panama-repair-v2.html').as_uri());p.wait_for_function('pilot.ready');p.evaluate('pilot.camera.position.set(-5,5.7,7)');p.wait_for_timeout(200);p.screenshot(path=str(root/'camera-trial-mobile.png'));b.close()
