from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent;old=R.parent/'morocco-atlas-v1'
# Fresh old/new same-camera detail captures from actual offline viewers.
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 for folder,tag in [(old,'v1'),(R,'v2')]:
  c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((folder/(folder.name+'.html')).as_uri());p.wait_for_function('pilot.ready')
  p.screenshot(path=str(R/(tag+'-matched-closed.png')))
  p.evaluate('pilot.camera.position.multiplyScalar(.76);pilot.camera.updateProjectionMatrix()');p.wait_for_timeout(200);p.screenshot(path=str(R/(tag+'-matched-detail.png')))
  p.locator('#reset').click();p.locator('#open').click();p.wait_for_function('pilot.progress===1');p.screenshot(path=str(R/(tag+'-matched-open.png')));c.close()
 b.close()
def board(paths,labels,out,width=700):
 ims=[]
 for path,label in zip(paths,labels):
  im=Image.open(path).convert('RGB');im=im.resize((width,round(im.height*width/im.width)))
  panel=Image.new('RGB',(width,im.height+45),(17,21,25));panel.paste(im,(0,45));ImageDraw.Draw(panel).text((15,15),label,fill=(235,221,192));ims.append(panel)
 canvas=Image.new('RGB',(width*len(ims),max(im.height for im in ims)),(17,21,25))
 for i,im in enumerate(ims):canvas.paste(im,(i*width,0))
 canvas.save(R/out,quality=92)
for pose in ['closed','open','detail']:board([R/f'v1-matched-{pose}.png',R/f'v2-matched-{pose}.png'],['V1 ACTUAL MODEL','V2 ACTUAL MODEL'],f'before-after-{pose}.jpg')
board([R/'checkpoints/pass1-materials.png',R/'checkpoints/pass2-tilework.png',R/'checkpoints/pass3-ridge-hardware.png',R/'poster.png'],['PASS 1 MATERIALS','PASS 2 TILEWORK','PASS 3 RIDGE / HARDWARE','FINAL INTEGRATED CORRECTION'],'three-pass-review.jpg',550)
ref=Path('C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-concepts/morocco.png');(R/'references').mkdir(exist_ok=True);(R/'references/primary-morocco.png').write_bytes(ref.read_bytes())
canvas=Image.new('RGB',(1500,1000),(17,21,25));report=[]
for i,(path,label) in enumerate([(ref,'PRIMARY CONCEPT / NOT ACTUAL MODEL'),(R/'poster.png','V2 ACTUAL AUTHORED MODEL')]):
 im=Image.open(path).convert('RGB');a=np.asarray(im).astype(float);m=(a[:,:,0]>55)&(a[:,:,0]>a[:,:,1]*1.18)&(a[:,:,0]>a[:,:,2]*1.35);ys,xs=np.where(m);scale=650/(xs.max()-xs.min()+1)
 scaled=im.resize((round(im.width*scale),round(im.height*scale)));panel=Image.new('RGB',(750,1000),(17,21,25));panel.paste(scaled,(round(50-xs.min()*scale),round(820-ys.max()*scale)));ImageDraw.Draw(panel).text((35,30),label,fill=(222,207,178));canvas.paste(panel,(i*750,0));report.append(dict(image=str(path),uniform_scale=scale,target_warm_object_width=650))
ImageDraw.Draw(canvas).text((35,950),'Equal warm-object width, uniform scaling only; lighting/perspective differ. No image warping.',fill=(222,207,178));canvas.save(R/'reference-comparison.jpg',quality=93);(R/'comparison-method.json').write_text(json.dumps(report,indent=2))
