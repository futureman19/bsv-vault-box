from pathlib import Path
import json
from PIL import Image,ImageStat
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent
maps={}
for p in (R/'maps').glob('*.png'):
 im=Image.open(p).convert('RGB'); ranges=[b-a for a,b in im.getextrema()];assert max(ranges)>0 and max(im.size)<=512;maps[p.name]=ranges
im=Image.open(R/'poster.png');assert max(ImageStat.Stat(im.convert('RGB')).stddev)>10
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True)
 c=b.new_context(offline=True,java_script_enabled=False);p=c.new_page();p.goto((R/'comoros-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#open').is_disabled();b.close()
r={'status':'PASS','map_ranges':maps,'source_poster_nonblank':True,'no_js_poster':True}
(R/'extended-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
