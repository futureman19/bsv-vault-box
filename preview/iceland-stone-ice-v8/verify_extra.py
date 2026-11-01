from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'iceland-stone-ice-v8.html').as_uri());p.wait_for_function('pilot.ready');p.wait_for_timeout(600)
 data=p.evaluate('''(()=>{let all=[],materials=[];pilot.root.updateMatrixWorld(true);pilot.root.traverse(o=>{if(o.isMesh){all.push({name:o.name,parent:o.parent.name,count:o.geometry.attributes.position.count});let m=o.material;materials.push({name:m.name,color:m.color.toArray(),roughness:m.roughness,metalness:m.metalness,transmission:m.transmission||0,maps:['map','normalMap','roughnessMap'].map(k=>m[k]?{kind:k,width:m[k].image.width,height:m[k].image.height}:null).filter(Boolean)})}});return {all,materials}})()''')
 mats={m['name']:m for m in data['materials']};assert any(len(m['maps'])==3 and all(t['width']==512 for t in m['maps']) for m in mats.values());assert any(m['transmission']>.3 for m in mats.values())
 data['materials']=list(mats.values());(R/'loader-materials.json').write_text(json.dumps(data,indent=2))
 # Capture raw stage plus projected model crop, same view as delivered initial camera.
 p.locator('#stage').screenshot(path=str(R/'closed-stage.png'))
 box=p.evaluate('''(()=>{let lo=[1,1],hi=[-1,-1];pilot.root.updateMatrixWorld(true);pilot.root.traverse(o=>{if(!o.isMesh)return;let a=o.geometry.attributes.position,v=pilot.root.position.clone();for(let i=0;i<a.count;i++){v.fromBufferAttribute(a,i).applyMatrix4(o.matrixWorld).project(pilot.camera);lo[0]=Math.min(lo[0],v.x);lo[1]=Math.min(lo[1],v.y);hi[0]=Math.max(hi[0],v.x);hi[1]=Math.max(hi[1],v.y)}});return {lo,hi}})()''')
 im=Image.open(R/'closed-stage.png');w,h=im.size;lo=box['lo'];hi=box['hi'];crop=(int((lo[0]+1)*w/2)-12,int((1-hi[1])*h/2)-12,int((hi[0]+1)*w/2)+12,int((1-lo[1])*h/2)+12);im.crop(crop).save(R/'actual-model-crop.png')
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');p.locator('#stage').screenshot(path=str(R/'open-stage.png'));c.close()
 c=b.new_context(java_script_enabled=False,offline=True,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'iceland-stone-ice-v8.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#open').is_disabled();p.screenshot(path=str(R/'no-js.png'),full_page=True);c.close();b.close()
# Comparison uses identical object WIDTH and left-front orientation; proportions are not warped.
ref=Image.open('C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-iceland-promotional/iceland-promotional.png').convert('RGB').crop((140,270,890,810))
actual=Image.open(R/'actual-model-crop.png').convert('RGB')
board=Image.new('RGB',(1600,1000),'#10151a');d=ImageDraw.Draw(board)
try:font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',19)
except:font=small=ImageFont.load_default()
for i,(im,title) in enumerate([(ref,'PRIMARY / AI promotional reference'),(actual,'V8 / actual offline GLTFLoader screenshot')]):
 im=im.resize((740,round(im.height*740/im.width)),Image.Resampling.LANCZOS);board.paste(im,(30+i*800,90+(560-im.height)//2));d.text((30+i*800,30),title,font=font,fill='white')
lines=['1  BLACK LID: original black material and browser lighting retained; no bloom added.', '2  RIVER: wider boolean-cut inlay, blue center and narrow pale edges; still reads ribbon-like.', '3  GLACIER: connected serrated ridge, blue-to-white depth and thickened apron; stylized.', '4  BASALT: all-side 512px grain and real varied wedge cuts; long column rhythm remains.', '5  BRASS + MOSS: hardware unchanged; existing green accents retained, some moss re-seated.', 'Approved wide baseline preserved. Equal object width; no geometric image warping.', 'Primary is AI promotional artwork, right is actual offline GLTFLoader; not photoreal parity.']
for i,t in enumerate(lines):d.text((30,690+i*37),t,font=small,fill='#d5dce2')
board.save(R/'reference-comparison.jpg',quality=94)
(R/'extra-check.json').write_text(json.dumps({'real_loader_maps_decoded':True,'ice_transmission':True,'no_js_poster':True,'comparison':'same object width, left-front orientation; proportion difference retained'},indent=2))
print('EXTRA_CHECK_PASS')
