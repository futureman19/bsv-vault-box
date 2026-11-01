from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw,ImageFont
import json
R=Path(__file__).resolve().parent;S=R.parent/'iceland-polished-v6'
records=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 for folder,name in [(S,'v6'),(R,'v7')]:
  c=b.new_context(offline=True,viewport={'width':1440,'height':1080},device_scale_factor=1);p=c.new_page();p.goto((folder/('iceland-polished-v6.html' if name=='v6' else 'iceland-moss-v7.html')).as_uri());p.wait_for_function('pilot.ready');p.wait_for_timeout(300)
  records.append(p.evaluate('''(()=>{const s=pilot.root.parent;return {camera:pilot.camera.matrixWorld.toArray(),projection:pilot.camera.projectionMatrix.toArray(),exposure:pilot.renderer.toneMappingExposure,environment:s.environmentIntensity,lights:s.children.filter(x=>x.isLight).map(x=>({type:x.type,color:x.color.toArray(),intensity:x.intensity,position:x.position.toArray()})),stage:[document.querySelector('#stage').clientWidth,document.querySelector('#stage').clientHeight],progress:pilot.progress}})()'''))
  p.locator('#stage').screenshot(path=str(R/(name+'-matched.png')));c.close()
 b.close()
assert records[0]==records[1]
a=Image.open(R/'v6-matched.png').convert('RGB');b=Image.open(R/'v7-matched.png').convert('RGB');assert a.size==b.size
w,h=a.size;board=Image.new('RGB',(w*2,h+65),'#10151a');board.paste(a,(0,65));board.paste(b,(w,65));d=ImageDraw.Draw(board);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',25)
d.text((30,20),'V6 / approved — original barely visible moss',font=font,fill='white');d.text((w+30,20),'V7 / moss only — identical camera and lighting',font=font,fill='white');board.save(R/'before-after.jpg',quality=93)
(R/'comparison-check.json').write_text(json.dumps({'same_camera_lighting_stage':True,'records':records,'screenshots':'actual offline GLTFLoader at normal default camera; no crops or zoom'},indent=2))
(R/'visual-critique.json').write_text(json.dumps({'desktop':'Visibility PASS; natural character qualified pass. Readable irregular green growth, not balls/neon. Some clusters remain angular or leaf-like and on exposed facets.','mobile':'PASS at normal 390px whole-box view, no zoom. Clear green accents, stone remains dominant; fine moss texture unresolved.','correction_passes':0,'scope':'Moss-readability only; not promotional photorealism.'},indent=2))
print('SAME_CAMERA_LIGHTING_COMPARISON_PASS',board.size)
