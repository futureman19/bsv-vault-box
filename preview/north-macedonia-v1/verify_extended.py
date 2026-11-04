from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
im=Image.open(R/'poster.png').convert('RGBA');assert im.getchannel('A').getextrema()[1]>0;assert max(im.convert('RGB').getextrema()[0])>30
with sync_playwright() as p:
 b=p.chromium.launch(channel='msedge',headless=True)
 c=b.new_context(java_script_enabled=False,offline=True,viewport={'width':390,'height':844});page=c.new_page();page.goto((R/'north-macedonia-v1.html').as_uri());assert page.locator('#fallback').is_visible();page.screenshot(path=str(R/'mobile-nojs.png'));b.close()
(R/'extended-check.json').write_text(json.dumps({'status':'PASS','source_poster_nonempty':True,'no_javascript_poster_visible':True},indent=2));print('EXTENDED PASS')
