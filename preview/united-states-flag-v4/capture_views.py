from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import json,math
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080},reduced_motion='reduce');p=c.new_page();p.goto((R/'united-states-flag-v4.html').as_uri());p.wait_for_function('pilot.ready');p.wait_for_timeout(150)
 # Rotate the actual loaded model around vertical Y, leaving mechanism untouched.
 initial=p.evaluate('pilot.root.rotation.y');views=[]
 for name,angle in [('front-left',0),('rear-left',math.pi/2),('rear-right',math.pi),('front-right',-math.pi/2)]:
  p.evaluate('(v)=>{pilot.root.rotation.y=v;pilot.root.updateMatrixWorld(true)}',initial+angle);p.wait_for_timeout(150);p.screenshot(path=str(R/f'view-{name}.png'),full_page=True);views.append(name)
 c.close();b.close()
# Equal-width image panels; no anisotropic stretching.
paths=[Path('C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-usa-flag-fireworks/united-states-flag-fireworks.png'),R.parent/'united-states-flag-v3/desktop-closed.png',R/'view-front-left.png']
board=Image.new('RGB',(1800,680),(19,23,30));d=ImageDraw.Draw(board)
for i,(path,label) in enumerate(zip(paths,['Approved marketing (illustration)','V3 rejected (actual model)','V4 lid-only canton (actual model)'])):
 im=Image.open(path).convert('RGB')
 # Browser screenshot viewer crop, illustration kept whole.
 if i:im=im.crop((480,380,920,730))
 else:im=im.crop((0,200,1072,976))
 # Normalize object region width uniformly, preserve aspect ratio.
 im=im.resize((560,round(im.height*560/im.width)),Image.Resampling.LANCZOS)
 im.thumbnail((580,600));board.paste(im,(i*600+(600-im.width)//2,55+(600-im.height)//2));d.text((i*600+20,20),label,fill='white')
board.save(R/'reference-comparison.jpg',quality=93)
(R/'views-check.json').write_text(json.dumps({'offline':True,'actual_loaded_glb':True,'views':views,'moving_lid':'Single lid-only navy field; all body sides striped'},indent=2))
