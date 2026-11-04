from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json
R=Path(__file__).resolve().parent
im=Image.open(R/'poster.png').convert('RGBA');assert im.getbbox();assert max(im.convert('RGB').getextrema()[0])>100
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True);p=b.new_page(viewport={'width':1440,'height':1080},offline=True);p.goto((R/'switzerland-v1.html').as_uri());p.wait_for_function('pilot.ready');p.locator('#open').click();p.wait_for_function('pilot.progress===1')
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(250);p.screenshot(path=str(R/'desktop-open-rear.png'));b.close()
(R/'poster-check.json').write_text(json.dumps({'status':'PASS','dimensions':im.size,'nonempty_source_render':True,'rear_open_capture':True}))
