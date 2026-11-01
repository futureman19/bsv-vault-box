from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw,ImageFont
import json
R=Path(__file__).resolve().parent;S=R.parent/'iceland-moss-v7';records=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 for folder,name in [(S,'v7'),(R,'v8')]:
  c=b.new_context(offline=True,viewport={'width':1440,'height':1080},device_scale_factor=1);p=c.new_page();p.goto((folder/('iceland-moss-v7.html' if name=='v7' else 'iceland-stone-ice-v8.html')).as_uri());p.wait_for_function('pilot.ready');p.wait_for_timeout(300)
  records.append(p.evaluate('''(()=>{const s=pilot.root.parent;return {camera:pilot.camera.matrixWorld.toArray(),projection:pilot.camera.projectionMatrix.toArray(),exposure:pilot.renderer.toneMappingExposure,environment:s.environmentIntensity,lights:s.children.filter(x=>x.isLight).map(x=>({type:x.type,color:x.color.toArray(),intensity:x.intensity,position:x.position.toArray()})),stage:[document.querySelector('#stage').clientWidth,document.querySelector('#stage').clientHeight],progress:pilot.progress}})()'''))
  p.locator('#stage').screenshot(path=str(R/(name+'-matched.png')))
  p.evaluate('pilot.camera.position.set(5,3.7,-7)');p.wait_for_timeout(200);p.locator('#stage').screenshot(path=str(R/(name+'-rear.png')))
  p.locator('#reset').click();p.evaluate('pilot.camera.zoom=1.75;pilot.camera.updateProjectionMatrix()');p.wait_for_timeout(200);p.locator('#stage').screenshot(path=str(R/(name+'-detail.png')))
  c.close()
 b.close()
assert records[0]==records[1]
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',25)
for suffix,out in [('matched','before-after.jpg'),('rear','rear-before-after.jpg'),('detail','detail-before-after.jpg')]:
 a=Image.open(R/f'v7-{suffix}.png').convert('RGB');bb=Image.open(R/f'v8-{suffix}.png').convert('RGB');w,h=a.size
 board=Image.new('RGB',(w*2,h+65),'#10151a');board.paste(a,(0,65));board.paste(bb,(w,65));d=ImageDraw.Draw(board)
 d.text((30,20),'V7 / approved baseline',font=font,fill='white');d.text((w+30,20),'V8 / stone + river + ice; same camera/light',font=font,fill='white');board.save(R/out,quality=93)
im=Image.open(R/'v8-detail.png');w,h=im.size
im.crop((int(w*.12),int(h*.42),int(w*.82),int(h*.95))).save(R/'stone-closeup.png')
im.crop((int(w*.10),int(h*.05),int(w*.85),int(h*.52))).save(R/'ice-river-closeup.png')
(R/'comparison-check.json').write_text(json.dumps({'same_camera_lighting_stage':True,'records':records,'detail_zoom':1.75,'screenshots':'Actual offline GLTFLoader; detail deliberately clips silhouette, not normal hero'},indent=2))
print('MATCHED_COMPARISON_PASS')
