"""Actual browser comparison, same v4/v5 pose and light, width normalization only."""
from pathlib import Path
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
import json,math
R=Path(__file__).resolve().parent;old=R.parent/'morocco-saturn-v4';report=[]
project='''(bodyOnly)=>{let minX=1e9,minY=1e9,maxX=-1e9,maxY=-1e9;let rect=pilot.renderer.domElement.getBoundingClientRect();pilot.root.updateMatrixWorld(true);pilot.root.traverse(o=>{if(!o.isMesh||(bodyOnly&&!o.name.startsWith('Rose_stone')))return;let a=o.geometry.attributes.position;for(let i=0;i<a.count;i++){let v=o.position.clone().fromBufferAttribute(a,i).applyMatrix4(o.matrixWorld).project(pilot.camera);let x=rect.x+(v.x+1)*rect.width/2,y=rect.y+(1-v.y)*rect.height/2;minX=Math.min(minX,x);minY=Math.min(minY,y);maxX=Math.max(maxX,x);maxY=Math.max(maxY,y)}});return [minX,minY,maxX,maxY]}'''
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 for folder,tag in [(old,'v4'),(R,'v5')]:
  c=b.new_context(offline=True,viewport={'width':1600,'height':1200});p=c.new_page();p.goto((folder/(folder.name+'.html')).as_uri());p.wait_for_function('pilot.ready');p.wait_for_timeout(250)
  # Same hero orientation, modestly closer so normal-view crops resolve body grain.
  p.evaluate('pilot.camera.fov=29;pilot.camera.updateProjectionMatrix()');p.wait_for_timeout(150)
  p.screenshot(path=str(R/(tag+'-matched-closed.png')));im=Image.open(R/(tag+'-matched-closed.png'))
  crops={}
  for body,name in [(False,'object'),(True,'body')]:
   bounds=p.evaluate(project,body);crop=tuple([math.floor(bounds[0])-4,math.floor(bounds[1])-4,math.ceil(bounds[2])+4,math.ceil(bounds[3])+4]);im.crop(crop).save(R/f'{tag}-{name}-crop.png');crops[name]=crop
  report.append({'tag':tag,'fov':29,'camera':p.evaluate('pilot.camera.position.toArray()'),'crops':crops,'light':'unchanged viewer','normalization':'uniform scale to equal object width only; no perspective warp'})
  c.close()
 b.close()
ref=Image.open(R/'references/primary-morocco.png').convert('RGB');ref.crop((130,265,900,825)).save(R/'original-object-crop.png');ref.crop((130,460,900,825)).save(R/'original-body-crop.png')
def board(kind,outname):
 ims=[Image.open(R/f'{tag}-{kind}-crop.png').convert('RGB') for tag in ['original','v4','v5']]
 width=700;ims=[im.resize((width,round(im.height*width/im.width)),Image.Resampling.LANCZOS) for im in ims];height=max(im.height for im in ims)+85
 out=Image.new('RGB',(width*3,height),'#171b20');d=ImageDraw.Draw(out)
 for k,(im,label) in enumerate(zip(ims,['ORIGINAL USER MARKETING ART','V4 PREVIOUS / SAME CAMERA + LIGHT','V5 ACTUAL BROWSER / REFERENCE-SOURCED'])):
  out.paste(im,(k*width,55));d.text((k*width+12,15),label,fill='white')
 d.text((15,height-20),'Equal object width, proportional scaling only. Original camera/lighting approximate; v4 and v5 camera/lighting identical.',fill='white');out.save(R/outname,quality=94)
board('object','reference-comparison.jpg');board('body','body-closeup-comparison.jpg')
(R/'comparison-method.json').write_text(json.dumps(report,indent=2));print(report)
