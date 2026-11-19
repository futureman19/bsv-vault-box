from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw,ImageFont
import json
R=Path(__file__).resolve().parent
with sync_playwright() as p:
 b=p.chromium.launch(channel='msedge',headless=True);c=b.new_context(offline=True,viewport={'width':1440,'height':1080});page=c.new_page();page.goto((R/'iceland-backright-v10.html').as_uri());page.wait_for_function('pilot.ready===true')
 result=page.evaluate('''()=>{let ice,river,maps=[];pilot.root.updateMatrixWorld(true);let all=[];pilot.root.traverse(o=>{if(!o.isMesh)return;let pos=o.geometry.attributes.position,v=pilot.root.position.clone(),vs=[];for(let i=0;i<pos.count;i++){v.fromBufferAttribute(pos,i).applyMatrix4(o.matrixWorld);vs.push([v.x,-v.z,v.y]);}if(o.name.startsWith('Glacier'))ice=vs;if(o.name.startsWith('River')&&o.name.includes('channel'))river=vs;for(let key of ['map','normalMap','roughnessMap'])if(o.material[key]){let im=o.material[key].image;maps.push({mesh:o.name,key,width:im.width,height:im.height});}});return {iceBounds:[0,1,2].map(i=>[Math.min(...ice.map(v=>v[i])),Math.max(...ice.map(v=>v[i]))]),riverBounds:[0,1,2].map(i=>[Math.min(...river.map(v=>v[i])),Math.max(...river.map(v=>v[i]))]),maps,asset:pilot.asset};}''')
 assert result['iceBounds'][0][0]>.8 and result['iceBounds'][1][0]>.35
 assert result['riverBounds'][0][1]>1.2 and result['riverBounds'][1][1]>.65
 assert result['maps'] and all(m['width']>0 and m['height']>0 for m in result['maps'])
 (R/'runtime-physical-check.json').write_text(json.dumps(result,indent=2));b.close()
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22)
im=Image.open(R/'top-down-source.png').convert('RGB');d=ImageDraw.Draw(im)
for xy,text in [((370,35),'BACK / +Y / REAR HINGES'),((345,830),'FRONT / -Y / FRONT LATCH'),((815,450),'RIGHT / +X'),((60,450),'LEFT / -X'),((650,180),'TARGET: BACK-RIGHT')]:d.text(xy,text,font=font,fill='#ffcc66')
d.rectangle((735,230,920,370),outline='#ffcc66',width=3)
im.save(R/'top-down-diagnostic.png')
old=Image.open(R.parent/'iceland-corner-ice-v9/desktop-closed.png').convert('RGB');new=Image.open(R/'desktop-closed.png').convert('RGB')
canvas=Image.new('RGB',(1440,600),'#13191e');d=ImageDraw.Draw(canvas)
for i,(image,label) in enumerate([(old,'V9: incorrect physical FRONT-RIGHT'),(new,'V10: physical BACK-RIGHT')]):
 crop=image.crop((260,280,1040,780));crop.thumbnail((700,540));canvas.paste(crop,(i*720,50));d.text((i*720+20,12),label,font=font,fill='white')
canvas.save(R/'before-after.jpg',quality=93)
promo=Image.open('C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-iceland-promotional/iceland-promotional.png').convert('RGB');canvas=Image.new('RGB',(1440,800),'#13191e');d=ImageDraw.Draw(canvas)
promo.thumbnail((700,720));canvas.paste(promo,((720-promo.width)//2,60));crop=new.crop((260,280,1040,780));crop.thumbnail((700,700));canvas.paste(crop,(730,130))
d.text((20,20),'Marketing illustration (not interactive model)',font=font,fill='white');d.text((740,20),'Actual v10 offline GLB viewer',font=font,fill='white');canvas.save(R/'reference-comparison.jpg',quality=93)
print('GLTFLoader back-right and decoded maps verified; comparisons saved')
