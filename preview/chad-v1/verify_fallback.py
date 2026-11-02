from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as p:
 b=p.chromium.launch(channel='msedge',headless=True)
 c=b.new_context(java_script_enabled=False,offline=True,viewport={'width':390,'height':844})
 page=c.new_page();page.goto((R/'chad-v1.html').as_uri());assert page.locator('#fallback').is_visible();assert page.locator('#open').is_disabled()
 assert page.locator('#fallback').evaluate('(i)=>i.complete&&i.naturalWidth>0')
 page.screenshot(path=str(R/'mobile-nojs.png'));b.close()
(R/'fallback-check.json').write_text(json.dumps({'status':'PASS','no_js_poster':True,'offline_file':True},indent=2))
print('PASS no-JS offline poster')
