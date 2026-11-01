from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files']);c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page()
 data=[]
 for label,path in [('original',R/'original/iceland-pilot.html'),('v3',R/'iceland-lightweight-v3.html')]:
  p.goto(path.as_uri());p.wait_for_function('pilot.ready');p.wait_for_timeout(300)
  mats=p.evaluate('''(()=>{const m=new Map();pilot.root.traverse(o=>{if(o.isMesh){let a=o.material;m.set(a.name,{name:a.name,roughness:a.roughness,metalness:a.metalness,map:a.map?[a.map.image.width,a.map.image.height]:null,normal:a.normalMap?[a.normalMap.image.width,a.normalMap.image.height]:null,roughnessMap:a.roughnessMap?[a.roughnessMap.image.width,a.roughnessMap.image.height]:null,uv:!!o.geometry.attributes.uv,normalScale:a.normalScale?.toArray()});}});return [...m.values()]})()''')
  if label=='v3':
   basalt=[m for m in mats if m['name'].startswith('Basalt')];assert len(basalt)==5
   assert all(m['map']==[256,256] and m['normal']==[256,256] and m['roughnessMap']==[256,256] and m['uv'] for m in basalt)
   lid=next(m for m in mats if m['name']=='Polished blue-black lid');assert lid['roughness']<.3 and not lid['map'] and not lid['normal']
  data.append({'version':label,'materials':mats,'asset':p.evaluate('pilot.asset')})
  for state in ['closed','open']:
   if state=='open':p.locator('#open').click();p.wait_for_function('pilot.progress===1');p.wait_for_timeout(150)
   p.locator('#stage').screenshot(path=str(R/f'{label}-{state}-stage.png'))
  p.locator('#reset').click();p.wait_for_timeout(150)
  p.evaluate('pilot.camera.position.sub({x:0,y:.95,z:0}).multiplyScalar(.62).add({x:0,y:.95,z:0})');p.wait_for_timeout(150)
  p.locator('#stage').screenshot(path=str(R/f'{label}-closeup.png'))
 b.close()
for state in ['closed','open','closeup']:
 suffix=f'{state}-stage' if state!='closeup' else state
 a=Image.open(R/f'original-{suffix}.png').convert('RGB');b=Image.open(R/f'v3-{suffix}.png').convert('RGB');out=Image.new('RGB',(a.width+b.width,a.height+40),(16,21,26));out.paste(a,(0,40));out.paste(b,(a.width,40));d=ImageDraw.Draw(out);d.text((15,12),'ORIGINAL V1 - matched camera',fill='white');d.text((a.width+15,12),'LIGHTWEIGHT V3 - matched camera',fill='white');out.save(R/f'comparison-{state}.jpg',quality=94)
assert data[0]['asset']['bounds']==data[1]['asset']['bounds']
(R/'pbr-check.json').write_text(json.dumps(data,indent=2));print('Actual loader maps, glossy lid, matched bounds and comparison captures PASS')
