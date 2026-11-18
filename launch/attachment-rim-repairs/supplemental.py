from pathlib import Path
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
import json,sys
R=Path(__file__).resolve().parents[2];results=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 for slug in ['ghana','chile']:
  root=R/'preview'/f'{slug}-repair-v2'
  if not root.exists():continue
  im=Image.open(root/'poster.png').convert('RGBA');assert im.getchannel('A').getextrema()[1]>0 and max(im.convert('RGB').getextrema()[0])>80
  c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((root/f'{slug}-repair-v2.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(root/'mobile-nojs.png'));c.close()
  for mode in ['desktop','mobile']:
   for state in ['closed','open']:
    old=Image.open(root/'before'/f'{mode}-{state}.png').convert('RGB');new=Image.open(root/f'{mode}-{state}.png').convert('RGB');assert old.size==new.size
    board=Image.new('RGB',(old.width*2,old.height+32),'#10151a');board.paste(old,(0,32));board.paste(new,(old.width,32));d=ImageDraw.Draw(board);d.text((12,8),'BEFORE / immutable V1',fill='white');d.text((old.width+12,8),'AFTER / repair V2',fill='white');board.save(root/f'comparison-{mode}-{state}.jpg',quality=90)
  results.append({'id':slug,'noJS':True,'poster_nonempty':True,'same_viewport_comparisons':4})
 b.close()
(R/'launch/attachment-rim-repairs/supplemental-check.json').write_text(json.dumps(results,indent=2));print(results)
