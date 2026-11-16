from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import numpy as np,io,json,math
R=Path(__file__).resolve().parent
rows=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 for width,height in [(1440,1080),(390,844)]:
  c=b.new_context(offline=True,viewport=dict(width=width,height=height),reduced_motion='reduce');p=c.new_page();p.goto((R/'united-states-flag-v9.html').as_uri());p.wait_for_function('pilot.ready');p.wait_for_timeout(150)
  # Capture first visible default reduced frame and test actual normal cycle pixels.
  p.screenshot(path=str(R/f'initial-{width}-static.png'),full_page=True)
  p.evaluate('window.originalFX=pilot.fireworks.update;pilot.fireworks.update=()=>{}')
  for opened in [False,True]:
   if opened:p.locator('#open').click();p.wait_for_function('pilot.progress===1');p.wait_for_timeout(100)
   p.evaluate('pilot.fireworks.group.visible=false');p.wait_for_timeout(60)
   background=np.array(Image.open(io.BytesIO(p.screenshot())).convert('RGB')).astype(int)
   p.evaluate('pilot.fireworks.group.visible=true')
   phases=[]
   for k in range(13):
    t=k*.3;p.evaluate('(t)=>{originalFX(t,false);pilot.renderer.render(pilot.root.parent,pilot.camera)}',t)
    raw=p.screenshot();a=np.array(Image.open(io.BytesIO(raw)).convert('RGB')).astype(int)
    changed=np.max(abs(a-background),axis=2)>35;pixels=int(changed.sum());assert pixels>100,(width,opened,t,pixels)
    phases.append(dict(time=t,visible_firework_pixels=pixels))
    if k in [0,6,12]:(R/f'cycle-{width}-{int(opened)}-{k}.png').write_bytes(raw)
   rows.append(dict(width=width,opened=opened,phases=phases))
   p.evaluate('originalFX(0,true)');p.wait_for_timeout(60)
   p.screenshot(path=str(R/f'final-{width}-{int(opened)}.png'),full_page=True)
   if width==1440 and not opened:
    # Actual browser element capture, no composited artwork or Blender substitution.
    p.locator('#stage').screenshot(path=str(R/'hero-fireworks.png'))
    Image.open(R/'hero-fireworks.png').convert('RGB').save(R/'poster.jpg',quality=92,optimize=True)
    Image.open(R/'hero-fireworks.png').save(R/'poster.png')
  c.close()
 # Four physical corners, reduced static fireworks.
 c=b.new_context(offline=True,viewport=dict(width=1440,height=1080),reduced_motion='reduce');p=c.new_page();p.goto((R/'united-states-flag-v9.html').as_uri());p.wait_for_function('pilot.ready')
 for name,angle in [('front-left',0),('rear-left',math.pi/2),('rear-right',math.pi),('front-right',-math.pi/2)]:
  p.evaluate('(a)=>pilot.root.rotation.y=a',angle);p.wait_for_timeout(120);p.screenshot(path=str(R/f'view-{name}.png'),full_page=True)
 # Matched normal camera and static fireworks v4/v5 image comparison.
 images=[]
 for version in ['v7','v9']:
  p.goto(((R.parent/'united-states-flag-v7' if version=='v7' else R)/f'united-states-flag-{version}.html').as_uri());p.wait_for_function('pilot.ready');p.wait_for_timeout(150)
  raw=p.locator('#stage').screenshot();im=Image.open(io.BytesIO(raw)).convert('RGB');im.thumbnail((800,650));images.append(im)
 board=Image.new('RGB',(1600,700),(16,21,26));d=ImageDraw.Draw(board)
 for i,im in enumerate(images):board.paste(im,(i*800,40));d.text((i*800+25,12),['V7 thick lid - no body continuation','V9 restored substantial lid - exact palette'][i],fill='white')
 board.save(R/'reference-comparison.jpg',quality=93)
 c.close();b.close()
(R/'fireworks-pixels-check.json').write_text(json.dumps(dict(PASS=True,threshold=35,minimum_pixels=100,cases=rows),indent=2));print('52 rendered phase checks passed; actual browser hero saved')
