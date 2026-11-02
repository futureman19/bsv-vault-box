from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 for slug in ['morocco-reference-v5','morocco-finish-v6']:
  c=b.new_context(viewport={'width':1440,'height':1080},offline=True);p=c.new_page();p.goto((R.parent/slug/(slug+'.html')).as_uri());p.wait_for_function('pilot.ready');p.wait_for_timeout(200);p.screenshot(path=str(R/(slug+'-matched-closed.png')))
  p.evaluate('pilot.camera.position.set(-4,6,6);pilot.camera.fov=27;pilot.camera.updateProjectionMatrix()');p.wait_for_timeout(200);p.screenshot(path=str(R/(slug+'-lid-closeup.png')));c.close()
 b.close()
ims=[Image.open(R/'references/primary.png').crop((110,280,915,795)),Image.open(R/'morocco-reference-v5-matched-closed.png').crop((395,350,1015,805)),Image.open(R/'morocco-finish-v6-matched-closed.png').crop((395,350,1015,805))]
board=Image.new('RGB',(1800,570),'#181c21');d=ImageDraw.Draw(board)
for i,(im,label) in enumerate(zip(ims,['PRIMARY MARKETING','APPROVED V5','V6 FINISH'])):
 im.thumbnail((590,515));board.paste(im,(i*600,35));d.text((i*600+10,10),label,fill='white')
board.save(R/'reference-comparison.jpg',quality=95)
board=Image.new('RGB',(1800,600),'#181c21');d=ImageDraw.Draw(board)
for i,(path,label) in enumerate([(R/'references/lid-crop.png','PRIMARY LID'),(R/'morocco-reference-v5-lid-closeup.png','V5 SAME CAMERA'),(R/'morocco-finish-v6-lid-closeup.png','V6 SAME CAMERA')]):
 im=Image.open(path)
 if i:im=im.crop((330,200,1100,650))
 im.thumbnail((590,550));board.paste(im,(i*600,35));d.text((i*600+10,10),label,fill='white')
board.save(R/'lid-comparison.jpg',quality=95)
