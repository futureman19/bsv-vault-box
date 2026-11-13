from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent
with sync_playwright() as p:
 b=p.chromium.launch(channel='msedge',headless=True)
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080})
 page=c.new_page();page.goto((R/'kenya-v1.html').as_uri());page.wait_for_function('pilot.ready');page.locator('#open').click();page.wait_for_function('pilot.progress===1')
 page.evaluate('pilot.camera.position.set(5,5,-7)');page.wait_for_timeout(500);page.screenshot(path=str(R/'desktop-open-rear.png'));b.close()
