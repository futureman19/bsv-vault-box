from pathlib import Path
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
import json,shutil
R=Path(__file__).resolve().parent;old=R.parent/'morocco-atlas-v2';report=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 for folder,tag in [(old,'v2'),(R,'v3')]:
  c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((folder/(folder.name+'.html')).as_uri());p.wait_for_function('pilot.ready');p.wait_for_timeout(300)
  p.screenshot(path=str(R/(tag+'-matched-closed.png')))
  p.evaluate('pilot.camera.fov=23;pilot.camera.updateProjectionMatrix()');p.wait_for_timeout(300)
  centre=p.evaluate('''(()=>{let v=pilot.root.position.clone().set(-.65,.8,1.44).project(pilot.camera),b=pilot.renderer.domElement.getBoundingClientRect();return [b.x+(v.x+1)*b.width/2,b.y+(1-v.y)*b.height/2]})()''')
  p.screenshot(path=str(R/(tag+'-macro-full.png')))
  im=Image.open(R/(tag+'-macro-full.png'));x,y=centre;crop=(round(x-410),round(y-180),round(x+410),round(y+180));im.crop(crop).save(R/(tag+'-body-closeup.png'));report.append({'tag':tag,'macro_fov':23,'crop':crop,'light':'unchanged viewer source','rescale':False})
  c.close()
 b.close()
def board(files,labels,name):
 ims=[Image.open(R/f).convert('RGB') for f in files];w=ims[0].width;h=max(i.height for i in ims);out=Image.new('RGB',(w*len(ims),h+45),(17,21,25));d=ImageDraw.Draw(out)
 for k,(im,label) in enumerate(zip(ims,labels)):out.paste(im,(k*w,45));d.text((k*w+20,15),label,fill=(240,220,190))
 out.save(R/name,quality=94)
board(['v2-body-closeup.png','v3-body-closeup.png'],['V2 / PRINTED WAVE-LIKE BODY','V3 / GRANULAR SANDSTONE BODY'],'before-after-body-closeup.jpg')
board(['v2-matched-closed.png','v3-matched-closed.png'],['V2 / SAME CAMERA AND LIGHT','V3 / BODY MATERIAL ONLY'],'before-after-closed.jpg')
ref=Path('C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-concepts/morocco.png');(R/'references').mkdir(exist_ok=True);shutil.copy2(ref,R/'references/primary-morocco.png')
(R/'comparison-method.json').write_text(json.dumps(report,indent=2));print(report)
